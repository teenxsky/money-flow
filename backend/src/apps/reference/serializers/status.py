from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.reference.enums.status import StatusEnum
from apps.reference.models import Status


class StatusCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate_name(self, value):
        if value not in StatusEnum.values():
            raise serializers.ValidationError(
                f'Invalid status name. Must be one of: {StatusEnum.values()}'
            )

        unique_validator = UniqueValidator(queryset=Status.objects.all())
        unique_validator(value, self.fields['name'])

        return value


class StatusDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
