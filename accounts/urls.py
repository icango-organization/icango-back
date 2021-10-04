from django.urls import path
from django.urls.resolvers import URLPattern

from rest_framework.routers import DefaultRouter
from accounts.views import FeedbackViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r"feedback", FeedbackViewSet, basename="feedback")

urlpatterns = [] + router.urls