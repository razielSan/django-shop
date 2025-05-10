from django.contrib import admin
from django.utils.safestring import mark_safe

from shop.models import Product, Category, Galery, Review, Mail


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
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "parent", "get_product_count"]
    prepopulated_fields = {"slug": ("title",)}

    def get_product_count(self, obj):
        return str(len(obj.products.all()))

    get_product_count.short_description = "Количество товаров"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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


admin.site.register(Galery)
