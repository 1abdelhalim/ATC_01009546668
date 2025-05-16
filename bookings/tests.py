from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from events.models import Event, Category
from .models import Booking
from datetime import datetime, timedelta

class BookingTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='booker',
            email='booker@example.com',
            password='testpass123',
        )
        self.category = Category.objects.create(name='Music')
        self.event = Event.objects.create(
            name='Concert',
            description='Live concert.',
            category=self.category,
            date=datetime.now() + timedelta(days=2),
            venue='Concert Hall',
            price=50.0,
        )

    def test_booking_creation(self):
        self.client.login(username='booker', password='testpass123')
        booking = Booking.objects.create(user=self.user, event=self.event, tickets=1)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking.event, self.event)
        self.assertEqual(booking.user, self.user)

    def test_prevent_double_booking(self):
        Booking.objects.create(user=self.user, event=self.event, tickets=1)
        with self.assertRaises(Exception):
            Booking.objects.create(user=self.user, event=self.event, tickets=1)

    def test_booking_list_view(self):
        Booking.objects.create(user=self.user, event=self.event, tickets=1)
        self.client.login(username='booker', password='testpass123')
        response = self.client.get(reverse('bookings:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Concert')
