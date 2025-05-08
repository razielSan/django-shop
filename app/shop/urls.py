from django.urls import path

from shop import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path(
        "category/<slug:slug>/", views.SubCategeries.as_view(), name="category_detail"
    ),
    path("product/<slug:slug>/", views.ProductPage.as_view(), name="product_page"),
    path("user/login_registration/", views.login_registration, name="login_registration"),
    path("user/register", views.user_registration, name="user_registration"),
    path("user/login", views.user_login, name="user_login"),
    path("user/logout", views.user_logout, name="user_logout"),
    path("save_review/<int:product_pk>/", views.save_review, name="save_review"),
    path("add_favorite/<slug:product_slug>/", views.save_favorite_products, name="add_favorite")
]
