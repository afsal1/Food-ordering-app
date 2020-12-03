from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.models import User, auth
from django.contrib import messages
from food_ordering_app.models import Vendor, CustomUser,OrderDetails, Category, Customer, OrderItem
import base64
from PIL import Image
from base64 import decodestring
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile
import datetime
from datetime import *



def admin_home(request):
    total_vendor = Vendor.objects.all().count()
    total_customers=Customer.objects.all().count()
    total_oders=OrderDetails.objects.all().count()

    orders=OrderDetails.objects.all()
    total = 0
    for order in orders:
        try:
            order_total=order.get_cart_total
        except:
            order_total=0
        total = total + order_total

    # total count of customers
    customer_count=Customer.objects.all().count()
    

    # chart
    year = datetime.now().year
    month = datetime.now().month
    chart_order = OrderDetails.objects.filter(date_ordered__year = year,date_ordered__month = month)
    

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

    context = {
        "total_customers":total_customers,
        "total_vendor":total_vendor,
        "total_oders":total_oders,
        "total":total,
        "chart_values":chart_values,
   
    }

    return render(request, "admin_template/home_content.html",context)





def manage_vendor(request):
    vendor=Vendor.objects.all()
    return render(request, "admin_template/manage_vendor_template.html",{"vendors":vendor})


def add_vendor(request):
    return render(request, "admin_template/add_vendor_template.html")

def add_vendor_save(request):
    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        shop_name=request.POST.get("shop_name")
        place=request.POST.get("place")
        color_picker=request.POST.get("colorpicker")
        image_file =request.POST.get('image64data')
        print(image_file)
        value = image_file.strip('data:image/png;base64,')

        format, imgstr = image_file.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
        #try:
        user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=2)
        user.vendor.shop_name=shop_name
        user.vendor.place=place
        user.vendor.color_picker=color_picker
        user.vendor.vendor_image=data
        user.save()
        messages.success(request,"Successfully Added Vendor")
        return HttpResponseRedirect(reverse("add_vendor"))
        # except:
        #     messages.error(request,"Failed to Add Vendor")
        #     return HttpResponseRedirect(reverse("add_vendor"))

def edit_vendor(request,vendor_id):
    vendor =Vendor.objects.get(admin=vendor_id)
    return render(request,"admin_template/edit_vendor_template.html",{"vendor":vendor})



def edit_vendor_save(request):
    if request.method == 'POST':
        vendor_id=request.POST.get("vendor_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        # username=request.POST.get("username")
        email=request.POST.get("email")
        shop_name=request.POST.get("shop_name")
        place=request.POST.get("place")
        image_file =request.POST.get('image64data')
        print(image_file)
        value = image_file.strip('data:image/png;base64,')

        format, imgstr = image_file.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)

        user = CustomUser.objects.get(id=vendor_id)
        print(vendor_id)

        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()

        vendor=Vendor.objects.get(admin=vendor_id)
        vendor.place=place
        vendor.shop_name=shop_name
        vendor.vendor_image=data
        vendor.save()

        messages.success(request,"Successfully Added Vendor")
        return HttpResponseRedirect(reverse("edit_vendor",kwargs={"vendor_id":vendor_id}))
    else:
        messages.error(request,"Successfully Added Vendor")
        return HttpResponseRedirect(reverse("edit_vendor",kwargs={"vendor_id":vendor_id}))


def delete_vendor(request,vendor_id):

    vendor = Vendor.objects.get(admin=vendor_id)
    vendor.delete()
    return redirect("manage_vendor")

def manage_category(request):
    category=Category.objects.all()
    return render(request, "admin_template/manage_category_template.html",{"categories":category})



def add_category(request):
    return render(request, "admin_template/add_category_template.html")




def add_category_save(request):
    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        category=request.POST.get("category_name")
        # try:

        category_modal=Category(category_name=category)
        category_modal.save()
        messages.success(request,"Successfully Added Category")
        return HttpResponseRedirect(reverse("add_category"))
        # except:
        #     messages.error(request,"Failed to Add Category")
        #     return HttpResponseRedirect(reverse("add_category"))


def edit_category(request,category_id):
    category=Category.objects.get(id=category_id)
    return render(request,"admin_template/edit_category_template.html",{"category" : category,"id": category_id})



def edit_category_save(request):
    if request.method!="POST":
        return HttpResponse("method not allowed")
    else:
        category_id=request.POST.get("category_id")
        category=request.POST.get("category_name")   
        try:
            category1=Category.objects.get(id=category_id)
            category1.category_name=category
            print(category1)
            category1.save()
            messages.success(request,"Successfully Added Category")
            return HttpResponseRedirect(reverse("edit_category",kwargs={"category_id":category_id}))
        except:
            messages.error(request,"Failed to Add Course")
            return HttpResponseRedirect(reverse("edit_category",kwargs={"category_id":category_id}))



def delete_category(request,category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    return HttpResponseRedirect(reverse("manage_category"))



def order_details(request):
    order=OrderDetails.objects.all()
    items =[]
    for i in order:
        details=OrderItem.objects.all()
        for j in details:
            items.append(j)

    context ={
        "items":items,
        "order":order,
       

    }
    return render(request, "admin_template/order_details_template.html",context)

def user_details(request):
    return render(request, "admin_template/user_details_template.html")


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request,"admin_template/admin_profile.html",{"user":user})



def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))

    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            user=CustomUser.objects.get(id=request.user.id)
            user.first_name=first_name
            user.last_name=last_name
            if password!=None and password!="":
                user.set_password(password)
            user.save()
            messages.success(request,"Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request,"Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


def manage_customers(request):
    customer = Customer.objects.all()
    context = {
        "customers":customer,
        }
    return render(request,"admin_template/manage_user_template.html",context)


def block_user(request,user_id):
    users = CustomUser.objects.get(id=user_id)
    users.is_staff = 1
    users.save()
    return redirect("manage_customers")

def unblock_user(request,user_id):
    users = CustomUser.objects.get(id=user_id)
    users.is_staff = 0
    users.save()
    return redirect("manage_customers")


def block_admin(request,user_id):
    users = CustomUser.objects.get(id=user_id)
    users.is_staff = 1
    users.save()
    return redirect("manage_vendor")

def unblock_admin(request,user_id):
    users = CustomUser.objects.get(id=user_id)
    users.is_staff = 0
    users.save()
    return redirect("manage_vendor")



