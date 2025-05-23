import stripe
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.urls import reverse
from django.core import paginator

from shop.models import (
    Category,
    Product,
    FavoriteProducts,
    Mail,
    Customer,
    ShippingAddress,
    Order,
)
from shop.forms import (
    UserAuthenticatedForm,
    UserRegisterForm,
    ReviewForms,
    CustomerForm,
    ShippingForm,
)
from shop.utils import CartForAuthenticatedUser, get_cart_data
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
    """ Вывод подкатегорий на отдельной странице """
    paginate_by = 3
    model = Product
    context_object_name = "products"
    template_name = "shop/category_page.html"

    def get_queryset(self):
        type_field = self.request.GET.get("type")

        if type_field:
            products = Product.objects.filter(category__slug=type_field)
            return products
        parent_category = Category.objects.get(slug=self.kwargs["slug"])
        sub = parent_category.subcategories.all()
        products = Product.objects.filter(category__in=sub)
        sorted_field = self.request.GET.get("sort")
        if sorted_field:
            products = products.order_by(sorted_field)

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


def checkout(request):
    """Оформление заказа"""
    cart_info = get_cart_data(request)
    context = {
        "order": cart_info["order"],
        "order_products": cart_info["order_products"],
        "cart_total_quantity": cart_info["cart_total_quantity"],
        "customer_form": CustomerForm(),
        "shipping_form": ShippingForm(),
        "title": "Оформление заказа",
    }
    return render(request, "shop/checkout.html", context)



def cart(request):
    """Страница корзины"""
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)
        context = {
            "order": cart_info["order"],
            "order_products": cart_info["order_products"],
            "cart_total_quantity": cart_info["cart_total_quantity"],
            "cart_total_price": cart_info["cart_total_price"],
            "title": "Корзина",
        }
        return render(request, "shop/cart.html", context)
    messages.error(
        request, "Авторизируйтесь чтобы совершать покупки", extra_tags="danger"
    )
    return redirect("login_registration")


def to_cart(request, product_id, action):
    """Добавление или удаление товара в корзину"""
    if request.user.is_authenticated:
        CartForAuthenticatedUser(request, product_id, action)
        return redirect("cart")
    messages.error(
        request, "Авторизируйтесь чтобы совершать покупки", extra_tags="danger"
    )
    return redirect("login_registration ")


def create_checkout_session(request):
    """Оплат на stripe"""
    print("-" * 50)
    print(settings.STRIPE_SECRET_KEY)
    print("------" *39)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        print("hello world")
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data["first_name"]
            customer.last_name = customer_form.cleaned_data["last_name"]
            customer.email = customer_form.cleaned_data["email"]
            customer.phone = customer_form.cleaned_data["phone"]
            customer.save()
        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = cart_info["order"]
            address.save()

        total_price = cart_info["cart_total_price"]
        total_quantity = cart_info["cart_total_quantity"]

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Товары тестовы"},
                        "unit_amount": int(total_price * 100),
                    },
                    "quantity": total_quantity,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("success")),
        )
        print("+++=" * 20)
        print(session.url)
        print("+++" * 20)
        return redirect(session.url, 303)


def success_payment(request):
    """Оплата прошла успшено"""
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    messages.success(request, "Оплата прошла успешно", extra_tags="success")
    return render(request, "shop/success.html")
