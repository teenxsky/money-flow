from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.reference.enums.category import CategoryEnum
from apps.reference.models import Category, TransactionType


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    transaction_type = serializers.PrimaryKeyRelatedField(
        queryset=TransactionType.objects.all()
    )
    transaction_type_name = serializers.CharField(
        source='transaction_type.name', read_only=True
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['name', 'transaction_type'],
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
        if attrs['name'] in CategoryEnum.MAP.value.keys():
            expected_type_enum = CategoryEnum.MAP.value[attrs['name']]
            expected_type = expected_type_enum.value
            if attrs['transaction_type'].name != expected_type:
                raise serializers.ValidationError(
                    f"Category '{attrs['name']}' must be associated with "
                    f"transaction type '{expected_type}'"
                )
        return attrs


class CategoryDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    transaction_type = serializers.StringRelatedField()
