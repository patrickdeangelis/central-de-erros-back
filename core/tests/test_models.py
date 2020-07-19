from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.models import Agent, Event


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Jose", email="jose@gmail.com", password="xxxxxxxxxxxxxxxxxxxxxxx"
        )
        self.agent = Agent.objects.create(
            address="192.168.1.1",
            env=Agent.Enviroments.DEV,
            version="1.1.1",
            user=self.user,
        )
        self.event = Event.objects.create(
            title="Event",
            level=Event.Levels.CRITICAL,
            description="django.core.exceptions.ValidationError",
            agent=self.agent,
            shelved=False,
        )

    def test_user_exists(self):
        user = User.objects.get(email="jose@gmail.com")
        self.assertEqual(user.username, "Jose")

    def test_agent_exists(self):
        agent = Agent.objects.get(address="192.168.1.1")
        self.assertEqual(agent.version, "1.1.1")

    def test_event_exists(self):
        event = Event.objects.get(level=Event.Levels.CRITICAL)

        self.assertEqual(event.description, "django.core.exceptions.ValidationError")

    def test_should_raise_validation_error_on_invalid_level(self):
        event = Event(
            title="Event",
            level="INVALID_LEVEL",
            description="django.core.exceptions.ValidationError",
            agent=self.agent,
            shelved=False,
        )
        self.assertRaises(ValidationError, event.full_clean)

    def test_user_should_count_number_of_events(self):
        Event.objects.create(
            title="Event",
            level=Event.Levels.CRITICAL,
            description="django.core.exceptions.ValidationError",
            agent=self.agent,
            shelved=False,
        )
        occurences = self.event.number_of_occurrences
        self.assertEqual(occurences, 2)

