# Generated by Django 3.1.2 on 2020-12-08 09:28

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'AdminUser'), (2, 'Vendor'), (3, 'Customer')], default=1, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('refered_person', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('order_status', models.CharField(default='Pending', max_length=200, null=True)),
                ('product_total', models.FloatField(default=0, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_ordering_app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shop_name', models.CharField(max_length=255)),
                ('place', models.CharField(max_length=255)),
                ('color_picker', models.CharField(max_length=200, null=True)),
                ('vendor_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAdress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('zipcode', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='food_ordering_app.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='food_ordering_app.orderdetails')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=200)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('price1', models.IntegerField(blank=True, default=0, null=True)),
                ('offer_price', models.IntegerField(default=1)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_ordering_app.category')),
                ('vendor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_ordering_app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_ordering_app.orderdetails')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_ordering_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='vendor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='food_ordering_app.vendor'),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('offer', models.CharField(max_length=200)),
                ('expiry_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_ordering_app.product')),
                ('vendor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_ordering_app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
