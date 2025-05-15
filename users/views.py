from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from rest_framework import viewsets, serializers, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import CustomUser

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'users/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return render(request, 'users/register.html')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'users/register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'users/register.html')
        
        # Create user
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'users/register.html')

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        # Get recent bookings
        recent_bookings = request.user.bookings.all().order_by('-created_at')[:5]
        
        context = {
            'recent_bookings': recent_bookings,
        }
        
        return render(request, 'users/profile.html', context)

class ProfileEditView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return render(request, 'users/profile_edit.html')
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)
        user.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('users:profile')

class PasswordChangeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return render(request, 'users/password_change.html')
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Validate
        if not request.user.check_password(old_password):
            messages.error(request, "Your old password was entered incorrectly")
            return render(request, 'users/password_change.html')
        
        if new_password1 != new_password2:
            messages.error(request, "The two password fields didn't match")
            return render(request, 'users/password_change.html')
        
        # Change password
        request.user.set_password(new_password1)
        request.user.save()
        
        # Update session
        login(request, request.user)
        
        messages.success(request, "Password changed successfully!")
        return redirect('users:profile')

# Custom permission
class IsUserOrAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only the owner or admin can modify
        return obj.id == request.user.id or request.user.role == CustomUser.Role.ADMIN

# API Serializers
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'password', 'role', 'phone_number', 'address')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'role': {'read_only': True}  # Regular users can't set role
        }
    
    def create(self, validated_data):
        # Extract password and create user with it
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # Handle password updates specially
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class AdminUserSerializer(UserSerializer):
    """Serializer for admin users that allows setting the role"""
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields
        extra_kwargs = {k: v for k, v in UserSerializer.Meta.extra_kwargs.items() if k != 'role'}

# API ViewSets
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrAdminOrReadOnly]
    
    def get_serializer_class(self):
        # Use admin serializer if user is admin
        if self.request.user.is_authenticated and self.request.user.role == CustomUser.Role.ADMIN:
            return AdminUserSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            # Allow anyone to register
            return [AllowAny()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # Only the user or admin can access/modify specific user data
            return [IsUserOrAdminOrReadOnly()]
        else:
            # Admin-only for user listing
            return [IsAdminUser()]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Endpoint to get current user's data"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Endpoint for user registration"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Endpoint to change password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {'error': 'Both old_password and new_password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Old password is incorrect'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        return Response({'success': 'Password changed successfully'})
