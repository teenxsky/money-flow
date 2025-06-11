from django.urls import include, path

from apps.reference.views.status import (
    StatusCreateView,
    StatusDeleteView,
    StatusDetailView,
    StatusListView,
    StatusUpdateView,
)

status_patterns = [
    path(
        'statuses/',
        include(
            [
                path('', StatusListView.as_view(), name='status-list'),
                path('create/', StatusCreateView.as_view(), name='status-create'),
                path('<int:id>/', StatusDetailView.as_view(), name='status-detail'),
                path(
                    '<int:id>/update/', StatusUpdateView.as_view(), name='status-update'
                ),
                path(
                    '<int:id>/delete/', StatusDeleteView.as_view(), name='status-delete'
                ),
            ]
        ),
        name='status',
    )
]
