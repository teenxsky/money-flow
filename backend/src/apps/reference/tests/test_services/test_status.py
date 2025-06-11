from django.test import TestCase
from rest_framework.exceptions import NotFound

from apps.reference.enums import StatusEnum
from apps.reference.models import Status
from apps.reference.services.status import (
    create_status,
    delete_status,
    get_all_statuses,
    get_status_by_id,
    update_status,
)
from apps.reference.tests.factories import StatusFactory


class StatusServiceTests(TestCase):
    """Test suite for status services."""

    def setUp(self):
        """Set up test data."""
        self.status_name = StatusEnum.BUSINESS.value
        self.status = StatusFactory(name=self.status_name)

    def test_get_all_statuses(self):
        """Test getting all statuses returns all statuses in the database."""
        other_status = StatusFactory(name=StatusEnum.PERSONAL.value)

        statuses = get_all_statuses()

        self.assertEqual(statuses.count(), 2)

        status_names = [status.name for status in statuses]
        self.assertIn(self.status_name, status_names)
        self.assertIn(other_status.name, status_names)

    def test_get_status_by_id(self):
        """Test getting a status by its ID."""
        retrieved_status = get_status_by_id(self.status.id)

        self.assertEqual(retrieved_status.id, self.status.id)
        self.assertEqual(retrieved_status.name, self.status_name)

    def test_get_status_by_id_not_found(self):
        """Test that getting a status with a non-existent ID raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            get_status_by_id(non_existent_id)

    def test_create_status(self):
        """Test creating a new status."""
        new_status_name = StatusEnum.TAX.value
        new_status = create_status(new_status_name)

        self.assertEqual(new_status.name, new_status_name)

        self.assertTrue(Status.objects.filter(name=new_status_name).exists())

    def test_update_status(self):
        """Test updating an existing status."""
        updated_name = StatusEnum.TAX.value
        updated_status = update_status(self.status.id, name=updated_name)

        self.assertEqual(updated_status.name, updated_name)

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, updated_name)

    def test_update_status_not_found(self):
        """Test that updating a non-existent status raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            update_status(non_existent_id, name=StatusEnum.PERSONAL.value)

    def test_delete_status(self):
        """Test deleting a status."""
        delete_status(self.status.id)

        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_delete_status_not_found(self):
        """Test that deleting a non-existent status raises NotFound."""
        non_existent_id = 999

        with self.assertRaises(NotFound):
            delete_status(non_existent_id)
