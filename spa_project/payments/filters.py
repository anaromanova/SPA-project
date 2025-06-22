import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    paid_from = django_filters.DateTimeFilter(field_name='paid_at', lookup_expr='gte')
    paid_to   = django_filters.DateTimeFilter(field_name='paid_at', lookup_expr='lte')
    course    = django_filters.NumberFilter(field_name='course__id')
    lesson    = django_filters.NumberFilter(field_name='lesson__id')
    method    = django_filters.ChoiceFilter(field_name='method', choices=Payment.PAYMENT_METHODS)

    class Meta:
        model  = Payment
        fields = ['paid_from', 'paid_to', 'course', 'lesson', 'method']
