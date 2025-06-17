from celery import shared_task
from django.utils import timezone
from .models import Meme, MemeGenerationLog, TrendingTopic
import openai
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings

@shared_task
def fetch_trending_topics():
    """Fetch trending topics from various sources."""
    # TODO: Implement fetching from different sources
    # For now, we'll just create a dummy topic
    topic = TrendingTopic.objects.create(
        title="Sample Trending Topic",
        source="manual",
        source_url="https://example.com"
    )
    return topic.id

@shared_task
def generate_meme_caption(topic_id):
    """Generate a meme caption using OpenAI's GPT model."""
    try:
        topic = TrendingTopic.objects.get(id=topic_id)
        
        # Initialize OpenAI client
        client = openai.OpenAI()
        
        # Generate caption
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a meme caption generator. Create funny, engaging captions for memes."},
                {"role": "user", "content": f"Generate a meme caption for this topic: {topic.title}"}
            ]
        )
        
        caption = response.choices[0].message.content
        
        # Create meme object
        meme = Meme.objects.create(
            topic=topic,
            caption=caption,
            status='pending'
        )
        
        # Log success
        MemeGenerationLog.objects.create(
            meme=meme,
            step='caption_generation',
            status='success',
            message='Caption generated successfully'
        )
        
        return meme.id
        
    except Exception as e:
        # Log error
        if 'meme' in locals():
            MemeGenerationLog.objects.create(
                meme=meme,
                step='caption_generation',
                status='error',
                message=str(e)
            )
        raise

@shared_task
def create_meme_image(meme_id):
    """Create the meme image using the template and caption."""
    try:
        meme = Meme.objects.get(id=meme_id)
        
        # Get a random template
        template = MemeTemplate.objects.filter(is_active=True).order_by('?').first()
        if not template:
            raise Exception("No active templates found")
        
        meme.template = template
        meme.save()
        
        # Open template image
        template_path = os.path.join(settings.MEDIA_ROOT, str(template.image))
        img = Image.open(template_path)
        
        # Add caption
        draw = ImageDraw.Draw(img)
        # TODO: Add proper font handling
        font = ImageFont.load_default()
        
        # Calculate text position (center of image)
        text_width = draw.textlength(meme.caption, font=font)
        text_position = ((img.width - text_width) // 2, img.height - 50)
        
        # Add text with outline
        draw.text(text_position, meme.caption, font=font, fill='white')
        
        # Save the meme
        meme_path = os.path.join(settings.MEDIA_ROOT, 'generated_memes', f'meme_{meme.id}.png')
        img.save(meme_path)
        
        # Update meme status
        meme.image = f'generated_memes/meme_{meme.id}.png'
        meme.status = 'generated'
        meme.save()
        
        # Log success
        MemeGenerationLog.objects.create(
            meme=meme,
            step='image_generation',
            status='success',
            message='Meme image created successfully'
        )
        
        return meme.id
        
    except Exception as e:
        # Log error
        if 'meme' in locals():
            MemeGenerationLog.objects.create(
                meme=meme,
                step='image_generation',
                status='error',
                message=str(e)
            )
        raise

@shared_task
def process_meme_generation():
    """Main task to orchestrate the meme generation process."""
    # Fetch trending topics
    topic_id = fetch_trending_topics()
    
    # Generate caption
    meme_id = generate_meme_caption(topic_id)
    
    # Create meme image
    create_meme_image(meme_id)
    
    return f"Meme generation completed for topic {topic_id}" 