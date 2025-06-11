from django.db import models

__all__ = ['TransactionType']


class TransactionType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
