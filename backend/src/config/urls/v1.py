from django.urls import include, path

__all__ = ['urlpatterns']

apps_patterns_v1 = [
    path('', include('apps.users.urls')),
]

third_party_patterns_v1 = []

urlpatterns = apps_patterns_v1 + third_party_patterns_v1
