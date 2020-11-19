from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from food_ordering_app.models import Vendor, Category, Product, Offer, CustomUser, OrderDetails
from django.urls import reverse 
import base64
from PIL import Image
from base64 import decodestring
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile


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
    return render(request, "vendor_template/home_content.html")


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
        quantity=request.POST.get("quantity")
        vendor_id=Vendor.objects.get(admin=request.user.id)
        image_file =request.POST.get('image64data')
        value = image_file.strip('data:image/png;base64,')

        format, imgstr = image_file.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)


        try:
            product=Product(product_name=product_name,category=category_name,price=price,quantity=quantity,vendor_id=vendor_id,product_image = data)
            product.save()
            messages.success(request,"Successfully Added Product")
            return HttpResponseRedirect(reverse("add_product"))
        except:
            messages.error(request,"Failed to Add Product")
            return HttpResponseRedirect(reverse("add_product"))


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
        product_name=Product.objects.get(id=product_id)
        vendor = Vendor.objects.get(admin=request.user.id)

        check_exist = Offer.objects.filter(product=product_name, vendor_id=vendor).exists()
        if check_exist:
            offer = Offer.objects.get(product=product_name,vendor_id=vendor)
            offer.offer = offer_name
            offer.save()
            messages.success(request,"Successfully Added Offer")
            return HttpResponseRedirect(reverse("add_offer"))

        else:

            offer = Offer(offer=offer_name,product=product_name,vendor_id=vendor)
            offer.save()
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
        vendor_id = Vendor.objects.get(admin=request.user.id)


        value = Offer.objects.get(id = offer_id)  

        value.offer = offer_name
        value.vendor_id = vendor_id
        product1 = Product.objects.get(id = product)
        value.product = product1
        value.save()
        messages.success(request,"Successfully Updated Offer")
        return HttpResponseRedirect(reverse("edit_offer",kwargs={"offer_id":offer_id}))



def delete_offer(request,offer_id):

    offer = Offer.objects.get(id = offer_id)
    offer.delete()
    return redirect("manage_offer")



def manage_vendor_order(request):
    
    orders = OrderDetails.objects.all()
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
