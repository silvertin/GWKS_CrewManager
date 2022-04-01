from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from .views import crew_list, crew_detail, user_list, user_detail
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


app_name = 'apis'

schema_url_patterns = [
    path('/apis/crew/', crew_list),
    path('/apis/crew/<int:pk>/', crew_detail),
    path('/apis/user/', user_list),
    path('/apis/user/<int:pk>/', user_detail),
]
schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Open API",
        default_version='v1',
        description="시스템 API",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns, )

urlpatterns = [
    path('crew/', crew_list),
    path('crew/<int:pk>/', crew_detail),
    path('user/', user_list),
    path('user/<int:pk>/', user_detail),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]