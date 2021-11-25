from .views import FeedbackViewSet, test

from django.urls            import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r"feedback", FeedbackViewSet, basename="feedback")

urlpatterns = [
    path('test', test)
] + router.urls