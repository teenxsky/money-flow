from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

docs_schema_view_v1 = get_schema_view(
    openapi.Info(
        default_version='v1',
        title='Money Flow API',
        description='Documentation API',
        terms_of_service='https://www.google.com/policies/terms/',
        license=openapi.License(name='Apache License'),
    ),
    public=True,
    authentication_classes=[JWTAuthentication],
    permission_classes=[AllowAny],
)
