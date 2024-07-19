from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.products_listing_view, name="products-listing"),
    path("<int:product_id>/", views.product_detail_view, name="detail"),
    path("search/", views.search, name="search"),
]
