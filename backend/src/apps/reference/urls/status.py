from django.urls import include, path

from apps.reference.views.status import (
    StatusDetailView,
    StatusListCreateView,
)

status_patterns = [
    path(
        'statuses/',
        include(
            [
                path('', StatusListCreateView.as_view(), name='status-list-create'),
                path('<int:id>/', StatusDetailView.as_view(), name='status-detail'),
            ]
        ),
        name='status',
    )
]
