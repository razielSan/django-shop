from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from shop.models import (
    Category,
    Product,
    Galery,
    Review,
    Customer,
    ShippingAddress
)


class UserAuthenticatedForm(AuthenticationForm):
    """Аутентификация пользователя"""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Логин"},
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"},
        )
    )


class UserRegisterForm(UserCreationForm):
    """Регистрация пользователя"""

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"},
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Подтвердите пароль",
            }
        )
    )

    class Meta:
        model = User
        fields = {
            "username",
            "email",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Имя пользователя",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Почта",
                }
            ),
        }


class ReviewForms(forms.ModelForm):
    """Форма для отзыва"""

    class Meta:
        model = Review
        fields = (
            "text",
            "grade",
        )
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ваш отзыв.....",
                }
            ),
            "grade": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ваша оценка",
                }
            ),
        }


class CustomerForm(forms.ModelForm):
    """Контактная информация"""

    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Вася",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Пупкин"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "vasya@pupkin.uz",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+99513437832"
                }
            )
        }


class ShippingForm(forms.ModelForm):
    """ Адрес Доставки """

    class Meta:
        model = ShippingAddress
        fields = ("city", "street", "state")
        widgets = {
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Киев",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Яшнабад"
                }
            ),
            "street": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Улица/Дом/Квартира....."
                }
            ),
        }