from celery import shared_task
from django.utils import timezone
from .models import SocialMediaAccount, SocialMediaPost, PostAnalytics
from memes.models import Meme
import requests
import json
from datetime import timedelta
import random

@shared_task
def post_to_instagram(meme_id, account_id):
    """Post a meme to Instagram using the Graph API."""
    try:
        meme = Meme.objects.get(id=meme_id)
        account = SocialMediaAccount.objects.get(id=account_id)
        
        # Create social media post record
        post = SocialMediaPost.objects.create(
            meme=meme,
            account=account,
            scheduled_time=timezone.now(),
            status='scheduled'
        )
        
        # TODO: Implement actual Instagram posting using Graph API
        # This is a placeholder for the actual implementation
        
        # Update post status
        post.status = 'posted'
        post.posted_at = timezone.now()
        post.post_id = 'dummy_post_id'  # Replace with actual post ID
        post.save()
        
        # Update meme status
        meme.status = 'posted'
        meme.posted_at = timezone.now()
        meme.posted_to['instagram'] = post.post_id
        meme.save()
        
        return post.id
        
    except Exception as e:
        if 'post' in locals():
            post.status = 'failed'
            post.error_message = str(e)
            post.save()
        raise

@shared_task
def collect_post_analytics():
    """Collect analytics for posted memes."""
    # Get posts from the last 24 hours
    time_threshold = timezone.now() - timedelta(days=1)
    posts = SocialMediaPost.objects.filter(
        status='posted',
        posted_at__gte=time_threshold
    )
    
    for post in posts:
        try:
            # TODO: Implement actual analytics collection
            # This is a placeholder for the actual implementation
            
            analytics = PostAnalytics.objects.create(
                post=post,
                likes=0,  # Replace with actual data
                comments=0,
                shares=0,
                views=0,
                engagement_rate=0.0
            )
            
        except Exception as e:
            print(f"Error collecting analytics for post {post.id}: {str(e)}")
            continue

@shared_task
def schedule_posts():
    """Schedule posts for the next 24 hours."""
    # Get memes that are ready to be posted
    memes = Meme.objects.filter(
        status='generated',
        posted_at__isnull=True
    )
    
    for meme in memes:
        # Get active Instagram accounts
        accounts = SocialMediaAccount.objects.filter(
            platform='instagram',
            is_active=True
        )
        
        for account in accounts:
            # Schedule post for a random time in the next 24 hours
            scheduled_time = timezone.now() + timedelta(
                hours=24 * random.random()
            )
            
            SocialMediaPost.objects.create(
                meme=meme,
                account=account,
                scheduled_time=scheduled_time,
                status='scheduled'
            ) 