from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from shop.models import Category, Product


class Index(ListView):
    """Главная страница"""

    model = Product
    context_object_name = "categories"
    extra_context = {"title": "Главная страница"}
    template_name = "shop/index.html"

    def get_queryset(self):
        """Вывод родительской категории"""
        return Category.objects.filter(parent=None)


class SubCategeries(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/category_page.html"

    def get_queryset(self):
        print(12345)
        parent_category = Category.objects.get(slug=self.kwargs["slug"])
        sub = parent_category.subcategories.all()
        products = Product.objects.filter(category__in=sub).order_by("?")
        return products