from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SubscriberSerializer, EmailSerializer
from .tasks import send_newsletter
from .models import Subscriber, EmailOpen, Email
import logging, base64
from django.http import HttpResponse
from celery import group



logger = logging.getLogger(__name__)




class SubscriberView(APIView):

    def get(self, request):
        try:
            return Response(SubscriberSerializer(Subscriber.objects.all(), many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'error', 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = SubscriberSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'error', 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewsletterView(APIView):

    def get(self, request):
        try:
            return Response(EmailSerializer(Email.objects.all(), many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'error', 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.save()
                subscribers = Subscriber.objects.all()
                tasks = group(send_newsletter.s(email.id, email.subject, str(email.body), subscriber.id) for subscriber in subscribers)
                tasks.apply_async(countdown=int(request.data.get('delay')) if 'delay' in request.data else 0)
                return Response({'status': 'success'}, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'error', 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailOpenView(APIView):
    def get(self, request, email_id, subscriber_id):
        try:
            email = Email.objects.get(id=email_id)
            subscriber = Subscriber.objects.get(id=subscriber_id)
            EmailOpen.objects.create(email=email, subscriber=subscriber)
            logger.info(f'Email with subject "{email.subject}" was opened by {subscriber.email}')

            PIXEL_GIF_DATA = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
            data = base64.b64decode(PIXEL_GIF_DATA)
            response = HttpResponse(data, content_type='image/gif')
            return response
            # return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except (Email.DoesNotExist, Subscriber.DoesNotExist):
            return Response({'status': 'error', 'message': 'Email or subscriber not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'error', 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

