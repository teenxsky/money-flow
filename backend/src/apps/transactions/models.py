from django.core.exceptions import ValidationError
from django.db import models

from apps.reference.models import Category, Status, Subcategory, TransactionType
from apps.users.models import User


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name='transactions',
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if (
            self.subcategory
            and self.category
            and self.subcategory.category != self.category
        ):
            raise ValidationError(
                'Selected subcategory does not belong to the selected category.'
            )

        if (
            self.category
            and self.transaction_type
            and self.category.transaction_type != self.transaction_type
        ):
            raise ValidationError(
                'Selected category does not belong to the selected transaction type.'
            )
