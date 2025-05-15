from django.contrib import admin
from .models import Event, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'venue', 'price', 'capacity', 'is_active', 'created_by')
    list_filter = ('category', 'is_active', 'date')
    search_fields = ('name', 'description', 'venue')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    filter_horizontal = ('tags',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'category', 'tags')
        }),
        ('Event Details', {
            'fields': ('date', 'venue', 'price', 'capacity', 'image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
