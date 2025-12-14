from django.db import models

class ScheduledEmail(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    pdf = models.BinaryField()
    send_at = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.send_at}"
