from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import (
    AgentSerializer,
    EventSerializer,
    EventInputSerializer,
)
from core.models import Event, Agent


class EventViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
):
    """
    A ViewSet for creating, listing, retrieving or delete events.
    """

    serializer_class = EventSerializer

    def get_queryset(self):
        env = self.request.query_params.get("env", None)
        orderBy = self.request.query_params.get("orderBy", "date")
        searchBy = self.request.query_params.get("searchBy", None)
        search = self.request.query_params.get("search", None)
        queryset = Event.objects.all()

        if env:
            queryset = Event.objects.filter(agent__env=env)

        if searchBy:
            searchBy = str(searchBy).lower()
            if searchBy == "level":
                queryset = queryset.filter(level=search)
            elif searchBy == "description":
                queryset = queryset.filter(description=search)
            elif searchBy == "origin":
                queryset = queryset.filter(agent__address=search)

        if orderBy:
            queryset = queryset.order_by(orderBy)

        return queryset

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

    def partial_update(self, request, pk=None):
        queryset = self.get_queryset()
        event = get_object_or_404(queryset, pk=pk)
        serializer = EventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
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
