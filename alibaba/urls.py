"""alibaba URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include , url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from quickstart import views
# Serializers define the API representation.
'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'stores', views.StoreViewSet)
router.register(r'notifs', views.NotifViewSet)
#router.register(r'notifs', views.AllNotifViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^', include('discover.urls') ),
	url(r'^shop/', include('shop.urls') ),
    url(r'^messenger/', include('messenger.urls') ),
    url(r'^authentication/', include('authentication.urls') ),
    url(r'^discover/', include('discover.urls') ),
    url(r'^notifications/', include('notifications.urls') ),
    url(r'^reactions/', include('reactions.urls') ),
    url(r'^collections/', include('collection.urls' , namespace="collections") ),
    url(r'^discounts/', include('discount.urls') ),
    url(r'^admin/', admin.site.urls),
    url(r'^router/', include(router.urls)),
    url(r'^quickstart/', include('quickstart.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
