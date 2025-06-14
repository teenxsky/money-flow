from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
from apps.users.services import login, logout, register


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        operation_summary='Register a new user',
        operation_description='Creates a new user account with email, password, '
        'and optional name details',
        security=[],
        request_body=serializer_class,
        responses={
            201: openapi.Response(
                description='User created successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='User created!'
                        )
                    },
                ),
            ),
            400: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation failed'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={'email': ['This field is required.']},
                        ),
                    },
                ),
            ),
        },
    )
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

    @swagger_auto_schema(
        operation_summary='Log in a user',
        operation_description='Authenticates a user with email and password, '
        'returns access and refresh tokens',
        security=[],
        request_body=serializer_class,
        responses={
            200: openapi.Response(
                description='User logged in successfully with tokens',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='User logged in successfully!',
                        ),
                        'access': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='eyJ0eXAiOiJKV1QiLCJhbGci...',
                        ),
                        'refresh': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='eyJ0eXAiOiJKV1QiLCJhbGci...',
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation failed'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={'email': ['This field is required.']},
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description='Authentication failed',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Authentication failed'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Invalid credentials'
                        ),
                    },
                ),
            ),
        },
    )
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

    @swagger_auto_schema(
        operation_summary='Log out a user',
        operation_description="Blacklists the user's refresh token, "
        'effectively logging them out',
        security=[],
        request_body=serializer_class,
        responses={
            200: openapi.Response(
                description='User logged out successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='User logged out successfully!',
                        )
                    },
                ),
            ),
            400: openapi.Response(
                description='Invalid token or validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Authentication failed'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Token is invalid or expired',
                        ),
                    },
                ),
            ),
        },
    )
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

    @swagger_auto_schema(
        operation_summary='Get user details',
        operation_description='Retrieves details of the currently authenticated user',
        security=[{'Bearer': []}],
        responses={
            200: openapi.Response(
                description='User details retrieved successfully',
                schema=serializer_class,
            ),
            401: openapi.Response(
                description='Authentication credentials were not provided',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Authentication credentials were not provided.',
                        )
                    },
                ),
            ),
        },
    )
    def get(self, request: Request):
        data = self.serializer_class(request.user).data
        return Response(data, status=status.HTTP_200_OK)
