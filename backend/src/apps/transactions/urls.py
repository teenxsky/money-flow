from django.urls import path

from apps.transactions.views import TransactionDetailView, TransactionListCreateView

urlpatterns = [
    path(
        'transactions/',
        TransactionListCreateView.as_view(),
        name='transaction-list-create',
    ),
    path(
        'transactions/<int:id>/',
        TransactionDetailView.as_view(),
        name='transaction-detail',
    ),
]
