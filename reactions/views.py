from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from shop.models import Product
from notifications.models import Notification
from django.shortcuts import get_object_or_404
# Create your views here.

def reactionRemove(request,id):
    if not request.user.is_authenticated():
        raise Http404
    product = get_object_or_404(Product,id=id)

    if(request.user in product.likes.all() ):
        product.likes.remove(request.user)

    if(request.user in product.smiles.all() ):
        product.smiles.remove(request.user)

    if(request.user in product.wishes.all() ):
        product.wishes.remove(request.user)

    print("reaction removed successfully from reactions application...")

    return HttpResponse(product.likes.count() + product.smiles.count() + product.wishes.count())

def reactionLike(request,id):
    if not request.user.is_authenticated():
        raise Http404
    print("this should work !")
    product = get_object_or_404(Product,id=id)
    if(request.user in product.likes.all() ):
        product.likes.remove(request.user)

    if(request.user in product.smiles.all() ):
        product.smiles.remove(request.user)

    if(request.user in product.wishes.all() ):
        product.wishes.remove(request.user)

    if request.user.id != product.store.user.id:
        notif = Notification(from_user=request.user,to_user=product.store.user,
                            notification_type='L',product=product)
        notif.save()


    product.likes.add(request.user)
    product.save()
    print("reaction --Like-- added  successfully from reactions application...")

    return HttpResponse(product.likes.count() + product.smiles.count() + product.wishes.count())

def reactionLove(request,id):
    if not request.user.is_authenticated():
        raise Http404
    product = get_object_or_404(Product,id=id)
    if(request.user in product.likes.all() ):
        product.likes.remove(request.user)

    if(request.user in product.smiles.all() ):
        product.smiles.remove(request.user)

    if(request.user in product.wishes.all() ):
        product.wishes.remove(request.user)

    if request.user.id != product.store.user.id:
        notif = Notification(from_user=request.user,to_user=product.store.user,
                            notification_type='O',product=product)
        notif.save()

    product.smiles.add(request.user)
    product.save()
    print("reaction --Love-- added successfully from reactions application...")

    return HttpResponse(product.likes.count() + product.smiles.count() + product.wishes.count())

def reactionWow(request,id):
    if not request.user.is_authenticated():
        raise Http404
    product = get_object_or_404(Product,id=id)
    if(request.user in product.likes.all() ):
        product.likes.remove(request.user)

    if(request.user in product.smiles.all() ):
        product.smiles.remove(request.user)

    if(request.user in product.wishes.all() ):
        product.wishes.remove(request.user)

    if request.user.id != product.store.user.id:
        notif = Notification(from_user=request.user,to_user=product.store.user,
                            notification_type='W',product=product)
        notif.save()

    product.wishes.add(request.user)
    product.save()
    print("reaction --Wow-- added successfully from reactions application...")

    return HttpResponse(product.likes.count() + product.smiles.count() + product.wishes.count())
