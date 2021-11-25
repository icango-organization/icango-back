from .views import RouteViewSet, StationViewSet

from django.urls            import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r"station", StationViewSet, basename="station")
router.register(r"route", RouteViewSet, basename="route")

urlpatterns = [
] + router.urls
