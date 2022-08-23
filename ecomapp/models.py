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


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print("hello in the signals")

    if created:
        print("inside created")
        Admin_mails = []
        previous = User.objects.get(id=instance.id)
        admins = User.objects.filter(user_type='admin').values()
        for i in range(0, len(admins)):
            Admin_mails.append(admins[i]['email'])
        print(Admin_mails)
        # print(previous.__dict__)
        # print(instance.__dict__)
        # print(instance.is_active)
        if not instance.is_active:

            approveurl = "http://127.0.0.1:8000/ecomapprove/"+str(instance.id)+"/"
            context = ({'id': instance.id, 'Username': instance.username, 'Firstname': instance.first_name, 'url':approveurl})
            html_content = render_to_string('ecomapp/adminmail.html', context)
            text_content = strip_tags(html_content)
            admins
            email = EmailMultiAlternatives('A cool subject', text_content, settings.EMAIL_HOST_USER,
                                           ['abhijeetss213@gmail.com'])
            email.attach_alternative(html_content, 'text/html')
            email.send()
            print(send_mail)
