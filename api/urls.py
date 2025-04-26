# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import ClientViewSet

# API Documentation Setup
schema_view = get_schema_view(
    openapi.Info(
        title="DaktariHub API",
        default_version='v1',
        description="API for DaktariHub Health Information System",
    ),
    public=True,
)

# Router Setup
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    # API Documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    
    # API Endpoints
    path('', include(router.urls)),
]