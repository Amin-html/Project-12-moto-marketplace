from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
# @shared_task — декоратор, который превращает обычную функцию
# в задачу, которую Celery может выполнить асинхронно, в фоне,
# не блокируя основной запрос
def send_order_status_email(order_id, new_status):
    from .models import Order
    # импорт внутри функции, а не наверху файла — частая практика
    # в Celery-задачах, чтобы избежать проблем с порядком загрузки
    # приложений при старте Django

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    send_mail(
        subject=f'Заказ #{order.id} — статус обновлён',
        message=f'Ваш заказ теперь в статусе: {new_status}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        fail_silently=True,
    )