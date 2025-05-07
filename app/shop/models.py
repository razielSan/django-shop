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
        """Ссылка на страница категорий"""
        return reverse("category_detail", kwargs={"slug": self.slug})

    def get_parent_cetegory_photo(self):
        """Для получения картинки родительской категории"""
        if self.image:
            return self.image.url
        return "https://stilsoft.ru/images/catalog/noup.png"

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
        return reverse("product_page", kwargs={"slug": self.slug})

    def get_first_photo(self):
        if self.images.all():
            return self.images.first().image.url
        return "data:image/png;base64,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"

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


CHOICES = (
    ("5", "Отлично"),
    ("4", "Хорошо"),
    ("3", "Нормально"),
    ("2", "Плохо"),
    ("1", "Ужасно"),
)


class Review(models.Model):
    """Модель для отзывов"""

    text = models.TextField(verbose_name="Текст")
    grade = models.CharField(
        max_length=20,
        choices=CHOICES,
        blank=True,
        null=True,
        verbose_name="Оценка",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата",
    )

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
