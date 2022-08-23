from django.db.models.signals import post_save, pre_delete, pre_save
from .models import User
from django.dispatch import receiver


# @receiver(pre_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     print("hello in the signals")
#     u = User.objects.filter(is_active=False)
#     print(u)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
