"""wall_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django_rest_passwordreset import views as reset_pass_view
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Wall App API Documentation",
        default_version='v1',
        description="This is an `API documentation` for "
                    "the [Wall Management App]( http://127.0.0.1:8000/) "
                    "Django Rest Framework project.\n"
                    "The `swagger-ui` view can be found [here](/swagger). The `ReDoc` view can be found "
                    "[here](/redoc).\n The `swagger YAML` document can be found [here](/swagger.yaml).",

        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@gmail.com"),
        license=openapi.License(name="Wall Management App License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/password_reset/validate_token/',
         reset_pass_view.ResetPasswordValidateToken.as_view(authentication_classes=[], permission_classes=[]),
         name="reset-password-validate"),
    path('api/password_reset/confirm/',
         reset_pass_view.ResetPasswordConfirm.as_view(authentication_classes=[], permission_classes=[]),
         name="reset-password-confirm"),
    path('api/password_reset/',
         reset_pass_view.ResetPasswordRequestToken.as_view(authentication_classes=[], permission_classes=[]),
         name='reset-password-request'),
    path('', include('users.urls')),
    path('api/wall/', include('wall.urls')),
]
