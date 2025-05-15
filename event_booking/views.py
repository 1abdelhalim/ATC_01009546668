from django.shortcuts import render
from django.utils.translation import activate

def home(request):
    # Get current language from request
    current_language = request.LANGUAGE_CODE
    
    # Set the language explicitly in case the translation system fails
    activate(current_language)
    
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
        'arabic_translations': arabic_translations
    }
    
    return render(request, 'home.html', context) 