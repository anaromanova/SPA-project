from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = Payment.objects.select_related('user', 'course', 'lesson')
    serializer_class   = PaymentSerializer
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = PaymentFilter
    ordering_fields    = ['paid_at', 'amount']
    ordering           = ['-paid_at']

