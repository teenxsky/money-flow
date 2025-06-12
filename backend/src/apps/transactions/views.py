from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.transactions.serializers import (
    TransactionCreateSerializer,
    TransactionDetailSerializer,
    TransactionListSerializer,
    TransactionUpdateSerializer,
)
from apps.transactions.services import (
    create_transaction,
    delete_transaction,
    get_transaction_by_id,
    get_user_transactions,
    update_transaction,
)


class TransactionListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Get
    list_serializer_class = TransactionListSerializer

    # Post
    create_in_serializer_class = TransactionCreateSerializer
    create_out_serializer_class = TransactionDetailSerializer

    @swagger_auto_schema(
        operation_summary='List user transactions',
        operation_description='Returns a list of all transactions '
        'for the authenticated user.',
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'created_at__gte',
                openapi.IN_QUERY,
                description='Filter by created date greater than or equal to',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                'created_at__lte',
                openapi.IN_QUERY,
                description='Filter by created date less than or equal to',
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description='Filter by status ID',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'transaction_type',
                openapi.IN_QUERY,
                description='Filter by transaction type ID',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description='Filter by category ID',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'subcategory',
                openapi.IN_QUERY,
                description='Filter by subcategory ID',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'amount__gte',
                openapi.IN_QUERY,
                description='Filter by amount greater than or equal to',
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                'amount__lte',
                openapi.IN_QUERY,
                description='Filter by amount less than or equal to',
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description='Order results by field (prefix with - for descending)',
                type=openapi.TYPE_STRING,
                enum=['created_at', '-created_at', 'amount', '-amount'],
            ),
        ],
        responses={
            200: list_serializer_class(many=True),
            401: 'Authentication credentials were not provided.',
        },
    )
    def get(self, request):
        filters = {}
        for param in [
            'created_at__gte',
            'created_at__lte',
            'created_at__exact',
            'status',
            'transaction_type',
            'category',
            'subcategory',
            'amount__gte',
            'amount__lte',
            'amount__exact',
        ]:
            if param in request.query_params:
                filters[param] = request.query_params.get(param)

        ordering = None
        if 'ordering' in request.query_params:
            ordering_param = request.query_params.get('ordering')
            valid_fields = ['created_at', '-created_at', 'amount', '-amount']
            if ordering_param in valid_fields:
                ordering = [ordering_param]
        else:
            ordering = ['-created_at']

        transactions = get_user_transactions(
            user=request.user, filters=filters, ordering=ordering
        )

        serializer = self.list_serializer_class(transactions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Create a transaction',
        operation_description='Creates a new transaction for the authenticated user.',
        security=[{'Bearer': []}],
        request_body=create_in_serializer_class,
        responses={
            201: create_out_serializer_class,
            400: 'Invalid data provided',
            401: 'Authentication credentials were not provided.',
        },
    )
    def post(self, request):
        serializer = self.create_in_serializer_class(
            data=request.data, context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            transaction = create_transaction(
                data=serializer.validated_data, user=request.user
            )
        except ValidationError as error:
            return Response(
                {'message': 'Validation failed', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            self.create_out_serializer_class(transaction).data,
            status=status.HTTP_201_CREATED,
        )


class TransactionDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    in_serializer_class = TransactionUpdateSerializer
    out_serializer_class = TransactionDetailSerializer

    @swagger_auto_schema(
        operation_summary='Get transaction details',
        operation_description='Returns detailed information about '
        'a specific transaction.',
        security=[{'Bearer': []}],
        responses={
            200: out_serializer_class,
            401: 'Authentication credentials were not provided.',
            403: "You don't have permission to access this transaction.",
            404: 'Transaction not found.',
        },
    )
    def get(self, request, id):
        try:
            transaction = get_transaction_by_id(transaction_id=id, user=request.user)
        except (NotFound, PermissionDenied) as error:
            if isinstance(error, NotFound):
                return Response(
                    {'message': 'Not found', 'error': error.detail},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {'message': 'Permission denied', 'error': error.detail},
                status=status.HTTP_403_FORBIDDEN,
            )

        transaction = get_transaction_by_id(transaction_id=id, user=request.user)
        return Response(
            self.out_serializer_class(transaction).data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary='Update a transaction',
        operation_description='Updates an existing transaction with new information.',
        security=[{'Bearer': []}],
        request_body=in_serializer_class,
        responses={
            200: out_serializer_class,
            400: 'Invalid data provided',
            401: 'Authentication credentials were not provided.',
            403: "You don't have permission to modify this transaction.",
            404: 'Transaction not found.',
        },
    )
    def patch(self, request, id):
        transaction = get_transaction_by_id(transaction_id=id, user=request.user)
        serializer = self.in_serializer_class(
            transaction, data=request.data, partial=True
        )

        if not serializer.is_valid():
            return Response(
                {'message': 'Validation failed', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            updated_transaction = update_transaction(
                transaction_id=id, data=serializer.validated_data, user=request.user
            )
        except (NotFound, PermissionDenied, ValidationError) as error:
            if isinstance(error, NotFound):
                return Response(
                    {'message': 'Transaction not found', 'errors': error.detail},
                    status=status.HTTP_404_NOT_FOUND,
                )
            elif isinstance(error, PermissionDenied):
                return Response(
                    {'message': 'Permission denied', 'errors': error.detail},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return Response(
                {'message': 'Validation failed', 'errors': error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            self.out_serializer_class(updated_transaction).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary='Delete a transaction',
        operation_description='Deletes a specific transaction.',
        security=[{'Bearer': []}],
        responses={
            204: 'Transaction deleted successfully',
            401: 'Authentication credentials were not provided.',
            403: "You don't have permission to delete this transaction.",
            404: 'Transaction not found.',
        },
    )
    def delete(self, request, id):
        try:
            delete_transaction(transaction_id=id, user=request.user)
        except (NotFound, PermissionDenied) as error:
            if isinstance(error, NotFound):
                return Response(
                    {'message': 'Not found', 'error': error.detail},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {'message': 'Permission denied', 'error': error.detail},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
