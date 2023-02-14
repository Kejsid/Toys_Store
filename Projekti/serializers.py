# 1
from rest_framework import serializers
# 3
from Projekti import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'lastname', 'age', 'gender', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            lastname=validated_data['lastname'],
            age=validated_data['age'],
            gender=validated_data['gender']
        )

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'category_name', 'description', 'image')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
        'id', 'description', 'product_name', 'quantity', 'price', 'created_date', 'is_available', 'category')

    def validate(self, data):
        if data['quantity'] < 0:
            raise serializers.ValidationError("Product quantity can't be negative")
        return data


class InvoiceSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, invoice):
        return InvoiceItemSerializer(invoice.invoiceitem_set.all(), many=True).data

    class Meta:
        model = models.Invoice
        fields = ('id', 'client', 'date', 'total', 'items')


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvoiceItem
        fields = ('id', 'product', 'invoice', 'quantity', 'price', 'total')
        extra_kwargs = {'total': {'read_only': True}, 'price ': {'read_only': True}}


class VariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variation
        fields = ('id', 'product', 'variations_category', 'gender', 'is_active', 'created_date')


class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewRating
        fields = ('id', 'product', 'user', 'subject', 'review', 'rating', 'created_at')
