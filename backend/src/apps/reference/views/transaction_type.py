from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reference.serializers.transaction_type import (
    TransactionTypeCreateUpdateSerializer,
    TransactionTypeDetailSerializer,
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
                                type=openapi.TYPE_STRING, example='Income'
                            ),
                        },
                    ),
                ),
            )
        },
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
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Transaction Type ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description='Transaction type found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Income'
                        ),
                    },
                ),
            ),
            404: openapi.Response(
                description='Transaction type not found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation failed'
                        ),
                        'errors': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='TransactionType with ID 999 not found',
                        ),
                    },
                ),
            ),
        },
    )
    def get(self, request: Request, id: int):
        try:
            status_obj = get_transaction_type_by_id(id)
        except NotFound as error:
            return Response(
                {'message': 'Validation failed', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(status_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionTypeCreateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = TransactionTypeCreateUpdateSerializer

    @swagger_auto_schema(
        operation_summary='Create a new transaction type',
        operation_description='Creates a new transaction type with the specified name.'
        ' Requires admin privileges.',
        security=[{'Bearer': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='Expense')
            },
        ),
        responses={
            201: openapi.Response(
                description='Transaction type created successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Expense'
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
                        'errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={'name': ['This field is required.']},
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

        status_obj = create_transaction_type(name=serializer.validated_data.get('name'))
        return Response(
            TransactionTypeDetailSerializer(status_obj).data,
            status=status.HTTP_201_CREATED,
        )


class TransactionTypeUpdateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = TransactionTypeCreateUpdateSerializer

    @swagger_auto_schema(
        operation_summary='Update a transaction type',
        operation_description='Updates an existing transaction type with '
        'new information. Requires admin privileges.',
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Transaction Type ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='Transfer')
            },
        ),
        responses={
            200: openapi.Response(
                description='Transaction type updated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Transfer'
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
                        'errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            example={'name': ['Invalid transaction type name.']},
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(
                description='Transaction type not found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation failed'
                        ),
                        'errors': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='TransactionType with ID 999 not found',
                        ),
                    },
                ),
            ),
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
            updated_status = update_transaction_type(
                transaction_type_id=id,
                name=serializer.validated_data.get('name'),
            )
        except NotFound as error:
            return Response(
                {'message': 'Validation failed', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            TransactionTypeDetailSerializer(updated_status).data,
            status=status.HTTP_200_OK,
        )


class TransactionTypeDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Delete a transaction type',
        operation_description='Deletes a transaction type by ID. '
        'Requires admin privileges.',
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Transaction Type ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            204: openapi.Response(description='Transaction type deleted successfully'),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(
                description='Transaction type not found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation failed'
                        ),
                        'errors': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='TransactionType with ID 999 not found',
                        ),
                    },
                ),
            ),
        },
    )
    def delete(self, request: Request, id: int):
        try:
            delete_transaction_type(id)
        except NotFound as error:
            return Response(
                {'message': 'Validation failed', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {'message': 'Transaction Type deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
        )
