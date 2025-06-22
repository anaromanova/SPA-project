from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка и детального просмотра платежей,
    включает все Stripe-поля и статус.
    """
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'paid_at',
            'course', 'lesson',
            'amount', 'method',
            'stripe_product_id', 'stripe_price_id',
            'stripe_session_id', 'payment_url', 'status',
        ]
        read_only_fields = fields


class PaymentCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания платежа:
    клиент передаёт course или lesson, amount и method.
   """
    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'amount', 'method']
