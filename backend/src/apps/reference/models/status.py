from django.db import models

__all__ = ['Status']


class Status(models.Model):
    """
    Transaction status reference model.
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
