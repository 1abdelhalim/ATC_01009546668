from django.shortcuts import render, redirect
from django.utils.translation import activate
from events.models import Event
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db import connection
import sys
import os
import django

def home(request):
    """
    Home page view that shows featured events
    """
    # If user is authenticated, check their preferred language
    if request.user.is_authenticated and hasattr(request.user, 'preferred_language') and request.user.preferred_language:
        activate(request.user.preferred_language)
    
    # Get 6 upcoming events
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now(),
        is_active=True
    ).order_by('date')[:6]
    
    # Get 3 featured events (most popular)
    featured_events = Event.objects.filter(
        is_active=True
    ).order_by('-created_at')[:3]
    
    context = {
        'upcoming_events': upcoming_events,
        'featured_events': featured_events,
    }
    
    return render(request, 'base/home.html', context)

# Diagnostic view to help troubleshoot Azure deployment issues
def diagnostic(request):
    """Return system and database diagnostic information"""
    
    # Basic system info
    info = {
        'python_version': sys.version,
        'django_version': django.__version__,
        'debug_mode': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'static_root': str(settings.STATIC_ROOT),
        'media_root': str(settings.MEDIA_ROOT),
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_response = cursor.fetchone()[0]
        info['database_connection'] = 'OK' if db_response == 1 else f'Error: {db_response}'
    except Exception as e:
        info['database_connection'] = f'Error: {str(e)}'
    
    # Check environment variables
    info['environment_variables'] = {
        'DATABASE_URL': os.environ.get('DATABASE_URL', 'Not set'),
        'DEBUG': os.environ.get('DEBUG', 'Not set'),
        'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS', 'Not set'),
    }
    
    # Check installed apps
    info['installed_apps'] = settings.INSTALLED_APPS
    
    return JsonResponse(info) 