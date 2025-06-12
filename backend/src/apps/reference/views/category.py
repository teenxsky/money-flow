from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
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


class CategoryListCreateView(APIView):
    in_serializer_class = CategorySerializer
    out_serializer_class = CategoryDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_summary='List all categories',
        operation_description='Returns a list of all transaction categories with '
        'their associated transaction types.',
        security=[],
        responses={200: out_serializer_class(many=True)},
    )
    def get(self, request: Request):
        categories = get_all_categories()
        serializer = self.out_serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create a new category',
        operation_description='Creates a new transaction category with '
        'the specified name and transaction type. Requires admin privileges.',
        security=[{'Bearer': []}],
        request_body=in_serializer_class,
        responses={
            201: out_serializer_class,
            400: openapi.Response(description='Validation error'),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
        },
    )
    def post(self, request: Request):
        serializer = self.in_serializer_class(data=request.data)
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
            self.out_serializer_class(category).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryDetailView(APIView):
    in_serializer_class = CategorySerializer
    out_serializer_class = CategoryDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_summary='Get category details',
        operation_description='Retrieves detailed information about '
        'a specific category by ID.',
        security=[],
        responses={
            200: out_serializer_class,
            404: openapi.Response(description='Category not found'),
        },
    )
    def get(self, request: Request, id: int):
        try:
            category = get_category_by_id(id)
        except NotFound as error:
            return Response(
                {'message': 'Not found', 'error': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.out_serializer_class(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Update a category',
        operation_description='Updates an existing category with new information. '
        'Requires admin privileges.',
        request_body=in_serializer_class,
        security=[{'Bearer': []}],
        responses={
            200: out_serializer_class,
            400: openapi.Response(
                description='Validation error',
            ),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(description='Category not found'),
        },
    )
    def put(self, request: Request, id: int):
        serializer = self.in_serializer_class(data=request.data)
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
        except (ValidationError, NotFound) as error:
            if isinstance(error, NotFound):
                return Response(
                    {'message': 'Not found', 'error': error.detail},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {'message': 'Validation error', 'error': error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            self.out_serializer_class(updated_category).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary='Delete a category',
        operation_description='Deletes a category by ID. Requires admin privileges.',
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
        try:
            delete_category(id)
        except NotFound as error:
            return Response(
                {'message': 'Not found', 'error': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {'message': 'Category deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
        )
