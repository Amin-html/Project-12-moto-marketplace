import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moto_config.settings')

app = Celery('moto_config')

# Читаем конфигурацию из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи (tasks.py) в ваших приложениях (accounts, catalog и т.д.)
app.autodiscover_tasks()
