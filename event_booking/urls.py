"""
URL configuration for event_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from . import views
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, JsonResponse
import traceback
import sys

# Azure health check endpoint
def health_check(request):
    return HttpResponse("OK", status=200)

# Custom error handlers
def handler500(request, *args, **kwargs):
    """Custom 500 error handler that returns error details in DEBUG mode"""
    type_, value, tb = sys.exc_info()
    error_info = {
        'error_type': str(type_.__name__),
        'error_value': str(value),
        'traceback': traceback.format_exception(type_, value, tb)
    }
    return JsonResponse(error_info, status=500)

# Non-localized URLs
urlpatterns = [
    path('robots933456.txt', health_check, name='azure_health_check'),  # Azure health check endpoint
    path('health/', health_check, name='health_check'),  # Generic health check
    path('diagnostic/', views.diagnostic, name='diagnostic'),  # Diagnostic endpoint for troubleshooting
    path('i18n/', include('django.conf.urls.i18n')),  # For language switching
    path('api/', include('core.api_urls')),  # API endpoints don't need localization
    path('__reload__/', include('django_browser_reload.urls')),
]

# Localized URLs
urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('bookings/', include('bookings.urls')),
    prefix_default_language=True,  # Add prefix for default language too
)

# Add non-namespaced password reset URLs for Django's built-in views
urlpatterns += [
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html', subject_template_name='registration/password_reset_subject.txt'), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Make handler500 accessible at module level so it can be properly imported
handler500 = handler500  # This registers the existing handler500 function at module level
