from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.validators import ValidationError

from apps.reference.enums import CategoryEnum
from apps.reference.models import Category


def get_all_categories():
    """
    Get all categories with related transaction types.

    Returns:
        QuerySet: All Category objects with their related transaction_type.
    """
    return Category.objects.select_related('transaction_type').all()


def get_category_by_id(category_id: int):
    """
    Get category by ID.

    Args:
        category_id (int): The ID of the category to retrieve.

    Returns:
        Category: Category object with its related transaction_type.

    Raises:
        NotFound: If the category with the specified ID doesn't exist.
    """
    try:
        return Category.objects.select_related('transaction_type').get(id=category_id)
    except ObjectDoesNotExist as err:
        raise NotFound(f'Category with ID {category_id} not found') from err


def create_category(name: str, transaction_type: str):
    """
    Create new category with validation.

    Args:
        name (str): The name of the category to create.
        transaction_type (str): The transaction type to associate with this category.

    Returns:
        Category: The newly created Category object.

    Raises:
        ValidationError: If the category name is invalid or if the transaction type
                        doesn't match the required one for this category.
    """
    if name not in CategoryEnum.values():
        raise ValidationError(f'Invalid category name: {name}')

    if Category.objects.filter(name=name).exists():
        raise ValidationError(f"Category with name '{name}' already exists")

    for cat_enum in CategoryEnum:
        if cat_enum.value == name:
            trans_type_enum = CategoryEnum.MAP.value.get(cat_enum)
            if trans_type_enum and trans_type_enum.value != transaction_type.name:
                raise ValidationError(
                    f"Category '{name}' must be associated with "
                    f"transaction type '{trans_type_enum.value}'"
                )
            break
    else:
        raise ValidationError(f"Category '{name}' not found in CategoryEnum")

    return Category.objects.create(name=name, transaction_type=transaction_type)


def update_category(category_id: int, name: str = None, transaction_type: str = None):
    """
    Update existing category.

    Args:
        category_id (int): The ID of the category to update.
        name (str, optional): The new name for the category. Defaults to None.
        transaction_type (str, optional): The new transaction type. Defaults to None.

    Returns:
        Category: The updated Category object.

    Raises:
        NotFound: If the category with the specified ID doesn't exist.
        ValidationError: If the new category name is invalid or if the new transaction
                        type doesn't match the required one for this category.
    """
    category = get_category_by_id(category_id)

    if name is not None:
        if name not in CategoryEnum.values():
            raise ValidationError(f'Invalid category name: {name}')
        category.name = name

    if transaction_type is not None:
        for cat_enum in CategoryEnum:
            if cat_enum.value == category.name:
                trans_type_enum = CategoryEnum.MAP.value.get(cat_enum)
                if trans_type_enum and trans_type_enum.value != transaction_type.name:
                    raise ValidationError(
                        f"Category '{category.name}' must be associated with "
                        f"transaction type '{trans_type_enum.value}'"
                    )
                break
        else:
            raise ValidationError(
                f"Category '{category.name}' not found in CategoryEnum"
            )
        category.transaction_type = transaction_type

    category.save()
    return category


def delete_category(category_id: int):
    """
    Delete category.

    Args:
        category_id (int): The ID of the category to delete.

    Raises:
        NotFound: If the category with the specified ID doesn't exist.
    """
    category = get_category_by_id(category_id)
    category.delete()
