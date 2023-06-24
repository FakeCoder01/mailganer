from celery import shared_task
from django.core.mail import EmailMessage
from .models import Subscriber
from django.conf import settings

@shared_task(bind=True)
def send_newsletter(self, email_id, email_subject:str, email_body:str, subscriber_id):
    try:
        tracking_url = f"{settings.DOMAIN_NAME}/api/'email_open/{email_id}/{subscriber_id}/"
        tracking_pixel = f'<img src="{tracking_url}"/>'

        subscriber = Subscriber.objects.get(id=subscriber_id)
        email_body.replace("[first_name]", subscriber.first_name)
        email_body.replace('[last_name]', subscriber.last_name)
        email_body.replace('[birthday]', str(subscriber.birthday))

        email_body += tracking_pixel
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email="asamajder836@gmail.com",
            to=[subscriber.email]
        )
        email.content_subtype = "html"
        email.send()
        print("sent..")
    except Exception as e:
        self.retry(exc=e, max_retries=3)


