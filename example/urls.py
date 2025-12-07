# example/urls.py
from django.urls import path
from example.views import index

from .views import contact_view 
from .views import index_view


urlpatterns = [
    path('', index),

    path('', index_view, name='index'),  # Renders the index.html file
    path('contact/', contact_view, name='contact'),
]
