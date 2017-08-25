from django.contrib.auth.models import User, Group
from rest_framework import serializers
from shop.models import Product , Store
from notifications.models import Notification

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('store','name', 'description','price','quantity','categorie','Ptype')

class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        fields = ('user','name', 'description')

class NotifSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('from_user','to_user', 'notification_type','product')

class AllNotifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('from_user','to_user', 'notification_type','product')
