from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from rest_framework import generics

from django.conf.urls.static import static
from notifications.models import Notification
from . import views
from serializers import UserSerializer, GroupSerializer , ProductSerializer , StoreSerializer , NotifSerializer , AllNotifSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404



class AllNotifList(generics.ListAPIView):
    serializer_class = AllNotifSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        user = get_object_or_404(User,username=username)
        return Notification.objects.filter(to_user=user)

class CreateNotif(generics.CreateAPIView):
    serializer_class = AllNotifSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        user = get_object_or_404(User,username=username)
        return Notification.objects.filter(to_user=user)

class NotifSendAPIView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotifSerializer
    def post(self,request,to_user ):
        serializer = MessageSendSerializer(data=request.data)
        serializer2 = MessageSendSerializer(data=request.data)
        user = User.objects.get(username=to_user)
        if serializer.is_valid() and serializer2.is_valid():
            serializer.save(from_user=request.user,user=user,conversation=request.user)
            serializer2.save(from_user=request.user, user=request.user, conversation=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
urlpatterns = [
    url('^Notifs/(?P<username>[^/]+)/$', AllNotifList.as_view(),name="test test test"),
    url('^CreateNotif/(?P<username>[^/]+)/$', CreateNotif.as_view(),name="test test test"),

]
