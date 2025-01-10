from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Названия")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Slider(models.Model):
    preview = models.ImageField(upload_to="images/slider", verbose_name="Изображение")

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдеры"


class Products(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="Категория"
    )
    short_description = models.TextField(max_length=40, verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание")
    preview = models.ImageField(upload_to="images/products", verbose_name="Изображение")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    in_stock = models.IntegerField(default=0, verbose_name="В наличии")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductsGallery(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    image = models.ImageField(
        upload_to="images/products_gallery", verbose_name="Изображение продукта"
    )

    class Meta:
        verbose_name = "Галерея товара"
        verbose_name_plural = "Галерея товаров"


class Comment(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name="Автор"
    )
    text = models.TextField(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return f"{self.post} - {self.author} - {self.created_at.date}"

    class Meta:
        verbose_name = "Коммент"
        verbose_name_plural = "Комменты"


class ProductsViews(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    session_id = models.TextField()


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        total = self.product.price * self.quantity
        return f"{self.user} - {self.product} - {self.quantity} - {total}$"

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="images/avatar", null=True, blank=True, verbose_name="Аватар"
    )
    bio = models.TextField(blank=True, verbose_name="Биография")

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
