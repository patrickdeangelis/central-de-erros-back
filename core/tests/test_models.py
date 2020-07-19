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
            address="192.168.1.1", env=Agent.Enviroments.DEV, version="1.1.1",
        )
        Event.objects.create(
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


# class TestAPI(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(
#             username="Jose", email="jose@gmail.com", password="xxxxxxxxxxxxxxxxxxxxxxx"
#         )
#         self.agent = Agent.objects.create(
#             address="192.168.1.1", env=Agent.Enviroments.DEV, version="1.1.1",
#         )
#         self.event = Event.objects.create(
#             title="Error",
#             level=Event.Levels.DEBUG,
#             description="django.core.exceptions.ValidationError",
#             agent=self.agent,
#             shelved=False,
#         )

#     def test_get_events(self):
#         factory = APIRequestFactory()
#         request = self.client.get("/events/")
#         print(json.loads(request.data))
#         print(self.event.date)
#         self.assertEqual(
#             json.loads(request.data),
#             {
#                 "id": 1,
#                 "title": "Error",
#                 "description": "django.core.exceptions.ValidationError",
#                 "level": "DEBUG",
#                 "shelved": False,
#                 "date": "2020-07-18T20:28:23.749791Z",
#                 "agent": 1,
#             },
#         )
