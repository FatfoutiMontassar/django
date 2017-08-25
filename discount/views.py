from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse, Http404
from shop.models import Product , Store
from collection.models import Collection
from discount.models import Discount
from datetime import datetime


from .tasks import activate
from celery import Task
from datetime import datetime, timedelta
# Create your views here.

def discounts(request):
    discounts = Discount.objects.all()
    #print len(discounts)
    return render(request,'discount/discounts.html',{
        'discounts':discounts,
    })

def newDiscount(request):
    if not request.user.is_authenticated():
        raise Http404

    if(request.method == 'POST'):
        relatedProducts = request.POST.get('relatedProducts')
        relatedCollections = request.POST.get('relatedCollections')
        products = str(relatedProducts).split('&')
        collections = str(relatedCollections).split('&')
        percentage = request.POST.get('percentage')
        discountType = request.POST.get('Discount')
        offset = request.POST.get('timeOffset')
        offset = int(offset)
        discountType = str(discountType)

        if(discountType == "regular"):
            startDate = request.POST.get('startDate')
            startDate = str(startDate).split('-')
            #print startDate
            startDate_Y = startDate[0]
            startDate_M = startDate[1]
            startDate_D = startDate[2]

            endDate = request.POST.get('endDate')
            endDate = str(endDate).split('-')
            endDate_Y = endDate[0]
            endDate_M = endDate[1]
            endDate_D = endDate[2]

            st = datetime(int(startDate_Y), int(startDate_M), int(startDate_D),0,0)
            ed = datetime(int(endDate_Y), int(endDate_M), int(endDate_D),23,59)

            #print st , " -- " , ed
            for i in range(len(products)-1):
                pid = products[i]
                p = get_object_or_404(Product,id=pid)
                discount = Discount(user=request.user,product=p,start=st,end=ed,discount_type="P",length_type="R",percentage=percentage)
                discount.save()
                activate.apply_async([discount.id],eta=st)
                activate.apply_async([discount.id],eta=ed)

            for i in range(len(collections)-1):
                cid = collections[i]
                c = get_object_or_404(Collection,id=cid)
                discount = Discount(user=request.user,collection=c,start=st,end=ed,discount_type="C",length_type="R",percentage=percentage)
                discount.save()
                activate.apply_async([discount.id],eta=st)
                activate.apply_async([discount.id],eta=ed)

        else:
            Date = request.POST.get('Date')
            Date = str(Date).split('-')

            Date_Y = Date[0]
            Date_M = Date[1]
            Date_D = Date[2]

            startTime = request.POST.get('startTime')
            startTime = str(startTime).split(':')
            startTime_H = startTime[0]
            startTime_M = startTime[1]
            endTime = request.POST.get('endTime')
            endTime = str(endTime).split(':')
            endTime_H = endTime[0]
            endTime_M = endTime[1]

            st = datetime(int(Date_Y), int(Date_M), int(Date_D),int(startTime_H),int(startTime_M))
            ed = datetime(int(Date_Y), int(Date_M), int(Date_D),int(endTime_H),int(endTime_M))

            stg = datetime(int(Date_Y), int(Date_M), int(Date_D),int(startTime_H)+(offset/60),int(startTime_M))
            edg = datetime(int(Date_Y), int(Date_M), int(Date_D),int(endTime_H)+(offset/60),int(endTime_M))

            print(st , " -- " , ed)
            for i in range(len(products)-1):
                pid = products[i]
                p = get_object_or_404(Product,id=pid)
                discount = Discount(user=request.user,product=p,start=st,end=ed,discount_type="P",length_type="F",percentage=percentage)
                discount.save()
                activate.apply_async([discount.id],eta=stg)
                activate.apply_async([discount.id],eta=edg)

            for i in range(len(collections)-1):
                cid = collections[i]
                c = get_object_or_404(Collection,id=cid)
                discount = Discount(user=request.user,collection=c,start=st,end=ed,discount_type="C",length_type="F",percentage=percentage)
                discount.save()
                activate.apply_async([discount.id],eta=stg)
                activate.apply_async([discount.id],eta=edg)

        return redirect('/discounts/')
    else:
        pro = []
        for store in request.user.store_set.all():
            for pr in store.product_set.all():
                pro.append(pr)

        col = []
        for collection in request.user.collection_set.all():
            col.append(collection)

        return render(request,'discount/newDiscount.html',
                    {
                        'products':pro,
                        'collections':col,
                    })

def myDiscounts(request):
    if not request.user.is_authenticated():
        raise Http404

    discounts = Discount.objects.all().filter(user=request.user)
    return render(request,'discount/myDiscounts.html',
    {
        'discounts':discounts,
    })
