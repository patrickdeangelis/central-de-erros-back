from django.test import TestCase
from core.api.serializers import EventInputSerializer


class TestEventInputSerializer(TestCase):
    def test_validating_correct_data(self):
        valid_data = {
            "env": "DEV",
            "version": "1.1.1",
            "title": "Error teste",
            "description": "Error description",
            "level": "DEBUG",
        }
        serializer = EventInputSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_fail_on_invalid_env(self):
        invalid_data = {
            "env": "invalid_env",
            "version": "1.1.1",
            "title": "Error teste",
            "description": "Error description",
            "level": "DEBUG",
        }
        serializer = EventInputSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_fail_on_invalid_level(self):
        invalid_data = {
            "env": "DEV",
            "version": "1.1.1",
            "title": "Error teste",
            "description": "Error description",
            "level": "invalid_level",
        }
        serializer = EventInputSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
