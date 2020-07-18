from django.test import TestCase


from django.core.exceptions import ValidationError
from .models import Agent, Event
from django.contrib.auth.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Jose", email="jose@gmail.com", password="xxxxxxxxxxxxxxxxxxxxxxx"
        )
        self.agent = Agent.objects.create(
            name="Machine1",
            address="192.168.1.1",
            status=True,
            env=Agent.Enviroments.DEV,
            version="1.1.1",
        )
        Event.objects.create(
            level=Event.Levels.CRITICAL,
            data="django.core.exceptions.ValidationError",
            agent=self.agent,
            shelved=False,
        )

    def test_user_exists(self):
        user = User.objects.get(email="jose@gmail.com")
        self.assertEqual(user.username, "Jose")

    def test_agent_exists(self):
        agent = Agent.objects.get(name="Machine1")
        self.assertEqual(agent.name, "Machine1")

    def test_event_exists(self):
        event = Event.objects.get(level=Event.Levels.CRITICAL)

        self.assertEqual(event.data, "django.core.exceptions.ValidationError")

    def test_should_raise_validation_error_on_invalid_level(self):
        event = Event(
            level="INVALID_LEVEL",
            data="django.core.exceptions.ValidationError",
            agent=self.agent,
            shelved=False,
        )
        self.assertRaises(ValidationError, event.full_clean)

