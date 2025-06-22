from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from spa_project.materials.models import Course, Lesson
from .models import Payment
from .serializers import (
    PaymentSerializer,
    PaymentCreateSerializer
)
from .services import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
    retrieve_session,
)
from .filters import PaymentFilter

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = Payment.objects.select_related('user', 'course', 'lesson')
    serializer_class   = PaymentSerializer
    filter_backends    = [DjangoFilterBackend]
    filterset_class    = PaymentFilter
    ordering_fields    = ['paid_at', 'amount']
    ordering           = ['-paid_at']


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    POST /api/payments/ — создать продукт, цену и сессию в Stripe,
    сохранить в нашей БД и вернуть ссылку на оплату.
   """
    serializer_class   = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        course = data.get('course') and get_object_or_404(Course, pk=data['course'])
        lesson = data.get('lesson') and get_object_or_404(Lesson, pk=data['lesson'])
        if not (course or lesson):
            return Response(
                {"detail": "Нужно указать поле course или lesson."},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount_cents = int(float(data['amount']) * 100)

        title = course.title if course else lesson.title
        desc  = getattr(course, 'description', '') or getattr(lesson, 'course').description
        prod  = create_stripe_product(name=title, description=desc)
        pres  = create_stripe_price(product_id=prod.id, unit_amount=amount_cents)
        domain = request.build_absolute_uri('/').rstrip('/')
        success_url = f"{domain}/payment/success/"
        cancel_url  = f"{domain}/payment/cancel/"
        sess    = create_checkout_session(
            price_id=pres.id,
            success_url=success_url,
            cancel_url=cancel_url
        )

        payment = Payment.objects.create(
            user               = user,
            course             = course,
            lesson             = lesson,
            amount             = float(data['amount']),
            method             = data['method'],
            stripe_product_id  = prod.id,
            stripe_price_id    = pres.id,
            stripe_session_id  = sess.id,
            payment_url        = sess.url,
            status             = 'created',
        )

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )


class PaymentStatusAPIView(generics.RetrieveAPIView):
    """
    GET /api/payments/{pk}/status/ — получить и обновить
    статус платежной сессии из Stripe.
    """
    serializer_class   = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset           = Payment.objects.all()
    lookup_field       = 'pk'

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()
        session = retrieve_session(payment.stripe_session_id)
        payment.status = session.payment_status
        payment.save(update_fields=['status'])
        return Response(self.get_serializer(payment).data)
