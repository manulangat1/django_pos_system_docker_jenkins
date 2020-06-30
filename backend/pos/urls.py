from django.urls import path,include
from .api import UserAPI,LoginAPI,RegisterAPI


urlpatterns = [
    path('register/',RegisterAPI.as_view(),name="user_registration"),
    path('login/',LoginAPI.as_view(),name="user_login"),
    path('user/',RegisterAPI.as_view(),name="user_api"),
]