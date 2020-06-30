from django.urls import path,include
from .api import UserAPI,LoginAPI,RegisterAPI
from knox import views as knox_views
urlpatterns = [
    path('register/',RegisterAPI.as_view(),name="user_registration"),
    path('login/',LoginAPI.as_view(),name="user_login"),
    path('user/',RegisterAPI.as_view(),name="user_api"),
    path('api/auth',include('knox.urls')),
    path('logout/',knox_views.LogoutView.as_view(),name='logout'),
]