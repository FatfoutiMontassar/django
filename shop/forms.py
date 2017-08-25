from django import forms
from .models import Store, Product , Contact , StoreImage , ProductMainImage , ProductSecImage , Trader , albumImage

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name","description","phoneNumber","facebookPage","locationUrl","isActive"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name","price","categorie","description","quantity","isActive","Ptype"]

class StoreImageForm(forms.ModelForm):
    class Meta:
        model = StoreImage
        fields = ["img"]

class albumImageForm(forms.ModelForm):
    class Meta:
        model = albumImage
        fields = ["img"]

class addProductMainImageForm(forms.ModelForm):
    class Meta:
        model = ProductMainImage
        fields = ["img"]

class productSImageForm(forms.ModelForm):
    class Meta:
        model = ProductSecImage
        fields = ["img"]

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name","price","categorie","description","quantity"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name","email","subject","text"]

class TraderForm(forms.ModelForm):
    class Meta:
        model = Trader
        fields = ["status"]
