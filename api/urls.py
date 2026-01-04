from django.contrib import admin
from django.urls import path
from example.views import index_view, contact_view, send_scheduled_emails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('api/cron/send-emails/', send_scheduled_emails, name='send_emails'),
]
