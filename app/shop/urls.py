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
    path("add_favorite/<slug:product_slug>/", views.save_favorite_products, name="add_favorite"),
    path("user_favorits/", views.FavoriteProductsView.as_view(), name="favorite_product_page"),
    path("save_email/", views.save_subscribers, name="mail_distribution"),
    path("send_email/", views.send_mail_to_subscribe, name="send_email"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/", views.create_checkout_session, name="payment"),
    path("payment_success/", views.success_payment, name="success"),
    path("cart/", views.cart, name="cart"),
    path("to-cart/<int:product_id>/<str:action>/", views.to_cart, name="to_cart"),
]
