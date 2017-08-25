from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from shop.models import Product
from collection.models import Collection
# Create your models here.
def rename(instance,name):
	return instance.user.username.replace('@','_')+'/profile/'+str(instance.created_at)+name


class Profile(models.Model):
	user = models.OneToOneField(User,default=1)
	url = models.CharField(max_length=50, null=True, blank=True)
	job_title = models.CharField(max_length=50, null=True, blank=True)
	picture = models.ImageField(null=True,upload_to=rename)
	created_at = models.DateTimeField(default=datetime.now, blank=True)
	wishedProducts = models.ManyToManyField(Product,blank=True,related_name="wished_products")
	wishedCollections = models.ManyToManyField(Collection,blank=True,related_name="wished_collections")
	location = models.CharField(max_length=50, null=True, blank=True)
	message = models.CharField(max_length=250, null=True, blank=True)

	def __str__ (self):
		return self.user.username
