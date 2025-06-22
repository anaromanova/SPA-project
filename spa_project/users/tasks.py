from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    cutoff = timezone.now() - timedelta(days=30)
    inactive = User.objects.filter(last_login__lt=cutoff, is_active=True)
    inactive.update(is_active=False)