

# example/urls.py
# from django.urls import path
# from example.views import index_view, contact_view
# from .views import send_scheduled_emails
# from example.views import db_test

# urlpatterns = [
#     path('', index_view, name='index'),
#     path('contact/', contact_view, name='contact'),
#     path("send-scheduled-emails/", send_scheduled_emails),
#     path("db-test/", db_test),
# ]


from django.urls import path
from .views import index_view, contact_view, send_scheduled_emails, run_migrations

urlpatterns = [
    path('', index_view),
    path('contact/', contact_view),
    path('api/cron/send-emails/', send_scheduled_emails),
    path('run-migrations/', run_migrations),  # ← Temporary! Remove after use
]

