from django.test import TestCase
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.reference.tests.factories import (
    CategoryFactory,
    StatusFactory,
    SubcategoryFactory,
    TransactionTypeFactory,
)
from apps.transactions.models import Transaction
from apps.transactions.services import (
    create_transaction,
    delete_transaction,
    get_categories_for_transaction_type,
    get_subcategories_for_category,
    get_transaction_by_id,
    get_user_transactions,
    update_transaction,
)
from apps.transactions.tests.factories import (
    TransactionFactory,
)
from apps.users.tests.factories import UserFactory


class TransactionServiceTests(TestCase):
    """Test cases for transaction service layer functions."""

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.status = StatusFactory()
        self.transaction_type = TransactionTypeFactory()
        self.category = CategoryFactory(transaction_type=self.transaction_type)
        self.subcategory = SubcategoryFactory(category=self.category)

        self.transaction = TransactionFactory(
            user=self.user,
            status=self.status,
            transaction_type=self.transaction_type,
            category=self.category,
            subcategory=self.subcategory,
        )

    def test_get_user_transactions_returns_only_user_transactions(self):
        """
        Test that get_user_transactions returns only transactions for specified user.
        """
        TransactionFactory(user=self.other_user)
        transactions = get_user_transactions(self.user)
        self.assertEqual(transactions.count(), 1)
        self.assertEqual(transactions.first().user, self.user)

    def test_get_user_transactions_with_filters(self):
        """Test that get_user_transactions correctly applies filters."""
        t2 = TransactionFactory(user=self.user, amount=500)
        filters = {'amount__gte': 400}
        transactions = get_user_transactions(self.user, filters=filters)
        self.assertIn(t2, transactions)
        self.assertNotIn(
            self.transaction, transactions
        ) if self.transaction.amount < 400 else None

    def test_get_user_transactions_with_ordering(self):
        """Test that get_user_transactions correctly applies ordering."""
        _ = TransactionFactory(user=self.user)
        _ = TransactionFactory(user=self.user)
        transactions = get_user_transactions(self.user, ordering=['created_at'])
        transactions_list = list(transactions)
        self.assertGreaterEqual(len(transactions_list), 2)
        self.assertTrue(
            transactions_list[0].created_at <= transactions_list[1].created_at
        )

    def test_get_transaction_by_id_success(self):
        """Test successful retrieval of a transaction by ID."""
        tx = get_transaction_by_id(self.transaction.id, self.user)
        self.assertEqual(tx, self.transaction)

    def test_get_transaction_by_id_not_found(self):
        """Test that NotFound is raised when transaction ID doesn't exist."""
        with self.assertRaises(NotFound):
            get_transaction_by_id(999999, self.user)

    def test_get_transaction_by_id_permission_denied(self):
        """Test that PermissionDenied is raised when user doesn't own transaction."""
        with self.assertRaises(PermissionDenied):
            get_transaction_by_id(self.transaction.id, self.other_user)

    def test_create_transaction_success(self):
        """Test successful transaction creation."""
        data = {
            'status': self.status,
            'transaction_type': self.transaction_type,
            'category': self.category,
            'subcategory': self.subcategory,
            'amount': 1000,
            'comment': 'Test transaction',
        }
        tx = create_transaction(data, self.user)
        self.assertIsInstance(tx, Transaction)
        self.assertEqual(tx.user, self.user)
        self.assertEqual(tx.amount, 1000)

    def test_create_transaction_with_invalid_relationships(self):
        """
        Test that ValidationError is raised when relationships are invalid.
        """
        transaction_type = TransactionTypeFactory(name='EXPENSE')
        category1 = CategoryFactory(name='Cat1', transaction_type=transaction_type)
        category2 = CategoryFactory(name='Cat2', transaction_type=transaction_type)
        subcategory2 = SubcategoryFactory(name='Subcat2', category=category2)
        data = {
            'status': self.status,
            'transaction_type': transaction_type,
            'category': category1,
            'subcategory': subcategory2,
            'amount': 1000,
        }
        with self.assertRaises(ValidationError):
            create_transaction(data, self.user)

    def test_update_transaction_success(self):
        """Test successful transaction update."""
        new_comment = 'Updated comment'
        data = {'comment': new_comment}
        tx = update_transaction(self.transaction.id, data, self.user)
        self.assertEqual(tx.comment, new_comment)

    def test_update_transaction_not_found(self):
        """Test that NotFound is raised when updating non-existent transaction."""
        with self.assertRaises(NotFound):
            update_transaction(999999, {'comment': 'nope'}, self.user)

    def test_update_transaction_permission_denied(self):
        """
        Test that PermissionDenied is raised when user doesn't own the transaction.
        """
        with self.assertRaises(PermissionDenied):
            update_transaction(
                self.transaction.id, {'comment': 'nope'}, self.other_user
            )

    def test_update_transaction_with_invalid_relationships(self):
        transaction_type = TransactionTypeFactory(name='EXPENSE')
        category1 = CategoryFactory(name='Cat1', transaction_type=transaction_type)
        category2 = CategoryFactory(name='Cat2', transaction_type=transaction_type)
        unrelated_subcategory = SubcategoryFactory(name='Subcat2', category=category2)
        self.transaction.category = category1
        self.transaction.transaction_type = transaction_type
        self.transaction.save()
        data = {'subcategory': unrelated_subcategory}
        with self.assertRaises(ValidationError):
            update_transaction(self.transaction.id, data, self.user)

    def test_delete_transaction_success(self):
        """Test successful transaction deletion."""
        tx = TransactionFactory(user=self.user)
        delete_transaction(tx.id, self.user)
        self.assertFalse(Transaction.objects.filter(id=tx.id).exists())

    def test_delete_transaction_not_found(self):
        """Test that NotFound is raised when deleting non-existent transaction."""
        with self.assertRaises(NotFound):
            delete_transaction(999999, self.user)

    def test_delete_transaction_permission_denied(self):
        """Test that PermissionDenied is raised when user doesn't own transaction."""
        tx = TransactionFactory(user=self.other_user)
        with self.assertRaises(PermissionDenied):
            delete_transaction(tx.id, self.user)

    def test_get_subcategories_for_category(self):
        """Test that get_subcategories_for_category returns correct subcategories."""
        subcat1 = SubcategoryFactory(category=self.category)
        subcat2 = SubcategoryFactory(category=self.category)
        subcategories = get_subcategories_for_category(self.category.id)
        self.assertIn(subcat1, subcategories)
        self.assertIn(subcat2, subcategories)

    def test_get_categories_for_transaction_type(self):
        """Test that get_categories_for_transaction_type returns correct categories."""
        cat1 = CategoryFactory(transaction_type=self.transaction_type)
        cat2 = CategoryFactory(transaction_type=self.transaction_type)
        categories = get_categories_for_transaction_type(self.transaction_type.id)
        self.assertIn(cat1, categories)
        self.assertIn(cat2, categories)
