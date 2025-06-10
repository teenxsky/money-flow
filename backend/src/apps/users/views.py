from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.serializers import (
    UserDetailSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserRegisterSerializer,
)
from apps.users.usecase import login, logout, register


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_data = serializer.validated_data
        register(
            email=user_data.get('email'),
            password=user_data.get('password'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
        )

        return Response({'message': 'User created!'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_data = serializer.validated_data
        try:
            tokens = login(
                email=user_data.get('email'), password=user_data.get('password')
            )
        except AuthenticationFailed as error:
            return Response(
                {'message': 'Authentication failed', 'error': error.detail},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {'message': 'User logged in successfully!', **tokens},
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLogoutSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh_token = serializer.validated_data.get('refresh')
        try:
            logout(refresh_token)
        except TokenError as error:
            return Response(
                {'message': 'Authentication failed', 'error': str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': 'User logged out successfully!'}, status=status.HTTP_200_OK
        )


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request: Request):
        data = self.serializer_class(request.user).data
        return Response(data, status=status.HTTP_200_OK)
