from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from shop.models import (
    Product,
    Category,
    Galery,
    Review,
    Mail,
    Order,
    OrderProduct,
    Customer,
    ShippingAddress,
)


class GaleryInline(admin.TabularInline):
    fk_name = "product"
    model = Galery
    extra = 1


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    """Почтовые подписки"""

    list_display = ("pk", "email", "user")
    readonly_fields = ("email", "user")


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["pk", "title", "parent", "get_product_count"]
    prepopulated_fields = {"slug": ("title",)}

    def get_product_count(self, obj):
        return str(len(obj.products.all()))

    get_product_count.short_description = "Количество товаров"


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = [
        "pk",
        "title",
        "price",
        "created_at",
        "quantity",
        "size",
        "color",
        "get_image",
    ]
    list_editable = (
        "price",
        "quantity",
        "size",
        "color",
    )
    list_filter = ["title", "price"]
    list_display_links = ["pk", "title"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = (GaleryInline,)
    # readonly_fields = ["watched"]

    def get_image(self, obj):
        if obj.images.all():
            return mark_safe(f"<img src='{obj.images.first().image.url}' width='75'>")
        return "-"

    get_image.short_description = "Миниатюра"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отображение отзывов в админке"""

    list_display = ["text", "author", "product", "created_at"]
    readonly_fields = ["text", "author", "created_at"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Корзинка"""

    list_display = ["customer", "created_at", "is_completed", "shipping"]
    readonly_fields = ["customer", "is_completed", "shipping"]
    list_filter = ["customer", "is_completed"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Заказчики"""

    list_display = ["user", "first_name", "last_name", "email", "phone"]
    readonly_fields = ["user", "first_name", "last_name", "email", "phone"]
    list_filter = ["user"]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    """Товара в заказах"""

    list_display = ["product", "order", "quantity", "added_at"]
    readonly_fields = ["product", "order", "quantity", "added_at"]
    list_filter = ["product"]


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """Адреса доставки"""

    list_display = ["customer", "order", "city", "street", "state", "created_at"]
    readonly_fields = ["customer", "order", "city", "street", "state", "created_at"]
    list_filter = ["customer"]


admin.site.register(Galery)
