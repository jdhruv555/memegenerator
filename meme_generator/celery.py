import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meme_generator.settings')

app = Celery('meme_generator')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'check-api-keys': {
        'task': 'core.tasks.check_api_keys',
        'schedule': crontab(hour='*/6'),  # Every 6 hours
    },
    'run-scheduled-tasks': {
        'task': 'core.tasks.run_scheduled_tasks',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'cleanup-old-logs': {
        'task': 'core.tasks.cleanup_old_logs',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
    'monitor-system-health': {
        'task': 'core.tasks.monitor_system_health',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 