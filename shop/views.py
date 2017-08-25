# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from .models import Product, Store, Contact, StoreImage, ProductMainImage, ProductSecImage , Trader , albumImage
from .forms import StoreForm, ProductForm, ContactForm, EditProductForm, StoreImageForm, addProductMainImageForm, \
    productSImageForm , TraderForm , albumImageForm
from authentication.models import Profile
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import re
from django.views.generic import RedirectView
from messenger.models import Message
import json

# Create your views here.


categoriesList = ["Vetement et accessoires", "Bijoux", "Founiture creatives", "Mariages", "Maison", "Enfant et bebe"]

def getCount(categorie):
    products = Product.objects.all()
    return products.filter(categorie=categorie).count()


def getCountFromList(categorie, tab):
    ret = 0
    for x in tab:
        if x.categorie == categorie:
            ret += 1
    return ret


def getId(cat):
    id = 1
    for x in categoriesList:
        if cat == x:
            return id
        id += 1
    return 0


def getMainImage(product):
    return product.get_image



def getStoreImage(store):
    imgs = StoreImage.objects.filter(store=store).order_by("-created_at")
    img = None
    if imgs:
        img = imgs[0]
    return img

def getSecImages(product):
    imgs = ProductSecImage.objects.filter(product=product).order_by("-created_at")
    ret = []

    #print "images here :: " + str(imgs.count())
    for img in imgs:
        ret.append(img)
        #print " --  : " + str(img.img)
    return ret

def match(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    # print str1 + " -- " + str2
    for i in range(0, len(str2) - len(str1) + 1):
        # print " i :: " + str(i) + str2[i]
        flag = True
        for j in range(0, len(str1)):
            # print "    j :: " + str(j) + str1[j]
            if str1[j] != str2[i + j]:
                flag = False
                break
        if flag:
            return True
    return False

def products(request):
    ans = Product.objects.all()
    ret = []
    template = '{0} ({1})'
    for p in ans:
        ret.append(p.name)
    data = json.dumps(ret)
    return HttpResponse(data,content_type='application/json')

def album(request, id):
    if (request.method == 'POST'):
        form = productSImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.product = Product.objects.get(id=id)
            instance.save()
            return redirect('/shop/album/' + str(id))
        else:
            #print "error !!"
            # print form.errors
            return redirect('/shop/album/' + str(id))
        return redirect(request, '/shop/album/' + str(id))
    else:
        product = get_object_or_404(Product, id=id)
        form = productSImageForm()
        imgs = ProductSecImage.objects.filter(product=product).order_by("-created_at")
        context = {
            'product': product,
            'form': form,
            'imgs': imgs,
        }
        return render(request, 'album.html', context)


def editStore(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == get_object_or_404(Store, id=id).user.id):
        raise Http404

    if (request.method == 'POST'):
        form = StoreForm(request.POST or None)

        if form.is_valid():
            store = get_object_or_404(Store, id=id)
            store.name = form.cleaned_data['name']
            store.description = form.cleaned_data['description']
            store.phoneNumber = form.cleaned_data['phoneNumber']
            store.facebookPage = form.cleaned_data['facebookPage']
            store.locationUrl = form.cleaned_data['locationUrl']
            store.isActive = form.cleaned_data['isActive']

            # print product.name
            # print str(product.id)
            store.save()
            return redirect('/shop/stores/' + str(id))

    else:
        store = get_object_or_404(Store, id=id)
        form = StoreForm(instance=store)
        context = {'store': store, 'form': form, }
        return render(request, 'editStore.html', context)


def duplicateProduct(request, id):
    product = get_object_or_404(Product, id=id)
    imgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")
    product.id = None
    product.created_at = datetime.now()
    product.save()
    # print product.id
    if imgs:
        img = imgs[0]
        newimg = ProductMainImage(img=img.img, product=product)
        newimg.save()

    return redirect('/shop/details/' + str(product.store.id))


def activateProduct(request, id):
    product = get_object_or_404(Product, id=id)
    if product.isActive == True:
        #print "become not active"
        product.isActive = False
    else:
        #print "become active"
        product.isActive = True
    product.save()
    return redirect('/shop/product_details/' + str(int(id)))


def addProductMainImage(request, id):
    form = addProductMainImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.product = Product.objects.get(id=id)
        instance.save()
        return redirect('/shop/product_details/' + str(id))
    else:
        #print "error !!"
        #print form.errors
        # print form.errors
        return redirect('/shop/product_details/' + str(id))

def search(request):
    # print "ok"
    # return redirect('/shop')
    Ptype = request.GET.get('Ptype', 'all')
    #print Ptype

    Prange = request.GET.get('Prange', 'all')
    #print Prange

    Pmin = request.GET.get('Pmin',0)
    Pmax = request.GET.get('Pmax',10000)

    categorie = "Tous les categories"

    srchFld = request.GET.get('q', '')

    srchTxt = request.GET.get('categorie', '')

    categorie = str(srchTxt)


    mapInt2String = ["Tous les categories", "Vetement et accessoires", "Bijoux", "Founiture creatives", "Mariages",
                     "Maison", "Enfant et bebe", "Boutiques", "utilisateurs"]
    mapString2Int = []

    '''
		i'm gonna redirect users to /shop/search/categorieIdx/TypeIdx
		and i'm gonna pass the search items in the context
		we could actually get the results from here and send them to the next page!
	'''
    #srchFld = request.POST.get('srchFld')
    #categorie = request.POST.get('srchTxt')
    wordList = re.sub("[^\]", " ", str(srchFld) ).split()

    products = Product.objects.all().order_by("-created_at")

    if(Ptype=="handMade"):
        products = products.filter(Ptype=1)
    if(Ptype=="vintage"):
        products = products.filter(Ptype=2)

    products = products.filter(price__gte=Pmin)
    products = products.filter(price__lte=Pmax)

    result = []
    tab = []

    for product in products:
        if(ok(product.price,str(Prange))):
            score = 0
            for word in wordList:
                # print word + " -- " + str(product.name)
                # print word + " -- " + str(product.description)
                if (match(word, str(product.name))):
                    # print "ok"
                    score += 4
                if (match(word, str(product.description))):
                    score += 1
            if score > 0:
                if ((product.categorie == categorie) or (categorie == "Tous les categories")):
                    result.append((product, score, getMainImage(product)))
                tab.append(product)

    result.sort(key=lambda tup: tup[1])
    # print len(result)
    n = len(result)

    filters = "?Ptype="+str(Ptype)+"&Pmin="+str(Pmin)+"&Pmax="+str(Pmax)
    context = {
        'result': reversed(result),
        'n': n,
        'input': str(srchFld),
        'Ptype':str(Ptype),
        'Prange':str(Prange),
        'Pmin':Pmin,
        'idC':str(getId(str(categorie))),
        'Pmax':Pmax,
        'filters':filters,
        'nC1': str(getCountFromList("Vetement et accessoires", tab)),
        'nC2': str(getCountFromList("Bijoux", tab)),
        'nC3': str(getCountFromList("Founiture creatives", tab)),
        'nC4': str(getCountFromList("Mariages", tab)),
        'nC5': str(getCountFromList("Maison", tab)),
        'nC6': str(getCountFromList("Enfant et bebe", tab)),
    }
    #print context['filters']
    #print "categorie id : " + context['idC']
    return render(request, 'search.html', context)


def discover(request,idC="0",idP="1"):
    #print "hello from discovermore!" + str(id)

    Ptype = request.GET.get('Ptype', 'all')
    #print Ptype

    Prange = request.GET.get('Prange', 'all')
    #print Prange

    Pmin = request.GET.get('Pmin',0)
    Pmax = request.GET.get('Pmax',10000)

    #print Pmin
    #print Pmax

    products = Product.objects.all().order_by("-created_at")
    if(not int(idC) == 0):
        products = products.filter(categorie=categoriesList[int(idC)-1])

    if(Ptype=="handMade"):
        #print "shuold filter elements wich are handMade"
        products = products.filter(Ptype=1)
    if(Ptype=="vintage"):
        products = products.filter(Ptype=2)

    if(Prange == "range1"):
        products = products.filter(price__gte=1)
        products = products.filter(price__lte=50)
    if(Prange == "range2"):
        products = products.filter(price__gte=50)
        products = products.filter(price__lte=1000)
    if(Prange == "range3"):
        products = products.filter(price__gte=1000)
        products = products.filter(price__lte=100000)

    products = products.filter(price__gte=Pmin)
    products = products.filter(price__lte=Pmax)

    pages = Paginator(products, 9)
    # print "number of pages : " + str((products.count()+8)/9)
    intList = list(range(1, ((products.count() + 8) / 9) + 1))
    verifiedId = idP
    values = []

    if (int(idP) > ((products.count() + 8) / 9) or int(idP) < 1):
        verifiedId = 1
    page = pages.page(verifiedId)

    for product in page:
            x = None
            imgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")
            if imgs:
                x = imgs[0]
            liked  = False
            smiled = False
            wished = False
            if(request.user in product.likes.all() ):
                liked = True
            if(request.user in product.smiles.all() ):
                smiled = True
            if(request.user in product.wishes.all() ):
                wished = True
            values.append((product, x,liked,smiled,wished,str(product.likes.count() + product.smiles.count() + product.wishes.count())))

    filters = "?Ptype="+str(Ptype)+"&Pmin="+str(Pmin)+"&Pmax="+str(Pmax)

    idList = []
    for i in intList:
        idList.append(str(i))

    context = {
        'nPages': pages.num_pages,
        'values': values,
        'pageId': verifiedId,
        'idC':str(idC),
        'page': page,
        'Pmin':str(Pmin),
        'Pmax':str(Pmax),
        'Ptype':str(Ptype),
        'Prange':str(Prange),
        'idList': idList,
        'filters':filters,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    # return render(request,'discover',context)
    return render(request, 'discover.html', context)

def product_details(request, id):
    product = Product.objects.get(id=id)
    form = addProductMainImageForm()
    editProductForm = ProductForm(instance=product)

    img = getMainImage(product)

    imgs = getSecImages(product)

    #print imgs

    context = {
        'form': form,
        'product': product,
        'img': img,
        'imgs':imgs,
        'editProductForm': editProductForm,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),

    }
    return render(request, 'product_details.html', context)


def store_details(request, id):
    store = Store.objects.get(id=id)
    form = StoreImageForm()
    context = {
        'store': store,
        'form': form,
        'nC1': getCount(categories[0]),
        'nC2': getCount(categories[1]),
        'nC3': getCount(categories[2]),
        'nC4': getCount(categories[3]),
        'nC5': getCount(categories[4]),
        'nC6': getCount(categories[5]),
    }
    return render(request, 'store_details.html', context)


def editProduct(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == get_object_or_404(Product, id=id).store.user.id):
        raise Http404

    if (request.method == 'POST'):

        form = ProductForm(request.POST or None)

        if form.is_valid():
            product = get_object_or_404(Product, id=id)
            product.name = form.cleaned_data['name']
            product.price = form.cleaned_data['price']
            product.categorie = form.cleaned_data['categorie']
            product.description = form.cleaned_data['description']
            product.quantity = form.cleaned_data['quantity']
            product.quantity = form.cleaned_data['quantity']
            product.Ptype = form.cleaned_data['Ptype']

            # print product.name
            # print str(product.id)
            product.save()
        return redirect('/shop/product_details/' + str(id))
    else:
        product = get_object_or_404(Product, id=id)
        form = ProductForm(instance=product)
        context = {
            'product': product,
            'form': form,
        }
        return render(request, 'editProduct.html', context)


def product_create(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == Store.objects.get(id=id).user.id):
        raise Http404
    else:
        if (request.method == 'POST'):
            form = ProductForm(request.POST or None, request.FILES or None)
            #print form.errors
            #print form
            if form.is_valid():
                instance = form.save(commit=False)
                store = Store.objects.get(id=id)
                # print instance
                instance.store = store
                instance.isActive = False
                instance.save()
            return redirect('/shop/details/' + id)
        else:
            store = Store.objects.get(id=id)
            form = ProductForm()
            context = {
                'form': form,
                'store': store,
            }
            # print store.name
            return render(request, 'product_form.html', context)

def store_create(request,comment):
    if not request.user.is_authenticated():
        raise Http404
    else:
        if (request.method == 'POST'):
            if(str(comment) == "ok"):
                form = StoreForm(request.POST or None, request.FILES or None)
                # print form.errors
                if form.is_valid():
                    instance = form.save(commit=False)
                    if (Store.objects.filter(name=instance.name).filter(user=request.user).exists()):
                        form = StoreForm()
                        context = {
                            'form': form,
                            'error_message': "Error !! you have already created a store with the same name",
                        }
                        return render(request, 'store_form.html', context)
                    else:
                        instance.user = request.user
                        instance.save()
                        return redirect('/shop/stores')
                else:
                    form = StoreForm()

                    context = {
                        'form': form,
                        'error_message': "Error !! form is not valid",
                    }
                    return render(request, 'store_form.html', context)
            elif(str(comment) == "addStatus"):
                form = TraderForm(request.POST or None)
                if form.is_valid:
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
                    return redirect('/shop/store_create/verifyFirst')
                else:
                    return redirect('/shop/stores/')
            else:
                raise Http404

        else:
            if not hasattr(request.user,'trader'):
                additional = "this is your first store !! please select your status"
                form = TraderForm()
                context = {
                    'form': form,
                    'additional':additional,
                }
                return render(request, 'store_form.html', context)
            else:
                form = StoreForm()
                context = {
                    'form': form,
                }
                return render(request, 'store_form.html', context)

def storesView(request):
    stores = Store.objects.all()[:18]
    values = []
    for store in stores:
        values.append((store, getStoreImage(store)))
    context = {
        'values': values,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    return render(request, 'stores.html', context)


def product(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def contact_create(request):
    if (request.method == 'POST'):
        form = ContactForm(request.POST or None)
        # print form.errors
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        else:
            print("Error !!")
        return redirect('/shop')
    else:
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, 'contact_create.html', context)


def addProduct(request, id):
    if (request.method == 'POST'):
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        imgUrl = request.POST['imgUrl']

        store = Store.objects.get(id=id)

        product = Product(name=name, price=price, storeName=store.name, description=description, imgUrl=imgUrl)
        product.save()

        return redirect('/shop/details/' + id)
    else:
        store = Store.objects.get(id=id)
        context = {
            'store': store,
        }
        print(store.name)
        return render(request, 'addProduct.html', context)


def details(request, id,idP="1"):
    # print str(id)

    Ptype = request.GET.get('Ptype', 'all')
    #print Ptype

    Prange = request.GET.get('Prange', 'all')
    #print Prange

    store = Store.objects.get(id=id)
    products = store.product_set.all().order_by("-created_at")

    Pmin = request.GET.get('Pmin',0)
    Pmax = request.GET.get('Pmax',10000)

    products = products.filter(price__gte=Pmin)
    products = products.filter(price__lte=Pmax)

    if(Ptype=="handMade"):
        products = products.filter(Ptype=1)
    if(Ptype=="vintage"):
        products = products.filter(Ptype=2)

    if(Prange == "range1"):
        products = products.filter(price__gte=1)
        products = products.filter(price__lte=50)
    if(Prange == "range2"):
        products = products.filter(price__gte=50)
        products = products.filter(price__lte=1000)
    if(Prange == "range3"):
        products = products.filter(price__gte=1000)
        products = products.filter(price__lte=100000)

    nP = products.count()
    form = StoreImageForm()
    imgs = StoreImage.objects.filter(store=store).order_by("-created_at")
    pages = Paginator(products, 9)
    vId = int(idP)
    if( ( vId > int((nP+8)/9) ) or (vId < 1) ):
        vId = 1
    page = pages.page(vId)
    values = []
    for product in page:
        x = getMainImage(product)
        #print x
        values.append((product, x))

    intList = list(range(1, ((products.count() + 8) / 9) + 1))
    idList = []
    for i in intList:
        idList.append(str(i))

    filters = "?Ptype="+str(Ptype)+"&Pmin="+str(Pmin)+"&Pmax="+str(Pmax)
    context = {
        'store': store,
        'values': values,
        'form': form,
        'page': page,
        'nP': nP,
        'Pmin':Pmin,
        'Pmax':Pmax,
        'idList': idList,
        'pageId': "1",
        'filters':filters,
        'Ptype':str(Ptype),
        'Prange':str(Prange),
        'idS': str(id),
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    if imgs:
        context['img'] = imgs[0]
        # print img.img

    #print str(id)
    return render(request, 'details.html', context)

def storesAlbum(request,id):
    if(request.method == 'POST'):
        form = albumImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.store = Store.objects.get(id=id)
            instance.save()
            return redirect('/shop/storesAlbum/' + str(id))
        else:
            #print "error !!"
            # print form.errors
            return redirect('/shop/storesAlbum/' + str(id))
        return redirect(request, '/shop/storesAlbum/' + str(id))
    else:
        form = albumImageForm()
        store = get_object_or_404(Store,id=id)
        imgs = albumImage.objects.filter(store=store)
        context = {
            'imgs':imgs,
            'form':form,
        }
        return render(request,'album.html',context)

def wishlist(request):
    profile = get_object_or_404(Profile,user=request.user)
    products = []
    for pr in profile.wishedProducts.all():
        products.append(pr)
    collections = []
    for cl in profile.wishedCollections.all():
        collections.append(cl)
    context = {
        'products':products,
        'collections':collections
    }
    return render(request,'wishlist.html',context)

def view(request, id,idP="1"):
    # print str(id)
    Ptype = request.GET.get('Ptype', 'all')
    #print Ptype

    Prange = request.GET.get('Prange', 'all')
    #print Prange

    store = Store.objects.get(id=id)

    # send message to store's owner
    if request.user != store.user:
        if(not (request.user in store.visitors.all())):
            print("visit ...")
            message = "This is an automatically generated message, welcome to my store ( " + str(store.name) + " ) , if you have any questions, please feel free :) "
            if store.user.profile.message != None:
                message = str(store.user.profile.message)
            msg = Message.send_message(store.user,request.user,message).save()
            store.visitors.add(request.user)


    products = store.product_set.all().order_by("-created_at")

    Pmin = request.GET.get('Pmin',0)
    Pmax = request.GET.get('Pmax',10000)

    products = products.filter(price__gte=Pmin)
    products = products.filter(price__lte=Pmax)

    if(Ptype=="handMade"):
        products = products.filter(Ptype=1)
    if(Ptype=="vintage"):
        products = products.filter(Ptype=2)

    nP = products.count()
    imgs = StoreImage.objects.filter(store=store).order_by("-created_at")
    pages = Paginator(products, 9)
    vId = int(idP)
    if( ( vId > int((nP+8)/9) ) or (vId < 1) ):
        vId = 1
    page = pages.page(vId)
    values = []
    for product in page:
        x = getMainImage(product)
        #print x
        values.append((product, x,product.likes.all(),product.smiles.all(),product.wishes.all(),product.likes.count()+product.smiles.count()+product.wishes.count()))

    intList = list(range(1, ((products.count() + 8) / 9) + 1))
    idList = []
    for i in intList:
        idList.append(str(i))

    filters = "?Ptype="+str(Ptype)+"&Pmin="+str(Pmin)+"&Pmax="+str(Pmax)
    context = {
        'flag':'yes',
        'store': store,
        'values': values,
        'page': page,
        'nP': nP,
        'Pmin':Pmin,
        'Pmax':Pmax,
        'idList': idList,
        'pageId': str(vId),
        'filters':filters,
        'Ptype':str(Ptype),
        'Prange':str(Prange),
        'idS': str(id),
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    if imgs:
        context['img'] = imgs[0]

    return render(request, 'discover.html', context)


def addStoreImage(request, id):
    form = StoreImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.store = Store.objects.get(id=id)
        instance.save()
        return redirect('/shop/stores')
    else:
        print("error !!")
        #print form.errors
        # print form.errors
        return redirect('/shop/stores')


def deleteStore(request, id):
    Store.objects.filter(id=id).delete()
    return redirect('/shop')


def deleteProduct(request, id):
    #print "delete : " + str(id)
    product = Product.objects.get(id=id)
    store = product.store
    Product.objects.filter(id=id).delete()
    return redirect('/shop/details/' + str(store.id))


def newStore(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        description = request.POST['description']
        imgUrl = request.POST['imgUrl']

        store = Store(name=name, description=description, img=imgUrl)
        store.save()

        return redirect('/shop')
    else:
        return render(request, 'newStore.html')
