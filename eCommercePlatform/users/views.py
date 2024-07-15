from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .forms import UserRegisterForm, OrderForm, UserUpdateForm
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            cart = Cart(user=request.user)
            cart.save()
            return redirect("products:products-listing")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("products:products-listing")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        redirect("products:products-listing")


@login_required(login_url="/login")
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("users:profile")
        else:
            error_message = (
                "Password change unsuccessful. Please correct the errors below."
            )
            if "password_form" in locals() and password_form.errors:
                error_message += f' Reason: {", ".join([", ".join(errors) for errors in password_form.errors.values()])}'
            messages.error(request, error_message)

    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {"user_form": user_form, "password_form": password_form}

    return render(request, "users/user_profile.html", context)


@login_required(login_url="/login")
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.cartitem_set.all()
    total_price = sum(item.quantity * item.product.price for item in items)

    return render(
        request, "users/cart.html", {"cart": cart, "total_price": total_price}
    )


@login_required(login_url="/login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    in_stock = product.stock > 0

    if in_stock:
        cart = Cart.objects.get(user=request.user)
        cart_item, is_created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )

        if not is_created:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1

    return redirect("products:products-listing")


@login_required(login_url="/login")
def update_cart_item(request, product_id):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.get(product_id=product_id)
        product = Product.objects.get(id=product_id)
        stock_left = product.stock
        quantity = int(request.POST.get("quantity"))
        if quantity <= stock_left:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            messages.warning(
                request, f"Only {stock_left} {product.name} left in stock."
            )
        return redirect("users:cart")
    return redirect("users:cart")


@login_required(login_url="/login")
def remove_item(request, product_id):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        cart_item = cart.cartitem_set.get(product_id=product_id)
        cart_item.delete()
        return redirect("users:cart")


@login_required(login_url="/login")
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.cartitem_set.all()
    total_price = sum(item.quantity * item.product.price for item in items)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order, product=cart_item.product, quantity=cart_item.quantity
                )
                product = Product.objects.get(id=cart_item.product.id)
                product.stock -= cart_item.quantity
                product.save()

            cart.cartitem_set.all().delete()

            return render(request, "users/order_confirmation.html", {"order": order})
    else:
        form = OrderForm()
    return render(
        request,
        "users/checkout.html",
        {"form": form, "cart": cart, "total_price": total_price},
    )


@login_required(login_url="/login")
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "users/order_history.html", {"orders": orders})


@login_required(login_url="/login")
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "users/order_detail.html", {"order": order})
