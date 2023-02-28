from django.db import models
from account.models import User


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    quantity=models.IntegerField()
