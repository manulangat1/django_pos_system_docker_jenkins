from django.db import models
from django.contrib.auth.models  import AbstractUser
# Create your models here.

class User(AbstractUser):
    bio = models.TextField()


    def __str__(self):
        return self.username

CATEGORY_CHOICES = (
    ('HOME','HOME'),
    ('OFFICE','OFFICE'),
    ('LUXURY','LUXURY'),
)
LABEL_CHOICES = (
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(blank=True,null=True)
    pic = models.ImageField(upload_to='articles/',null=True,blank=True)
    # pic1 = models.ImageField(upload_to='articles/',null=True,blank=True)
    # pic2 = models.ImageField(upload_to='articles/',null=True,blank=True)
    discount_price = models.FloatField(blank=True,null=True)
    slug = models.SlugField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=10,blank=True,null=True)
    label = models.CharField(choices=LABEL_CHOICES,max_length=10,blank=True,null=True)
    
    def __str__(self):
        return self.title