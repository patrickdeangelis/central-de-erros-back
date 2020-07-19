from rest_framework import serializers
from core.models import Agent, Event


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ("user", "adress", "env", "version")


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "level",
            "agent",
            "date",
            "shelved",
            "number_of_occurrences",
        )
        depth = 1


class EventPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["shelved"]


class EventInputSerializer(serializers.Serializer):
    env = serializers.ChoiceField(choices=Agent.Enviroments.choices)
    version = serializers.CharField(required=True)
    title = serializers.CharField()
    description = serializers.CharField()
    level = serializers.ChoiceField(choices=Event.Levels.choices)

