from apps.reference.enums.base import BaseEnum

__all__ = ['StatusEnum']


class StatusEnum(BaseEnum):
    """Transaction Statuses"""

    BUSINESS = 'Business'
    PERSONAL = 'Personal'
    TAX = 'Tax'
