from django.shortcuts import render
from django.utils.translation import activate
from events.models import Event
from django.utils import timezone

def home(request):
    # Get current language from request
    current_language = request.LANGUAGE_CODE
    
    # Set the language explicitly in case the translation system fails
    activate(current_language)
    
    # Get featured events (upcoming events)
    featured_events = Event.objects.filter(
        is_active=True,
        date__gte=timezone.now()
    ).order_by('date')[:6]  # Get next 6 upcoming events
    
    # Prepare Arabic translations for important elements if in Arabic mode
    arabic_translations = {
        'Home': 'الرئيسية',
        'Events': 'الفعاليات',
        'My Bookings': 'حجوزاتي',
        'Login': 'تسجيل الدخول',
        'Register': 'التسجيل',
        'Account': 'الحساب',
        'Profile': 'الملف الشخصي',
        'Logout': 'تسجيل الخروج',
        'Welcome': 'مرحباً',
        'Browse Events': 'تصفح الفعاليات',
        'Book Now': 'احجز الآن',
        'Search events...': 'البحث عن الفعاليات...',
        'Search': 'بحث',
        'Sign Up': 'التسجيل',
    }
    
    context = {
        'is_arabic': current_language == 'ar',
        'arabic_translations': arabic_translations,
        'featured_events': featured_events
    }
    
    return render(request, 'base/home.html', context) 