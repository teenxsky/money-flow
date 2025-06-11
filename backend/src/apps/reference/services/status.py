from rest_framework.exceptions import NotFound

from apps.reference.models import Status


def get_all_statuses():
    """
    Get all statuses from the database.

    Returns:
        QuerySet: All Status objects.
    """
    return Status.objects.all()


def get_status_by_id(status_id: int):
    """
    Get status by ID from the database.

    Args:
        status_id (int): The ID of the status to retrieve.

    Returns:
        Status: The retrieved status object.

    Raises:
        NotFound: If the status with the specified ID does not exist.
    """
    try:
        return Status.objects.get(id=status_id)
    except Status.DoesNotExist as err:
        raise NotFound(f'Status with ID {status_id} not found') from err


def create_status(name: str):
    """
    Create new status in the database.

    Args:
        name (str): The name of the new status.

    Returns:
        Status: The newly created status object.
    """
    return Status.objects.create(name=name)


def update_status(status_id: int, name: str):
    """
    Update existing status in the database.

    Args:
        status_id (int): The ID of the status to update.
        name (str): The new name for the status.

    Returns:
        Status: The updated status object.

    Raises:
        NotFound: If the status with the specified ID does not exist.
    """
    status = get_status_by_id(status_id)
    status.name = name
    status.save()
    return status


def delete_status(status_id: int):
    """
    Delete status from the database.

    Args:
        status_id (int): The ID of the status to delete.

    Raises:
        NotFound: If the status with the specified ID does not exist.
    """
    status = get_status_by_id(status_id)
    status.delete()
