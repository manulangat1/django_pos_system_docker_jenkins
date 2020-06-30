from rest_framework import serializers
from rest_framework.response import Response

from django.contrib.auth import authenticate

from .models import User 


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = (
            'id',
            'username',
            'email',
            'password',
            'bio'
            'is_staff'
        )
        extra_kwargs = {'password':{'write_only':'True'}}
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],email=validated_data['email'],password=validated_data['password'],)
        user.bio = validated_data['bio']
        user.is_staff = validated_data['is_staff']
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        return serializers.ValidationError({"Incorrect Validations"})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email', 
            'bio'
            'is_staff')