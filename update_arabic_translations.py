import os
import django
import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from events.models import Event, Category, Tag

def update_arabic_translations():
    """Update the Arabic translations for existing events with proper translations."""
    
    # Arabic translations for categories
    category_translations = {
        "Music": "الموسيقى",
        "Technology": "التكنولوجيا",
        "Sports": "الرياضة",
        "Networking": "التواصل الشبكي",
        "Business": "الأعمال",
    }
    
    # Arabic translations for events
    event_translations = {
        "Summer Music Festival": {
            "name": "مهرجان الصيف الموسيقي",
            "description": "انضم إلينا لقضاء عطلة نهاية أسبوع من العروض الموسيقية المذهلة التي تضم فنانين بارزين من جميع أنحاء العالم. هذا المهرجان السنوي هو أبرز أحداث موسم الصيف مع مسارح متعددة وبائعي طعام وأنشطة لجميع الأعمار.",
            "venue": "الحديقة المركزية"
        },
        "Web Development Conference": {
            "name": "مؤتمر تطوير الويب",
            "description": "مؤتمر لمدة يومين يركز على أحدث الاتجاهات والتقنيات في تطوير الويب. تشمل الجلسات أطر عمل الواجهة الأمامية، وتحسين الخلفية، وأفضل ممارسات الأمان، وورش عمل عملية.",
            "venue": "مركز المؤتمرات التقنية"
        },
        "Marathon Championships": {
            "name": "بطولات الماراثون",
            "description": "يجمع ماراثون المدينة السنوي العدائين المحترفين والهواة من جميع أنحاء البلاد. يتضمن فئات سباق متعددة بما في ذلك الماراثون الكامل ونصف الماراثون وجري 10 كم.",
            "venue": "مسارات وسط المدينة"
        },
        "Professional Networking Summit": {
            "name": "قمة التواصل المهني",
            "description": "تواصل مع المحترفين من مختلف الصناعات في هذا الحدث الرئيسي للتواصل. وسّع شبكة علاقاتك، واكتشف فرصًا جديدة، وشارك في جلسات التواصل الموجهة مع قادة الصناعة.",
            "venue": "مركز المؤتمرات على الواجهة البحرية"
        },
        "Startup Networking Event": {
            "name": "حدث التواصل للشركات الناشئة",
            "description": "تواصل مع رجال الأعمال والمستثمرين وخبراء الصناعة في هذا الحدث الرئيسي للتواصل. مثالي للشركات الناشئة التي تبحث عن تمويل أو شراكات أو فرص إرشاد.",
            "venue": "مركز ابتكار الأعمال"
        },
        "Jazz Night": {
            "name": "ليلة الجاز",
            "description": "أمسية من موسيقى الجاز الهادئة تضم موسيقيين محليين ودوليين. استمتع بالأجواء الراقية مع توفر خيارات تناول الطعام الفاخر.",
            "venue": "نادي النوتة الزرقاء"
        },
        "AI and Machine Learning Workshop": {
            "name": "ورشة الذكاء الاصطناعي والتعلم الآلي",
            "description": "ورشة عمل عملية تقدم أساسيات الذكاء الاصطناعي والتعلم الآلي. سيتعلم المشاركون بناء وتدريب النماذج الأساسية باستخدام أطر العمل الشائعة.",
            "venue": "مختبر الابتكار الرقمي"
        },
        "Basketball Tournament": {
            "name": "بطولة كرة السلة",
            "description": "بطولة كرة السلة السنوية التي تضم فرقًا من الهواة من جميع أنحاء المنطقة تتنافس على لقب البطولة والجوائز.",
            "venue": "ساحة الرياضة"
        }
    }

    # Update category translations
    for english_name, arabic_name in category_translations.items():
        try:
            categories = Category.objects.filter(name=english_name)
            for category in categories:
                category.name_ar = arabic_name
                category.save()
                print(f"Updated category: {english_name} -> {arabic_name}")
        except Exception as e:
            print(f"Error updating category {english_name}: {e}")

    # Update tag translations
    tag_translations = {
        "Featured": "مميز",
        "Free": "مجاني",
        "Outdoors": "في الهواء الطلق",
        "Virtual": "افتراضي",
        "Premium": "مميز",
        "Family-friendly": "مناسب للعائلات",
        "Workshop": "ورشة عمل",
        "Conference": "مؤتمر"
    }
    
    for english_name, arabic_name in tag_translations.items():
        try:
            tags = Tag.objects.filter(name=english_name)
            for tag in tags:
                tag.name_ar = arabic_name
                tag.save()
                print(f"Updated tag: {english_name} -> {arabic_name}")
        except Exception as e:
            print(f"Error updating tag {english_name}: {e}")

    # Update event translations
    for event in Event.objects.all():
        try:
            if event.name in event_translations:
                translation = event_translations[event.name]
                event.name_ar = translation["name"]
                event.description_ar = translation["description"]
                event.venue_ar = translation["venue"]
                event.save()
                print(f"Updated event: {event.name} -> {event.name_ar}")
            else:
                print(f"No translation found for event: {event.name}")
        except Exception as e:
            print(f"Error updating event {event.name}: {e}")
            
    print("Arabic translations update completed!")

if __name__ == "__main__":
    update_arabic_translations() 