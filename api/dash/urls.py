from django.urls import path
from .views import SubscriberDashView, EmailDashView
urlpatterns = [
    path('email/<str:email_id>/', EmailDashView.as_view({'get' : 'get'}), name="email_dash_view"),
    path("subscriber/<str:subscriber_id>/", SubscriberDashView.as_view({
        'get' : 'get', 'put': 'put'
    }), name="subscriber_dash_view"),
]