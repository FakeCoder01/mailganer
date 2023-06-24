from django.contrib import admin
from .models import Email, EmailOpen, Subscriber


# Register your models here.


admin.site.register(Email)
admin.site.register(EmailOpen)
admin.site.register(Subscriber)