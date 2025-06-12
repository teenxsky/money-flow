from django.core.management.base import BaseCommand
from django.db import transaction

from apps.reference.enums import (
    CategoryEnum,
    StatusEnum,
    SubcategoryEnum,
    TransactionTypeEnum,
)
from apps.reference.models import Category, Status, Subcategory, TransactionType


class Command(BaseCommand):
    help = 'Clears and loads reference data from enumerations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-clear',
            action='store_true',
            dest='no_clear',
            default=False,
            help='Do not clear existing data before loading',
        )

    def handle(self, *args, **options):
        no_clear = options['no_clear']

        if not no_clear:
            self.clear_reference_data()
            self.stdout.write(self.style.SUCCESS('Reference data cleared'))

        @transaction.atomic
        def load_all_reference_data(self):
            self.load_transaction_types()
            self.load_categories()
            self.load_subcategories()
            self.load_statuses()

        load_all_reference_data(self)

        self.stdout.write(self.style.SUCCESS('Reference data loaded successfully'))

    def clear_reference_data(self):
        self.stdout.write('Clearing existing reference data...')
        Subcategory.objects.all().delete()
        Category.objects.all().delete()
        TransactionType.objects.all().delete()
        Status.objects.all().delete()

    def load_transaction_types(self):
        self.stdout.write('Loading transaction types...')
        transaction_types = []
        for transaction_type_value in TransactionTypeEnum.values():
            transaction_types.append(TransactionType(name=transaction_type_value))

        if transaction_types:
            TransactionType.objects.bulk_create(
                transaction_types, ignore_conflicts=True
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {len(transaction_types)} transaction types'
                )
            )

    def load_categories(self):
        self.stdout.write('Loading categories...')
        categories = []

        for category_enum in CategoryEnum:
            if category_enum.name == 'MAP':
                continue

            transaction_type_enum = CategoryEnum.MAP.value.get(category_enum.value)
            try:
                if not transaction_type_enum:
                    self.stdout.write(
                        self.style.WARNING(
                            f'No transaction type mapping found for '
                            f'{category_enum.value}'
                        )
                    )
                    continue

                transaction_type = TransactionType.objects.get(
                    name=transaction_type_enum.value
                )

                categories.append(
                    Category(
                        name=category_enum.value, transaction_type=transaction_type
                    )
                )
            except TransactionType.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Transaction type {transaction_type_enum.value} not found for '
                        f'{category_enum.value}'
                    )
                )

        if categories:
            Category.objects.bulk_create(categories, ignore_conflicts=True)
            self.stdout.write(
                self.style.SUCCESS(f'Created {len(categories)} categories')
            )

    def load_subcategories(self):
        self.stdout.write('Loading subcategories...')
        subcategories = []

        for subcategory_enum in SubcategoryEnum:
            if subcategory_enum.name == 'MAP':
                continue

            category_enum = SubcategoryEnum.MAP.value.get(subcategory_enum.value)
            try:
                if not category_enum:
                    self.stdout.write(
                        self.style.WARNING(
                            f'No category mapping found for {subcategory_enum.value}'
                        )
                    )
                    continue

                category = Category.objects.get(name=category_enum.value)

                subcategories.append(
                    Subcategory(name=subcategory_enum.value, category=category)
                )
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Category {category_enum.value} not found for '
                        f'{subcategory_enum.value}'
                    )
                )

        if subcategories:
            Subcategory.objects.bulk_create(subcategories, ignore_conflicts=True)
            self.stdout.write(
                self.style.SUCCESS(f'Created {len(subcategories)} subcategories')
            )

    def load_statuses(self):
        self.stdout.write('Loading statuses...')
        statuses = []
        for status_value in StatusEnum.values():
            statuses.append(Status(name=status_value))

        if statuses:
            Status.objects.bulk_create(statuses, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Created {len(statuses)} statuses'))
