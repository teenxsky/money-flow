from django.db.models.query import QuerySet
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.reference.models import Category, Subcategory
from apps.reference.models.transaction_type import TransactionType
from apps.transactions.models import Transaction
from apps.users.models import User


def get_user_transactions(user: User, filters: dict = None, ordering: list = None):
    """
    Retrieve transactions for a specific user with optional filtering and ordering.

    Args:
        user: User object for whom to retrieve transactions
        filters (dict, optional): Dictionary of filters to apply
        ordering (list, optional): List of fields to order by

    Returns:
        QuerySet: Filtered and ordered transactions queryset
    """
    queryset = Transaction.objects.filter(user=user).select_related(
        'status', 'transaction_type', 'category', 'subcategory'
    )

    if filters:
        queryset = apply_filters(queryset, filters)

    if ordering:
        queryset = queryset.order_by(*ordering)
    else:
        queryset = queryset.order_by('-created_at')

    return queryset


def apply_filters(queryset: QuerySet, filters: dict):
    """
    Apply filters to a transaction queryset.

    Args:
        queryset: Transaction queryset to filter
        filters (dict): Dictionary of filters to apply

    Returns:
        QuerySet: Filtered transactions queryset
    """
    filter_handlers = {
        'created_at__gte': lambda q, v: q.filter(created_at__gte=v) if v else q,
        'created_at__lte': lambda q, v: q.filter(created_at__lte=v) if v else q,
        'created_at__exact': lambda q, v: q.filter(created_at__exact=v) if v else q,
        'created_at__gt': lambda q, v: q.filter(created_at__gt=v) if v else q,
        'created_at__lt': lambda q, v: q.filter(created_at__lt=v) if v else q,
        'status': lambda q, v: q.filter(status=v) if v else q,
        'transaction_type': lambda q, v: q.filter(transaction_type=v) if v else q,
        'category': lambda q, v: q.filter(category=v) if v else q,
        'subcategory': lambda q, v: q.filter(subcategory=v) if v else q,
        'amount__gte': lambda q, v: q.filter(amount__gte=v) if v else q,
        'amount__lte': lambda q, v: q.filter(amount__lte=v) if v else q,
        'amount__exact': lambda q, v: q.filter(amount__exact=v) if v else q,
    }

    for key, value in filters.items():
        if key in filter_handlers:
            queryset = filter_handlers[key](queryset, value)

    return queryset


def get_transaction_by_id(transaction_id: int, user: User):
    """
    Retrieve a specific transaction for a user.

    Args:
        transaction_id: ID of the transaction to retrieve
        user: User object who owns the transaction

    Returns:
        Transaction: The requested transaction object

    Raises:
        NotFound: If the transaction doesn't exist or doesn't belong to the user
        PermissionDenied: If the user doesn't have permission to access the transaction
    """
    try:
        transaction = Transaction.objects.select_related(
            'status', 'transaction_type', 'category', 'subcategory', 'user'
        ).get(id=transaction_id)

        if transaction.user != user:
            raise PermissionDenied(
                "You don't have permission to access this transaction"
            )

        return transaction
    except Transaction.DoesNotExist as error:
        raise NotFound(f'Transaction with ID {transaction_id} not found') from error


def create_transaction(data: dict, user: User):
    """
    Create a new transaction.

    Args:
        data (dict): Transaction data
        user: User object who will own the transaction

    Returns:
        Transaction: The newly created transaction

    Raises:
        ValidationError: If validation fails
    """
    validate_transaction_relationships(
        data.get('category'), data.get('subcategory'), data.get('transaction_type')
    )

    transaction = Transaction.objects.create(user=user, **data)
    return transaction


def update_transaction(transaction_id: int, data: dict, user: User):
    """
    Update an existing transaction.

    Args:
        transaction_id: ID of the transaction to update
        data (dict): Updated transaction data
        user: User object who owns the transaction

    Returns:
        Transaction: The updated transaction object

    Raises:
        NotFound: If the transaction doesn't exist
        PermissionDenied: If the user doesn't own the transaction
        ValidationError: If validation fails
    """
    transaction = get_transaction_by_id(transaction_id, user)

    # Prepare data for validation with current values as fallback
    category = data.get('category', transaction.category)
    subcategory = data.get('subcategory', transaction.subcategory)
    transaction_type = data.get('transaction_type', transaction.transaction_type)

    validate_transaction_relationships(category, subcategory, transaction_type)

    for key, value in data.items():
        setattr(transaction, key, value)

    transaction.save()
    return transaction


def delete_transaction(transaction_id: int, user: User):
    """
    Delete a transaction.

    Args:
        transaction_id: ID of the transaction to delete
        user: User object who owns the transaction

    Raises:
        NotFound: If the transaction doesn't exist
        PermissionDenied: If the user doesn't own the transaction
    """
    transaction = get_transaction_by_id(transaction_id, user)
    transaction.delete()


def validate_transaction_relationships(
    category: Category, subcategory: Subcategory, transaction_type: TransactionType
):
    """
    Validate relationships between transaction elements.

    Args:
        category: Category object
        subcategory: Subcategory object
        transaction_type: TransactionType object

    Raises:
        ValidationError: If relationships are invalid
    """
    if subcategory and category and subcategory.category != category:
        raise ValidationError(
            {
                'subcategory': 'The selected subcategory does not belong to '
                'the selected category.'
            }
        )

    if category and transaction_type and category.transaction_type != transaction_type:
        raise ValidationError(
            {
                'category': 'The selected category does not belong to '
                'the selected transaction type.'
            }
        )


def get_subcategories_for_category(category_id: int):
    """
    Get subcategories for a specific category.

    Args:
        category_id: ID of the category

    Returns:
        QuerySet: Subcategories belonging to the category
    """
    return Subcategory.objects.filter(category_id=category_id)


def get_categories_for_transaction_type(transaction_type_id: int):
    """
    Get categories for a specific transaction type.

    Args:
        transaction_type_id: ID of the transaction type

    Returns:
        QuerySet: Categories belonging to the transaction type
    """
    return Category.objects.filter(transaction_type_id=transaction_type_id)
