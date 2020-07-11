from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('auth/v1/',include('pos.urls')),
    path('tulipe/',include('pos.mpesa_urls')),
    path('admin/', admin.site.urls),
]
