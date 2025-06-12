from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'transaction_type',
        'category',
        'subcategory',
        'amount',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'status',
        'transaction_type',
        'category',
        'subcategory',
        'created_at',
    )
    search_fields = (
        'user__email',
        'comment',
    )
    ordering = ('-created_at',)
