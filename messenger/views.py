import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render ,  get_object_or_404
from .decorators import ajax_required
from .models import Message
from shop.models import ProductMainImage
from .forms import AttachImageForm
from shop.models import Product
from shop import views

def getMainImage(product):
    imgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")
    img = None
    if imgs:
        img = imgs[0]
    return img

def inbox(request):
    if not request.user.is_authenticated():
        return redirect('/shop/')
    conversations = Message.get_conversations(user=request.user)
    active_conversation = None
    messages = None
    products = []
    if conversations:
        conversation = conversations[0]
        active_conversation = conversation['user'].username
        user = conversation['user']

        for store in user.store_set.all():
            #print store.name
            for product in store.product_set.all():
                products.append((product,getMainImage(product)))


        messages = Message.objects.filter(user=request.user,
                                          conversation=conversation['user'])
        messages.update(is_read=True)
        for conversation in conversations:
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0

    for store in request.user.store_set.all():
        #print store.name
        for product in store.product_set.all():
            products.append((product,getMainImage(product)))
    #print "messages data type : "  + str(type(messages))
    newestMessages = []
    for i in range(0,min(10,len(messages))):
        newestMessages.append(messages[len(messages)-min(10,len(messages))+i])

    context = {
        'products':products,
        'numberOfMessages':min(10,len(messages)),
        'messages': newestMessages,
        'conversations': conversations,
        'active': active_conversation
    }
    return render(request, 'messenger/inbox.html',context)


@login_required
def messages(request, username):
    if not request.user.is_authenticated():
        return redirect('/shop/')
    conversations = Message.get_conversations(user=request.user)
    active_conversation = username
    messages = Message.objects.filter(user=request.user,
                                      conversation__username=username)
    messages.update(is_read=True)
    for conversation in conversations:
        if conversation['user'].username == username:
            conversation['unread'] = 0

    products = []
    ouser = get_object_or_404(User,username=username)
    print("other user's username :: " + str(ouser.username)+ "  " + str(hasattr(request.user , 'trader')) + "  " + str(hasattr(ouser,'trader')) )
    if (hasattr(request.user , 'trader') and not hasattr(ouser,'trader')) or (not hasattr(request.user , 'trader') and hasattr(ouser,'trader') ):
            print("ok!!!")
    else:
        print("not ok at all :p")

    print("other user ...")
    for store in ouser.store_set.all():
        #print store.name
        for product in store.product_set.all():
            products.append((product,getMainImage(product)))

    print("connected user ...")
    for store in request.user.store_set.all():
        #print store.name
        for product in store.product_set.all():
            products.append((product,getMainImage(product)))

    newestMessages = []
    for i in range(0,min(10,len(messages))):
        newestMessages.append(messages[len(messages)-min(10,len(messages))+i])

    return render(request, 'messenger/inbox.html', {
        'products':products,
        'numberOfMessages':min(10,len(messages)),
        'messages': newestMessages,
        'conversations': conversations,
        'active': active_conversation
        })


@login_required
def new(request):
    if not request.user.is_authenticated():
        return redirect('/shop/')
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        #productId = request.POST.get('productId')
        #print str(productId)
        product = None
        #product = get_object_or_404(Product, id=productId)
        #print product.name
        try:
            to_user = User.objects.get(username=to_user_username)
            #print("new message has secceffuly found the user..")
        except Exception:
            try:
                to_user_username = to_user_username[
                    to_user_username.rfind('(')+1:len(to_user_username)-1]
                to_user = User.objects.get(username=to_user_username)

            except Exception:
                return redirect('/messages/new/')

        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return redirect('/messages/new/')

        Message.send_message(from_user, to_user, message)

        return redirect('/messenger/new/')
        #return redirect('/messages/{0}/'.format(to_user_username))

    else:
        to = request.GET.get('to', 'empty')
        productId = request.GET.get('productId','notSet')
        conversations = Message.get_conversations(user=request.user)
        context = {
            'conversations': conversations,
        }
        if(to != "empty"):
            context["to"] = to
            context["productId"] = productId

        return render(request, 'messenger/new.html',context)


@login_required
@ajax_required
def delete(request):
    return HttpResponse()


@login_required
@ajax_required
def send(request):
    if request.method == 'POST':
        relatedProducts =  str(request.POST.get('relatedProducts'))
        relatedProducts = relatedProducts.split('&')
        #print relatedProducts

        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return HttpResponse()
        #this line has been modified , it used to test (from_user != to_user)
        if True:
            msg = Message.send_message(from_user, to_user, message)
            omsg = get_object_or_404(Message,id=str(int(msg.id)+1))
            for p in relatedProducts:
                if(len(p) > 0 ):
                    pr = get_object_or_404(Product,id=str(p))
                    msg.relatedProducts.add(pr)
                    omsg.relatedProducts.add(pr)
                    #print pr.name
            msg.save()
            omsg.save()
            #print str(msg.id) + " -- " + str(omsg.id)
            return render(request, 'messenger/includes/partial_message.html',
                          {'message': msg})

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def load_more(request):
    #print("load_more function call ... " + str(request.POST.get('numberOfMessages')))
    nom = request.POST.get('numberOfMessages')
    to = request.POST.get('to')
    required = request.POST.get('required')
    req = int(required)
    #print "to : " + str(to)
    messages = Message.objects.filter(user=request.user,
                            conversation__username=to)
    ret = []
    #print nom + " -- " + to + " -- " + required + " -- " + str(len(messages))
    for i in range(0,req):
        if(len(messages)-(int(nom)+i+1) >= 0):
            #print str(i) + " -- " + str(len(messages))
            ret.append(messages[len(messages)-(int(nom)+i+1)])
        else:
            #print str(i) + " -- " + str(len(messages))
            break
    return render(request, 'messenger/includes/partial_message_list.html',
                  {'messages': reversed(ret) })

def get_products(request):
    to = request.POST.get('to')
    ouser = User.objects.get(username=to)
    ret = []

    for store in ouser.store_set.all():
        for product in store.product_set.all():
            ret.append((product,getMainImage(product)))

    for store in request.user.store_set.all():
        for product in store.product_set.all():
            ret.append((product,getMainImage(product)))

    return render(request,'messenger/includes/products_list.html',
                {'values':reversed(ret) } )

def add_new_messages(request):
    print("add_new_messages function called ...")
    username = request.POST.get('username')
    print(str(username))
    active_conversation = username
    messages = Message.objects.filter(user=request.user,
                                      conversation__username=username,is_read=False)

    if len(messages) > 0 :
        message = messages[0]
        #print message
        messages.update(is_read=True)
        return render(request, 'messenger/includes/partial_message.html',
                  {'message': message})
    else:
        return HttpResponse()

def send_image(request):
    #print "hello from send image !!"
    to = request.POST.get('to')
    val = request.POST.get('test')
    to_user = get_object_or_404(User,username=to)
    image = request.FILES.get('picture')
    #print type(image)
    message = "image.."
    msg  = Message.send_message_with_image(request.user ,to_user,message,image)

    return render(request, 'messenger/includes/partial_message.html',
                  {'message': msg})

@login_required
@ajax_required
def users(request):
    users = User.objects.filter(is_active=True)
    #print "I have been called :p"
    dump = []
    template = '{0} ({1})'
    for user in users:
        #this condition used to be (user.profile.get_screen_name() != user.username)
        if False:
            dump.append(template.format(user.username,
                                        user.username))
        else:
            dump.append(user.username)
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


@login_required
@ajax_required
def check(request):
    count = Message.objects.filter(user=request.user, is_read=False).count()
    return HttpResponse(count)
