from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


def register(email: str, password: str, first_name: str, last_name: str) -> None:
    """
    Register a new user in the system.

    Args:
        email (str): User's email address.
        password (str): User's password.
        first_name (str): User's first name.
        last_name (str): User's last name.

    Returns:
        None
    """
    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()


def login(email: str, password: str) -> dict[str, str]:
    """
    Authenticate a user with their email and password.

    Args:
        email (str): User's email address.
        password (str): User's password.

    Returns:
        dict[str, str]: Dictionary containing access and refresh tokens.
            - 'access': JWT access token for authentication
            - 'refresh': JWT refresh token for obtaining new access tokens

    Raises:
        AuthenticationFailed: If the credentials are invalid.
    """
    user = authenticate(
        email=email,
        password=password,
    )

    if user is None:
        raise AuthenticationFailed('Invalid credentials')

    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def logout(refresh_token: str) -> None:
    """
    Logs out a user by blacklisting their refresh token and related access tokens.

    This prevents both the refresh token and all access tokens associated with the user
    from being used, effectively logging the user out of the system immediately.

    Args:
        refresh_token (str): The JWT refresh token to blacklist.

    Returns:
        None

    Raises:
        TokenError: If the refresh token is invalid.
    """
    refresh = RefreshToken(refresh_token)
    user_id = refresh.payload['user_id']

    refresh.blacklist()

    tokens = OutstandingToken.objects.filter(user_id=user_id)
    for token in tokens:
        _, _ = BlacklistedToken.objects.get_or_create(token=token)
