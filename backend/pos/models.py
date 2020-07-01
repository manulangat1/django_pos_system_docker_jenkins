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

class OrderItems(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False,blank=True,null=True)
    quantity = models.IntegerField(default=1,blank=True,null=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_item_price(self):
        return self.quantity * self.item.price
    def get_discount_price(self):
        return self.quantity * self.item.price
    def get_amount_saved(self):
        return self.get_item_price() - self.get_discount_price()
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_price()
        return self.get_item_price()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItems)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    