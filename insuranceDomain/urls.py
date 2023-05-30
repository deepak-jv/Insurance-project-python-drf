from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Your API Title',
        default_version='v1',
        description='Your API description',
        # Add other relevant information
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('insurance.urls')),
    path('api/', include('User.urls')),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # For postman to get json response
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger for browser
]
