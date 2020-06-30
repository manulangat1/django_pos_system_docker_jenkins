from django.urls import path,include
from .api import UserAPI,LoginAPI,RegisterAPI,ItemAPI,ItemDetailsAPI,OrderItemsAPI
from knox import views as knox_views
urlpatterns = [
    path('api/auth',include('knox.urls')),
    path('register/',RegisterAPI.as_view(),name="user_registration"),
    path('items/',ItemAPI.as_view(),name="items_list"),
    path('items/<slug>/',ItemDetailsAPI.as_view(),name="item_details"),
    path('ordered/',OrderItemsAPI.as_view(),name="order_list"),
    path('login/',LoginAPI.as_view(),name="user_login"),
    path('user/',RegisterAPI.as_view(),name="user_api"),
    path('logout/',knox_views.LogoutView.as_view(),name='logout'),
]