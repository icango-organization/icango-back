"""icango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls           import path
from django.urls.conf      import include
from django.contrib        import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin', admin.site.urls),
    path('accounts', include('accounts.urls')),
    path('information', include('information.urls')),
    path('accounts/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('accounts/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('information/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('information/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]





