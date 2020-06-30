from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth import authenticate

from .models import User ,Item, OrderItems


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
    item = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItems
        fields = (
            'id',
            'item',
            'ordered',
            'final_price'
        )
    def get_item(self,obj):
        return ItemSerializer(self.item.all(),many=True).data
    def get_final_price(self,obj):
        return obj.get_final_price()