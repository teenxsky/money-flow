from django.test import TestCase
from rest_framework.exceptions import NotFound, ValidationError

from apps.reference.enums import CategoryEnum, TransactionTypeEnum
from apps.reference.models import Category
from apps.reference.services.category import (
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    update_category,
)
from apps.reference.tests.factories import CategoryFactory, TransactionTypeFactory


class CategoryServiceTests(TestCase):
    """Test suite for category services."""

    def setUp(self):
        """Set up test data."""
        self.category_name = CategoryEnum.INFRASTRUCTURE.value
        transaction_type_name = TransactionTypeEnum.EXPENSE.value

        self.transaction_type = TransactionTypeFactory(name=transaction_type_name)

        self.category = CategoryFactory(
            name=self.category_name, transaction_type=self.transaction_type
        )

    def test_get_all_categories(self):
        """Test getting all categories returns all categories in the database."""
        categories = get_all_categories()

        self.assertEqual(categories.count(), 1)

        category_names = [category.name for category in categories]
        self.assertIn(self.category_name, category_names)

    def test_get_category_by_id(self):
        """Test getting a category by its ID."""
        retrieved_category = get_category_by_id(self.category.id)

        self.assertEqual(retrieved_category.id, self.category.id)
        self.assertEqual(retrieved_category.name, self.category_name)
        self.assertEqual(retrieved_category.transaction_type, self.transaction_type)

    def test_get_category_by_id_not_found(self):
        """Test that getting a category with a non-existent ID raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            get_category_by_id(non_existent_id)

    def test_create_category(self):
        """Test creating a new category."""
        new_category_name = CategoryEnum.MARKETING.value
        new_transaction_type_name = TransactionTypeEnum.EXPENSE.value

        new_transaction_type = TransactionTypeFactory(name=new_transaction_type_name)

        new_category = create_category(new_category_name, new_transaction_type)

        self.assertEqual(new_category.name, new_category_name)
        self.assertEqual(new_category.transaction_type, new_transaction_type)

        self.assertTrue(Category.objects.filter(name=new_category_name).exists())

    def test_create_category_invalid_name(self):
        """Test that creating a category with an invalid name raises ValidationError."""
        with self.assertRaises(ValidationError):
            create_category('Invalid Category Name', self.transaction_type)

    def test_create_category_invalid_transaction_type(self):
        """
        Test that creating a category with an incorrect transaction type
        raises ValidationError.
        """
        other_transaction_type = TransactionTypeFactory(
            name=TransactionTypeEnum.INCOME.value
        )

        with self.assertRaises(ValidationError):
            create_category(self.category_name, other_transaction_type)

    def test_update_category(self):
        """Test updating an existing category."""
        new_category_name = CategoryEnum.MARKETING.value

        updated_category = update_category(self.category.id, name=new_category_name)

        self.assertEqual(updated_category.name, new_category_name)

        self.category.refresh_from_db()
        self.assertEqual(self.category.name, new_category_name)

    def test_update_category_not_found(self):
        """Test that updating a non-existent category raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            update_category(non_existent_id, name="Doesn't Matter")

    def test_update_category_invalid_name(self):
        """Test that updating a category with an invalid name raises ValidationError."""
        with self.assertRaises(ValidationError):
            update_category(self.category.id, name='Invalid Category Name')

    def test_delete_category(self):
        """Test deleting a category."""
        delete_category(self.category.id)

        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_delete_category_not_found(self):
        """Test that deleting a non-existent category raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            delete_category(non_existent_id)
