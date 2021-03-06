from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.


# def show_login_page(request):
#     return render(request, "login_page.html")

def do_login(request):
    if request.user.is_authenticated:
        return redirect("admin_home")
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if user.user_type == "1":
                    return redirect("admin_home")
                    print("login")
            else:
                messages.error(request,"Inavalid login details")
                return redirect("do_login")
                print("not login")
        except:
            messages.error(request,"Inavalid login details")
            return redirect("do_login")
            print(" not  h login")

    else:
        return render(request,"login_page.html")


# def admin_home(request):
#     return render(request, "admin_template/home_content.html")
@login_required(login_url="/do_login")
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("do_login")