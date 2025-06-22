from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lesson
from .tasks import send_update_notifications

@receiver(post_save, sender=Lesson)
def lesson_updated_handler(sender, instance, created, **kwargs):
    if not created:
        send_update_notifications.delay(instance.course.id)