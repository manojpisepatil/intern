# # example/urls.py
# from django.urls import path
# from example.views import index

# urlpatterns = [
#     path('', index),
# ]



# example/urls.py
from django.urls import path
from example.views import index_view, contact_view

urlpatterns = [
    path('', index_view, name='index'),
    path('contact/', contact_view, name='contact'),
]
