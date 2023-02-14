from Projekti import serializers
from rest_framework import viewsets
from Projekti import models
from rest_framework.authentication import TokenAuthentication
from Projekti import permissions

from rest_framework import filters

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


# 3
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    # 2
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = (IsAuthenticated,)


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = (IsAuthenticated,)


class InvoiceViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.InvoiceSerializer
    queryset = models.Invoice.objects.all()
    permission_classes = (permissions.UpdateOwnInvoice, IsAuthenticated)


class InvoiceItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.InvoiceItemSerializer
    queryset = models.InvoiceItem.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        if serializer.is_valid():
            item = serializer.validated_data
            product = item.get('product')
            product.quantity -= item.get('quantity')
            if product.quantity >= 0:
                product.save()
                serializer.save(price=product.price)

    def perform_update(self, serializer):
        item = serializer.validated_data
        product = item.get('product')
        product.quantity -= serializer.validated_data.get('quantity')
        product.save()
        serializer.save(price=product.price)


class VariationViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.VariationsSerializer
    queryset = models.Variation.objects.all()
    permission_classes = (IsAuthenticated,)


class ReviewRatingViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ReviewRatingSerializer
    queryset = models.ReviewRating.objects.all()
    permission_classes = (IsAuthenticated,)
