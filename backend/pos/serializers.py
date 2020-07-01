from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth import authenticate

from .models import User ,Item, OrderItems, Order

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


# class StringSerializer(serializers.StringRelatedField):
#     def to_internal_value(self,value):
#         return value
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = (
            'id',
            'username',
            'email',
            'password',
            'bio'
        )
        extra_kwargs = {'password':{'write_only':'True'}}
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],email=validated_data['email'],password=validated_data['password'])
        user.bio = validated_data['bio']
        user.is_staff = True
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password =  serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        return serializers.ValidationError("Incorect Credential")
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email', 
            'bio')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'price',
            'description',
            'pic',
            'discount_price',
            'slug',
            'category',
            'label'
        )

class OrderItemsSerializer(serializers.ModelSerializer):
    item_obj = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    item = StringSerializer()
    class Meta:
        model = OrderItems
        fields = (
            'id',
            'item',
            'item_obj',
            'ordered',
            'final_price',
            'quantity'
        )
    def get_item_obj(self,obj):
        return ItemSerializer(obj.item).data
    def get_final_price(self,obj):
        return obj.get_final_price()

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = (
            'id',
            'items',
            'total',
            'orderItems'
        )
    def get_orderItems(self,obj):
        return OrderItemsSerializer(obj.items.all(),many=True).data
    def get_total(self,obj):
        return obj.get_total()