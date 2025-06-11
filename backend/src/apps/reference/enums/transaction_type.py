from apps.reference.enums.base import BaseEnum

__all__ = ['TransactionTypeEnum']


class TransactionTypeEnum(BaseEnum):
    """Transaction Types"""

    INCOME = 'Income'
    EXPENSE = 'Expense'
