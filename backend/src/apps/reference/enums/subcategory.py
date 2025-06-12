from apps.reference.enums.base import BaseEnum
from apps.reference.enums.category import CategoryEnum

__all__ = ['SubcategoryEnum']


class SubcategoryEnum(BaseEnum):
    """Subcategories for transactions, organized by category."""

    VPS = 'VPS'
    PROXY = 'Proxy'
    FARPOST = 'Farpost'
    AVITO = 'Avito'

    # Mapping of subcategories to categories
    MAP = {
        VPS: CategoryEnum.INFRASTRUCTURE,
        PROXY: CategoryEnum.INFRASTRUCTURE,
        FARPOST: CategoryEnum.MARKETING,
        AVITO: CategoryEnum.MARKETING,
    }
