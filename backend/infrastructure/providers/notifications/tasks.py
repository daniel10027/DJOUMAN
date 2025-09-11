from celery import shared_task
from infrastructure.providers.notifications.fcm_adapter import FcmAdapter
from infrastructure.providers.notifications.email_adapter import EmailAdapter
from infrastructure.providers.notifications.sms_adapter import SmsAdapter

@shared_task
def task_send_push(user_id: int, title: str, body: str, data: dict | None = None):
    FcmAdapter().send_push(user_id, title, body, data)

@shared_task
def task_send_email(to: str, subject: str, html: str):
    EmailAdapter().send_email(to, subject, html)

@shared_task
def task_send_sms(to: str, message: str):
    SmsAdapter().send_sms(to, message)
