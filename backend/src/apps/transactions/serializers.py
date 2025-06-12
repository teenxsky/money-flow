from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.reference.models import Category, Status, Subcategory, TransactionType


class TransactionCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    transaction_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.objects.all()
    )
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all(), required=False, allow_null=True
    )
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    comment = serializers.CharField(required=False, allow_blank=True, max_length=50)

    def validate(self, attrs):
        status = attrs.pop('status_id')
        category = attrs.pop('category_id')
        subcategory = attrs.pop('subcategory_id')
        transaction_type = attrs.pop('transaction_type_id')

        if subcategory and category and subcategory.category != category:
            raise ValidationError(
                {
                    'subcategory': 'The selected subcategory does not belong '
                    'to the selected category.'
                }
            )

        if (
            category
            and transaction_type
            and category.transaction_type != transaction_type
        ):
            raise ValidationError(
                {
                    'category': 'The selected category does not belong '
                    'to the selected transaction type.'
                }
            )

        attrs['status'] = status
        attrs['category'] = category
        attrs['subcategory'] = subcategory
        attrs['transaction_type'] = transaction_type

        return attrs


class TransactionUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), required=False
    )
    transaction_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.objects.all(),
        required=False,
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False
    )
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.all(), required=False, allow_null=True
    )
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        required=False,
    )
    comment = serializers.CharField(required=False, allow_blank=True, max_length=50)

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)

        status = attrs.pop('status_id', instance.status if instance else None)
        category = attrs.pop('category_id', instance.category if instance else None)
        subcategory = attrs.pop(
            'subcategory_id', instance.subcategory if instance else None
        )
        transaction_type = attrs.pop(
            'transaction_type_id', instance.transaction_type if instance else None
        )

        if subcategory and category and subcategory.category != category:
            raise ValidationError(
                {
                    'subcategory': 'The selected subcategory does not belong '
                    'to the selected category.'
                }
            )

        if (
            category
            and transaction_type
            and category.transaction_type != transaction_type
        ):
            raise ValidationError(
                {
                    'category': 'The selected category does not belong to '
                    'the selected transaction type.'
                }
            )

        attrs['status'] = status
        attrs['category'] = category
        attrs['subcategory'] = subcategory
        attrs['transaction_type'] = transaction_type

        return attrs


class TransactionDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    transaction_type_id = serializers.PrimaryKeyRelatedField(read_only=True)
    transaction_type_name = serializers.CharField(
        source='transaction_type.name', read_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(read_only=True)
    subcategory_name = serializers.CharField(
        source='subcategory.name', read_only=True, allow_null=True
    )
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    comment = serializers.CharField(read_only=True)


class TransactionListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    transaction_type_id = serializers.PrimaryKeyRelatedField(read_only=True)
    transaction_type_name = serializers.CharField(
        source='transaction_type.name', read_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(read_only=True)
    subcategory_name = serializers.CharField(
        source='subcategory.name', read_only=True, allow_null=True
    )
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
