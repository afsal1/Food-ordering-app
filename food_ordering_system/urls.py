"""food_ordering_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from food_ordering_app import views, admin_views, vendor_views, user_views
from django.conf.urls.static import static
from food_ordering_system import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('show_login_page',views.show_login_page, name="show_login_page"),
    path('do_login',views.do_login, name="do_login"),
    path('admin_home' ,views.admin_home, name="admin_home"),
    path('logout_user' ,views.logout_user, name="logout_user"),
    path('accounts/' ,include('allauth.urls')),

#admin Views 

    path('admin_profile' ,admin_views.admin_profile, name="admin_profile"),
    path('admin_profile_save' ,admin_views.admin_profile_save, name="admin_profile_save"),
    path('add_vendor' ,admin_views.add_vendor, name="add_vendor"),
    path('add_vendor_save' ,admin_views.add_vendor_save, name="add_vendor_save"),
    path('manage_vendor' ,admin_views.manage_vendor, name="manage_vendor"),
    path('add_category' ,admin_views.add_category, name="add_category"),
    path('add_category_save' ,admin_views.add_category_save, name="add_category_save"),
    path('manage_category' ,admin_views.manage_category, name="manage_category"),
    path('order_details' ,admin_views.order_details, name="order_details"),
    path('user_details' ,admin_views.user_details, name="user_details"),
    path('edit_category/<str:category_id>' ,admin_views.edit_category, name="edit_category"),
    path('edit_category_save' ,admin_views.edit_category_save, name="edit_category_save"),
    path('delete_category/<category_id>' ,admin_views.delete_category, name="delete_category"),
    path('edit_vendor/<str:vendor_id>' ,admin_views.edit_vendor, name="edit_vendor"),
    path('edit_vendor_save' ,admin_views.edit_vendor_save, name="edit_vendor_save"),
    path('delete_vendor/<vendor_id>' ,admin_views.delete_vendor, name="delete_vendor"),


#vendor views
    path('vendor_profile' ,vendor_views.vendor_profile, name="vendor_profile"),
    path('vendor_profile_save' ,vendor_views.vendor_profile_save, name="vendor_profile_save"),
    path('show_vendor_login_page',vendor_views.show_vendor_login_page, name="show_vendor_login_page"),
    path('do_vendor_login',vendor_views.do_vendor_login, name="do_vendor_login"),
    path('vendor_home' ,vendor_views.vendor_home, name="vendor_home"),
    path('logout_vendor' ,vendor_views.logout_vendor, name="logout_vendor"),
    path('add_product' ,vendor_views.add_product, name="add_product"),
    path('add_product_save' ,vendor_views.add_product_save, name="add_product_save"),
    path('manage_product' ,vendor_views.manage_product, name="manage_product"),
    path('manage_order' ,vendor_views.manage_order, name="manage_order"),
    path('order_history' ,vendor_views.order_history, name="order_history"),
    path('edit_product/<str:product_id>' ,vendor_views.edit_product, name="edit_product"),
    path('edit_product_save' ,vendor_views.edit_product_save, name="edit_product_save"),
    path('delete_product/<product_id>' ,vendor_views.delete_product, name="delete_product"),
    path('manage_offer' ,vendor_views.manage_offer, name="manage_offer"),
    path('add_offer' ,vendor_views.add_offer, name="add_offer"),
    path('add_offer_save' ,vendor_views.add_offer_save, name="add_offer_save"),
    path('manage_vendor_order' ,vendor_views.manage_vendor_order, name="manage_vendor_order"),
    path('update_order/' ,vendor_views.update_order, name="update_order"),
    path('edit_offer/<str:offer_id>' ,vendor_views.edit_offer, name="edit_offer"),
    path('edit_offer_save' ,vendor_views.edit_offer_save, name="edit_offer_save"),
    path('delete_offer/<str:offer_id>' ,vendor_views.delete_offer, name="delete_offer"),
    path('manage_category_offer' ,vendor_views.manage_category_offer, name="manage_category_offer"),
    path('add_category_offer' ,vendor_views.add_category_offer, name="add_category_offer"),
    path('add_category_offer_save' ,vendor_views.add_category_offer_save, name="add_category_offer_save"),
    path('edit_category_offer/<str:offer_id>' ,vendor_views.edit_category_offer, name="edit_category_offer"),
    path('edit_category_offer_save' ,vendor_views.edit_category_offer_save, name="edit_category_offer_save"),
    path('delete_category_offer/<str:offer_id>' ,vendor_views.delete_category_offer, name="delete_category_offer"),





#user views
    path('show_referal_id' ,user_views.show_referal_id, name="show_referal_id"),
    path('demo_template' ,user_views.demo_template, name="demo_template"),
    path('user_home' ,user_views.user_home, name="user_home"),
    path('' ,user_views.select_baker, name="select_baker"),
    path('cart/',user_views.cart, name="cart"),
    # path('selected_baker_product' ,user_views.selected_baker_product, name="selected_baker_product"),
    path('checkout',user_views.checkout, name="checkout"),
    path('update_item',user_views.update_item, name="update_item"),
    path('process_order',user_views.process_order, name="process_order "),
    path('store/<int:vendor_id>',user_views.store, name="store"),
    path('product/<str:product_id>',user_views.product, name="product"),
    path('user_login',user_views.user_login, name="user_login"),
    path('register/<int:vendor_id>/<str:referal>',user_views.register, name="register"),
    path('logout',user_views.logout, name="logout"),
    path('mobile_verification',user_views.mobile_verification, name="mobile_verification"),
    path('otp_verification',user_views.otp_verification, name="otp_verification"),
    path('user_logout',user_views.user_logout, name="user_logout"),
    path('user_view_orders',user_views.user_view_orders, name="user_view_orders"),
    path('payment',user_views.payment, name="payment"),
    path('response/',user_views.response, name="response"),
    path('VerifyPaytmResponse',user_views.VerifyPaytmResponse, name="VerifyPaytmResponse"),
    path('category/<str:vendor_id>/<str:cat_id>',user_views.category, name="category"),
    path('getshipping/',user_views.Getshipping.as_view()),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
