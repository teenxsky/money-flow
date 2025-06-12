from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.reference.enums.transaction_type import TransactionTypeEnum
from apps.reference.models import TransactionType


class TransactionTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField(required=False, read_only=True)

    def validate_name(self, value):
        if value not in TransactionTypeEnum.values():
            valid_values = TransactionTypeEnum.values()
            raise serializers.ValidationError(
                f'Invalid transaction type name. Must be one of: {valid_values}'
            )

        instance_id = self.instance.id if self.instance else None

        queryset = TransactionType.objects.all()
        if instance_id:
            queryset = queryset.exclude(id=instance_id)

        unique_validator = UniqueValidator(queryset=queryset)
        unique_validator(value, self.fields['name'])

        return value


class TransactionTypeDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
