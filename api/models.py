from django.db import models
import uuid
# Create your models here.

class Subscriber(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birthday = models.DateField()

    def __str__(self):
        return self.email


class Email(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class EmailOpen(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    opened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subscriber.email} opened {self.email.subject}'
