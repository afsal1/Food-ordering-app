from django.contrib import admin

# Register your models here.


from .models import Vendor, AdminUser

admin.site.register(Vendor)