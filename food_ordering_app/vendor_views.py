from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from food_ordering_app.models import Vendor, Category, Product, Offer, CustomUser, OrderDetails, Customer
from django.urls import reverse 
import base64
from PIL import Image
from base64 import decodestring
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile
import datetime
from datetime import *


def show_vendor_login_page(request):
    return render(request, "vendor_template/login_page.html")

def do_vendor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #try:
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            if user.user_type == "2":
                return redirect("vendor_home")
        else:
            messages.error(request,"Inavalid login details")
            return HttpResponseRedirect("show_vendor_login_page")
                # return redirect("show_vendor_login_page")
        # except:
        #     messages.error(request,"Inavalid login details")
        #     return HttpResponseRedirect("show_vendor_login_page")
        #     # return redirect("show_vendor_login_page")
        #     print(" not  h login")

    else:
        return render(request,"vendor_template/login_page.html")

def vendor_home(request):
    vendor_obj=Vendor.objects.get(admin=request.user.id)
    total_products=Product.objects.filter(vendor_id = vendor_obj).count()
    total_offers=Offer.objects.filter(vendor_id = vendor_obj).count()
    total_oders=OrderDetails.objects.filter(vendor_id = vendor_obj).count()

    orders=OrderDetails.objects.filter(vendor_id = vendor_obj)
    total = 0
    for order in orders:
        try:
            order_total=order.get_cart_total
        except:
            order_total=0
        total=total+order_total

    # total count of customers
    # customer_count=Customer.objects.all().count()
    customer_count=Customer.objects.all().count()
    

    # chart
    year = datetime.now().year
    month = datetime.now().month
    chart_order = OrderDetails.objects.filter(date_ordered__year = year,date_ordered__month = month,vendor_id = vendor_obj)
    

    chart_values = []
    
    for i in range(0,6):
        chart_order = OrderDetails.objects.filter(date_ordered__year = year,date_ordered__month = month-5+i)
        order_total = 0
        for items in chart_order:
            try:
                order_total += round(items.get_cart_total,2)
            except:
                order_total += 0
        chart_values.append(round(order_total,2)) 

    # context = {
    #     "products":products,
    #     "order_count":order_count,
    #     "total":total,
    #     "customer_count":customer_count,
    #     "chart_values":chart_values,
    # }

    return render(request, "vendor_template/home_content.html",{"total_products":total_products,"total_offers":total_offers,"total_oders":total_oders,"total":total,"chart_values":chart_values,"customer_count":customer_count})


def logout_vendor(request):
    logout(request)
    return redirect( "show_vendor_login_page")





def manage_product(request):

    vendor = Vendor.objects.get(admin = request.user.id)
    product = Product.objects.filter(vendor_id = vendor)
    return render(request, "vendor_template/manage_product_template.html",{"products":product})


def add_product(request):
    category = Category.objects.all()
    return render(request, "vendor_template/add_product_template.html",{"categories":category})


def add_product_save(request):
    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        product_name=request.POST.get("product_name")
        category_id=request.POST.get("category_name")
        category_name=Category.objects.get(id=category_id)
        price=request.POST.get("price")
        # price1=request.POST.get("offer1")
        # offer_price=request.POST.get("offer")
        quantity=request.POST.get("quantity")
        vendor_id=Vendor.objects.get(admin=request.user.id)
        image_file =request.POST.get('image64data')
        value = image_file.strip('data:image/png;base64,')

        format, imgstr = image_file.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
        # ab = 100
        # pr = price
        # price = int(price)
        # offer_price = int(offer_price)
        # print(price1,'hai')
        # if offer_price == 1 :
        #     new_amount = price
        # else:
        #     amount = int(price * offer_price)/100
        #     new_amount = price - amount



        # try:
        product=Product(product_name=product_name,category=category_name,price=price,quantity=quantity,vendor_id=vendor_id,product_image = data)
        product.save()
        messages.success(request,"Successfully Added Product")
        return HttpResponseRedirect(reverse("add_product"))
        # except:
        #     messages.error(request,"Failed to Add Product")
        #     return HttpResponseRedirect(reverse("add_product"))


def edit_product(request,product_id):
    product=Product.objects.get(id=product_id)
    category = Category.objects.all()
    return render(request,"vendor_template/edit_product_template.html",{"product" : product,"id": product_id,"categories":category})


def edit_product_save(request):

    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        product_id = request.POST.get("product_id")
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category_name')
        image_file = request.POST.get('image64data')
        vendor_id = Vendor.objects.get(admin=request.user.id)
        value = image_file.strip('data:image/png;base64,')

        format, imgstr = image_file.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)

        value = Product.objects.get(id=product_id)  

        value.product_name = product_name
        value.vendor_id = vendor_id
        value.price = price
        value.quantity = quantity
        category1 = Category.objects.get(id = category)
        value.category = category1
        value.product_image = data
        value.save()
        messages.success(request,"Successfully Added Product")
        return HttpResponseRedirect(reverse("edit_product",kwargs={"product_id":product_id}))
    # else:
    #     messages.error(request,"Successfully Added Product")
    #     return HttpResponseRedirect(reverse("edit_product",kwargs={"product_id":product_id}))


def delete_product(request,product_id):

    product = Product.objects.get(id = product_id)
    product.delete()
    return redirect("manage_product")


def manage_offer(request):

    vendor = Vendor.objects.get(admin=request.user.id)
    offer = Offer.objects.filter(vendor_id=vendor)
    return render(request, "vendor_template/manage_offer_template.html",{"offers":offer})

def add_offer(request):
    vendor = Vendor.objects.get(admin=request.user.id)
    product = Product.objects.filter(vendor_id=vendor)
    return render(request, "vendor_template/add_offer_template.html",{"products":product})


def add_offer_save(request):

    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        offer_name=request.POST.get("offer_name")
        product_id=request.POST.get("product_name")
        offer_type = request.POST.get("offer_type")
        product_name=Product.objects.get(id=product_id)
        vendor = Vendor.objects.get(admin=request.user.id)
        price2=product_name.price
        print(price2)
        ab = 100
        # pr = price
        price2 = int(price2)
        offer_name = int(offer_name)
        if offer_type == 'Price Offer':
            new_amount = price2 - offer_name
        else:    
            if offer_name == 1 :
                new_amount = price2
            else:
                amount = int(price2 * offer_name)/100
                new_amount = price2 - amount
                print(new_amount)

        check_exist = Offer.objects.filter(product=product_name, vendor_id=vendor).exists()
        if check_exist:
            offer = Offer.objects.get(product=product_name,vendor_id=vendor)
            offer.offer = offer_name
            offer.save()
            product_name.price1=price2
            product_name.price=new_amount
            product_name.save()
            messages.success(request,"Successfully Added Offer")
            return HttpResponseRedirect(reverse("add_offer"))

        else:

            offer = Offer(offer=offer_name,product=product_name,vendor_id=vendor)
            offer.save()
            product_name.price1=price2
            product_name.price=new_amount
            product_name.save()
            messages.success(request,"Successfully Added Offer")
            return HttpResponseRedirect(reverse("add_offer"))


def edit_offer(request,offer_id):

    offer = Offer.objects.get(id = offer_id)
    product = Product.objects.all()
    return render(request,"vendor_template/edit_offer_template.html",{"offer" : offer ,"id": offer_id,"products" : product})

def edit_offer_save(request):

    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        offer_id = request.POST.get("offer_id")
        offer_name = request.POST.get('offer_name')
        product = request.POST.get('product_name')
        offer_type = request.POST.get('offer_type')
        product_name1=Product.objects.get(id=product)
        vendor_id = Vendor.objects.get(admin=request.user.id)

        price2=product_name1.price1
        print(price2)
        # ab = 100
        # pr = price
        price2 = int(price2)
        offer_name = int(offer_name)
        if offer_type == 'Price Offer':
            new_amount = price2 - offer_name
        else:
            if offer_name == 1 :
                new_amount = price2
            else:
                amount = int(price2 * offer_name)/100
                new_amount = price2 - amount
                print(new_amount)

        value = Offer.objects.get(id = offer_id)  

        value.offer = offer_name
        value.vendor_id = vendor_id
        product1 = Product.objects.get(id = product)
        value.product = product1
        value.save()
        product_name1.price1=price2
        product_name1.price=new_amount
        product_name1.save()
        messages.success(request,"Successfully Updated Offer")
        return HttpResponseRedirect(reverse("edit_offer",kwargs={"offer_id":offer_id}))


def delete_offer(request,offer_id):

    offer = Offer.objects.get(id = offer_id)
    product1 = offer.product.id
    product_obj = Product.objects.get(id=product1)
    product_obj.price = product_obj.price1
    product_obj.price1 = 0
    product_obj.save()
    print(product1)
    offer.delete()
    return redirect("manage_offer")

def manage_category_offer(request):

    vendor = Vendor.objects.get(admin=request.user.id)
    # product = Product.objects.get(id = )
    # category = Category.objects.get(category_name = )
    offer = Offer.objects.filter(vendor_id=vendor)
    return render(request, "vendor_template/manage_category_offer_template.html",{"offers":offer})



def add_category_offer(request):

    vendor = Vendor.objects.get(admin=request.user.id)
    category_obj = Category.objects.all()
    return render(request, "vendor_template/add_category_offer_template.html",{"categories":category_obj})


def add_category_offer_save(request):

    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        offer_name=request.POST.get("offer_name")
        category_id=request.POST.get("category_name")
        offer_type = request.POST.get("offer_type")
        vendor = Vendor.objects.get(admin=request.user.id)
        category_name=Category.objects.get(id=category_id)
        product = Product.objects.filter(vendor_id=vendor,category=category_name)
        for products in product:
            price2 = products.price
            if offer_type == 'Price Offer':
                price2 = int(price2)
                offer_name = int(offer_name)
                new_amount = price2 - offer_name
            else: 
                if products.price1 == 0:
                    print(products)
                    price2 = products.price
                    price2 = int(price2)
                    offer_name = int(offer_name)
                    amount = int(price2 * offer_name)/100
                    new_amount = price2 - amount
                    print(new_amount)
                else:
                    price2 = products.price1
                    print(products)
                    price2 = int(price2)
                    offer_name = int(offer_name)
                    amount = int(price2 * offer_name)/100
                    new_amount = price2 - amount
                    print(new_amount)

            check_exist = Offer.objects.filter(product=products, vendor_id=vendor).exists()
            if check_exist:
                offer = Offer.objects.get(product=products,vendor_id=vendor)
                offer.offer = offer_name
                offer.save()
                products.price1 = price2
                products.price=new_amount
                products.save()
            else:

                offer = Offer(offer=offer_name,product=products,vendor_id=vendor)
                offer.save()
                products.price1=price2
                products.price=new_amount
                products.save()
        messages.success(request,"Successfully Added Offer")
        return HttpResponseRedirect(reverse("add_category_offer"))


def edit_category_offer(request,offer_id):

    offer = Offer.objects.get(id = offer_id)
    category_obj = Category.objects.all()
    return render(request,"vendor_template/edit_category_offer_template.html",{"offer" : offer ,"id": offer_id,"categories" : category_obj})



def edit_category_offer_save(request):
    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        offer_id = request.POST.get("offer_id")
        offer_name=request.POST.get("offer_name")
        category_id=request.POST.get("category_name")
        offer_type = request.POST.get("offer_type")
        vendor = Vendor.objects.get(admin=request.user.id)
        category_name=Category.objects.get(id=category_id)
        product = Product.objects.filter(vendor_id=vendor,category=category_name)
        for products in product:
            price2 = products.price
            if offer_type == 'Price Offer':
                price2 = int(price2)
                offer_name = int(offer_name)
                new_amount = price2 - offer_name
            else:
                if products.price1 == 0:
                    price2 = products.price
                    print(products)
                    price2 = int(price2)
                    offer_name = int(offer_name)
                    amount = int(price2 * offer_name)/100
                    new_amount = price2 - amount
                    print(new_amount)
                else:
                    price2 = products.price1
                    print(products)
                    price2 = int(price2)
                    offer_name = int(offer_name)
                    amount = int(price2 * offer_name)/100
                    new_amount = price2 - amount
                    print(new_amount)

            value = Offer.objects.get(id = offer_id)
            value.offer = offer_name
            value.vendor_id = vendor
            value.product.category = category_name
            value.save()
            products.price1=price2
            products.price=new_amount
            products.save()
        messages.success(request,"Successfully Added Offer")
        return HttpResponseRedirect(reverse("add_category_offer"))        



def delete_category_offer(request,offer_id):

    offer = Offer.objects.get(id = offer_id)
    category1 = offer.product.category.id
    category_obj = Product.objects.filter(category=category1)
    for category_objs in category_obj:
        category_objs.price = category_objs.price1
        category_objs.price1 = 0
        category_objs.save()
    offer.delete()
    print(category_obj,'hai')
    
    return redirect("manage_category_offer")



def manage_vendor_order(request):
    admin = request.user.id
    vendor = Vendor.objects.get(admin=admin)
    orders = OrderDetails.objects.filter(vendor_id = vendor)
    return render(request,"vendor_template/vendor_status_template.html",{"orders":orders})


def update_order(request):
    id = request.POST.get('order_id')
    status = request.POST.get('order_status')
    print(status)

    order = OrderDetails.objects.get(id = id)
    order.order_status = status
    order.save()

    return redirect('manage_vendor_order')


def manage_order(request):
    return render(request, "vendor_template/manage_order_template.html")


def order_history(request):
    return render(request, "vendor_template/order_history_template.html")


def vendor_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    vendor = Vendor.objects.get(admin = user)
    return render(request,"vendor_template/vendor_profile.html",{"user":user,"vendor":vendor})



def vendor_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("vendor_profile"))

    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        place =request.POST.get("place")
        shop_name=request.POST.get("shop_name")
        # try:
        user = CustomUser.objects.get(id=request.user.id)
        user.first_name=first_name
        user.last_name=last_name
        if password!=None and password!="":
            user.set_password(password)
        user.save()

        vendor = Vendor.objects.get(admin = user.id)
        vendor.place=place
        vendor.shop_name=shop_name
        vendor.save()
        messages.success(request,"Successfully Updated Profile")
        return HttpResponseRedirect(reverse("vendor_profile"))
        # except:
        #     messages.error(request,"Failed to Update Profile")
        #     return HttpResponseRedirect(reverse("vendor_profile"))
