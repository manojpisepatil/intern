from .views import clear_cache

urlpatterns = [
    path('', index_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('api/cron/send-emails/', send_scheduled_emails, name='send_emails'),
    path('clear-cache/', clear_cache),
]
