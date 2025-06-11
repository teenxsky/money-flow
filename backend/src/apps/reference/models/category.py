from django.db import models

from apps.reference.models.transaction_type import TransactionType

__all__ = ['Category']


class Category(models.Model):
    name = models.CharField(max_length=50)
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.CASCADE,
        related_name='categories',
    )

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'transaction_type'], name='unique_category_per_type'
            ),
        ]
