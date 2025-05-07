from django import template
from django.template.defaulttags import register as range_register

from shop.models import Category


register = template.Library()


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
