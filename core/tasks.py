from celery import shared_task
from django.utils import timezone
from .models import SystemLog, ScheduledTask, APIKey
from memes.tasks import process_meme_generation
from social.tasks import collect_post_analytics, schedule_posts
import requests
import json

@shared_task
def check_api_keys():
    """Check if API keys are valid and active."""
    api_keys = APIKey.objects.filter(is_active=True)
    
    for key in api_keys:
        try:
            if key.service == 'openai':
                # Test OpenAI API
                response = requests.get(
                    'https://api.openai.com/v1/models',
                    headers={'Authorization': f'Bearer {key.key}'}
                )
                if response.status_code != 200:
                    key.is_active = False
                    key.save()
                    
            elif key.service == 'newsapi':
                # Test NewsAPI
                response = requests.get(
                    'https://newsapi.org/v2/top-headlines',
                    params={'country': 'us'},
                    headers={'X-Api-Key': key.key}
                )
                if response.status_code != 200:
                    key.is_active = False
                    key.save()
                    
            # Add more API checks as needed
            
        except Exception as e:
            SystemLog.objects.create(
                level='error',
                message=f'API key check failed for {key.service}',
                context={'error': str(e)}
            )
            continue

@shared_task
def run_scheduled_tasks():
    """Run all scheduled tasks that are due."""
    now = timezone.now()
    tasks = ScheduledTask.objects.filter(
        status__in=['pending', 'failed'],
        next_run__lte=now
    )
    
    for task in tasks:
        try:
            task.status = 'running'
            task.save()
            
            if task.task_type == 'meme_generation':
                process_meme_generation.delay()
            elif task.task_type == 'analytics_collection':
                collect_post_analytics.delay()
            elif task.task_type == 'post_scheduling':
                schedule_posts.delay()
            # Add more task types as needed
            
            task.status = 'completed'
            task.last_run = now
            task.next_run = now + timedelta(hours=24)  # Example: run daily
            task.save()
            
        except Exception as e:
            task.status = 'failed'
            task.save()
            
            SystemLog.objects.create(
                level='error',
                message=f'Task {task.name} failed',
                context={'error': str(e)}
            )

@shared_task
def cleanup_old_logs():
    """Clean up old system logs."""
    # Keep logs for 30 days
    time_threshold = timezone.now() - timedelta(days=30)
    SystemLog.objects.filter(created_at__lt=time_threshold).delete()

@shared_task
def monitor_system_health():
    """Monitor system health and create alerts if needed."""
    try:
        # Check database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            
        # Check Redis connection
        from django.core.cache import cache
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') != 'ok':
            raise Exception("Redis connection failed")
            
        # Log success
        SystemLog.objects.create(
            level='info',
            message='System health check passed',
            context={'timestamp': timezone.now().isoformat()}
        )
        
    except Exception as e:
        SystemLog.objects.create(
            level='critical',
            message='System health check failed',
            context={'error': str(e)}
        ) 