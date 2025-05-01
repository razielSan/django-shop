from django.urls import path

from shop import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("category/<slug:slug>/", views.SubCategeries.as_view(), name='category_detail')
]
