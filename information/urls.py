from .views import StationViewSet

from django.urls            import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=True)
router.register(r"station", StationViewSet, basename="station")

urlpatterns = [
] + router.urls
