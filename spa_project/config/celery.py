import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
# Загрузка конфигурации из настроек Django, пространство имён CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')
# Автоматический поиск тасков в установленных приложениях
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Опционально: логирование
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')