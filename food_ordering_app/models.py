from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class CustomUser(AbstractUser):
    user_type_data=((1,"AdminUser"),(2,"Vendor"),(3,"Customer"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)


class AdminUser(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Vendor(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/' ,null = True, blank = True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()



class Category(models.Model):
    id=models.AutoField(primary_key=True)
    category_name = models.CharField(max_length = 200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Product(models.Model):
    id=models.AutoField(primary_key=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 200)
    price = models.IntegerField(default=0,null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    product_image = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.product_name
    
    @property
    def imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url


class OrderDetails(models.Model):
    id=models.AutoField(primary_key=True)
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Offer(models.Model):
    id=models.AutoField(primary_key=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer = models.CharField(max_length = 200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()




@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminUser.objects.create(admin=instance)
        if instance.user_type==2:
            Vendor.objects.create(admin=instance)
        if instance.user_type==3:
            Customer.objects.create(admin=instance)




@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminuser.save()
    if instance.user_type==2:
        instance.vendor.save()
    if instance.user_type==3:
        instance.customer.save()