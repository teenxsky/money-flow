from rest_framework.exceptions import NotFound

from apps.reference.models import TransactionType


def get_all_transaction_types():
    """
    Get all Transaction Types from the database.

    Returns:
        QuerySet: All TransactionType objects.
    """
    return TransactionType.objects.all()


def get_transaction_type_by_id(transaction_type_id: int):
    """
    Get TransactionType by ID from the database.

    Args:
        transaction_type_id (int): The ID of the TransactionType to retrieve.

    Returns:
        TransactionType: The retrieved TransactionType object.

    Raises:
        NotFound: If the TransactionType with the specified ID does not exist.
    """
    try:
        return TransactionType.objects.get(id=transaction_type_id)
    except TransactionType.DoesNotExist as err:
        raise NotFound(
            f'TransactionType with ID {transaction_type_id} not found'
        ) from err


def create_transaction_type(name: str):
    """
    Create new TransactionType in the database.

    Args:
        name (str): The name of the new TransactionType.

    Returns:
        TransactionType: The newly created TransactionType object.
    """
    return TransactionType.objects.create(name=name)


def update_transaction_type(transaction_type_id: int, name: str):
    """
    Update existing TransactionType in the database.

    Args:
        transaction_type_id (int): The ID of the TransactionType to update.
        name (str): The new name for the TransactionType.

    Returns:
        TransactionType: The updated TransactionType object.

    Raises:
        NotFound: If the TransactionType with the specified ID does not exist.
    """
    transaction_type = get_transaction_type_by_id(transaction_type_id)
    transaction_type.name = name
    transaction_type.save()
    return transaction_type


def delete_transaction_type(transaction_type_id: int):
    """
    Delete TransactionType from the database.

    Args:
        transaction_type_id (int): The ID of the TransactionType to delete.

    Raises:
        NotFound: If the TransactionType with the specified ID does not exist.
    """
    transaction_type = get_transaction_type_by_id(transaction_type_id)
    transaction_type.delete()
