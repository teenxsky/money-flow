from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.reference.enums.status import StatusEnum
from apps.reference.models import Status
from apps.reference.tests.factories import StatusFactory


class StatusViewsTests(APITestCase):
    """Test suite for the Status views."""

    def setUp(self):
        """Set up test data."""
        self.list_url = reverse('status-list')
        self.create_url = reverse('status-create')

        self.status_obj = StatusFactory(name=StatusEnum.BUSINESS.value)

        self.detail_url = reverse('status-detail', args=[self.status_obj.id])
        self.update_url = reverse('status-update', args=[self.status_obj.id])
        self.delete_url = reverse('status-delete', args=[self.status_obj.id])

        self.valid_payload = {
            'name': StatusEnum.PERSONAL.value,
        }

        self.invalid_payload = {
            'name': '',
        }

    def test_get_all_statuses(self):
        """Test retrieving all statuses."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.status_obj.name)

    def test_get_single_status(self):
        """Test retrieving a single status."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.status_obj.name)

    def test_create_valid_status(self):
        """Test creating a new status with valid data."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        initial_count = Status.objects.count()

        response = self.client.post(self.create_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), initial_count + 1)
        self.assertEqual(
            Status.objects.get(name=self.valid_payload['name']).name,
            self.valid_payload['name'],
        )

    def test_create_invalid_status(self):
        """Test creating a new status with invalid data."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        initial_count = Status.objects.count()

        invalid_data = {'name': ''}

        response = self.client.post(self.create_url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Status.objects.count(), initial_count)
        self.assertIn('errors', response.data)
        self.assertEqual(Status.objects.count(), initial_count)
        self.assertIn('errors', response.data)

    def test_update_status(self):
        """Test updating an existing status."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        update_payload = {
            'name': StatusEnum.TAX.value,
        }

        response = self.client.put(self.update_url, update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status_obj.refresh_from_db()
        self.assertEqual(self.status_obj.name, update_payload['name'])

    def test_delete_status(self):
        """Test deleting a status."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        self.client.force_authenticate(user=admin_user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Status.objects.filter(id=self.status_obj.id).exists())

    def test_unauthorized_create_status(self):
        """Test creating a status without admin privileges."""
        initial_count = Status.objects.count()

        response = self.client.post(self.create_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Status.objects.count(), initial_count)

    def test_unauthorized_update_status(self):
        """Test updating a status without admin privileges."""
        original_name = self.status_obj.name
        update_payload = {
            'name': StatusEnum.TAX.value,
        }

        response = self.client.put(self.update_url, update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.status_obj.refresh_from_db()
        self.assertEqual(self.status_obj.name, original_name)

    def test_unauthorized_delete_status(self):
        """Test deleting a status without admin privileges."""
        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Status.objects.filter(id=self.status_obj.id).exists())

    def test_get_nonexistent_status(self):
        """Test retrieving a non-existent status."""
        non_existent_url = reverse('status-detail', args=[999])

        response = self.client.get(non_existent_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
