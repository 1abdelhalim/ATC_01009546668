from django.test import TestCase
from django.urls import reverse
from .models import Event, Category
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

# Create your tests here.

class EventTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Tech')
        self.event = Event.objects.create(
            name='Test Event',
            description='A test event.',
            category=self.category,
            date=datetime.now() + timedelta(days=1),
            venue='Test Venue',
            price=100.0,
        )

    def test_event_list_view(self):
        response = self.client.get(reverse('events:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_event_detail_view(self):
        response = self.client.get(reverse('events:detail', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')
        self.assertContains(response, 'A test event.')

    def test_event_creation(self):
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.name, 'Test Event')
