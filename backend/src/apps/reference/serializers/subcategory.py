from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from apps.reference.enums.subcategory import SubcategoryEnum
from apps.reference.models import Category, Subcategory


class SubcategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=True
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Subcategory.objects.all(),
                fields=['name', 'category_id'],
                message='Subcategory with this name and category already exists.',
            )
        ]

    def validate_name(self, value):
        valid_names = SubcategoryEnum.values()
        if value not in valid_names:
            raise ValidationError(
                f'Invalid subcategory name. Must be one of: {valid_names}'
            )
        return value

    def validate(self, attrs):
        category = attrs.pop('category_id')
        name = attrs['name']

        attrs['category'] = category

        subcategory_map = SubcategoryEnum.MAP.value

        if name in subcategory_map:
            expected_category_name = subcategory_map[name].value
            actual_category_name = category.name

            if actual_category_name != expected_category_name:
                raise ValidationError(
                    f"Subcategory '{name}' must be associated "
                    f"with category '{expected_category_name}'"
                )

        return attrs


class SubcategoryDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    category_id = serializers.IntegerField(source='category.id')
