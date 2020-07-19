from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Event, Agent
from django.contrib.auth import get_user_model


User = get_user_model()


class TestAPI(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "Error",
            "description": "Null pointer exception",
            "level": "DEBUG",
            "env": "DEV",
            "version": "v1.0",
            "shelved": False,
        }

        self.user = User.objects.create(
            name="joao", email="joao@joao.com", password="any_password"
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

        self.event_2 = Event.objects.create(
            title="Event 2",
            level=Event.Levels.DEBUG,
            description="django.core.exceptions.ValidationError",
            agent=self.agent,
            shelved=False,
        )

    def test_create_event(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/events/", data=self.valid_data, REMOTE_ADDR="127.0.0.1"
        )
        self.assertEqual(request.status_code, 201)

    def test_create_event_obj(self):
        self.client.force_login(self.user)
        request = self.client.post(
            "/events/", data=self.valid_data, REMOTE_ADDR="127.0.0.1"
        )
        event_obj = Event.objects.get(
            title=self.valid_data["title"],
            description=self.valid_data["description"],
            level=Event.Levels[self.valid_data["level"]],
        )

        self.assertIsNotNone(event_obj)
        self.assertEqual(event_obj.title, self.valid_data["title"])

    def test_retrieve_an_event(self):
        request = self.client.get(
            f"/events/{self.event.pk}/", content_type="application/json"
        )
        response_data = request.json()
        self.assertEqual(response_data["id"], self.event.pk)

    def test_retrieve_events(self):
        request = self.client.get("/events/", content_type="application/json")
        response_data = request.json()
        self.assertEqual(response_data[0]["id"], self.event.pk)
        self.assertEqual(response_data[1]["id"], self.event_2.pk)

    def test_update_shelved_property(self):
        request = self.client.patch(
            f"/events/{self.event.pk}/",
            data={"shelved": True},
            content_type="application/json",
        )
        response_data = request.json()
        self.assertTrue(response_data["shelved"])

    def test_update_only_shelved_property(self):
        payload = {"shelved": True, "description": "new descr"}
        request = self.client.patch(
            f"/events/{self.event.pk}/", data=payload, content_type="application/json",
        )
        response_data = request.json()

        self.assertTrue(response_data["shelved"])
        self.assertNotEqual(response_data["description"], payload["description"])

