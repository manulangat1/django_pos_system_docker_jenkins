from django.urls import path
from . import api 


urlpatterns = [
    path('access/token', api.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', api.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    # register, confirmation, validation and callback urls
    path('c2b/register', api.register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation', api.confirmation, name="confirmation"),
    path('c2b/validation', api.validation, name="validation"),
    path('c2b/callback', api.call_back, name="call_back"),
]