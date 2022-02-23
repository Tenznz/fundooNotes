# from celery import task
from celery import shared_task
from celery.utils.log import get_task_logger
from .email import Email

# from django.conf import settings

logger = get_task_logger(__name__)


@shared_task
def send_email_task(token, email):
    try:
        Email().send_email(token=token, email_id=email)
    except Exception as e:
        print("task fail")
        logger.error(e)
