from django.db import models
from account.models import UserManager
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class AuthToken(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    api_access_token = models.CharField(max_length=2000)
    api_refresh_token = models.CharField(max_length=2000)
    api_consumer_key= models.CharField(max_length=1000)
    api_account_number=models.CharField(max_length=100)

@receiver(post_save, sender=User)
def create_user_auth_token(sender, instance, created, **kwargs):
    if created:
        AuthToken.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_auth_token(sender, instance, **kwargs):
    instance.authtoken.save()
