from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription

@shared_task
def send_update_notifications(course_id):
    course = Course.objects.get(pk=course_id)
    # Проверяем, что курс не обновлялся более 4 часов
    if course.updated_at and (timezone.now() - course.updated_at) < timedelta(hours=4):
        return

    subs = Subscription.objects.filter(course=course).select_related('user')
    for sub in subs:
        send_mail(
            subject=f"Новый материал в курсе '{course.title}'",
            message=f"Здравствуйте, {sub.user}! В курсе {course.title} появились новые материалы.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
        )