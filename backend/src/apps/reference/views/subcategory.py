from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reference.serializers.subcategory import (
    SubcategoryDetailSerializer,
    SubcategorySerializer,
)
from apps.reference.services.subcategory import (
    create_subcategory,
    delete_subcategory,
    get_all_subcategories,
    get_subcategory_by_id,
    update_subcategory,
)


class SubcategoryListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='List all subcategories',
        operation_description='Returns a list of all transaction subcategories '
        'with their associated categories.',
        security=[],
        responses={
            200: openapi.Response(
                description='Successful operation',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            'name': openapi.Schema(
                                type=openapi.TYPE_STRING, example='Groceries'
                            ),
                            'category': openapi.Schema(
                                type=openapi.TYPE_STRING, example='Food'
                            ),
                        },
                    ),
                ),
            )
        },
    )
    def get(self, request: Request):
        subcategories = get_all_subcategories()
        serializer = SubcategoryDetailSerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubcategoryDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Get subcategory details',
        operation_description='Retrieves detailed information about a specific '
        'subcategory by ID.',
        security=[],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Subcategory ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description='Subcategory found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Groceries'
                        ),
                        'category': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Food'
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
                            type=openapi.TYPE_STRING, example='Validation error'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Subcategory not found'
                        ),
                    },
                ),
            ),
        },
    )
    def get(self, request: Request, id: int):
        try:
            subcategory = get_subcategory_by_id(id)
        except ValidationError as error:
            return Response(
                {'message': 'Validation error', 'error': error.message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = SubcategoryDetailSerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubcategoryCreateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Create a new subcategory',
        operation_description='Creates a new transaction subcategory with the '
        'specified name and category. Requires admin privileges.',
        security=[{'Bearer': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'category_id'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='Groceries'),
                'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            },
        ),
        responses={
            201: openapi.Response(
                description='Subcategory created successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Groceries'
                        ),
                        'category': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Food'
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
                            type=openapi.TYPE_STRING, example='Validation error'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid subcategory name.',
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
        },
    )
    def post(self, request: Request):
        serializer = SubcategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subcategory = create_subcategory(
                name=serializer.validated_data.get('name'),
                category=serializer.validated_data.get('category'),
            )
            return Response(
                SubcategoryDetailSerializer(subcategory).data,
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as error:
            return Response(
                {'message': 'Validation error', 'error': error.message},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SubcategoryUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Update a subcategory',
        operation_description='Updates an existing subcategory with new information. '
        'Requires admin privileges.',
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Subcategory ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'category_id'],
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING, example='Organic Groceries'
                ),
                'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            },
        ),
        responses={
            200: openapi.Response(
                description='Subcategory updated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Organic Groceries'
                        ),
                        'category': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Food'
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
                            type=openapi.TYPE_STRING, example='Validation error'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid subcategory name.',
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
        },
    )
    def put(self, request: Request, id: int):
        serializer = SubcategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            updated_subcategory = update_subcategory(
                subcategory_id=id,
                name=serializer.validated_data.get('name'),
                category=serializer.validated_data.get('category'),
            )
        except ValidationError as error:
            return Response(
                {'message': 'Validation error', 'error': error.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            SubcategoryDetailSerializer(updated_subcategory).data,
            status=status.HTTP_200_OK,
        )


class SubcategoryDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Delete a subcategory',
        operation_description='Deletes a subcategory by ID. Requires admin privileges.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Subcategory ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        security=[{'Bearer': []}],
        responses={
            204: openapi.Response(description='Subcategory deleted successfully'),
            400: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation error'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Subcategory not found'
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
        },
    )
    def delete(self, request: Request, id: int):
        try:
            delete_subcategory(id)
        except ValidationError as error:
            return Response(
                {'message': 'Validation error', 'error': error.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': 'Subcategory deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
        )
