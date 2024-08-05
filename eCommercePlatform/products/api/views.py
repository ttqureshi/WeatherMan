from rest_framework import viewsets
from django.contrib.auth.models import User

from products.models import Category, Product, ReviewRating
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewRatingSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewRatingViewSet(viewsets.ModelViewSet):
    queryset = ReviewRating.objects.all()
    serializer_class = ReviewRatingSerializer
