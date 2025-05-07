import math

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages

from shop.models import Category, Product
from shop.forms import UserAuthenticatedForm, UserRegisterForm, ReviewForms


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

        # Вычисление среднего арифметического оценок ревью
        star_reviews = product.reviews.filter(grade__gt=0)
        list_reviews_count = []
        grade = 0
        for rev in star_reviews:
            list_reviews_count.append(int(rev.grade))
        if list_reviews_count:
            grade = math.ceil(sum(list_reviews_count) / len(list_reviews_count))
        context["grade"] = grade

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
    """ Аутентификация пользователя """
    form = UserAuthenticatedForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Вы успешно вошли в аккаунт", extra_tags="success")
        return redirect("index")
    else:
        messages.error(request, "Не верное имя пользователя или пароль", extra_tags="danger")
        return redirect("login_registration")


def user_logout(request):
    """ Выход пользователя """
    logout(request)
    return redirect("index")


def user_registration(request):
    """ Регистрация пользователя """
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
    """ Сохранение отзыва """
    form = ReviewForms(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(pk=product_pk)
        review.product = product
        form.save()
        messages.success(request, "Вы успешно оставили отзыв", extra_tags="success")

        return redirect("product_page", product.slug)