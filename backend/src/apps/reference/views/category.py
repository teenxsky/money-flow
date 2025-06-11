from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView

from apps.reference.serializers.category import (
    CategoryDetailSerializer,
    CategorySerializer,
)
from apps.reference.services.category import (
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    update_category,
)


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='List all categories',
        operation_description='Returns a list of all transaction categories with '
        'their associated transaction types.',
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
                                type=openapi.TYPE_STRING, example='Salary'
                            ),
                            'transaction_type': openapi.Schema(
                                type=openapi.TYPE_STRING, example='Income'
                            ),
                        },
                    ),
                ),
            )
        },
    )
    def get(self, request: Request):
        categories = get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Get category details',
        operation_description='Retrieves detailed information about '
        'a specific category by ID.',
        security=[],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Category ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: CategoryDetailSerializer,
            404: openapi.Response(description='Category not found'),
        },
    )
    def get(self, request: Request, id: int):
        category = get_category_by_id(id)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_summary='Create a new category',
        operation_description='Creates a new transaction category with '
        'the specified name and transaction type. Requires admin privileges.',
        security=[{'Bearer': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'transaction_type'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='Salary'),
                'transaction_type': openapi.Schema(
                    type=openapi.TYPE_INTEGER, example=1
                ),
            },
        ),
        responses={
            201: CategoryDetailSerializer,
            400: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation error'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={'name': ['Invalid category name.']},
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
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            category = create_category(
                name=serializer.validated_data.get('name'),
                transaction_type=serializer.validated_data.get('transaction_type'),
            )
        except ValidationError as error:
            return Response(
                {'message': 'Validation error', 'error': error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CategoryDetailSerializer(category).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryUpdateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_summary='Update a category',
        operation_description='Updates an existing category with new information. '
        'Requires admin privileges.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Category ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'transaction_type'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='Salary'),
                'transaction_type': openapi.Schema(
                    type=openapi.TYPE_INTEGER, example=1
                ),
            },
        ),
        security=[{'Bearer': []}],
        responses={
            200: CategoryDetailSerializer,
            400: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation error'
                        ),
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={'name': ['Invalid category name.']},
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(description='Category not found'),
        },
    )
    def put(self, request: Request, id: int):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            updated_category = update_category(
                category_id=id,
                name=serializer.validated_data.get('name'),
                transaction_type=serializer.validated_data.get('transaction_type'),
            )
            return Response(
                CategoryDetailSerializer(updated_category).data,
                status=status.HTTP_200_OK,
            )
        except ValidationError as error:
            return Response(
                {'message': 'Validation error', 'error': error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CategoryDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Delete a category',
        operation_description='Deletes a category by ID. Requires admin privileges.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Category ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        security=[{'Bearer': []}],
        responses={
            204: openapi.Response(description='Category deleted successfully'),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(description='Category not found'),
        },
    )
    def delete(self, request: Request, id: int):
        delete_category(id)
        return Response(
            {'message': 'Category deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
        )
