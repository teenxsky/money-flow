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
    serializer_class = SubcategoryDetailSerializer

    @swagger_auto_schema(
        operation_summary='List all subcategories',
        operation_description='Returns a list of all transaction subcategories '
        'with their associated categories.',
        security=[],
        responses={200: serializer_class(many=True)},
    )
    def get(self, request: Request):
        subcategories = get_all_subcategories()
        serializer = self.serializer_class(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubcategoryDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SubcategoryDetailSerializer

    @swagger_auto_schema(
        operation_summary='Get subcategory details',
        operation_description='Retrieves detailed information about a specific '
        'subcategory by ID.',
        security=[],
        responses={
            200: serializer_class,
            400: openapi.Response(
                description='Validation error',
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
        serializer = self.serializer_class(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubcategoryCreateView(APIView):
    permission_classes = [IsAdminUser]
    in_serializer_class = SubcategorySerializer
    out_serializer_class = SubcategoryDetailSerializer

    @swagger_auto_schema(
        operation_summary='Create a new subcategory',
        operation_description='Creates a new transaction subcategory with the '
        'specified name and category. Requires admin privileges.',
        security=[{'Bearer': []}],
        request_body=in_serializer_class,
        responses={
            201: out_serializer_class,
            400: openapi.Response(
                description='Validation error',
            ),
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
            subcategory = create_subcategory(
                name=serializer.validated_data.get('name'),
                category=serializer.validated_data.get('category'),
            )
        except ValidationError as error:
            return Response(
                {'message': 'Validation error', 'error': error.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            self.out_serializer_class(subcategory).data,
            status=status.HTTP_201_CREATED,
        )


class SubcategoryUpdateView(APIView):
    permission_classes = [IsAdminUser]
    in_serializer_class = SubcategorySerializer
    out_serializer_class = SubcategoryDetailSerializer

    @swagger_auto_schema(
        operation_summary='Update a subcategory',
        operation_description='Updates an existing subcategory with new information. '
        'Requires admin privileges.',
        security=[{'Bearer': []}],
        request_body=in_serializer_class,
        responses={
            200: out_serializer_class,
            400: openapi.Response(
                description='Validation error',
            ),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
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
            self.out_serializer_class(updated_subcategory).data,
            status=status.HTTP_200_OK,
        )


class SubcategoryDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Delete a subcategory',
        operation_description='Deletes a subcategory by ID. Requires admin privileges.',
        security=[{'Bearer': []}],
        responses={
            204: openapi.Response(description='Subcategory deleted successfully'),
            400: openapi.Response(
                description='Validation error',
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
