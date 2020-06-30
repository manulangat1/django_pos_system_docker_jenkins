from django.db import models
from django.contrib.auth.models  import AbstractBaseUser
# Create your models here.

class User(AbstractBaseUser):
    bio = models.TextField()


    def __str__(self):
        return self.username