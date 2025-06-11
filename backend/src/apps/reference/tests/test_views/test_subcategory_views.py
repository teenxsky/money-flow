from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.reference.enums.category import CategoryEnum
from apps.reference.enums.subcategory import SubcategoryEnum
from apps.reference.enums.transaction_type import TransactionTypeEnum
from apps.reference.models import Category, Subcategory
from apps.reference.tests.factories import (
    CategoryFactory,
    SubcategoryFactory,
    TransactionTypeFactory,
)


class SubcategoryViewsTests(APITestCase):
    """Test suite for the Subcategory views."""

    def setUp(self):
        """Set up test data."""
        self.list_url = reverse('subcategory-list')
        self.create_url = reverse('subcategory-create')

        self.transaction_type = TransactionTypeFactory(
            name=TransactionTypeEnum.EXPENSE.value
        )
        self.category = CategoryFactory(
            name=CategoryEnum.INFRASTRUCTURE.value,
            transaction_type=self.transaction_type,
        )
        self.subcategory = SubcategoryFactory(
            name=SubcategoryEnum.VPS.value, category=self.category
        )

        self.detail_url = reverse('subcategory-detail', args=[self.subcategory.id])
        self.update_url = reverse('subcategory-update', args=[self.subcategory.id])
        self.delete_url = reverse('subcategory-delete', args=[self.subcategory.id])

        self.valid_payload = {
            'name': SubcategoryEnum.PROXY.value,
            'category_id': self.category.id,
        }

        self.invalid_payload = {
            'name': 'Invalid Subcategory Name',
            'category_id': self.category.id,
        }

        self.category_obj = Category.objects.get(id=self.category.id)

    def test_get_all_subcategories(self):
        """Test retrieving all subcategories."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.subcategory.name)

    def test_get_single_subcategory(self):
        """Test retrieving a single subcategory."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.subcategory.name)
        self.assertEqual(response.data['category'], self.category.name)

    def test_create_valid_subcategory(self):
        """Test creating a new subcategory with valid data."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        initial_count = Subcategory.objects.count()

        valid_payload = {
            'name': SubcategoryEnum.PROXY.value,
            'category_id': self.category.id,
        }

        response = self.client.post(self.create_url, valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subcategory.objects.count(), initial_count + 1)
        self.assertEqual(
            Subcategory.objects.get(name=valid_payload['name']).name,
            valid_payload['name'],
        )

    def test_create_invalid_subcategory(self):
        """Test creating a new subcategory with invalid data."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        initial_count = Subcategory.objects.count()

        response = self.client.post(
            self.create_url, self.invalid_payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Subcategory.objects.count(), initial_count)
        self.assertTrue('errors' in response.data or 'error' in response.data)

    def test_update_subcategory(self):
        """Test updating an existing subcategory."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        marketing_category = CategoryFactory(
            name=CategoryEnum.MARKETING.value, transaction_type=self.transaction_type
        )

        update_payload = {
            'name': SubcategoryEnum.FARPOST.value,
            'category_id': marketing_category.id,
        }

        response = self.client.put(self.update_url, update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subcategory.refresh_from_db()
        self.assertEqual(self.subcategory.name, update_payload['name'])

    def test_delete_subcategory(self):
        """Test deleting a subcategory."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subcategory.objects.filter(id=self.subcategory.id).exists())

    def test_unauthorized_create_subcategory(self):
        """Test creating a subcategory without admin privileges."""
        initial_count = Subcategory.objects.count()

        response = self.client.post(self.create_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Subcategory.objects.count(), initial_count)

    def test_unauthorized_update_subcategory(self):
        """Test updating a subcategory without admin privileges."""
        original_name = self.subcategory.name

        marketing_category = CategoryFactory(
            name=CategoryEnum.MARKETING.value, transaction_type=self.transaction_type
        )

        update_payload = {
            'name': SubcategoryEnum.FARPOST.value,
            'category_id': marketing_category.id,
        }

        response = self.client.put(self.update_url, update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.subcategory.refresh_from_db()
        self.assertEqual(self.subcategory.name, original_name)

    def test_unauthorized_delete_subcategory(self):
        """Test deleting a subcategory without admin privileges."""
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Subcategory.objects.filter(id=self.subcategory.id).exists())

    def test_create_duplicate_subcategory(self):
        """Test creating a subcategory that already exists."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        duplicate_payload = {
            'name': self.subcategory.name,
            'category_id': self.category.id,
        }

        response = self.client.post(self.create_url, duplicate_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('errors' in response.data or 'error' in response.data)
