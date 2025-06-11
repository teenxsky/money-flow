from django.db import models

from apps.reference.models.category import Category

__all__ = ['Subcategory']


class Subcategory(models.Model):
    """
    Subcategory reference model
    """

    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
    )

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'], name='unique_subcategory_name_category'
            ),
        ]
