from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reference.serializers.status import (
    StatusDetailSerializer,
    StatusSerializer,
)
from apps.reference.services.status import (
    create_status,
    delete_status,
    get_all_statuses,
    get_status_by_id,
    update_status,
)


class StatusListCreateView(APIView):
    in_serializer_class = StatusSerializer
    out_serializer_class = StatusDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_summary='List all statuses',
        operation_description='Returns a list of all transaction statuses.',
        security=[],
        responses={200: out_serializer_class(many=True)},
    )
    def get(self, request: Request):
        statuses = get_all_statuses()
        serializer = self.out_serializer_class(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Create a new status',
        operation_description='Creates a new transaction status with '
        'the specified name. Requires admin privileges.',
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

        status_obj = create_status(name=serializer.validated_data.get('name'))
        return Response(
            self.out_serializer_class(status_obj).data,
            status=status.HTTP_201_CREATED,
        )


class StatusDetailView(APIView):
    in_serializer_class = StatusSerializer
    out_serializer_class = StatusDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_summary='Get status details',
        operation_description='Retrieves detailed information about '
        'a specific status by ID.',
        security=[],
        responses={
            200: in_serializer_class,
            404: openapi.Response(
                description='Status not found',
            ),
        },
    )
    def get(self, request: Request, id: int):
        try:
            status_obj = get_status_by_id(id)
        except NotFound as error:
            return Response(
                {'message': 'Not found', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.in_serializer_class(status_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Update a status',
        operation_description='Updates an existing status with '
        'new information. Requires admin privileges.',
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
            404: openapi.Response(
                description='Status not found',
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
            updated_status = update_status(
                status_id=id,
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

    @swagger_auto_schema(
        operation_summary='Delete a status',
        operation_description='Deletes a status by ID. Requires admin privileges.',
        security=[{'Bearer': []}],
        responses={
            204: openapi.Response(description='Status deleted successfully'),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(
                description='Status not found',
            ),
        },
    )
    def delete(self, request: Request, id: int):
        try:
            delete_status(id)
        except NotFound as error:
            return Response(
                {'message': 'Not found', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {'message': 'Status deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
        )
