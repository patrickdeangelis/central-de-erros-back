from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import (
    AgentSerializer,
    EventSerializer,
    EventInputSerializer,
    EventPatchSerializer,
)
from core.models import Event, Agent


class EventViewSet(ViewSet):
    """
    A ViewSet for creating, listing, retrieving or delete events.
    """

    def create(self, request):
        user = request.user
        client_ip = self._get_client_ip(request)

        serializer = EventInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            agent = Agent.objects.get(
                user=user,
                address=client_ip,
                env=serializer.data["env"],
                version=serializer.data["version"],
            )
        except Agent.DoesNotExist:
            agent = Agent.objects.create(
                user=user,
                address=client_ip,
                env=serializer.data["env"],
                version=serializer.data["version"],
            )

        event = Event.objects.create(
            title=serializer.data["title"],
            description=serializer.data["description"],
            level=Event.Levels[serializer.data["level"]],
            agent=agent,
        )

        event_serializer = EventSerializer(event)
        return Response(event_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)
        # data = {"shelved": request.data["shelved"]}
        # serializer = EventSerializer(event, data=data, partial=True)
        serializer = EventPatchSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
