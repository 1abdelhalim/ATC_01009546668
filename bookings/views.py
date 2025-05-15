from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from rest_framework import viewsets, serializers, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from events.models import Event
from .models import Booking
from django.utils import timezone

# Template Views
class BookingListView(LoginRequiredMixin, ListView):
    template_name = 'bookings/booking_list.html'
    model = Booking
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

class BookingCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'bookings/booking_create.html'
    
    def get(self, request, event_slug=None):
        event = get_object_or_404(Event, slug=event_slug, is_active=True)
        
        # Check if event is sold out
        if event.is_sold_out:
            messages.error(request, "Sorry, this event is sold out!")
            return redirect('events:detail', slug=event_slug)
        
        # Check if user already has a booking for this event
        if event.bookings.filter(user=request.user).exists():
            messages.info(request, "You have already booked this event!")
            return redirect('bookings:list')
        
        return render(request, 'bookings/booking_create.html', {'event': event})
    
    def post(self, request, event_slug=None):
        event = get_object_or_404(Event, slug=event_slug, is_active=True)
        
        # Check if event is sold out
        if event.is_sold_out:
            messages.error(request, "Sorry, this event is sold out!")
            return redirect('events:detail', slug=event_slug)
        
        # Check if user already has a booking for this event
        if event.bookings.filter(user=request.user).exists():
            messages.info(request, "You have already booked this event!")
            return redirect('bookings:list')
        
        # Get quantity from form data
        quantity = int(request.POST.get('quantity', 1))
        
        # Validate quantity
        if quantity <= 0 or quantity > event.available_tickets:
            messages.error(request, "Invalid ticket quantity!")
            return redirect('bookings:create', event_slug=event_slug)
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            event=event,
            quantity=quantity,
            total_price=event.price * quantity,
            status=Booking.Status.CONFIRMED
        )
        
        messages.success(request, f"Successfully booked {event.name}!")
        return redirect('bookings:confirmation', booking_id=booking.id)

class BookingDetailView(LoginRequiredMixin, DetailView):
    template_name = 'bookings/booking_detail.html'
    model = Booking
    context_object_name = 'booking'
    pk_url_kwarg = 'booking_id'
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingConfirmationView(LoginRequiredMixin, DetailView):
    template_name = 'bookings/booking_confirmation.html'
    model = Booking
    context_object_name = 'booking'
    pk_url_kwarg = 'booking_id'
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingCancelView(LoginRequiredMixin, DetailView):
    template_name = 'bookings/booking_cancel.html'
    model = Booking
    context_object_name = 'booking'
    pk_url_kwarg = 'booking_id'
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.status = Booking.Status.CANCELLED
        booking.save()
        
        messages.success(request, "Booking cancelled successfully!")
        return redirect('bookings:list')

class AdminBookingListView(LoginRequiredMixin, ListView):
    template_name = 'bookings/admin_booking_list.html'
    model = Booking
    context_object_name = 'bookings'
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Booking.objects.all().order_by('-created_at')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by event
        event_id = self.request.GET.get('event')
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        
        # Filter by user
        user_id = self.request.GET.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        context['statuses'] = Booking.Status.choices
        return context

class AdminBookingDetailView(LoginRequiredMixin, DetailView):
    template_name = 'bookings/admin_booking_detail.html'
    model = Booking
    context_object_name = 'booking'
    pk_url_kwarg = 'booking_id'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class AdminBookingUpdateView(LoginRequiredMixin, DetailView):
    template_name = 'bookings/admin_booking_update.html'
    model = Booking
    context_object_name = 'booking'
    pk_url_kwarg = 'booking_id'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = request.POST.get('status', booking.status)
        booking.quantity = int(request.POST.get('quantity', booking.quantity))
        booking.total_price = booking.event.price * booking.quantity
        booking.save()
        
        messages.success(request, "Booking updated successfully!")
        return redirect('bookings:admin_detail', booking_id=booking.id)

# Custom Permissions
class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a booking or admins to see/edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.role == 'ADMIN':
            return True
        
        # Only the booking owner can view or modify the booking
        return obj.user == request.user

# API Classes
class BookingSerializer(serializers.ModelSerializer):
    event_name = serializers.SerializerMethodField()
    event_date = serializers.SerializerMethodField()
    event_venue = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_reference', 'created_at', 'updated_at', 'user']
    
    def get_event_name(self, obj):
        return obj.event.name
    
    def get_event_date(self, obj):
        return obj.event.date
    
    def get_event_venue(self, obj):
        return obj.event.venue
    
    def get_username(self, obj):
        return obj.user.username
    
    def validate(self, attrs):
        # Get user from context
        user = self.context['request'].user
        
        # Check if event is active
        event = attrs.get('event')
        if event and not event.is_active:
            raise serializers.ValidationError({"event": "This event is not available for booking"})
        
        # Check if event is sold out
        if event and event.is_sold_out:
            raise serializers.ValidationError({"event": "This event is sold out"})
        
        # Check if user already has a booking for this event
        if self.instance is None and event and event.bookings.filter(user=user).exists():
            raise serializers.ValidationError({"event": "You have already booked this event"})
        
        # Validate quantity
        quantity = attrs.get('quantity', 1)
        if quantity <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be a positive integer"})
        
        # Validate available capacity
        if event and quantity > event.available_tickets:
            raise serializers.ValidationError(
                {"quantity": f"Only {event.available_tickets} tickets available"}
            )
        
        # Set total price
        if event:
            attrs['total_price'] = event.price * quantity
        
        return attrs

class BookingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    pagination_class = BookingPagination
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = Booking.objects.all()  # Add default queryset
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin can see all bookings
        if user.role == 'ADMIN':
            queryset = Booking.objects.all()
            
            # Filter by status
            status = self.request.query_params.get('status')
            if status:
                queryset = queryset.filter(status=status)
            
            # Filter by event
            event_id = self.request.query_params.get('event')
            if event_id:
                queryset = queryset.filter(event_id=event_id)
            
            # Filter by user
            user_id = self.request.query_params.get('user')
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            # Regular users can only see their own bookings
            queryset = Booking.objects.filter(user=user)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        # Validate booking can be cancelled
        if booking.status == Booking.Status.CANCELLED:
            return Response(
                {"error": "Booking is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancel booking
        booking.status = Booking.Status.CANCELLED
        booking.save()
        
        return Response({"status": "Booking cancelled successfully"})
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get user's upcoming bookings"""
        # Get confirmed bookings for future events
        user = request.user
        queryset = Booking.objects.filter(
            user=user,
            status=Booking.Status.CONFIRMED,
            event__date__gt=timezone.now()
        ).order_by('event__date')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get user's past bookings"""
        # Get bookings for past events
        user = request.user
        queryset = Booking.objects.filter(
            user=user,
            event__date__lte=timezone.now()
        ).order_by('-event__date')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
