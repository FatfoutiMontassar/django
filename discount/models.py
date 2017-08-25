from __future__ import unicode_literals

from django.db import models
from django.conf import  settings
from datetime import datetime

# Create your models here.

class Discount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    product = models.ForeignKey('shop.Product',null=True,blank=True,related_name='discount_product')
    collection = models.ForeignKey('collection.Collection',null=True,blank=True,related_name='discount_collection')
    start = models.DateTimeField(default=datetime.now, blank=True)
    end   = models.DateTimeField(default=datetime.now, blank=True)
    discount_type = models.CharField(max_length=1)
    length_type= models.CharField(max_length=10)
    percentage = models.IntegerField(null=True,default=1)
    activationChoices = (
	    (True, "Yes I acknowledge this"),
	    (False, "No, I do not like this")
	)
    isActive = models.NullBooleanField(choices = activationChoices,default=False)

    def secondsLeft(self):
        delta = self.end.replace(tzinfo=None) - datetime.now()
        return delta.seconds

    def __str__(self):
        return str(self.percentage)
