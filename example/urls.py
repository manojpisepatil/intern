# # example/urls.py
# from django.urls import path
# from example.views import index

# urlpatterns = [
#     path('', index),
# ]



# example/urls.py
from django.urls import path
from example.views import index_view, contact_view
from .views import send_scheduled_emails


urlpatterns = [
    path('', index_view, name='index'),
    path('contact/', contact_view, name='contact'),
    path("send-scheduled-emails/", send_scheduled_emails),
    path("db-test/", db_test),
]

