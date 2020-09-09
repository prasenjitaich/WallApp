from django.core.mail import send_mail
from wall_app.settings import settings


def send_email(subject, recipient, body, message=None):
    sender = settings.EMAIL_HOST_USER
    send_mail(
        subject=subject,
        message=message,
        from_email=sender,
        recipient_list=recipient,
        html_message=body,
    )
