from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from apps.reference.enums.category import CategoryEnum
from apps.reference.models import Category, TransactionType


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    transaction_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.objects.all(), required=True
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['name', 'transaction_type_id'],
                message='Category with this name and type already exists.',
            )
        ]

    def validate_name(self, value):
        if value not in CategoryEnum.values():
            raise serializers.ValidationError(
                f'Invalid category name. Must be one of: {CategoryEnum.values()}'
            )
        return value

    def validate(self, attrs):
        transaction_type = attrs.pop('transaction_type_id')
        name = attrs['name']

        attrs['transaction_type'] = transaction_type

        category_map = CategoryEnum.MAP.value

        if name in category_map:
            expected_transaction_type_name = category_map[name].value
            actual_transaction_type_name = transaction_type.name

            if actual_transaction_type_name != expected_transaction_type_name:
                raise ValidationError(
                    f"Category '{name}' must be associated "
                    f"with transaction type '{expected_transaction_type_name}'"
                )

        return attrs


class CategoryDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    transaction_type_id = serializers.IntegerField(source='transaction_type.id')
