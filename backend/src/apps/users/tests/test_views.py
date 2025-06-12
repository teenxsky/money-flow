from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.tests.factories import UserFactory


class UserRegisterViewTests(APITransactionTestCase):
    """Test suite for the UserRegisterView."""

    def setUp(self):
        """Set up test data."""
        self.register_url = '/v1/users/register/'

        fake_user = UserFactory.build()
        self.email = fake_user.email
        self.password = fake_user.password
        self.first_name = fake_user.first_name
        self.last_name = fake_user.last_name

        self.valid_payload = {
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    def test_user_registration_success(self):
        """Test successful user registration."""
        initial_count = User.objects.count()

        response = self.client.post(
            self.register_url, self.valid_payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created!')
        self.assertEqual(User.objects.count(), initial_count + 1)

        user = User.objects.get(email=self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertTrue(user.check_password(self.password))

    def test_user_registration_invalid_data(self):
        """Test user registration with invalid data."""
        initial_count = User.objects.count()
        invalid_payload = {
            'email': self.email,
            # password is missing
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        response = self.client.post(self.register_url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('password', response.data['error'])
        self.assertEqual(User.objects.count(), initial_count)

    def test_user_registration_duplicate_email(self):
        """Test user registration with an email that already exists."""
        User.objects.create_user(
            email=self.valid_payload['email'], password=self.valid_payload['password']
        )
        initial_count = User.objects.count()

        response = self.client.post(
            self.register_url, self.valid_payload, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('email', response.data['error'])
        self.assertEqual(User.objects.count(), initial_count)


class UserLoginViewTests(APITransactionTestCase):
    """Test suite for the UserLoginView."""

    def setUp(self):
        """Set up test data."""
        self.login_url = '/v1/users/login/'

        fake_user = UserFactory.build()
        self.email = fake_user.email
        self.password = fake_user.password

        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.valid_payload = {'email': self.email, 'password': self.password}

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(self.login_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User logged in successfully!')
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        detail_response = self.client.get('/v1/users/me/')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(
            self.login_url,
            {'email': 'wrong@example.com', 'password': 'WrongPassword123!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get('error'),
            'Invalid credentials',
        )

    def test_login_invalid_data(self):
        """Test login with missing required fields."""
        invalid_payload = {
            'email': self.email,
            # password is missing
        }

        response = self.client.post(self.login_url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('password', response.data['error'])


class UserLogoutViewTests(APITransactionTestCase):
    """Test suite for the UserLogoutView."""

    def setUp(self):
        """Set up test data."""
        self.logout_url = '/v1/users/logout/'
        self.user = UserFactory.create()
        refresh = RefreshToken.for_user(self.user)
        self.valid_payload = {'refresh': str(refresh)}

    def test_logout_success(self):
        """Test successful logout."""
        response = self.client.post(self.logout_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User logged out successfully!')

        response = self.client.post(self.logout_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_missing_token(self):
        """Test logout with missing refresh token."""
        invalid_payload = {}  # Empty payload, refresh token is missing

        response = self.client.post(self.logout_url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('refresh', response.data['error'])


class UserDetailViewTests(APITestCase):
    """Test suite for the UserDetailView."""

    def setUp(self):
        """Set up test data."""
        self.detail_url = '/v1/users/me/'
        self.user = UserFactory.create()

    def test_get_user_details_authenticated(self):
        """Test getting user details when authenticated."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['id']), str(self.user.id))
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_get_user_details_unauthenticated(self):
        """Test getting user details without authentication."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserViewsIntegrationTests(APITransactionTestCase):
    """Integration tests for user views working together."""

    def setUp(self):
        """Set up test data."""
        self.register_url = '/v1/users/register/'
        self.login_url = '/v1/users/login/'
        self.logout_url = '/v1/users/logout/'
        self.detail_url = '/v1/users/me/'
        self.refresh_url = '/v1/users/refresh/'

        fake_user = UserFactory.build()
        self.user_data = {
            'email': fake_user.email,
            'password': fake_user.password,
            'first_name': fake_user.first_name,
            'last_name': fake_user.last_name,
        }

    def test_full_user_flow(self):
        """Test full user flow: register, login, get details, logout."""
        # Step 1: Register a new user
        register_response = self.client.post(
            self.register_url, self.user_data, format='json'
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # Step 2: Login with the new user
        login_response = self.client.post(
            self.login_url,
            {'email': self.user_data['email'], 'password': self.user_data['password']},
            format='json',
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)

        # Step 3: Get user details with the access token
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}'
        )
        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['email'], self.user_data['email'])

        # Step 4: Logout
        logout_response = self.client.post(
            self.logout_url, {'refresh': login_response.data['refresh']}, format='json'
        )
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        # Step 5: Verify refresh token is no longer valid
        refresh_response_after_logout = self.client.post(
            self.refresh_url, {'refresh': login_response.data['refresh']}
        )
        self.assertEqual(
            refresh_response_after_logout.status_code, status.HTTP_401_UNAUTHORIZED
        )
