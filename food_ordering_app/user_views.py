from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse 
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from food_ordering_app.models import Vendor, Product,Customer, Category, OrderDetails, ShippingAdress, CustomUser, OrderItem, Offer
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import razorpay
from . import Checksum  
from django.conf import settings
from django.views.generic import View
import datetime
from datetime import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control



def demo_template(request):
    return render(request, "user_template/demo.html")



def mobile_verification(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        print(mobile)
        responce = redirect('otp_verification')
        responce.set_cookie('mobile', mobile)
        return responce

    return render(request, 'user_template/mobile_verification_template.html')



def otp_verification(request):
    if request.method == 'GET':
        phone = request.COOKIES['mobile']
        print(phone)
        user = CustomUser.objects.filter(last_name = phone).exists()
        print(user)
        if not user:
            messages.info(request,'The mobile number is not registered')
            return redirect('mobile_verification')
        

        url = "https://d7networks.com/api/verifier/send"

        mob = str(91)+ phone

        payload = {
            'mobile': mob,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900'}
        files = [

        ]
        headers = {
        'Authorization': 'Token 1b12e42f2d97a7e160e11a4a41eed212bc5442dd'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))
        
        otp_id = response.text[11:47] 
        print(otp_id)                                                          
        responce  = render(request, 'user_template/otp_verification_template.html')
        responce.set_cookie('otp_id', otp_id)
        return responce

    else:

        otp_num = request.POST.get('otp')
        print(otp_num)

        otp_id = request.COOKIES['otp_id']

        url = "https://d7networks.com/api/verifier/verify"

        payload = {
            'otp_id': otp_id,
            'otp_code': otp_num }
        files = [

        ]
        headers = {
            'Authorization': 'Token 1b12e42f2d97a7e160e11a4a41eed212bc5442dd'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))

        b = json.loads(response.text)
        try:
            print(b["status"])
        except:
            b["status"] = 'failed'
            print(b["status"])
        if (b["status"] == "success"):
            phone = request.COOKIES['mobile']
            user = CustomUser.objects.get(last_name = phone )
            print(user)
            username = user.username
            password = user.first_name
            print(password)
            print(username)
            user = auth.authenticate(request, username = username, password = password)
            print(user)
            if user is not None:
                login(request,user)
                print('login request')
                return redirect('select_baker')
            else:
                messages.info(request, 'OTP did not match')
                return redirect('mobile_verification')
        print(response.text.encode('utf8'))
        messages.info(request, 'OTP did not match')
        return redirect('mobile_verification')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect("select_baker")
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        print(username)
        print('user login')
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            print('login request')
            if user.is_staff == 0:
                login(request,user)
            else:
                messages.error(request,'Your account is blocked')
                return HttpResponseRedirect("/")
            if user.user_type == "3":
                return redirect('select_baker')
            else:
                messages.info(request, 'Invalid credentials')
                return HttpResponseRedirect("/")
        else:
            messages.info(request, 'Invalid credentials')
            return HttpResponseRedirect("/")

    else:
        return render(request,'user_template/user_login.html')

# @login_required(login_url="/select_baker")
def user_logout(request):
    logout(request)
    return redirect("select_baker")



def show_referal_id(request):
    if request.user.is_authenticated:
        admin1 = request.user.customer
        order, created = OrderDetails.objects.get_or_create(customer = admin1, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        order_count = OrderDetails.objects.filter(customer=admin1,complete=True)
        oc = order_count.count()
        item_count = items.count()
        cust = Customer.objects.filter(refered_person = request.user.id).count()
        reward = 0
        reward = cust * 10
    else:
        reward = 0
        customer = 0
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
    context = {'customer':admin1,'reward':reward,'items':items,'order':order,'item_count':item_count,'oc':oc,"cartItems":cartItems}
    return render(request, "user_template/offer_id_template.html",context)



def signup(request):
    if request.method == 'POST':  

        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST['mobile']
        password1 = request.POST.get('password')
        password2 = request.POST.get('password0')
        # referal = request.POST.get('referal_code')
        offer_id = Checksum.__id_generator__()
        

        if password1==password2 :
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return render(request, 'user_template/signup.html')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return render(request, 'user_template/signup.html')
            elif CustomUser.objects.filter(last_name=mobile).exists():
                messages.info(request, 'mobile number taken')
                return render(request, 'user_template/signup.html')
            else:    
              

                user = CustomUser.objects.create_user(username = username, password = password1, email = email,first_name = password2,last_name = mobile,user_type=3)
                user.customer.status=offer_id
                user.customer.name = username
                user.customer.email = email
                user.customer.save()
                responce = redirect('otp_verification')
                responce.set_cookie('mobile', mobile)
                return responce
            
              

                
        else:
            messages.info(request, 'password not matching')       
            return render(request, 'user_template/signup.html')
       

    else:
        return render(request, 'user_template/signup.html')





def register(request,vendor_id,referal):
    if request.method == 'POST':  

        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST['mobile']
        password1 = request.POST.get('password')
        password2 = request.POST.get('password0')
        # referal = request.POST.get('referal_code')
        offer_id = Checksum.__id_generator__()
        

        if password1==password2 :
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return render(request, 'user_template/register.html')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return render(request, 'user_template/register.html')
            elif CustomUser.objects.filter(last_name=mobile).exists():
                messages.info(request, 'mobile number taken')
                return render(request, 'user_template/register.html')
            else:    
                if referal == "":

                    user = CustomUser.objects.create_user(username = username, password = password1, email = email,first_name = password2,last_name = mobile,user_type=3)
                    user.customer.status=offer_id
                    user.customer.name = username
                    user.customer.email = email
                    print('tt',offer_id)
                    user.save()
                    print('User created')
                    responce = redirect('otp_verification')
                    responce.set_cookie('mobile', mobile)
                    return responce
                else:
                    if Customer.objects.filter(status = referal).exists():
                        user = CustomUser.objects.create_user(username = username, password = password1, email = email,first_name = password2,last_name = mobile,user_type=3)
                        user.customer.status=offer_id
                        user.customer.name = username
                        user.customer.email = email
                        print('pp',offer_id)
                        cust = Customer.objects.get(status=referal)
                        user.customer.refered_person=vendor_id
                        user.save()
                        responce = redirect('otp_verification')
                        responce.set_cookie('mobile', mobile)
                        return responce

                # return redirect('user_login')
            # return render(request, 'user_template/register.html')

                
        else:
            messages.info(request, 'password not matching')       
            return render(request, 'user_template/register.html')
       

    else:
        return render(request, 'user_template/register.html')



def user_home(request):
    return render(request, "user_template/home_content.html")

def select_baker(request):
    vendor=Vendor.objects.all()

    if request.user.is_superuser:
        admin=request.user
        return redirect('admin_home')
    elif request.user.is_staff == 1:
        return redirect('vendor_home')
    elif request.user.is_authenticated:
        admin1 = request.user.customer
        order, created = OrderDetails.objects.get_or_create(customer = admin1, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        today = date.today()
        DAY = today.day
        print('dadada',DAY)
        offer = Offer.objects.all()
        print('blablabla',offer)
        print(today)
        for offers in offer:
            if offers.expiry_date == today:
                print('lala',offers)
                print('HAI')
                product_id = offers.product.id
                product = Product.objects.get(id=product_id)
                normal_price = product.price1
                product.price = normal_price
                product.price1 = 0
                offers.offer = 0
                product.save()
                offers.delete()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
    context = {"vendors":vendor,"order":order,"cartItems":cartItems,"items":items}
    return render(request, "user_template/select_baker_template.html", context)
    


# def selected_baker_product(request):
#     if request.user.is_authenticated:
#         admin = request.user.customer
#     # vendor = Vendor.objects.get(admin=vendor_id)
#         category = Category.objects.all()
#         product = Product.objects.all()
#         order, created = OrderDetails.objects.get_or_create(customer = admin, complete = False)
#         items = order.orderitem_set.all()
#         order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
#         cartItems = order['get_cart_items']
#     # cartItems = order.get_cart_items
#     return render(request,"user_template/view_products_template.html",{"products":product,"categories":category,"cartItems":cartItems})



def store(request,vendor_id):

    # if request.user.is_superuser:
    #     admin = request.user.id
    #     order, created = Order.objects.get_or_create(admin = admin, complete = False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items

    if request.user.is_authenticated:

        login_user = request.user
        login_name = request.user.username
        login_email = request.user.email
        user  = Customer.objects.filter( admin = login_user, name = login_name, email = login_email)
        print(login_user)
        print(login_name)
        print(login_email)
        admin1 = request.user.customer
        # category = Category.objects.all()
        # products = Product.objects.all()
        # customer, created = Customer.objects.get_or_create(user = login_user, name = login_name, email = login_email)
        order, created = OrderDetails.objects.get_or_create(customer = admin1, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        vendor = Vendor.objects.get(id=vendor_id)
        

        
    else:
        # category = Category.objects.all()
        # products = Product.objects.all()
        return redirect("select_baker")
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
        # cookieData = cookieCart(request)
        # cartItems = cookieData['cartItems']
    # vendor = Vendor.objects.get(admin = request.user.id)
    products = Product.objects.filter(vendor_id=vendor_id)
    category = Category.objects.all()
    context = {'products':products, 'cartItems':cartItems,"items":items,"categories":category,'vendor':vendor}
    return render(request, 'user_template/view_products_template.html', context)


def category(request,vendor_id,cat_id):
    if request.user.is_authenticated:
        category = Category.objects.all()
        cat = Category.objects.get(id=cat_id)
        cat_name = cat.category_name
        print(cat_name,"haloe")
        product1 = Product.objects.filter(vendor_id=vendor_id,category=cat)
        print("ff",product1)
        admin1 = request.user.customer
        order, created = OrderDetails.objects.get_or_create(customer = admin1, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        vendor = Vendor.objects.get(id=vendor_id)
        
    context={"product1":product1,"cat_name":cat_name, 'cartItems':cartItems,"items":items}
    return render(request, 'user_template/category_template.html',context)



def cart(request):
    if request.user.is_authenticated:
        admin = request.user.customer
        order , created =OrderDetails.objects.get_or_create( customer = admin, complete  = False)
        items = order.orderitem_set.all()
        
        cartItems = order.get_cart_items
        
        


    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']


    return render(request, 'user_template/cart_template.html',{"items":items,"order":order,"cartItems":cartItems})

  # Data = cartData(request)
    # cartItems = Data['cartItems']
    # order = Data['order']
    # items = Data['items']

    # context = {'items': items, 'order':order, 'cartItems':cartItems}


def checkout(request):
    if request.user.is_authenticated:
        admin = request.user.customer
        order , created =OrderDetails.objects.get_or_create( customer = admin, complete  = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        item_count = items.count()
        if admin.refered_person and OrderDetails.objects.filter(customer=admin, complete=True).count() < 1 :
 
            ch = order.get_cart_total
            print('ch',ch)
            changes = (order.get_cart_total)*(90/100)
            print("ff",changes)
            change = round(changes)
            print("change",change)
           
        else:
            change = 0 
        # offer_id = request.POST.get('offer_id')
        # print(offer_id,'hai')
    


        #razor pay
        client = razorpay.Client(auth=('rzp_test_pMt7Hdv04s334f', 'ptMwn6Dlg3ekQKMz40HYkAfK'))
        if request.user.is_authenticated:
            if admin.refered_person and OrderDetails.objects.filter(customer=admin, complete=True).count() < 1 :
                ch = order.get_cart_total
                changes = (order.get_cart_total)*(90/100)
                print("ff",changes)
                totals = round(changes)
                total = int((totals*100))
            else:    
                total = int((order.get_cart_total*100))
        else:
            total = int(order['get_cart_total']*100)
        order_amount =total
        order_currency = 'USD'
        admin = request.user.customer
        ship = ShippingAdress.objects.filter(customer=admin).distinct()
        if order_amount == 0:
            return redirect('cart')
        else:
            response = client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture=0))
            print(response)
            order_id = response['id']
       

    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']


    return render(request, 'user_template/checkout_template.html',{'change':change,'shipping':ship,"items":items,"order":order,"cartItems":cartItems,"order_id":order_id,"id":id})


class Getshipping(View):
    def get(self, request):
        text = request.GET.get('ship_id')
        print(text)

        shipi = ShippingAdress.objects.get(id=text)

        a = shipi.address
        b = shipi.city
        vb = {
            'address': shipi.address,
            'city': shipi.city,
            'state': shipi.state,
            'zipcode': shipi.zipcode,

        }
        return JsonResponse({'count2': vb}, status=200)
        return redirect('/')


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId'] 
    action = data['action'] 

    print('Action :',action)
    print('productId :',productId)

    admin = request.user.customer
    product = Product.objects.get(id=productId)
    vendor = product.vendor_id
    print("hi",vendor)
    order , created =OrderDetails.objects.get_or_create( customer = admin,  complete  = False)

    if order.vendor_id == vendor:
        orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

        if action =='add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action =='remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
             orderItem.delete()

    elif order.vendor_id != vendor:
        del_item =  order.orderitem_set.all()
        del_item.delete()
        order.vendor_id = vendor

        orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
        order.save()
        if action =='add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action =='remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()
        
    else:
        order.vendor_id = vendor

        orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
        order.save()

        if action =='add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action =='remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()
        
    return JsonResponse('Item was Added', safe=False)


@csrf_exempt
def process_order(request):
    transaction_id=datetime.now().timestamp()
    data = json.loads(request.body) 

    if request.user.is_authenticated:
        admin = request.user.customer
        order , created =OrderDetails.objects.get_or_create( customer = admin, complete  = False)
        if admin.refered_person and OrderDetails.objects.filter(customer=admin, complete=True).count() < 1 :
            ch = order.get_cart_total
            changes = (order.get_cart_total)*(90/100)
            total = round(changes)
        else:
            total = str(data['form']['total'])
        order.transaction_id = transaction_id

        if admin.refered_person and OrderDetails.objects.filter(customer=admin, complete=True).count() < 1 :
            order.complete = True
            order.product_total = total
        else:
            if str(total) == str(order.get_cart_total):
                order.complete = True
                order.product_total = total

        order.save()

        if order.shipping == True:
            ShippingAdress.objects.create(
                customer = admin,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )


    else:

        print('User is not logged in ')
    return JsonResponse('Payment Complete', safe=False)



def product(request, product_id):

    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        admin = request.user.customer
        order, created = OrderDetails.objects.get_or_create(customer = admin, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        context = {'product': product, 'cartItems':cartItems}
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            print('cart:', cart)  
            items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        for i in cart:
            cartItems += cart[i]['quantity']   
        product = Product.objects.get( id = product_id)
        context = {'product': product, 'cartItems':cartItems}
    


    return render(request, 'user_template/product_view_template.html', context)



def user_view_orders(request):
    # try:
    customer=request.user.customer
    print(customer)
    order=OrderDetails.objects.filter(customer=customer,complete=True)
    items =[]
    for i in order:
        details=OrderItem.objects.filter(order=i,product__isnull=False)
        for j in details:
            items.append(j)

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = OrderDetails.objects.get_or_create(customer=customer,complete=False)
        # items=order.orderitem_set.all()
        cartItems=order.get_cart_items

    else:
        # items=[]
        order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    # except:
    #     return redirect("/")
    context ={
        "items":items,
        "order":order,
        "cartItems":cartItems,

    }
    return render(request,"user_template/user_order_status.html",context)


def payment(request):
    admin = request.user.customer
    order, created = OrderDetails.objects.get_or_create(customer = admin, complete = False)
    print(order)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    order_id = Checksum.__id_generator__()
    print(Checksum.__id_generator__(),'hai')
    
    bill_amount = str(order.get_cart_total)
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': '7405505665',
        'EMAIL': 'dhaval.savalia6@gmail.com',
        'CUST_ID': '123123',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': bill_amount,
    } # This data should ideally come from database
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'user_template/payment.html', context)


@csrf_exempt
def response(request):
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        # save success details to db; details in resp['paytm']
        return redirect("user_view_orders")
    else:
        # check what happened; details in resp['paytm']
        return render(request, 'user_template/paytm_response_template.html')



def VerifyPaytmResponse(response):
    response_dict = {}
    if response.method == "POST":
        data_dict = {}
        for key in response.POST:
            data_dict[key] = response.POST[key]
        MID = data_dict['MID']
        ORDERID = data_dict['ORDERID']
        verify = Checksum.verify_checksum(data_dict, settings.PAYTM_MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            STATUS_URL = settings.PAYTM_TRANSACTION_STATUS_URL
            headers = {
                'Content-Type': 'application/json',
            }
            data = '{"MID":"%s","ORDERID":"%s"}'%(MID, ORDERID)
            check_resp = requests.post(STATUS_URL, data=data, headers=headers).json()
            if check_resp['STATUS']=='TXN_SUCCESS':
                response_dict['verified'] = True
                response_dict['paytm'] = check_resp
                return (response_dict)
            else:
                response_dict['verified'] = False
                response_dict['paytm'] = check_resp
                return (response_dict)
        else:
            response_dict['verified'] = False
            return (response_dict)
    response_dict['verified'] = False
    return response_dict