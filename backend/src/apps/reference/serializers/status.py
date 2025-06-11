from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.reference.enums.status import StatusEnum
from apps.reference.models import Status


class StatusSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate_name(self, value):
        if value not in StatusEnum.values():
            raise serializers.ValidationError(
                f'Invalid status name. Must be one of: {StatusEnum.values()}'
            )

        instance_id = self.instance.id if self.instance else None

        queryset = Status.objects.all()
        if instance_id:
            queryset = queryset.exclude(id=instance_id)

        unique_validator = UniqueValidator(queryset=queryset)
        unique_validator(value, self.fields['name'])

        return value


class StatusDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
