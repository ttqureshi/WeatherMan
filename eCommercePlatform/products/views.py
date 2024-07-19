from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    return render(request, "products/product_detail.html", {"product": product})


def search(request):
    search_query = request.GET.get('search')
    search_results = Product.objects.filter(description__icontains=search_query)
    return render(request, "products/search.html", {
        "search_query": search_query,
        "search_results": search_results,
    })
