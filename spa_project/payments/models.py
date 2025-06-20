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

    def __str__(self):
        target = self.course or self.lesson
        return f'{self.user} → {target} ({self.amount}₽)'

