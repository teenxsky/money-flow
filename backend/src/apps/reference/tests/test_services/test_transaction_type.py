from django.test import TestCase
from rest_framework.exceptions import NotFound

from apps.reference.enums import TransactionTypeEnum
from apps.reference.models import TransactionType
from apps.reference.services.transaction_type import (
    create_transaction_type,
    delete_transaction_type,
    get_all_transaction_types,
    get_transaction_type_by_id,
    update_transaction_type,
)
from apps.reference.tests.factories import TransactionTypeFactory


class TransactionTypeServiceTests(TestCase):
    """Test suite for transaction type services."""

    def setUp(self):
        """Set up test data."""
        self.transaction_type_name = TransactionTypeEnum.INCOME.value
        self.transaction_type = TransactionTypeFactory(name=self.transaction_type_name)

    def test_get_all_transaction_types(self):
        """Test getting all transaction types returns all types in the database."""
        transaction_types = get_all_transaction_types()

        self.assertEqual(transaction_types.count(), 1)

        type_names = [transaction_type.name for transaction_type in transaction_types]
        self.assertIn(self.transaction_type_name, type_names)

    def test_get_transaction_type_by_id(self):
        """Test getting a transaction type by its ID."""
        retrieved_type = get_transaction_type_by_id(self.transaction_type.id)

        self.assertEqual(retrieved_type.id, self.transaction_type.id)
        self.assertEqual(retrieved_type.name, self.transaction_type_name)

    def test_get_transaction_type_by_id_not_found(self):
        """
        Test that getting a transaction type with a non-existent ID raises NotFound.
        """
        non_existent_id = 999

        with self.assertRaises(NotFound):
            get_transaction_type_by_id(non_existent_id)

    def test_create_transaction_type(self):
        """Test creating a new transaction type."""
        new_type_name = TransactionTypeEnum.EXPENSE.value
        new_type = create_transaction_type(new_type_name)

        self.assertEqual(new_type.name, new_type_name)

        self.assertTrue(TransactionType.objects.filter(name=new_type_name).exists())

    def test_update_transaction_type(self):
        """Test updating an existing transaction type."""
        updated_name = TransactionTypeEnum.EXPENSE.value
        updated_type = update_transaction_type(
            self.transaction_type.id, name=updated_name
        )

        self.assertEqual(updated_type.name, updated_name)

        self.transaction_type.refresh_from_db()
        self.assertEqual(self.transaction_type.name, updated_name)

    def test_update_transaction_type_not_found(self):
        """Test that updating a non-existent transaction type raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            update_transaction_type(non_existent_id, name="Doesn't Matter")

    def test_delete_transaction_type(self):
        """Test deleting a transaction type."""
        delete_transaction_type(self.transaction_type.id)

        self.assertFalse(
            TransactionType.objects.filter(id=self.transaction_type.id).exists()
        )

    def test_delete_transaction_type_not_found(self):
        """Test that deleting a non-existent transaction type raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            delete_transaction_type(non_existent_id)
