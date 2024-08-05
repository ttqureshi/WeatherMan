from rest_framework import serializers
from django.contrib.auth.models import User

from products.models import Category, Product, ReviewRating


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    reviews = serializers.HyperlinkedRelatedField(many=True, view_name='reviewrating-detail', read_only=True)

    class Meta:
        model = Product
        fields = ["url", "id", "name", "description", "price", "image", "stock", "category", "reviews"]


class ReviewRatingSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True)
    class Meta:
        model = ReviewRating
        fields = ["id", "product", "user", "review", "rating", "created_at"]
