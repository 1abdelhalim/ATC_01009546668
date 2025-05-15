from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from events.views import EventViewSet
from bookings.views import BookingViewSet
from users.views import UserViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'users', UserViewSet)

# Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Event Booking API",
        default_version='v1',
        description="API documentation for the Event Booking System",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # API authentication
    path('auth/', include('rest_framework.urls')),
    
    # API documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] 