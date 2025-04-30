from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Имя категории",
    )
    image = models.ImageField(
        upload_to="categories/",
        verbose_name="Изображение категории",
        null=True,
        blank=True,
    )
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="subcategories",
    )

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Категория: pk={self.pk}, title={self.title}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    title = models.CharField(
        max_length=250,
        verbose_name="Наименование товара",
    )
    price = models.FloatField(verbose_name="Цена товара")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    watched = models.IntegerField(
        default=0,
        verbose_name="Количество просмотров",
    )
    quantity = models.IntegerField(
        default=0,
        verbose_name="Количество на складе",
    )
    description = models.TextField(
        default="Здесь скоро будет описание", verbose_name="Описание товара"
    )
    info = models.TextField(
        default="Дополнительная информация о товаре",
        verbose_name="Информация о товаре",
    )
    category = models.ForeignKey(
        Category,
        related_name="products",
        verbose_name="Категории",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        unique=True,
        null=True,
    )
    size = models.IntegerField(default=30, verbose_name="Размер в мм")
    color = models.CharField(
        default="Серебро", max_length=30, verbose_name="Цвет/Материал"
    )


    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Товар: pk={self.pk}, title={self.title}, price={self.price}"


    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Galery(models.Model):
    image = models.ImageField(upload_to="products/", verbose_name="Изображение")
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Изображения"
        verbose_name_plural = "Галерея товаров"
