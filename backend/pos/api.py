from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST


from knox.models import AuthToken

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .serializers import RegisterSerializer,LoginSerializer,UserSerializer,ItemSerializer,OrderItemsSerializer, OrderSerializer
from .models import User,Item,OrderItems, Order, MpesaPayment


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


class AddToCartView(APIView):
    def post(self,request,*args,**kwargs):
        slug = request.data.get('slug',None)
        if not slug:
            return Response({"Message":"Invalid Request"})
        item = get_object_or_404(Item,slug=slug)
        print(item.title)
        order_item,created = OrderItems.objects.get_or_create(item=item,user=request.user,ordered=False)
        order_qs = Order.objects.filter(user=request.user,ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            print(order)
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                print(order_item)
                return Response(status=HTTP_200_OK)
            else:
                order.items.add(order_item)
                return Response(status=HTTP_200_OK)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user,ordered_date=ordered_date)
            order.items.add(order_item)
        return Response(status=HTTP_200_OK)

class OrderDetailsAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    # queryset = Order.objects.filter(user)
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user,ordered=False)

class RemoveFromCart(APIView):
    def post(self,request,*args,**kwargs):
        slug = request.data['slug']
        if not slug:
            return Response({"Item to be reomved is requuire "},status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(Item,slug=slug)
        order_qs = Order.objects.filter(user=request.user,ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItems.objects.filter(
                    user= request.user,
                    ordered=False
                )[0]
                print(order_item)
                order.items.remove(order_item)
        return Response({"Successfully removed from cart"},status=HTTP_200_OK)

class ManipulateQuantity(APIView):
    def post(self,request,*args,**kwargs):
        slug = request.data['slug']
        quantity = request.data['quantity']

        if not slug and not quantity:
             return Response({"Item to be reomved is requuire "},status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(Item,slug=slug)
        order_qs = Order.objects.filter(user=request.user,ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=slug).exists():
                order_item = OrderItems.objects.filter(user=request.user,item=item)[0]
                if order_item.quantity  >= quantity:
                    order_item.quantity -=  quantity
                    order_item.save()
                    print(order_item.quantity)
                    return Response({"done"})
                return Response(status=HTTP_400_BAD_REQUEST)
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_400_BAD_REQUEST)

##mpesa intergrations 
from django.http import HttpResponse,JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json 
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
# from django.views.decorators import csrf_exempt
from django.views.decorators.csrf import  csrf_exempt

from decouple import config 
def getAccessToken(request):
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL,auth=HTTPBasicAuth(consumer_key,consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254740415950,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254740415950,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Manulangat",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')
@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    print(request.host())
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "http://127.0.0.1:8000/api/v1/c2b/confirmation",
               "ValidationURL": "http://127.0.0.1:8000/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)
@csrf_exempt
def call_back(request):
    pass
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))