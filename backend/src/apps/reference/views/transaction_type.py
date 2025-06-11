from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reference.serializers.transaction_type import (
    TransactionTypeDetailSerializer,
    TransactionTypeSerializer,
)
from apps.reference.services.transaction_type import (
    create_transaction_type,
    delete_transaction_type,
    get_all_transaction_types,
    get_transaction_type_by_id,
    update_transaction_type,
)


class TransactionTypeListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = TransactionTypeDetailSerializer

    @swagger_auto_schema(
        operation_summary='List all transaction types',
        operation_description='Returns a list of all transaction types.',
        security=[],
        responses={200: serializer_class(many=True)},
    )
    def get(self, request: Request):
        statuses = get_all_transaction_types()
        serializer = self.serializer_class(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionTypeDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = TransactionTypeDetailSerializer

    @swagger_auto_schema(
        operation_summary='Get transaction type details',
        operation_description='Retrieves detailed information about a specific '
        'transaction type by ID.',
        security=[],
        responses={
            200: serializer_class,
            404: openapi.Response(
                description='Transaction type not found',
            ),
        },
    )
    def get(self, request: Request, id: int):
        try:
            status_obj = get_transaction_type_by_id(id)
        except NotFound as error:
            return Response(
                {'message': 'Not found', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(status_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionTypeCreateView(APIView):
    permission_classes = [IsAdminUser]
    in_serializer_class = TransactionTypeSerializer
    out_serializer_class = TransactionTypeDetailSerializer

    @swagger_auto_schema(
        operation_summary='Create a new transaction type',
        operation_description='Creates a new transaction type with the specified name.'
        ' Requires admin privileges.',
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

        status_obj = create_transaction_type(name=serializer.validated_data.get('name'))
        return Response(
            self.out_serializer_class(status_obj).data,
            status=status.HTTP_201_CREATED,
        )


class TransactionTypeUpdateView(APIView):
    permission_classes = [IsAdminUser]
    in_serializer_class = TransactionTypeSerializer
    out_serializer_class = TransactionTypeDetailSerializer

    @swagger_auto_schema(
        operation_summary='Update a transaction type',
        operation_description='Updates an existing transaction type with '
        'new information. Requires admin privileges.',
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
            404: openapi.Response(
                description='Transaction type not found',
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
            updated_status = update_transaction_type(
                transaction_type_id=id,
                name=serializer.validated_data.get('name'),
            )
        except NotFound as error:
            return Response(
                {'message': 'Not found', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            self.out_serializer_class(updated_status).data,
            status=status.HTTP_200_OK,
        )


class TransactionTypeDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Delete a transaction type',
        operation_description='Deletes a transaction type by ID. '
        'Requires admin privileges.',
        security=[{'Bearer': []}],
        responses={
            204: openapi.Response(description='Transaction type deleted successfully'),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(
                description='Transaction type not found',
            ),
        },
    )
    def delete(self, request: Request, id: int):
        try:
            delete_transaction_type(id)
        except NotFound as error:
            return Response(
                {'message': 'Not found', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {'message': 'Transaction Type deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
        )
