from django.db import models
from django.conf import settings
from events.models import Event

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    booking_reference = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.name} ({self.booking_reference})"
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate a unique booking reference
            import uuid
            self.booking_reference = str(uuid.uuid4())[:8].upper()
        
        if not self.total_price:
            self.total_price = self.event.price * self.quantity
        
        super().save(*args, **kwargs)
    
    @property
    def is_cancelled(self):
        return self.status == self.Status.CANCELLED
    
    @property
    def is_confirmed(self):
        return self.status == self.Status.CONFIRMED
    
    @classmethod
    def is_event_booked_by_user(cls, event, user):
        """Check if a specific user has booked this event"""
        if not user.is_authenticated:
            return False
        return cls.objects.filter(event=event, user=user).exists()