from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Product, ReviewRating
from .forms import ReviewForm

def products_listing_view(request):
    category = request.GET.get("category")
    if category:
        products = Product.objects.filter(category__name=category)
    else:
        products = Product.objects.all()

    p = Paginator(products, 6)
    page_number = request.GET.get("page")
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(
        request,
        "products/products_listing.html",
        {"page_obj": page_obj, "selected_category": category},
    )


def product_detail_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    reviews = ReviewRating.objects.filter(product=product)
    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, "products/product_detail.html", context)


def search(request):
    search_query = request.GET.get('search')
    search_results = Product.objects.filter(description__icontains=search_query)
    return render(request, "products/search.html", {
        "search_query": search_query,
        "search_results": search_results,
    })


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thanks You! Your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.product = Product.objects.get(id=product_id)
                data.user = User.objects.get(id=request.user.id)
                data.save()
                messages.success(request, "Thank You! Your review has been submitted.")
                return redirect(url)
