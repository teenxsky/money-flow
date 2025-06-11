from apps.reference.enums.base import BaseEnum
from apps.reference.enums.transaction_type import TransactionTypeEnum

__all__ = ['CategoryEnum']


class CategoryEnum(BaseEnum):
    """Categories for transactions"""

    INFRASTRUCTURE = 'Infrastructure'
    MARKETING = 'Marketing'
    SALARY = 'Salary'

    # Mapping of categories to transaction types
    MAP = {
        INFRASTRUCTURE: TransactionTypeEnum.EXPENSE,
        MARKETING: TransactionTypeEnum.EXPENSE,
        SALARY: TransactionTypeEnum.INCOME,
    }
