import os
import django
import datetime
import random
from django.utils import timezone

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from django.contrib.auth import get_user_model
from events.models import Category, Tag, Event

User = get_user_model()

def create_sample_data():
    # Get admin user
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("No admin user found. Please create a superuser first.")
            return
    except Exception as e:
        print(f"Error getting admin user: {e}")
        return
    
    # Create categories
    categories = [
        {"name": "Music", "description": "Music concerts and festivals"},
        {"name": "Technology", "description": "Tech conferences and workshops"},
        {"name": "Sports", "description": "Sports events and competitions"},
        {"name": "Networking", "description": "Networking events and meetups"},
        {"name": "Business", "description": "Business conferences and networking events"},
    ]
    
    created_categories = []
    for category_data in categories:
        try:
            category, created = Category.objects.get_or_create(
                name=category_data["name"],
                defaults={"description": category_data["description"]}
            )
            created_categories.append(category)
            if created:
                print(f"Created category: {category.name}")
            else:
                print(f"Category already exists: {category.name}")
        except Exception as e:
            print(f"Error creating category {category_data['name']}: {e}")
    
    # Create tags
    tags = ["Featured", "Free", "Outdoors", "Virtual", "Premium", "Family-friendly", "Workshop", "Conference"]
    created_tags = []
    
    for tag_name in tags:
        try:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            created_tags.append(tag)
            if created:
                print(f"Created tag: {tag.name}")
            else:
                print(f"Tag already exists: {tag.name}")
        except Exception as e:
            print(f"Error creating tag {tag_name}: {e}")
    
    # Create events
    events = [
        {
            "name": "Summer Music Festival",
            "description": "Join us for a weekend of amazing music performances featuring top artists from around the world. This annual festival is the highlight of the summer season with multiple stages, food vendors, and activities for all ages.",
            "venue": "Central Park",
            "date": timezone.now() + datetime.timedelta(days=30),
            "price": 59.99,
            "capacity": 5000,
            "category": "Music"
        },
        {
            "name": "Web Development Conference",
            "description": "A two-day conference focused on the latest trends and technologies in web development. Sessions include frontend frameworks, backend optimization, security best practices, and hands-on workshops.",
            "venue": "Tech Convention Center",
            "date": timezone.now() + datetime.timedelta(days=45),
            "price": 299.99,
            "capacity": 800,
            "category": "Technology"
        },
        {
            "name": "Marathon Championships",
            "description": "The annual city marathon brings together professional and amateur runners from across the country. Featuring multiple race categories including full marathon, half marathon, and 10K run.",
            "venue": "Downtown City Routes",
            "date": timezone.now() + datetime.timedelta(days=60),
            "price": 75.00,
            "capacity": 3000,
            "category": "Sports"
        },
        {
            "name": "Professional Networking Summit",
            "description": "Connect with professionals from diverse industries in this premier networking event. Expand your network, discover new opportunities, and participate in guided networking sessions with industry leaders.",
            "venue": "Waterfront Convention Center",
            "date": timezone.now() + datetime.timedelta(days=15),
            "price": 85.00,
            "capacity": 1500,
            "category": "Networking"
        },
        {
            "name": "Startup Networking Event",
            "description": "Connect with entrepreneurs, investors, and industry experts at this premier networking event. Perfect for startups looking for funding, partnerships, or mentorship opportunities.",
            "venue": "Business Innovation Hub",
            "date": timezone.now() + datetime.timedelta(days=7),
            "price": 49.99,
            "capacity": 300,
            "category": "Business"
        },
        {
            "name": "Jazz Night",
            "description": "An evening of smooth jazz music featuring local and international jazz musicians. Enjoy the sophisticated atmosphere with fine dining options available.",
            "venue": "Blue Note Club",
            "date": timezone.now() + datetime.timedelta(days=14),
            "price": 35.00,
            "capacity": 200,
            "category": "Music"
        },
        {
            "name": "AI and Machine Learning Workshop",
            "description": "Hands-on workshop introducing the fundamentals of artificial intelligence and machine learning. Participants will learn to build and train basic models using popular frameworks.",
            "venue": "Digital Innovation Lab",
            "date": timezone.now() + datetime.timedelta(days=21),
            "price": 149.99,
            "capacity": 50,
            "category": "Technology"
        },
        {
            "name": "Basketball Tournament",
            "description": "Annual basketball tournament featuring amateur teams from across the region competing for the championship title and prizes.",
            "venue": "Sports Arena",
            "date": timezone.now() + datetime.timedelta(days=40),
            "price": 15.00,
            "capacity": 1000,
            "category": "Sports"
        }
    ]
    
    for event_data in events:
        try:
            # Get the category
            category = next((c for c in created_categories if c.name == event_data["category"]), None)
            if not category:
                print(f"Category {event_data['category']} not found, skipping event {event_data['name']}")
                continue
            
            # Check if event already exists
            if Event.objects.filter(name=event_data["name"]).exists():
                print(f"Event already exists: {event_data['name']}")
                continue
            
            # Create event without image first
            event = Event(
                name=event_data["name"],
                description=event_data["description"],
                venue=event_data["venue"],
                category=category,
                date=event_data["date"],
                price=event_data["price"],
                capacity=event_data["capacity"],
                created_by=admin_user,
                is_active=True
            )
            
            # Save to get an id
            event.save()
            
            # Add random tags (1 to 3 tags per event)
            num_tags = random.randint(1, 3)
            selected_tags = random.sample(created_tags, min(num_tags, len(created_tags)))
            event.tags.set(selected_tags)
            
            print(f"Created event: {event.name}")
            
            # Add Arabic translations for demonstration
            event.name_ar = f"عربي: {event.name}"
            event.description_ar = f"وصف عربي: {event.description[:50]}..."
            event.venue_ar = f"مكان عربي: {event.venue}"
            event.save()
            
        except Exception as e:
            print(f"Error creating event {event_data['name']}: {e}")

if __name__ == "__main__":
    create_sample_data()
    print("Sample data creation completed!") 