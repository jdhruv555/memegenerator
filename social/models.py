from django.db import models
from django.contrib.auth.models import User
from memes.models import Meme

class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('reddit', 'Reddit'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    username = models.CharField(max_length=100)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True)
    token_expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'platform')

    def __str__(self):
        return f"{self.platform}: {self.username}"

class SocialMediaPost(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('posted', 'Posted'),
        ('failed', 'Failed'),
    ]

    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=100, blank=True)  # ID from social media platform
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_time = models.DateTimeField()
    posted_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)  # Store platform-specific metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post: {self.meme} to {self.account} ({self.status})"

class PostAnalytics(models.Model):
    post = models.ForeignKey(SocialMediaPost, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics: {self.post} ({self.collected_at})"
