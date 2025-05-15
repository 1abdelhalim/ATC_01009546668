import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

def create_basic_arabic_translations():
    """Create a basic Arabic translation file with essential translations."""
    
    translations = {
        # Basic site elements
        "Home": "الرئيسية",
        "Events": "الفعاليات",
        "My Bookings": "حجوزاتي",
        "Login": "تسجيل الدخول",
        "Register": "تسجيل",
        "Logout": "تسجيل الخروج",
        "Profile": "الملف الشخصي",
        "Admin Dashboard": "لوحة التحكم",
        "Account": "الحساب",
        
        # Event details
        "About This Event": "عن هذه الفعالية",
        "Date": "التاريخ",
        "Time": "الوقت",
        "Location": "الموقع",
        "Price": "السعر",
        "Book Now": "احجز الآن",
        "Booked": "تم الحجز",
        "Available": "متوفر",
        "Sold Out": "نفدت التذاكر",
        "Organizer": "المنظم",
        "View Profile": "عرض الملف الشخصي",
        "Share": "مشاركة",
        "Save": "حفظ",
        "per person": "للشخص",
        "Book Tickets": "حجز التذاكر",
        
        # Booking related
        "Booking Details": "تفاصيل الحجز",
        "Booking Reference": "رقم الحجز",
        "Booking Date": "تاريخ الحجز",
        "Total Amount": "المبلغ الإجمالي",
        "Cancel Booking": "إلغاء الحجز",
        "View Details": "عرض التفاصيل",
        
        # Authentication
        "Username": "اسم المستخدم",
        "Password": "كلمة المرور",
        "Email": "البريد الإلكتروني",
        "Sign In": "تسجيل الدخول",
        "Sign Up": "إنشاء حساب",
        "Welcome Back": "مرحباً بعودتك",
        "Remember me": "تذكرني",
        "Forgot Password?": "نسيت كلمة المرور؟",
        "Don't have an account?": "ليس لديك حساب؟",
        
        # Navigation
        "Previous": "السابق",
        "Next": "التالي",
        
        # Languages
        "English": "الإنجليزية",
        "Arabic": "العربية",
        "Toggle Dark/Light Mode": "تبديل الوضع المظلم/الفاتح",
        
        # Footer
        "Event Booking": "حجز الفعاليات",
        "Quick Links": "روابط سريعة",
        "Support": "الدعم",
        "Stay Updated": "ابق على اطلاع",
        "Subscribe": "اشترك",
        "Your email": "بريدك الإلكتروني",
        "About Us": "من نحن",
        "Contact": "اتصل بنا",
        "Help Center": "مركز المساعدة",
        "FAQ": "الأسئلة الشائعة",
        "Privacy Policy": "سياسة الخصوصية",
        "Terms of Service": "شروط الخدمة",
        "Subscribe to our newsletter for the latest events and offers.": "اشترك في نشرتنا الإخبارية للحصول على أحدث الفعاليات والعروض.",
        "Event Booking System. All rights reserved.": "نظام حجز الفعاليات. جميع الحقوق محفوظة.",
        
        # Messages
        "Welcome": "مرحباً",
        "Food and beverages will be available for purchase. No outside food allowed.": "الطعام والمشروبات متوفرة للشراء. غير مسموح بإدخال طعام من الخارج.",
        "Discover and book amazing events in your area. Never miss out on what matters most to you.": "اكتشف واحجز فعاليات مذهلة في منطقتك. لا تفوت ما يهمك.",
        
        # Home page
        "Find Your Next Experience": "ابحث عن تجربتك القادمة",
        "Discover": "استكشف",
        "Amazing Events": "فعاليات رائعة",
        "Near You": "بالقرب منك",
        "Find and book the most exciting events in your area. From concerts to workshops, we've got you covered.": "ابحث واحجز أكثر الفعاليات إثارة في منطقتك. من الحفلات الموسيقية إلى ورش العمل، لدينا كل ما تحتاجه.",
        "Browse Events": "تصفح الفعاليات",
        "Search events...": "البحث عن فعاليات...",
        "Search events": "البحث عن فعاليات",
        "Search": "بحث",
        "Events Monthly": "فعالية شهرياً",
        "Happy Users": "مستخدم سعيد",
        "Categories": "فئات",
        "Satisfaction Rate": "معدل الرضا",
        "Browse by Category": "تصفح حسب الفئة",
        "Find events that match your interests": "ابحث عن فعاليات تناسب اهتماماتك",
        "Concerts": "حفلات موسيقية",
        "Workshops": "ورش عمل",
        "Food & Drinks": "طعام ومشروبات",
        "Entertainment": "ترفيه",
        "Upcoming Events": "الفعاليات القادمة",
        "View All": "عرض الكل",
        "Don't miss out on these exciting events happening soon": "لا تفوت هذه الفعاليات المثيرة القادمة قريباً",
        "Category": "الفئة",
        "May": "مايو",
        "going": "متوجه",
        "Event Title": "عنوان الفعالية",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris.": "يمكنك الآن حجز الفعاليات بسهولة من خلال منصتنا.",
        "Event Location": "موقع الفعالية",
        "What Our Users Say": "ماذا يقول مستخدمينا",
        "Discover why people love our platform": "اكتشف لماذا يحب الناس منصتنا",
        "\"This platform made finding local events so easy! I've discovered amazing concerts I would have missed otherwise.\"": "هذه المنصة جعلت العثور على الفعاليات المحلية سهلاً جداً! لقد اكتشفت حفلات موسيقية رائعة كنت سأفوتها لولا ذلك.",
        "John Doe": "محمد أحمد",
        "Event Enthusiast": "مهتم بالفعاليات",
        "\"As an event organizer, this platform has helped me reach new audiences and manage bookings effortlessly.\"": "كمنظم فعاليات، ساعدتني هذه المنصة في الوصول إلى جماهير جديدة وإدارة الحجوزات بسهولة.",
        "Jane Smith": "سارة خالد",
        "Event Organizer": "منظم فعاليات",
        "\"The booking process is seamless, and I love that I can see all my upcoming events in one place.\"": "عملية الحجز سلسة، وأحب أنني أستطيع رؤية جميع الفعاليات القادمة في مكان واحد.",
        "Robert Johnson": "أحمد محمود",
        "Regular Attendee": "حاضر منتظم",
        "Ready to Experience Amazing Events?": "هل أنت مستعد لتجربة فعاليات مذهلة؟",
        "Your email address": "عنوان بريدك الإلكتروني",
        "Email address": "عنوان البريد الإلكتروني",
        "Subscribe to our newsletter to get the latest updates on events and special offers.": "اشترك في نشرتنا الإخبارية للحصول على آخر التحديثات حول الفعاليات والعروض الخاصة.",
        
        # Event filters and categories
        "Discover Events": "استكشف الفعاليات",
        "Find the perfect event for you": "ابحث عن الفعالية المناسبة لك",
        "Sort By": "ترتيب حسب",
        "Upcoming": "القادمة",
        "Price: Low to High": "السعر: من الأقل إلى الأعلى",
        "Price: High to Low": "السعر: من الأعلى إلى الأقل",
        "Most Popular": "الأكثر شعبية",
        "Filters": "تصفية",
        "Today": "اليوم",
        "Tomorrow": "غداً",
        "This Weekend": "نهاية الأسبوع",
        "This Week": "هذا الأسبوع",
        "This Month": "هذا الشهر",
        "$0 - $50": "0 - 50 دولار",
        "$50 - $100": "50 - 100 دولار",
        "$100+": "أكثر من 100 دولار",
        "Apply Filters": "تطبيق التصفية",
        "tickets available": "تذكرة متاحة",
        "total": "الإجمالي",
        "No events found matching your criteria.": "لم يتم العثور على فعاليات مطابقة لمعاييرك",

        # Additional translations for navbar and base
        "Event": "فعالية",
        "Booking": "حجز",
        "Why Choose Us": "لماذا تختارنا",
        "Booking Events Has Never Been": "حجز الفعاليات لم يكن أبداً",
        "This Easy": "بهذه السهولة",
        "Discover Events": "اكتشف الفعاليات",
        "Easily find events that match your interests with our powerful search and filtering tools.": "اعثر بسهولة على الفعاليات التي تناسب اهتماماتك من خلال أدوات البحث والتصفية القوية لدينا.",
        "Instant Booking": "حجز فوري",
        "Book tickets in seconds without any complicated checkout process.": "احجز التذاكر في ثوانٍ دون أي عملية دفع معقدة.",
        "Event Reminders": "تذكيرات الفعاليات",
        "Get notified about your upcoming events so you never miss out.": "احصل على إشعارات حول الفعاليات القادمة حتى لا تفوتك أبداً.",
        "App Features": "ميزات التطبيق",
        "You Might Also Like": "قد يعجبك أيضاً",
        "Discover similar events happening nearby": "اكتشف فعاليات مماثلة تحدث بالقرب منك",
        "View": "عرض",
        "January": "يناير",
        "February": "فبراير",
        "March": "مارس",
        "April": "أبريل",
        "June": "يونيو",
        "July": "يوليو",
        "August": "أغسطس",
        "September": "سبتمبر",
        "October": "أكتوبر",
        "November": "نوفمبر",
        "December": "ديسمبر"
    }
    
    # Create the output directory if it doesn't exist
    os.makedirs('locale/ar/LC_MESSAGES', exist_ok=True)
    
    # Write the translations to a new .po file
    with open('locale/ar/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write('# Arabic translation file for Event Booking System\n')
        f.write('msgid ""\n')
        f.write('msgstr ""\n')
        f.write('"Project-Id-Version: 1.0\\n"\n')
        f.write('"Report-Msgid-Bugs-To: \\n"\n')
        f.write('"PO-Revision-Date: 2023-05-15\\n"\n')
        f.write('"Last-Translator: AI Assistant\\n"\n')
        f.write('"Language-Team: Arabic\\n"\n')
        f.write('"Language: ar\\n"\n')
        f.write('"MIME-Version: 1.0\\n"\n')
        f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        f.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        f.write('"Plural-Forms: nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5;\\n"\n\n')
        
        # Write the translations
        for english, arabic in translations.items():
            # Escape double quotes in source and translation strings
            english_escaped = english.replace('"', '\\"')
            arabic_escaped = arabic.replace('"', '\\"')
            f.write(f'msgid "{english_escaped}"\n')
            f.write(f'msgstr "{arabic_escaped}"\n\n')
    
    print(f"Created basic Arabic translation file with {len(translations)} translations.")

if __name__ == "__main__":
    create_basic_arabic_translations() 