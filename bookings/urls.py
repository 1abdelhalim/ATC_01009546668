from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='list'),
    path('create/<slug:event_slug>/', views.BookingCreateView.as_view(), name='create'),
    path('<int:booking_id>/', views.BookingDetailView.as_view(), name='detail'),
    path('<int:booking_id>/confirmation/', views.BookingConfirmationView.as_view(), name='confirmation'),
    path('<int:booking_id>/cancel/', views.BookingCancelView.as_view(), name='cancel'),
    
    # Admin URLs
    path('admin/', views.AdminBookingListView.as_view(), name='admin_list'),
    path('admin/<int:booking_id>/', views.AdminBookingDetailView.as_view(), name='admin_detail'),
    path('admin/<int:booking_id>/update/', views.AdminBookingUpdateView.as_view(), name='admin_update'),
] 