from rest_framework import serializers
from .models import Subscriber, Email, EmailOpen

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'first_name', 'last_name', 'email', 'birthday']

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'subject', 'body', 'sent_at']

class EmailOpenSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="email.subject")
    first_name = serializers.CharField(source="subscriber.first_name")
    last_name = serializers.CharField(source="subscriber.last_name")
    address = serializers.EmailField(source="subscriber.email")
    class Meta:
        model = EmailOpen
        fields = ["id", "opened_at", "email", "subscriber", "subject", "first_name", "last_name", "address"]
