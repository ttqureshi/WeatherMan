from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"  # designates that these urls are inside the users app

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="products:products-listing"),
        name="logout",
    ),
    path("profile/", views.profile, name="profile"),
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:product_id>", views.add_to_cart, name="add-to-cart"),
    path(
        "update-cart-item/<int:product_id>",
        views.update_cart_item,
        name="update-cart-item",
    ),
    path("remove-item/<int:product_id>", views.remove_item, name="remove-item"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.orders, name="orders"),
    path("order-detail/<int:order_id>", views.order_detail, name="order-detail"),
]
