"""
    this models.py file contains all the models of this projects
"""
# from urllib import request
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# from django.http import HttpResponse

from .manager import CustomUserManager

# Create your models here.
USERS = (
    ('admin', 'admin'),
    ('shopuser', 'shopuser'),
    ('customer', 'customer')
)


class User(AbstractUser):
    """
        this class Contains User we three different user Admin, Customer, Shop users
    """
    user_type = models.CharField(max_length=20, choices=USERS, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    # mob = models.CharField(max_length=11, blank=True, null=True)
    objects = CustomUserManager()
    mobile_no = models.CharField(max_length=11, blank=True, null=True)
    addressof_customer = models.CharField(max_length=50, blank=True, null=True)
    models.BooleanField(default=False)
    shop_name = models.CharField(max_length=40, blank=True)


SIZES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
)

GENDER = (
    ('male', 'male'),
    ('female', 'female')
)


class Product(models.Model):
    """
        this class Contains Product details
    """
    product_type = models.CharField(max_length=40)
    product_name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    product_img = models.ImageField(null=True, blank=True, default='images/background.jpeg')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    # wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, blank=True, null=True)


PRODUCTCOLOR = (
    ("Red", "red"),
    ("Black", "Black"),
    ("Blue", "Blue"),
    ("White", "White"),
    ("Gray", "Gray"),
)

QUANTITY = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)


class Variations(models.Model):
    """
        this class Contains Variation for different products
    """
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE,
                                related_name="product_variations")
    # quantity = models.CharField(max_length=10,choices=quantity)
    color = models.CharField(max_length=10, choices=PRODUCTCOLOR)
    size = models.CharField(max_length=20, choices=SIZES, blank=True, null=True)


class Wishlist(models.Model):
    """
        this class Contains Wishlist for the customers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)


class WishItems(models.Model):
    """
        this class Contains wishlist items for the customers
    """
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)


class CartItems(models.Model):
    """
        this class Contains CartItems
    """
    quantity = models.PositiveIntegerField(blank=True, null=True)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    color = models.CharField(max_length=10, blank=True, null=True)
    size = models.CharField(max_length=10, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)


class MyOrders(models.Model):
    """
        this class Contains Orders of the customers and respective shops
    """
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product_id = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    product_type = models.CharField(max_length=40, blank=True, null=True)
    product_name = models.CharField(max_length=40, blank=True, null=True)
    size = models.CharField(max_length=20, choices=SIZES, blank=True, null=True)
    color = models.CharField(max_length=10, choices=PRODUCTCOLOR, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    product_img = models.ImageField(null=True, blank=True, default='images/background.jpeg')
    gender = models.CharField(max_length=10, choices=GENDER, blank=True)


# class OrderPlaced(models.Model):
#     wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE,blank=True,null=True)
#     product_id = models.CharField(max_length=10,blank=True,null=True)
#     quantity = models.IntegerField(default='0',blank=True, null=True)
#     size = models.CharField(max_length=20, choices=sizes, blank=True, null=True)
#     color = models.CharField(max_length=10,choices=product_color,blank=True,null=True)
#     price = models.IntegerField(blank=True, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)


@receiver(post_save, sender=User)
def create_profile(sender,instance, created,**kwargs):
    """
        this is the signals which is used for the post save of user models
    """
    print("hello in the signals")

    if created:
        print("inside created")
        admin_mails = []
        previous = User.objects.get(id=instance.id)
        print(previous)
        print("calling wishlist instance")
        wishlist = Wishlist(user=previous)
        wishlist.save()
        admins = User.objects.filter(user_type='admin').values()
        for i in range(0, len(admins)):
            admin_mails.append(admins[i]['email'])
        print(admin_mails)
        # print(previous.__dict__)
        # print(instance.__dict__)
        # print(instance.is_active)
        if not instance.is_active:
            approveurl = "http://127.0.0.1:8000/ecom/approve/" + str(instance.id) + "/"
            context = (
                {'id': instance.id, 'Username': instance.username,
                 'Firstname': instance.first_name, 'url': approveurl})
            html_content = render_to_string('ecomapp/adminmail.html', context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('A cool subject', text_content, settings.EMAIL_HOST_USER,
                                           ['abhijeetss213@gmail.com'])
            email.attach_alternative(html_content, 'text/html')
            email.send()
            print(send_mail)
