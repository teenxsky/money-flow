from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.reference.enums.subcategory import SubcategoryEnum
from apps.reference.models import Category, Subcategory


class SubcategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    category_id = serializers.IntegerField()

    def validate_name(self, value):
        if value not in SubcategoryEnum.values():
            raise ValidationError(
                f'Invalid subcategory name. Must be one of: {SubcategoryEnum.values()}'
            )
        return value

    def validate(self, attrs):
        try:
            category = Category.objects.get(id=attrs['category_id'])
        except Category.DoesNotExist as error:
            raise ValidationError({'category_id': 'Category does not exist'}) from error

        if attrs['name'] in SubcategoryEnum.MAP.value.keys():
            expected_category_enum = SubcategoryEnum.MAP.value[attrs['name']]
            expected_category = expected_category_enum.value
            if category.name != expected_category:
                raise ValidationError(
                    f"Subcategory '{attrs['name']}' must be associated with "
                    f"category '{expected_category}'"
                )

        if Subcategory.objects.filter(name=attrs['name'], category=category).exists():
            raise ValidationError(
                'Subcategory with this name and category already exists'
            )

        attrs['category'] = category
        return attrs


class SubcategoryDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    category = serializers.CharField(source='category.name')
