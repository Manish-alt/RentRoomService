from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

#Create Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length = 20, blank=True)
    address1 = models.CharField(max_length = 200, blank=True)
    address2 = models.CharField(max_length = 200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_bookmark = models.CharField(max_length = 200, blank=True, null=True )

    
    def __str__(self):
        return self.user.username
    
#Create a user profile by default when user sign up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
post_save.connect(create_profile, sender=User)



# Property Type
class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

# Customer Details
class Customer(models.Model):

    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 20)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone} {self.email} {self.password}'


# Room Details
class Product(models.Model):
    name = models.CharField(max_length = 50)
    price = models.DecimalField(default = 0, decimal_places = 2, max_digits = 10)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default = 1)
    description = models.CharField(max_length = 1000, default = '', blank=True, null=True)
    image = models.ImageField(upload_to='upload/product/')
    is_available = models.BooleanField(default = False)
    address = models.CharField(max_length = 200, blank=False, null=False, default = "")
    city = models.CharField(max_length = 100, blank=False, null=False, default = "")
    state = models.CharField(max_length = 100, blank=False, null=False, default = "")
    zipcode = models.CharField(max_length = 10, blank=False, null=False, default = "")
    country = models.CharField(max_length = 50, blank=False, null=False, default="")
    extension = models.CharField(max_length = 10, default="")
    phone = models.CharField(max_length = 20, blank=False, null=False, default="")
    is_sharable = models.BooleanField(default = False)
    is_Fully_Furnished = models.BooleanField(default = False)
    amenities = models.CharField(max_length = 200, default = "")

    def __str__(self):
        return f'{self.name} {self.price} {self.description} {self.category} {self.image}'

#Room Rent
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    address =  models.CharField(max_length = 100, default = '', blank = True)
    phone = models.CharField(max_length = 20, default = '', blank = True)
    date = models.DateField(default = datetime.datetime.today)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.product

