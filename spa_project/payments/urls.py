from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentCreateAPIView, PaymentStatusAPIView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('payments-create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/<int:pk>/status/', PaymentStatusAPIView.as_view(), name='payment-status'),
]
