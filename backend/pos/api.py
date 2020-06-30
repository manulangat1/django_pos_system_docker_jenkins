from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from knox.models import AuthToken

from .serializers import RegisterSerializer,LoginSerializer,UserSerializer,ItemSerializer,OrderItemsSerializer
from .models import User,Item,OrderItems


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
        })
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
        })
class UserAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class =UserSerializer
    def get_object(self):
        return self.request.user
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        return Response({"Added successfully"})

class ItemAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

class ItemDetailsAPI(generics.RetrieveAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    lookup_field = 'slug'

class OrderItemsAPI(generics.ListCreateAPIView):
    serializer_class = OrderItemsSerializer

    def get_queryset(self):
        qs = OrderItems.objects.filter(ordered=False,user=self.request.user)
        print(qs)
        return qs
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
