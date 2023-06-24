from django.urls import path, include
from .views import SubscriberView, NewsletterView, EmailOpenView

urlpatterns = [
    path('subscriber/', SubscriberView.as_view(), name='api_subscriber'),
    path('newsletter/', NewsletterView.as_view(), name='api_newsletter'),
    path('email_open/<str:email_id>/<int:subscriber_id>/', EmailOpenView.as_view(), name='email_open'),
    path('', include('api.dash.urls'),name="dash_view"),
]