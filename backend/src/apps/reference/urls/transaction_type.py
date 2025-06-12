from django.urls import include, path

from apps.reference.views.transaction_type import (
    TransactionTypeDetailView,
    TransactionTypeListCreateView,
)

transaction_type_patterns = [
    path(
        'transaction-types/',
        include(
            [
                path(
                    '',
                    TransactionTypeListCreateView.as_view(),
                    name='transaction-type-list-create',
                ),
                path(
                    '<int:id>/',
                    TransactionTypeDetailView.as_view(),
                    name='transaction-type-detail',
                ),
            ]
        ),
        name='transaction-type',
    )
]
