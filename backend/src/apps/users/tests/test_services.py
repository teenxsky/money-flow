from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.services import login, logout, register
from apps.users.tests.factories import UserFactory


class RegisterServiceTests(TestCase):
    """Test suite for the register function in service."""

    def setUp(self):
        fake_user = UserFactory.build()

        self.email = fake_user.email
        self.password = fake_user.password
        self.first_name = fake_user.first_name
        self.last_name = fake_user.last_name

    def test_register_creates_user(self):
        """Test that calling register creates a new user in the database."""
        self.assertFalse(User.objects.filter(email=self.email).exists())

        register(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

        self.assertTrue(User.objects.filter(email=self.email).exists())

        user = User.objects.get(email=self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)

    def test_register_without_name(self):
        """
        Test that register works with empty first and last name.
        """
        register(email=self.email, password=self.password, first_name='', last_name='')

        user = User.objects.get(email=self.email)
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_register_duplicate_email_raises_error(self):
        """
        Test registration with an existing email address raises IntegrityError.
        """
        register(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

        with self.assertRaises(IntegrityError):
            register(
                email=self.email,
                password=self.password,
                first_name=self.first_name,
                last_name=self.last_name,
            )


class LoginServiceTests(TestCase):
    """
    Test suite for the login function in service.
    """

    def setUp(self):
        """
        Create a test user for login tests.
        """
        fake_user = UserFactory.build()

        self.email = fake_user.email
        self.password = fake_user.password
        self.user = User(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_login_success(self):
        """
        Test successful login returns access and refresh tokens.
        """
        tokens = login(email=self.email, password=self.password)

        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)
        self.assertTrue(tokens['access'])
        self.assertTrue(tokens['refresh'])

        refresh = RefreshToken(tokens['refresh'])
        self.assertEqual(refresh['user_id'], self.user.id)

    def test_login_invalid_email(self):
        """
        Test login with non-existent email raises AuthenticationFailed.
        """
        with self.assertRaises(AuthenticationFailed):
            login(email='wrong@example.com', password=self.password)

    def test_login_invalid_password(self):
        """
        Test login with incorrect password raises AuthenticationFailed.
        """
        with self.assertRaises(AuthenticationFailed):
            login(email=self.email, password='WrongPassword123')

    def test_login_inactive_user(self):
        """
        Test login with an inactive user raises AuthenticationFailed.
        """
        self.user.is_active = False
        self.user.save()

        with self.assertRaises(AuthenticationFailed):
            login(email=self.email, password=self.password)


class LogoutServiceTests(TransactionTestCase):
    """
    Test suite for the logout function in service.
    """

    def setUp(self):
        """
        Create a test user and get a refresh token for logout tests.
        """
        fake_user = UserFactory.build()

        self.email = fake_user.email
        self.password = fake_user.password
        self.user = User(email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        self.refresh = RefreshToken.for_user(self.user)
        self.refresh_token_str = str(self.refresh)

    def test_logout_blacklists_token(self):
        """
        Test that logout blacklists the refresh token.
        """
        logout(self.refresh_token_str)

        with self.assertRaises(TokenError):
            RefreshToken(self.refresh_token_str)

    def test_logout_invalid_token(self):
        """
        Test that logout with invalid token raises TokenError.
        """
        with self.assertRaises(TokenError):
            logout('invalid_token_string')

    def test_logout_blacklists_token_in_db(self):
        """
        Test that logout actually creates a BlacklistedToken record in the database.
        """
        token_jti = self.refresh['jti']

        logout(self.refresh_token_str)

        outstanding_token = OutstandingToken.objects.get(jti=token_jti)
        self.assertTrue(
            BlacklistedToken.objects.filter(token=outstanding_token).exists()
        )

    @override_settings(SIMPLE_JWT={'BLACKLIST_AFTER_ROTATION': False})
    def test_logout_works_with_blacklist_after_rotation_disabled(self):
        """
        Test that logout works even when BLACKLIST_AFTER_ROTATION is disabled.
        """
        logout(self.refresh_token_str)

        with self.assertRaises(TokenError):
            RefreshToken(self.refresh_token_str)

    def test_integration_login_then_logout(self):
        """
        Integration test for login followed by logout.
        """
        tokens = login(email=self.email, password=self.password)
        refresh_token = tokens['refresh']

        logout(refresh_token)

        with self.assertRaises(TokenError):
            RefreshToken(refresh_token)
