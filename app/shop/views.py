from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.core.mail import send_mail

from shop.models import Category, Product, FavoriteProducts, Mail
from shop.forms import UserAuthenticatedForm, UserRegisterForm, ReviewForms
from config import settings


class Index(ListView):
    """Главная страница"""

    model = Product
    context_object_name = "categories"
    extra_context = {"title": "Главная страница"}
    template_name = "shop/index.html"

    def get_queryset(self):
        """Вывод родительской категории"""
        return Category.objects.filter(parent=None)

    def get_context_data(self, **kwargs):
        """Вывод на страницу дополнительных элементов"""
        context = super().get_context_data()
        products = Product.objects.order_by("-watched")[:8]
        context["top_products"] = products
        return context


class SubCategeries(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/category_page.html"

    def get_queryset(self):

        type_field = self.request.GET.get("type")
        if type_field:
            products = Product.objects.filter(category__slug=type_field)[:3]
            return products
        parent_category = Category.objects.get(slug=self.kwargs["slug"])
        sub = parent_category.subcategories.all()
        products = Product.objects.filter(category__in=sub).order_by("?")[:3]

        sorted_field = self.request.GET.get("sort")
        if sorted_field:
            products = products.order_by(sorted_field)[:3]

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        parent_category = Category.objects.get(slug=self.kwargs["slug"])
        context["category"] = parent_category
        context["title"] = parent_category.title
        return context


class ProductPage(DetailView):
    """ "  Вывод товаро на отдельной странице"""

    model = Product
    template_name = "shop/product_page.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs["slug"])
        products = Product.objects.filter(category=product.category).exclude(
            slug=self.kwargs["slug"]
        )
        products = products.order_by("?")
        context["products"] = products
        reviews = product.reviews.all().order_by("-pk")

        if self.request.user.is_authenticated:
            context["review_form"] = ReviewForms
            context["reviews"] = reviews
        return context


def login_registration(request):
    """ Регистрация пользователя """ ""

    context = {
        "title": "Войти или Зарегестрироваться",
        "user_auth": UserAuthenticatedForm,
        "user_register": UserRegisterForm,
    }
    return render(request, "shop/login_registration.html", context)


def user_login(request):
    """Аутентификация пользователя"""
    form = UserAuthenticatedForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Вы успешно вошли в аккаунт", extra_tags="success")
        return redirect("index")
    else:
        messages.error(
            request, "Не верное имя пользователя или пароль", extra_tags="danger"
        )
        return redirect("login_registration")


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect("index")


def user_registration(request):
    """Регистрация пользователя"""
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Вы успешно зарегестрированны", extra_tags="success")
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text(), extra_tags="danger")
        # messages.error(request, "Что то пошло не так", extra_tags="danger")
    return redirect("login_registration")


def save_review(request, product_pk):
    """Сохранение отзыва"""
    form = ReviewForms(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(pk=product_pk)
        review.product = product
        form.save()
        messages.success(request, "Вы успешно оставили отзыв", extra_tags="success")

        return redirect("product_page", product.slug)


def save_favorite_products(request, product_slug):
    """Добавление или удаление товаров с избранных"""

    user = request.user if request.user.is_authenticated else None
    if user:
        product = Product.objects.get(slug=product_slug)
        favorite_products = FavoriteProducts.objects.filter(user=user)
        if product in [i.product for i in favorite_products]:
            fav_product = FavoriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavoriteProducts.objects.create(user=user, product=product)

        # Узнаем с какой страницы пришел пользователь а если не найдет перенаправим на нужную страницу
        next_page = request.META.get("HTTP_REFERER", "category_detail")
        return redirect(next_page)
    else:
        return redirect("user_registration")


class FavoriteProductsView(LoginRequiredMixin, ListView):
    """Для вывода избранных на страницу"""

    model = FavoriteProducts
    context_object_name = "products"
    template_name = "shop/favorite_products.html"
    login_url = "login_registration"

    def get_queryset(self):
        """Получаем товары конкретного пользователя"""
        favs = FavoriteProducts.objects.filter(user=self.request.user)
        products = [i.product for i in favs]
        return products


def save_subscribers(request):
    """Собиратель почтовых адресов"""
    email = request.POST.get("email")
    user = request.user if request.user.is_authenticated else None
    if email:
        try:
            Mail.objects.create(email=email, user=user)
            messages.success(
                request, "Вы успешно подписались на рассылку", extra_tags="success"
            )
        except IntegrityError as err:
            messages.error(request, "Такая почта уже существует", extra_tags="danger")

    return redirect("index")


def send_mail_to_subscribe(request):
    """Отправка писем подписчикам"""

    if request.method == "POST":
        text = request.POST.get("text")
        mail_lists = Mail.objects.all()
        for user in mail_lists:
            send_mail(
                subject="У нас новая акция",
                message=text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            print(f"Сообщение отправлено на почту {user.email}")

    context = {"title": "Спамер"}
    return render(request, "shop/send_email.html", context)


def payments(request):
    return render(request, "shop/payments.html")


def cart(request):
    """ Страница корзины"""
    return render(request, "shop/cart.html")

def to_cart(request, product_id, action):
    """ Добавление или удаление товара в корзину """
    return render("cart")