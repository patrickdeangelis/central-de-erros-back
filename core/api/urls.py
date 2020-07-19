from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.generics import views
from .viewsets import EventViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")

