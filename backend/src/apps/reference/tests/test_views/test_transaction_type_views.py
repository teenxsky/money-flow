from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.reference.enums.transaction_type import TransactionTypeEnum
from apps.reference.models import TransactionType
from apps.reference.tests.factories import TransactionTypeFactory


class TransactionTypeViewsTests(APITestCase):
    """Test suite for the TransactionType views."""

    def setUp(self):
        """Set up test data."""
        self.list_url = reverse('transaction-type-list')
        self.create_url = reverse('transaction-type-create')

        self.transaction_type = TransactionTypeFactory(
            name=TransactionTypeEnum.INCOME.value
        )

        self.detail_url = reverse(
            'transaction-type-detail', args=[self.transaction_type.id]
        )
        self.update_url = reverse(
            'transaction-type-update', args=[self.transaction_type.id]
        )
        self.delete_url = reverse(
            'transaction-type-delete', args=[self.transaction_type.id]
        )

        self.valid_payload = {
            'name': TransactionTypeEnum.EXPENSE.value,
        }

        self.invalid_payload = {
            'name': '',
        }

    def test_get_all_transaction_types(self):
        """Test retrieving all transaction types."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.transaction_type.name)

    def test_get_single_transaction_type(self):
        """Test retrieving a single transaction type."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.transaction_type.name)

    def test_create_valid_transaction_type(self):
        """Test creating a new transaction type with valid data."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        initial_count = TransactionType.objects.count()

        response = self.client.post(self.create_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TransactionType.objects.count(), initial_count + 1)
        self.assertEqual(
            TransactionType.objects.get(name=self.valid_payload['name']).name,
            self.valid_payload['name'],
        )

    def test_create_invalid_transaction_type(self):
        """Test creating a new transaction type with invalid data."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        initial_count = TransactionType.objects.count()

        invalid_data = {'name': ''}

        response = self.client.post(self.create_url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TransactionType.objects.count(), initial_count)
        self.assertTrue('errors' in response.data or 'message' in response.data)

        def test_update_transaction_type(self):
            """Test updating an existing transaction type."""
            from django.contrib.auth import get_user_model

            User = get_user_model()
            admin_user = User.objects.create_superuser(
                email='admin@example.com', password='adminpassword'
            )
            self.client.force_authenticate(user=admin_user)

            update_payload = {
                'name': TransactionTypeEnum.INCOME.value,
            }

            response = self.client.put(self.update_url, update_payload, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.transaction_type.refresh_from_db()
            self.assertEqual(self.transaction_type.name, update_payload['name'])

    def test_delete_transaction_type(self):
        """Test deleting a transaction type."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            TransactionType.objects.filter(id=self.transaction_type.id).exists()
        )

    def test_unauthorized_update_transaction_type(self):
        """Test updating a transaction type without admin privileges."""
        original_name = self.transaction_type.name
        update_payload = {
            'name': TransactionTypeEnum.INCOME.value,
        }

        response = self.client.put(self.update_url, update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.transaction_type.refresh_from_db()
        self.assertEqual(self.transaction_type.name, original_name)

    def test_unauthorized_delete_transaction_type(self):
        """Test deleting a transaction type without admin privileges."""
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(
            TransactionType.objects.filter(id=self.transaction_type.id).exists()
        )

    def test_get_nonexistent_transaction_type(self):
        """Test retrieving a non-existent transaction type."""
        non_existent_url = reverse('transaction-type-detail', args=[999])

        response = self.client.get(non_existent_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
