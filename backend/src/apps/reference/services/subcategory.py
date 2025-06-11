from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, ValidationError

from apps.reference.enums import SubcategoryEnum
from apps.reference.models import Subcategory
from apps.reference.models.category import Category


def get_all_subcategories():
    """
    Get all subcategories with related categories.

    Returns:
        QuerySet: All subcategories with their related categories preloaded.
    """
    return Subcategory.objects.select_related('category').all()


def get_subcategory_by_id(subcategory_id: int):
    """
    Get subcategory by ID.

    Args:
        subcategory_id: The ID of the subcategory to retrieve.

    Returns:
        Subcategory: The subcategory object with related category.

    Raises:
        NotFound: If no subcategory with the given ID exists.
    """
    try:
        return Subcategory.objects.select_related('category').get(id=subcategory_id)
    except ObjectDoesNotExist as error:
        raise NotFound('Subcategory not found') from error


def create_subcategory(name: str, category: Category):
    """
    Create new subcategory with validation.

    Args:
        name (str): The name of the subcategory to create.
        category (Category): The category object to associate with the subcategory.

    Returns:
        Subcategory: The newly created subcategory object.

    Raises:
        ValidationError: If the name is invalid, the category association is incorrect,
                         or a duplicate subcategory already exists.
    """
    if name not in SubcategoryEnum.values():
        raise ValidationError(f'Invalid subcategory name: {name}')

    if Subcategory.objects.filter(name=name).exists():
        raise ValidationError(f"Category with name '{name}' already exists")

    for subcat_enum in SubcategoryEnum:
        if subcat_enum.value == name:
            cat_enum = SubcategoryEnum.MAP.value.get(subcat_enum)
            if cat_enum and cat_enum.value != category:
                raise ValidationError(
                    f"Subcategory '{name}' must be associated with "
                    f"category '{cat_enum.value}'"
                )
            break

    if Subcategory.objects.filter(name=name, category=category).exists():
        raise ValidationError('Subcategory with this name and category already exists')

    return Subcategory.objects.create(name=name, category=category)


def update_subcategory(
    subcategory_id: int, name: str = None, category: Category = None
):
    """
    Update existing subcategory.

    Args:
        subcategory_id: The ID of the subcategory to update.
        name (str, optional): The new name for the subcategory.
        category (Category, optional): The new category for the subcategory.

    Returns:
        Subcategory: The updated subcategory object.

    Raises:
        NotFound: If no subcategory with the given ID exists.
        ValidationError: If the new name is invalid or the category is incorrect.
    """
    subcategory = get_subcategory_by_id(subcategory_id)

    if name is not None:
        if name not in SubcategoryEnum.values():
            raise ValidationError(f'Invalid subcategory name: {name}')
        subcategory.name = name

    if category is not None:
        for subcat_enum in SubcategoryEnum:
            if subcat_enum.value == subcategory.name:
                cat_enum = SubcategoryEnum.MAP.value.get(subcat_enum)
                if cat_enum and cat_enum.value != category:
                    raise ValidationError(
                        f"Subcategory '{subcategory.name}' must be associated with "
                        f"category '{cat_enum.value}'"
                    )
                break
        subcategory.category = category

    subcategory.save()
    return subcategory


def delete_subcategory(subcategory_id: int):
    """
    Delete subcategory.

    Args:
        subcategory_id: The ID of the subcategory to delete.

    Raises:
        NotFound: If no subcategory with the given ID exists.
    """
    subcategory = get_subcategory_by_id(subcategory_id)
    subcategory.delete()
