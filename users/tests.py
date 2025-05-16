from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class UserAuthTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
        )

    def test_register_view(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(self.user_model.objects.filter(username='newuser').exists())

    def test_login_view(self):
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

    def test_user_permissions(self):
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
