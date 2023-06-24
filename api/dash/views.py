from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from api.serializers import SubscriberSerializer, EmailSerializer, EmailOpenSerializer
from api.models import Subscriber, EmailOpen, Email
from api.views import logger



class SubscriberDashView(viewsets.ModelViewSet):
    serializer_class = SubscriberSerializer
    def get_queryset(self):
        return Subscriber.objects.get(id=self.id)

    def get(self, request, subscriber_id):
        try:
            if Subscriber.objects.filter(id=subscriber_id).exists():
                self.id = subscriber_id
                opened_emails = EmailOpen.objects.filter(subscriber=self.get_queryset())
                serializer = EmailOpenSerializer(opened_emails, many=True)
                return Response({
                    'person' : SubscriberSerializer(self.get_queryset()).data,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'status': 'error', 'details' : 'no subscriber exists'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'error', 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, subscriber_id):
        try:
            if Subscriber.objects.filter(id=subscriber_id).exists():
                self.id = subscriber_id
                subscriber = self.get_queryset()
                serializer = SubscriberSerializer(subscriber, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'error', 'details' : 'no subscriber exists'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'error', 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class EmailDashView(viewsets.ModelViewSet):
    serializer_class = EmailOpenSerializer
    def get_queryset(self):
        return Email.objects.get(id=self.id)
    
    def get(self, request, email_id):
        try:
            if Email.objects.filter(id=email_id).exists():
                self.id = email_id
                opened_users = EmailOpen.objects.filter(email=self.get_queryset())
                serializer = EmailOpenSerializer(opened_users, many=True)
                return Response({
                    'newsletter' : EmailSerializer(self.get_queryset()).data,
                    'data' : serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'status': 'error', 'details' : 'no email exists'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'error', 'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
