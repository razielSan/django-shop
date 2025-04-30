from django.urls import path

from shop import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
]
