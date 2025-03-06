
from django.db import models


class Meeting(models.Model):
    calendar_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_link = models.URLField(null=True, blank=True)
    description = models.TextField()
    attendees = models.JSONField()
    source = models.CharField(max_length=10, choices=[('google', 'Google'), ('outlook', 'Outlook')])