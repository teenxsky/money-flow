from django.test import TestCase
from rest_framework.exceptions import NotFound, ValidationError

from apps.reference.enums import CategoryEnum, SubcategoryEnum, TransactionTypeEnum
from apps.reference.models import Subcategory
from apps.reference.services.subcategory import (
    create_subcategory,
    delete_subcategory,
    get_all_subcategories,
    get_subcategory_by_id,
    update_subcategory,
)
from apps.reference.tests.factories import (
    CategoryFactory,
    SubcategoryFactory,
    TransactionTypeFactory,
)


class SubcategoryServiceTests(TestCase):
    """Test suite for subcategory services."""

    def setUp(self):
        """Set up test data."""
        self.subcategory_name = SubcategoryEnum.VPS.value
        category_name = CategoryEnum.INFRASTRUCTURE.value
        transaction_type_name = TransactionTypeEnum.EXPENSE.value

        self.transaction_type = TransactionTypeFactory(name=transaction_type_name)
        self.category = CategoryFactory(
            name=category_name, transaction_type=self.transaction_type
        )

        self.subcategory = SubcategoryFactory(
            name=self.subcategory_name, category=self.category
        )

    def test_get_all_subcategories(self):
        """Test getting all subcategories returns all subcategories in the database."""
        another_subcategory_name = SubcategoryEnum.PROXY.value

        SubcategoryFactory(name=another_subcategory_name, category=self.category)

        subcategories = get_all_subcategories()

        self.assertEqual(subcategories.count(), 2)

        subcategory_names = [subcategory.name for subcategory in subcategories]
        self.assertIn(self.subcategory_name, subcategory_names)
        self.assertIn(another_subcategory_name, subcategory_names)

    def test_get_subcategory_by_id(self):
        """Test getting a subcategory by its ID."""
        retrieved_subcategory = get_subcategory_by_id(self.subcategory.id)

        self.assertEqual(retrieved_subcategory.id, self.subcategory.id)
        self.assertEqual(retrieved_subcategory.name, self.subcategory_name)
        self.assertEqual(retrieved_subcategory.category, self.category)

    def test_get_subcategory_by_id_not_found(self):
        """Test that getting a subcategory with a non-existent ID raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            get_subcategory_by_id(non_existent_id)

    def test_create_subcategory(self):
        """Test creating a new subcategory."""
        new_subcategory_name = SubcategoryEnum.PROXY.value

        new_subcategory = create_subcategory(new_subcategory_name, self.category)

        self.assertEqual(new_subcategory.name, new_subcategory_name)
        self.assertEqual(new_subcategory.category, self.category)

        self.assertTrue(Subcategory.objects.filter(name=new_subcategory_name).exists())

    def test_create_subcategory_invalid_name(self):
        """
        Test that creating a subcategory with an invalid name raises ValidationError.
        """
        with self.assertRaises(ValidationError):
            create_subcategory('Invalid Subcategory Name', self.category)

    def test_create_subcategory_invalid_category(self):
        """
        Test that creating a subcategory with incorrect category raises ValidationError.
        """
        other_category_name = CategoryEnum.MARKETING.value
        other_transaction_type_name = TransactionTypeEnum.EXPENSE.value

        other_transaction_type = TransactionTypeFactory(
            name=other_transaction_type_name
        )
        other_category = CategoryFactory(
            name=other_category_name, transaction_type=other_transaction_type
        )

        with self.assertRaises(ValidationError):
            create_subcategory(self.subcategory_name, other_category)

    def test_create_duplicate_subcategory(self):
        """Test that creating a duplicate subcategory raises ValidationError."""
        with self.assertRaises(ValidationError):
            create_subcategory(self.subcategory_name, self.category)

    def test_update_subcategory(self):
        """Test updating an existing subcategory."""
        new_subcategory_name = SubcategoryEnum.PROXY.value

        updated_subcategory = update_subcategory(
            self.subcategory.id, name=new_subcategory_name
        )

        self.assertEqual(updated_subcategory.name, new_subcategory_name)

        self.subcategory.refresh_from_db()
        self.assertEqual(self.subcategory.name, new_subcategory_name)

    def test_update_subcategory_not_found(self):
        """Test that updating a non-existent subcategory raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            update_subcategory(non_existent_id, name="Doesn't Matter")

    def test_update_subcategory_invalid_name(self):
        """
        Test that updating a subcategory with an invalid name raises ValidationError.
        """
        with self.assertRaises(ValidationError):
            update_subcategory(self.subcategory.id, name='Invalid Subcategory Name')

    def test_delete_subcategory(self):
        """Test deleting a subcategory."""
        delete_subcategory(self.subcategory.id)

        self.assertFalse(Subcategory.objects.filter(id=self.subcategory.id).exists())

    def test_delete_subcategory_not_found(self):
        """Test that deleting a non-existent subcategory raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            delete_subcategory(non_existent_id)
