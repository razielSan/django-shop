from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from shop.models import Category, Product, Galery, Review, Customer, ShippingAddress


class UserAuthenticatedForm(AuthenticationForm):
    """Аутентификация пользователя"""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Логин")},
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Пароль")},
        )
    )


class UserRegisterForm(UserCreationForm):
    """Регистрация пользователя"""

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Введите пароль"),
            },
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Подтвердите пароль"),
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
                    "placeholder": _("Имя пользователя"),
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Почта"),
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
                    "placeholder": _("Ваш отзыв....."),
                }
            ),
            "grade": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Ваша оценка"),
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
                    "placeholder": _("Вася"),
                }
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Пупкин")}
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("vasya@pupkin.uz"),
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+99513437832",
                }
            ),
        }


class ShippingForm(forms.ModelForm):
    """Адрес Доставки"""

    class Meta:
        model = ShippingAddress
        fields = ("city", "street", "state")
        widgets = {
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Киев"),
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Яшнабад"),
                }
            ),
            "street": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Улица/Дом/Квартира....."),
                }
            ),
        }
