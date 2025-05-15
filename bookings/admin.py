from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'event', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('booking_reference', 'user__username', 'event__name')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('booking_reference', 'user', 'event')
        }),
        ('Booking Details', {
            'fields': ('quantity', 'total_price', 'status')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Disable direct adding in admin to enforce business rules
        return False
