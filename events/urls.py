from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('category/<slug:slug>/', views.CategoryEventListView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagEventListView.as_view(), name='tag'),
    path('<slug:slug>/', views.EventDetailView.as_view(), name='detail'),
    
    # Admin URLs
    path('admin/create/', views.EventCreateView.as_view(), name='create'),
    path('admin/<slug:slug>/edit/', views.EventUpdateView.as_view(), name='update'),
    path('admin/<slug:slug>/delete/', views.EventDeleteView.as_view(), name='delete'),
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
] 