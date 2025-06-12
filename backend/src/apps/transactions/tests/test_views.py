from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.reference.tests.factories import (
    CategoryFactory,
    StatusFactory,
    SubcategoryFactory,
    TransactionTypeFactory,
)
from apps.transactions.models import Transaction
from apps.transactions.tests.factories import TransactionFactory
from apps.users.tests.factories import UserFactory


class TransactionViewsTestCase(APITestCase):
    """Test suite for Transaction API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
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
        self.list_url = reverse('transaction-list-create')
        self.detail_url = lambda pk: reverse('transaction-detail', args=[pk])

    def test_list_transactions(self):
        """Test retrieving a list of transactions."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(any(tx['id'] == self.transaction.id for tx in response.data))

    def test_create_transaction(self):
        """Test creating a new transaction with valid data."""
        data = {
            'status_id': self.status.id,
            'transaction_type_id': self.transaction_type.id,
            'category_id': self.category.id,
            'subcategory_id': self.subcategory.id,
            'amount': '123.45',
            'comment': 'Test transaction',
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], '123.45')
        self.assertEqual(response.data['comment'], 'Test transaction')

    def test_create_transaction_invalid(self):
        """Test creating a transaction with invalid data fails."""
        transaction_type = TransactionTypeFactory(name='EXPENSE')
        category1 = CategoryFactory(name='Cat1', transaction_type=transaction_type)
        category2 = CategoryFactory(name='Cat2', transaction_type=transaction_type)
        subcategory2 = SubcategoryFactory(name='Subcat2', category=category2)
        data = {
            'status_id': self.status.id,
            'transaction_type_id': transaction_type.id,
            'category_id': category1.id,
            'subcategory_id': subcategory2.id,
            'amount': '123.45',
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertIn(
            response.status_code,
            (status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND),
        )

    def test_get_transaction_detail(self):
        """Test retrieving a specific transaction by ID."""
        response = self.client.get(self.detail_url(self.transaction.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.transaction.id)

    def test_update_transaction(self):
        """Test updating a transaction with valid data."""
        data = {'comment': 'Updated comment'}
        response = self.client.patch(
            self.detail_url(self.transaction.id), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], 'Updated comment')

    def test_update_transaction_invalid(self):
        """Test updating a transaction with invalid data fails."""
        transaction_type = TransactionTypeFactory(name='EXPENSE')
        category1 = CategoryFactory(name='Cat1', transaction_type=transaction_type)
        unrelated_category = CategoryFactory(
            name='Cat2', transaction_type=transaction_type
        )
        unrelated_subcategory = SubcategoryFactory(
            name='Subcat2', category=unrelated_category
        )
        self.transaction.category = category1
        self.transaction.transaction_type = transaction_type
        self.transaction.save()
        data = {'subcategory_id': unrelated_subcategory.id}
        response = self.client.patch(
            self.detail_url(self.transaction.id), data, format='json'
        )
        self.assertIn(
            response.status_code,
            (status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND),
        )

    def test_delete_transaction(self):
        """Test deleting a transaction removes it from the database."""
        response = self.client.delete(self.detail_url(self.transaction.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaction.objects.filter(id=self.transaction.id).exists())

    def test_permission_denied_for_other_user(self):
        """Test that users cannot access transactions that belong to other users."""
        other_user = UserFactory()
        self.client.force_authenticate(user=other_user)
        response = self.client.get(self.detail_url(self.transaction.id))
        self.assertIn(
            response.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
        )

    def test_unauthenticated_access(self):
        """Test that unauthenticated requests are rejected for all endpoints."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(self.list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.detail_url(self.transaction.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch(
            self.detail_url(self.transaction.id), {}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(self.detail_url(self.transaction.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
