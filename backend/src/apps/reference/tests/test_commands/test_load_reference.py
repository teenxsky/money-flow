from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from apps.reference.enums import (
    CategoryEnum,
    StatusEnum,
    SubcategoryEnum,
    TransactionTypeEnum,
)
from apps.reference.models import Category, Status, Subcategory, TransactionType


class LoadReferenceCommandTest(TestCase):
    """Test suite for the load_reference management command."""

    def setUp(self):
        """Set up test data."""
        self.transaction_type = TransactionType.objects.create(name='Test Type')
        self.category = Category.objects.create(
            name='Test Category', transaction_type=self.transaction_type
        )
        self.subcategory = Subcategory.objects.create(
            name='Test Subcategory', category=self.category
        )
        self.status = Status.objects.create(name='Test Status')

    def test_load_reference_with_clear(self):
        """Test that the command clears existing data and loads new data from enums."""
        self.assertEqual(TransactionType.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Subcategory.objects.count(), 1)
        self.assertEqual(Status.objects.count(), 1)

        out = StringIO()
        call_command('load_reference', stdout=out)

        output = out.getvalue()
        self.assertIn('Reference data cleared', output)
        self.assertIn('Reference data loaded successfully', output)

        self.assertEqual(
            TransactionType.objects.count(),
            len([t for t in TransactionTypeEnum if t.name != 'MAP']),
        )
        self.assertEqual(
            Category.objects.count(), len([c for c in CategoryEnum if c.name != 'MAP'])
        )
        self.assertEqual(
            Subcategory.objects.count(),
            len([s for s in SubcategoryEnum if s.name != 'MAP']),
        )
        self.assertEqual(
            Status.objects.count(), len([s for s in StatusEnum if s.name != 'MAP'])
        )

        for enum_value in TransactionTypeEnum.values():
            self.assertTrue(
                TransactionType.objects.filter(name=enum_value).exists(),
                f"Transaction Type '{enum_value}' was not loaded",
            )

        for enum_value in CategoryEnum.values():
            self.assertTrue(
                Category.objects.filter(name=enum_value).exists(),
                f"Category '{enum_value}' was not loaded",
            )

        for enum_value in SubcategoryEnum.values():
            self.assertTrue(
                Subcategory.objects.filter(name=enum_value).exists(),
                f"Subcategory '{enum_value}' was not loaded",
            )

        for enum_value in StatusEnum.values():
            self.assertTrue(
                Status.objects.filter(name=enum_value).exists(),
                f"Status '{enum_value}' was not loaded",
            )

    def test_load_reference_without_clear(self):
        """
        Test that the command loads data without clearing when --no-clear is specified.
        """
        initial_transaction_type_count = TransactionType.objects.count()
        initial_category_count = Category.objects.count()
        initial_subcategory_count = Subcategory.objects.count()
        initial_status_count = Status.objects.count()

        out = StringIO()
        call_command('load_reference', no_clear=True, stdout=out)

        output = out.getvalue()
        self.assertNotIn('Reference data cleared', output)
        self.assertIn('Reference data loaded successfully', output)

        self.assertTrue(
            TransactionType.objects.filter(id=self.transaction_type.id).exists()
        )
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())
        self.assertTrue(Subcategory.objects.filter(id=self.subcategory.id).exists())
        self.assertTrue(Status.objects.filter(id=self.status.id).exists())

        self.assertGreaterEqual(
            TransactionType.objects.count(), initial_transaction_type_count
        )
        self.assertGreaterEqual(Category.objects.count(), initial_category_count)
        self.assertGreaterEqual(Subcategory.objects.count(), initial_subcategory_count)
        self.assertGreaterEqual(Status.objects.count(), initial_status_count)

        for enum_value in TransactionTypeEnum.values():
            self.assertTrue(
                TransactionType.objects.filter(name=enum_value).exists(),
                f"Transaction Type '{enum_value}' was not loaded",
            )
