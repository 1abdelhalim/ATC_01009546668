import os
import django
import shutil
from datetime import datetime, timedelta

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from django.utils import timezone
from events.models import Event, Category
from django.core.files import File

print("Updating events with consistent data...")

# Get available images
images_path = os.path.join('static', 'img', 'events')
available_images = {
    'music': os.path.join(images_path, 'music-festival.jpg'),
    'technology': os.path.join(images_path, 'tech-conference.jpg'),
    'business': os.path.join(images_path, 'startup-networking.jpg'),
    'networking': os.path.join(images_path, 'startup-networking.jpg'),
    'sports': os.path.join(images_path, 'tech-conference.jpg'),  # Reusing tech image for sports
}

# Create media directory if it doesn't exist
media_events_dir = os.path.join('media', 'events')
os.makedirs(media_events_dir, exist_ok=True)

# Set base date for events (starting from tomorrow)
base_date = timezone.now() + timedelta(days=1)

# Update events
for index, event in enumerate(Event.objects.all()):
    # Set consistent dates (spaced 10 days apart)
    event_date = base_date + timedelta(days=index*10)
    event.date = event_date
    
    # Get category name
    category = event.category
    category_name = category.slug if category else 'default'
    
    # Copy image to media folder
    if category_name in available_images:
        source_img_path = available_images[category_name]
        
        # Determine target path
        filename = f"{event.slug}.jpg"
        target_img_path = os.path.join(media_events_dir, filename)
        
        # Copy file
        shutil.copy(source_img_path, target_img_path)
        
        # Update event image field
        event.image = f"events/{filename}"
    
    # Make sure venue is filled
    if not event.venue or event.venue.strip() == '':
        venues = {
            'music': 'Grand Concert Hall',
            'technology': 'Tech Innovation Center',
            'business': 'Business Conference Center',
            'networking': 'Networking Plaza',
            'sports': 'Sports Arena',
            'food': 'Culinary Center',
        }
        event.venue = venues.get(category_name, 'Convention Center')
    
    event.save()
    print(f"Updated event: {event.name} - Date: {event.date} - Image: {event.image} - Venue: {event.venue}")

print("All events updated successfully!") 