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
    color_picker = models.CharField(max_length = 200, null=True)
    vendor_image = models.ImageField(null = True, blank = True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    @property
    def imageURL(self):
        try:
            url = self.vendor_image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(default=0,null=True,blank=True)
    name = models.CharField(max_length = 200,null = True)
    email = models.CharField(max_length= 200, null = True)
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
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True,blank=False)
    transaction_id = models.CharField(max_length = 200, null = True )
    order_status = models.CharField(default = 'Pending',max_length = 200, null = True )

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
                shipping = True
        return shipping
    
    
        
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    id=models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        try:
            total = self.product.price * self.quantity
        except:
            total = 0
        return total


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank= True, null=True)
    order = models.ForeignKey(OrderDetails, on_delete=models.SET_NULL, blank = True, null = True)
    address = models.CharField(max_length = 200,null = True)
    city = models.CharField(max_length = 200,null = True)
    state = models.CharField(max_length = 200,null = True)
    zipcode = models.CharField(max_length = 200,null = True)
    country = models.CharField(max_length = 200,null = True)
    date_added = models.DateTimeField(auto_now_add=True)


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