from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    # USERNAME_FIELD = 'username'

    # username = models.CharField(max_length=20, unique=True, null=True)
    name = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=2, default='男')
    age = models.IntegerField(null=True)
    adname = models.CharField(max_length=20, null=True)

    def __str__(self):
        return 'Users object(%s)' % self.id
