from django.urls import path
from Projekti import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('category', views.CategoryViewSet)
router.register('product', views.ProductViewSet)
router.register('variations', views.VariationViewSet)
router.register('review', views.ReviewRatingViewSet)
router.register('invoice', views.InvoiceViewSet)
router.register('invoice_item', views.InvoiceItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
]
