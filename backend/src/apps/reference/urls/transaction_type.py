from django.urls import include, path

from apps.reference.views.transaction_type import (
    TransactionTypeCreateView,
    TransactionTypeDeleteView,
    TransactionTypeDetailView,
    TransactionTypeListView,
    TransactionTypeUpdateView,
)

transaction_type_patterns = [
    path(
        'types/',
        include(
            [
                path(
                    '', TransactionTypeListView.as_view(), name='transaction-type-list'
                ),
                path(
                    'create/',
                    TransactionTypeCreateView.as_view(),
                    name='transaction-type-create',
                ),
                path(
                    '<int:id>/',
                    TransactionTypeDetailView.as_view(),
                    name='transaction-type-detail',
                ),
                path(
                    '<int:id>/update/',
                    TransactionTypeUpdateView.as_view(),
                    name='transaction-type-update',
                ),
                path(
                    '<int:id>/delete/',
                    TransactionTypeDeleteView.as_view(),
                    name='transaction-type-delete',
                ),
            ]
        ),
        name='transaction-type',
    )
]
