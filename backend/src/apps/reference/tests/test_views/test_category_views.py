from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.reference.enums.category import CategoryEnum
from apps.reference.enums.transaction_type import TransactionTypeEnum
from apps.reference.models import Category, TransactionType
from apps.reference.tests.factories import CategoryFactory, TransactionTypeFactory


class CategoryViewsTests(APITestCase):
    """Test suite for the Category views."""

    def setUp(self):
        """Set up test data."""
        self.list_url = reverse('category-list')
        self.create_url = reverse('category-create')

        self.transaction_type = TransactionTypeFactory(
            name=TransactionTypeEnum.EXPENSE.value
        )
        self.category = CategoryFactory(
            name=CategoryEnum.INFRASTRUCTURE.value,
            transaction_type=self.transaction_type,
        )

        self.detail_url = reverse('category-detail', args=[self.category.id])
        self.update_url = reverse('category-update', args=[self.category.id])
        self.delete_url = reverse('category-delete', args=[self.category.id])

        self.valid_payload = {
            'name': CategoryEnum.MARKETING.value,
            'transaction_type_id': self.transaction_type.id,
        }

        self.invalid_payload = {
            'name': 'Invalid Category Name',
            'transaction_type_id': self.transaction_type.id,
        }

        self.transaction_type_obj = TransactionType.objects.get(
            id=self.transaction_type.id
        )

    def test_get_all_categories(self):
        """Test retrieving all categories."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category.name)

    def test_get_single_category(self):
        """Test retrieving a single category."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

        self.assertIn('transaction_type_id', response.data)

    def test_create_valid_category(self):
        """Test creating a new category with valid data."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        initial_count = Category.objects.count()

        valid_payload = {
            'name': CategoryEnum.MARKETING.value,
            'transaction_type_id': self.transaction_type_obj.id,
        }

        response = self.client.post(self.create_url, valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), initial_count + 1)
        self.assertEqual(
            Category.objects.get(name=valid_payload['name']).name, valid_payload['name']
        )

    def test_create_invalid_category(self):
        """Test creating a new category with invalid data."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        initial_count = Category.objects.count()

        response = self.client.post(
            self.create_url, self.invalid_payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), initial_count)
        self.assertIn('errors', response.data)

    def test_update_category(self):
        """Test updating an existing category."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        update_payload = {
            'name': CategoryEnum.MARKETING.value,
            'transaction_type_id': self.transaction_type_obj.id,
        }

        response = self.client.put(self.update_url, update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, update_payload['name'])

    def test_delete_category(self):
        """Test deleting a category."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_unauthorized_create_category(self):
        """Test creating a category without admin privileges."""
        initial_count = Category.objects.count()

        response = self.client.post(self.create_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Category.objects.count(), initial_count)

    def test_unauthorized_update_category(self):
        """Test updating a category without admin privileges."""
        original_name = self.category.name
        update_payload = {
            'name': CategoryEnum.MARKETING.value,
            'transaction_type_id': self.transaction_type_obj.id,
        }

        response = self.client.put(self.update_url, update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, original_name)

    def test_unauthorized_delete_category(self):
        """Test deleting a category without admin privileges."""
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())
