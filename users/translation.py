from modeltranslation.translator import register, TranslationOptions
from .models import CustomUser

@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    fields = ('address',) 