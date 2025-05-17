#!/usr/bin/env python
"""
Script to verify and fix event image paths
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings_postgres')
os.environ['DJANGO_LOCAL_DEVELOPMENT'] = 'True'
django.setup()

from django.conf import settings
from events.models import Event

# Check all events and their images
print("Checking event images...")
for event in Event.objects.all():
    print(f"Event: {event.name}")
    print(f"  Image: {event.image}")
    
    if event.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(event.image))
        image_url = f"{settings.MEDIA_URL}{event.image}"
        exists = os.path.exists(image_path)
        print(f"  Image path: {image_path}")
        print(f"  Image URL: {image_url}")
        print(f"  File exists: {exists}")
    else:
        print("  No image set")
    print("-" * 50) 