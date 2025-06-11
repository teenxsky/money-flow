import factory
from factory import fuzzy

from apps.reference.enums import (
    CategoryEnum,
    StatusEnum,
    SubcategoryEnum,
    TransactionTypeEnum,
)
from apps.reference.models import (
    Category,
    Status,
    Subcategory,
    TransactionType,
)


def fuzzy_enum_value(enum_cls):
    return fuzzy.FuzzyChoice([item.value for item in enum_cls]).fuzz()


def get_enum_by_value(enum_cls, value):
    return next((e for e in enum_cls if e.value == value), None)


class TransactionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionType
        django_get_or_create = ('name',)

    name = factory.declarations.LazyFunction(
        lambda: fuzzy_enum_value(TransactionTypeEnum)
    )


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.declarations.LazyFunction(lambda: fuzzy_enum_value(CategoryEnum))

    @factory.helpers.lazy_attribute
    def transaction_type(self):
        category_enum = get_enum_by_value(CategoryEnum, self.name)
        transaction_enum = TransactionTypeEnum.EXPENSE
        if category_enum in CategoryEnum.MAP.value:
            transaction_enum = CategoryEnum.MAP.value[category_enum]

        return TransactionTypeFactory(name=transaction_enum.value)


class SubcategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subcategory
        django_get_or_create = ('name', 'category')

    name = factory.declarations.LazyFunction(lambda: fuzzy_enum_value(SubcategoryEnum))

    @factory.helpers.lazy_attribute
    def category(self):
        subcategory_enum = get_enum_by_value(SubcategoryEnum, self.name)
        category_enum = CategoryEnum.INFRASTRUCTURE
        if subcategory_enum in SubcategoryEnum.MAP.value:
            category_enum = CategoryEnum.MAP.value[subcategory_enum]

        return CategoryFactory(name=category_enum.value)


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
        django_get_or_create = ('name',)

    name = factory.declarations.LazyFunction(lambda: fuzzy_enum_value(StatusEnum))
