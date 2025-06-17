from django.db import models

# Create your models here.

class TrendingTopic(models.Model):
    text = models.CharField(max_length=255)
    source = models.CharField(max_length=50)  # 'google_trends', 'reddit', 'twitter'
    source_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} ({self.source})"

class Caption(models.Model):
    topic = models.ForeignKey(TrendingTopic, on_delete=models.CASCADE, related_name='captions')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}... (Topic: {self.topic.text})"
