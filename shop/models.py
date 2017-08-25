# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

from django.conf import  settings
from discount.models import Discount

# Create your models here.
def rename(instance,name):
	return instance.store.user.username.replace('@','_')+'/'+instance.store.name+'/'+str(instance.store.created_at)+name

def renameP(instance,name):
	return instance.product.store.user.username.replace('@','_')+'/'+instance.product.store.name + '/' + instance.product.name + '/' +str(instance.created_at)+name

class Store(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	visitors = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='stores_visiters')
	created_at = models.DateTimeField(default=datetime.now, blank=True)
	phoneNumber = models.CharField(max_length=200,null=True)
	facebookPage = models.CharField(max_length=200,null=True)
	locationUrl = models.TextField(null=True)
	activationChoices = (
	    (None, "I do not know now"),
	    (True, "Yes I acknowledge this"),
	    (False, "No, I do not like this")
	)
	isActive = models.NullBooleanField(choices = activationChoices,default=None)
	def __str__(self):
		return self.name

	def get_image(self):
		img = None
		imgs = StoreImage.objects.filter(store=self).order_by("-created_at")
		if imgs:
			img = imgs[0]
		return img



class Trader(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	statusChoices = (("entreprise","entreprise"),("particulier","particulier"))
	status = models.CharField(max_length=200,null=True,choices = statusChoices)
	def __str__(self):
		return self.user.username

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	description = models.TextField()
	quantity = models.IntegerField(null=True,default=1)
	created_at = models.DateTimeField(default=datetime.now, blank=True)
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='likes_of_this_product')
	smiles = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='smiles_of_this_product')
	wishes = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='wishes_of_this_product')
	store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True)
	categorie_choices = (
		('Vetement et accessoires','Vetement et accessoires')
		,('Bijoux','Bijoux')
		,('Founiture creatives','Founiture creatives')
		,('Mariages','Mariages')
		,('Maison','Maison')
		,('Enfant et bebe','Enfant et bebe'))
	categorie = models.CharField(max_length=200,null=True,choices = categorie_choices)
	activationChoices = (
	    (None, "I do not know now"),
	    (True, "Yes I acknowledge this"),
	    (False, "No, I do not like this")
	)
	isActive = models.NullBooleanField(choices = activationChoices,default=None)
	typeChoices = (
	    (1, "Faits main"),
		(2, "Vintage"),
	)
	Ptype = models.IntegerField(null=True,default=2,choices = typeChoices)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('editProduct', kwargs={'id':self.id})

	def get_image(self):
		img = None
		imgs = ProductMainImage.objects.filter(product=self).order_by("-created_at")
		if imgs:
			img = imgs[0]
		return img

	def get_discount(self):
		discounts = Discount.objects.filter(product=self,isActive=True).order_by("-percentage")
		if(discounts):
			return discounts[0]
		else:
			return None

class albumImage(models.Model):
	store = models.ForeignKey(Store,on_delete=models.CASCADE,null=True)
	img = models.ImageField(null=True,upload_to=rename)
	created_at = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.store.name

class ProductMainImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
	img = models.ImageField(null=True,upload_to=renameP)
	created_at = models.DateTimeField(default=datetime.now, blank=True)

class ProductSecImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
	img = models.ImageField(null=True,upload_to=renameP)
	created_at = models.DateTimeField(default=datetime.now, blank=True)

class StoreImage(models.Model):
	store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True)
	img = models.ImageField(null=True,upload_to=rename)
	created_at = models.DateTimeField(default=datetime.now, blank=True)

class Contact(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	subject = models.CharField(max_length=200)
	text = models.TextField()
	created_at = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.subject
