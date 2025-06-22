from django.db import models
from django.conf import settings
from spa_project.materials.models import Course, Lesson

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('bank', 'Перевод на счёт'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='payments')
    paid_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='payments')
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10,
                              choices=PAYMENT_METHODS)
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    payment_url = models.URLField(blank=True, null=True)

    STATUS_CHOICES = [
                ('created', 'Создана'),
                ('paid', 'Оплачена'),
                ('failed', 'Неудачно'),
        ]
    status = models.CharField(
            max_length = 20,
            choices = STATUS_CHOICES,
            default = 'created',
        )

    def __str__(self):
        target = self.course or self.lesson
        return f'{self.user} → {target} ({self.amount}₽)'

