# example/urls.py
from django.urls import path, include
from django.contrib import admin

from example.views import index


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
