from modeltranslation.translator import register, TranslationOptions
from .models import Event, Category, Tag

@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'venue')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',) 