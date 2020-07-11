from django.contrib import admin
from .models import User,Item,OrderItems, Order
# Register your models here.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(OrderItems)
admin.site.register(Order)
