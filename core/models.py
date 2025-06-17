from django.db import models
from django.contrib.auth.models import User

class APIKey(models.Model):
    SERVICE_CHOICES = [
        ('openai', 'OpenAI'),
        ('newsapi', 'NewsAPI'),
        ('twitter', 'Twitter API'),
        ('reddit', 'Reddit API'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'service')

    def __str__(self):
        return f"{self.service} API Key"

class SystemLog(models.Model):
    LEVEL_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    context = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.level}: {self.message[:50]}"

class ScheduledTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    name = models.CharField(max_length=100)
    task_type = models.CharField(max_length=50)
    schedule = models.CharField(max_length=100)  # Cron expression or interval
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    parameters = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"
