from django.urls            import path

from rest_framework.routers import DefaultRouter

from .views import RouteViewSet, StationViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"/station", StationViewSet, basename="station")
router.register(r"/route", RouteViewSet, basename="route")

urlpatterns = [
] + router.urls
