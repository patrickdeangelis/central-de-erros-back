from rest_framework import serializers
from core.models import Agent, Event


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ("user", "address", "env", "version", "name")
        read_only_fields = ["name"]


class EventSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(many=False, read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "level",
            "date",
            "shelved",
            "agent",
            "number_of_occurrences",
        )
        read_only_fields = (
            "id",
            "title",
            "description",
            "level",
            "date",
            "number_of_occurrences",
        )
        depth = 1


class EventInputSerializer(serializers.Serializer):
    env = serializers.ChoiceField(choices=Agent.Enviroments.choices)
    version = serializers.CharField(required=True)
    title = serializers.CharField()
    description = serializers.CharField()
    level = serializers.ChoiceField(choices=Event.Levels.choices)

