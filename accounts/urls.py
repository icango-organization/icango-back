from django.urls.conf import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    FeedbackViewSet, SignUpView,
    test, permission_classes_allowany, permission_classes_isauthenicated, permission_classes_isadminuser
)

router = DefaultRouter(trailing_slash=False)
router.register(r"/feedback", FeedbackViewSet, basename="feedback")

urlpatterns = [
    path('/sign-up', SignUpView.as_view(), name='sign_up'),
    path('/sign-in', TokenObtainPairView.as_view(), name='sign_in'),
    path('/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('/test', test, name='test'),
    path('/permission-classes-allowany', permission_classes_allowany, name='permission_classes_allowany'),
    path('/permission-classes-isauthenticated', permission_classes_isauthenicated, name='permission_classes_isauthenicated'),
    path('/permission-classes-isadminuser', permission_classes_isadminuser, name='permission_classes_isadminuser'),
] + router.urls