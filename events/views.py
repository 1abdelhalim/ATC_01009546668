from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from rest_framework import viewsets, serializers, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Category, Tag
from django.utils import timezone
import datetime
from django.db.models import Count

# Create your views here.

# Template Views
class EventListView(ListView):
    template_name = 'events/event_list.html'
    model = Event
    context_object_name = 'events'
    paginate_by = 9
    
    def dispatch(self, request, *args, **kwargs):
        # Initialize language support
        current_language = request.LANGUAGE_CODE
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True).order_by('date')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(venue__icontains=search_query)
            )
        
        # Date filter
        date_filter = self.request.GET.get('date_filter', '')
        today = timezone.now().date()
        if date_filter == 'today':
            queryset = queryset.filter(date__date=today)
        elif date_filter == 'tomorrow':
            tomorrow = today + datetime.timedelta(days=1)
            queryset = queryset.filter(date__date=tomorrow)
        elif date_filter == 'weekend':
            # Find the next Saturday and Sunday
            days_until_saturday = (5 - today.weekday()) % 7
            saturday = today + datetime.timedelta(days=days_until_saturday)
            sunday = saturday + datetime.timedelta(days=1)
            queryset = queryset.filter(date__date__range=[saturday, sunday])
        elif date_filter == 'week':
            # Find the end of the current week (next Sunday)
            days_until_sunday = (6 - today.weekday()) % 7
            end_of_week = today + datetime.timedelta(days=days_until_sunday)
            queryset = queryset.filter(date__date__range=[today, end_of_week])
        elif date_filter == 'month':
            # Find the last day of the current month
            next_month = today.replace(day=28) + datetime.timedelta(days=4)
            end_of_month = next_month - datetime.timedelta(days=next_month.day)
            queryset = queryset.filter(date__date__range=[today, end_of_month])
        
        # Category filter
        category_slugs = self.request.GET.get('category', '').split(',')
        if category_slugs and category_slugs[0]:
            queryset = queryset.filter(category__slug__in=category_slugs)
        
        # Price filter
        price_ranges = self.request.GET.get('price', '').split(',')
        if price_ranges and price_ranges[0]:
            price_q = Q()
            for price_range in price_ranges:
                if price_range == 'free':
                    price_q |= Q(price=0)
                elif price_range == '0-50':
                    price_q |= Q(price__gt=0, price__lte=50)
                elif price_range == '50-100':
                    price_q |= Q(price__gt=50, price__lte=100)
                elif price_range == '100-':
                    price_q |= Q(price__gt=100)
            queryset = queryset.filter(price_q)
        
        # Sort functionality
        sort = self.request.GET.get('sort', '')
        if sort == 'date':
            queryset = queryset.order_by('date')
        elif sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'popularity':
            # Sort by number of bookings (most popular first)
            queryset = queryset.annotate(booking_count=Count('bookings')).order_by('-booking_count')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        
        # Add language-specific content
        context['is_arabic'] = self.request.LANGUAGE_CODE == 'ar'
        
        # Set is_booked_by_user flag for each event
        if self.request.user.is_authenticated:
            for event in context['events']:
                event.is_booked_by_user = event.is_booked_by_user(self.request.user)
                
        return context

class EventDetailView(DetailView):
    template_name = 'events/event_detail.html'
    model = Event
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if user has booked this event
        if self.request.user.is_authenticated:
            event = self.object
            event.is_booked_by_user = event.is_booked_by_user(self.request.user)
        
        # Get similar events
        event = self.object
        similar_events = Event.objects.filter(
            Q(category=event.category) | Q(tags__in=event.tags.all())
        ).exclude(id=event.id).distinct()[:3]
        
        # Check if user has booked any of the similar events
        if self.request.user.is_authenticated:
            for similar_event in similar_events:
                similar_event.is_booked_by_user = similar_event.is_booked_by_user(self.request.user)
        
        context['similar_events'] = similar_events
        return context

class CategoryEventListView(ListView):
    template_name = 'events/category_event_list.html'
    model = Event
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        return Event.objects.filter(
            category__slug=self.kwargs.get('slug'),
            is_active=True
        ).order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return context

class TagEventListView(ListView):
    template_name = 'events/tag_event_list.html'
    model = Event
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        return Event.objects.filter(
            tags__slug=self.kwargs.get('slug'),
            is_active=True
        ).order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return context

class EventCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'events/event_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class EventUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'events/event_update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, slug=self.kwargs.get('slug'))
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        
        # Check if user can edit this event
        if not self.request.user.role == 'ADMIN' and context['event'].created_by != self.request.user:
            context['error'] = "You don't have permission to edit this event"
        
        return context

class EventDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'events/event_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, slug=self.kwargs.get('slug'))
        
        # Check if user can delete this event
        if not self.request.user.role == 'ADMIN' and context['event'].created_by != self.request.user:
            context['error'] = "You don't have permission to delete this event"
        
        return context

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'events/admin_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 'ADMIN':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all().order_by('-created_at')
        context['total_events'] = Event.objects.count()
        context['active_events'] = Event.objects.filter(is_active=True).count()
        return context

# Custom Permissions
class IsAdminOrCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of an event or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the creator or admin
        return obj.created_by == request.user or request.user.role == 'ADMIN'

# API Classes
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    available_tickets = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'slug']
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_tags_list(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def get_available_tickets(self, obj):
        return obj.available_tickets
    
    def validate(self, attrs):
        # Ensure capacity is positive
        if attrs.get('capacity', 0) <= 0:
            raise serializers.ValidationError({"capacity": "Capacity must be a positive integer"})
        
        # Ensure price is non-negative
        if attrs.get('price', 0) < 0:
            raise serializers.ValidationError({"price": "Price cannot be negative"})
        
        return attrs

class EventPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 48

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    pagination_class = EventPagination
    permission_classes = [IsAdminOrCreatorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active', 'date']
    search_fields = ['name', 'description', 'venue', 'category__name', 'tags__name']
    ordering_fields = ['name', 'date', 'price', 'created_at']
    lookup_field = 'slug'
    queryset = Event.objects.all()  # Add default queryset at class level
    
    def get_queryset(self):
        # By default, show only active events
        queryset = Event.objects.all()
        
        # Add filter for active events
        is_active = self.request.query_params.get('is_active')
        if is_active is None:
            queryset = queryset.filter(is_active=True)
        elif is_active.lower() == 'true':
            queryset = queryset.filter(is_active=True)
        elif is_active.lower() == 'false':
            queryset = queryset.filter(is_active=False)
        
        # Filter by tag
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(price__lte=float(max_price))
        
        return queryset.distinct()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def similar(self, request, slug=None):
        """Get similar events based on category and tags"""
        event = self.get_object()
        similar_events = Event.objects.filter(
            Q(category=event.category) | Q(tags__in=event.tags.all())
        ).exclude(id=event.id).distinct()[:4]
        
        page = self.paginate_queryset(similar_events)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(similar_events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all categories"""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def tags(self, request):
        """Get all tags"""
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def check_availability(self, request, slug=None):
        """Check event availability"""
        event = self.get_object()
        available = event.available_tickets
        sold_out = event.is_sold_out
        
        return Response({
            'available_tickets': available,
            'sold_out': sold_out,
            'capacity': event.capacity,
            'bookings_count': event.bookings.count()
        })
