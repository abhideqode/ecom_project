from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import HttpResponse

from .manager import CustomUserManager

# Create your models here.
users = (
    ('admin', 'admin'),
    ('shopuser', 'shopuser'),
    ('customer', 'customer')
)


class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=users, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    mob = models.CharField(max_length=11, blank=True, null=True)
    objects = CustomUserManager()
    models.BooleanField(default=False)
    shop_name = models.CharField(max_length=40, blank=True)


sizes = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
)
gender = (
    ('male', 'male'),
    ('female', 'female'))


class Product(models.Model):
    product_type = models.CharField(max_length=40)
    product_name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    product_size = models.CharField(max_length=20, choices=sizes)
    price = models.IntegerField()
    product_img = models.ImageField(null=True, blank=True, default='images/background.jpeg')
    gender = models.CharField(max_length=10, choices=gender, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, blank=True, null=True)


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)


class WishItems(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print("hello in the signals")

    if created:
        print("inside created")
        Admin_mails = []
        previous = User.objects.get(id=instance.id)
        print(previous)
        print("calling wishlist instance")
        wishlist = Wishlist(user = previous)
        wishlist.save()
        admins = User.objects.filter(user_type='admin').values()
        for i in range(0, len(admins)):
            Admin_mails.append(admins[i]['email'])
        print(Admin_mails)
        # print(previous.__dict__)
        # print(instance.__dict__)
        # print(instance.is_active)
        if not instance.is_active:
            approveurl = "http://127.0.0.1:8000/ecomapprove/" + str(instance.id) + "/"
            context = (
                {'id': instance.id, 'Username': instance.username, 'Firstname': instance.first_name, 'url': approveurl})
            html_content = render_to_string('ecomapp/adminmail.html', context)
            text_content = strip_tags(html_content)
            admins
            email = EmailMultiAlternatives('A cool subject', text_content, settings.EMAIL_HOST_USER,
                                           ['abhijeetss213@gmail.com'])
            email.attach_alternative(html_content, 'text/html')
            email.send()
            print(send_mail)
