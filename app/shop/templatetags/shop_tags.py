import math

from django import template
from django.template.defaulttags import register as range_register

from shop.models import Category, FavoriteProducts, Product


register = template.Library()


@register.simple_tag()
def get_average_rating(product_slug):
    """ Вычисление среднего арифметического оценок ревью """
    product =  Product.objects.get(slug=product_slug)
    star_reviews = product.reviews.filter(grade__gt=0)
    list_reviews_count = []
    grade = 0
    for rev in star_reviews:
        list_reviews_count.append(int(rev.grade))
    if list_reviews_count:
        grade = math.ceil(sum(list_reviews_count) / len(list_reviews_count))

    return grade


@range_register.filter
def get_positive_range(value):
    return range(int(value))


@range_register.filter
def get_negative_range(value):
    return range(5 - int(value))


@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_all_parent_category():
    return Category.objects.filter(parent=None)


@register.simple_tag()
def get_sorted():
    return [
        {
            "title": "Цена",
            "sorters": [
                ("price", "По возрастанию"),
                ("-price", "По убыванию"),
            ],
        },
        {
            "title": "Цвет",
            "sorters": [
                ("color", "От А до Я"),
                ("-color", "От Я до А"),
            ],
        },
        {
            "title": "Размер",
            "sorters": [
                ("size", "По возрастанию"),
                ("-size", "По убыванию"),
            ],
        },
    ]


@register.simple_tag
def get_favoriter_products(user):
    """Вывод всех избранных продуктов на страницу"""

    fav = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products

@register.simple_tag()
def get_favorite_product(user, product):
    product = FavoriteProducts.objects.filter(user=user, product=product)
    return product
