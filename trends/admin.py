from django.contrib import admin
from .models import TrendingTopic, Caption

@admin.register(TrendingTopic)
class TrendingTopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'source', 'created_at')
    search_fields = ('text', 'source')

@admin.register(Caption)
class CaptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'created_at')
    search_fields = ('text', 'topic__text')
