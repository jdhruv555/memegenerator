from django.db import models
from django.contrib.auth.models import User

class TrendingTopic(models.Model):
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=50)  # e.g., 'twitter', 'reddit', 'news'
    source_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.source})"

class MemeTemplate(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='meme_templates/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Meme(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generated', 'Generated'),
        ('posted', 'Posted'),
        ('failed', 'Failed'),
    ]

    topic = models.ForeignKey(TrendingTopic, on_delete=models.CASCADE)
    template = models.ForeignKey(MemeTemplate, on_delete=models.SET_NULL, null=True)
    caption = models.TextField()
    image = models.ImageField(upload_to='generated_memes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    posted_to = models.JSONField(default=dict)  # Store social media post IDs
    metadata = models.JSONField(default=dict)  # Store additional metadata

    def __str__(self):
        return f"Meme: {self.topic.title} ({self.status})"

class MemeGenerationLog(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    step = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log: {self.meme} - {self.step} ({self.status})"
