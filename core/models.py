from django.db import models

# from django.contrib.auth.models import User
from django.core.validators import (
    MinLengthValidator,
    EmailValidator,
    validate_ipv4_address,
)
from django.contrib.auth import get_user_model


User = get_user_model()


class Agent(models.Model):
    class Enviroments(models.TextChoices):
        PRODUCTION = ("PRODUCTION", "PRODUCTION")
        HOMOLOGATION = ("HOMOLOGATION", "HOMOLOGATION")
        DEV = ("DEV", "DEV")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.GenericIPAddressField(
        validators=[validate_ipv4_address], null=True
    )
    env = models.CharField(max_length=20, choices=Enviroments.choices)
    version = models.CharField(max_length=5)

    @property
    def name(self):
        self.user.name

    def __str__(self):
        return self.user.name + " - " + self.address

    class Meta:
        ordering = ["user"]


class Event(models.Model):
    class Levels(models.TextChoices):
        CRITICAL = ("CRITICAL", "CRITICAL")
        DEBUG = ("DEBUG", "DEBUG")
        ERROR = ("ERROR", "ERROR")
        WARNING = ("WARNING", "WARNING")
        INFO = ("INFO", "INFO")

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    level = models.CharField(max_length=20, choices=Levels.choices)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    shelved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.level + " in " + str(self.agent)

    @property
    def number_of_occurrences(self):
        return Event.objects.filter(
            title=self.title,
            description=self.description,
            level=self.level,
            agent=self.agent,
        ).count()

    class Meta:
        ordering = ["date"]

