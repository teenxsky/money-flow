from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.reference.serializers.status import (
    StatusCreateUpdateSerializer,
    StatusDetailSerializer,
)
from apps.reference.services.status import (
    create_status,
    delete_status,
    get_all_statuses,
    get_status_by_id,
    update_status,
)


class StatusListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = StatusDetailSerializer

    @swagger_auto_schema(
        operation_summary='List all statuses',
        operation_description='Returns a list of all transaction statuses.',
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
                                type=openapi.TYPE_STRING, example='Pending'
                            ),
                        },
                    ),
                ),
            )
        },
    )
    def get(self, request: Request):
        statuses = get_all_statuses()
        serializer = self.serializer_class(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatusDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = StatusDetailSerializer

    @swagger_auto_schema(
        operation_summary='Get status details',
        operation_description='Retrieves detailed information about '
        'a specific status by ID.',
        security=[],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Status ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description='Status found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Pending'
                        ),
                    },
                ),
            ),
            404: openapi.Response(
                description='Status not found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation failed'
                        ),
                        'errors': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Status with ID 999 not found',
                        ),
                    },
                ),
            ),
        },
    )
    def get(self, request: Request, id: int):
        try:
            status_obj = get_status_by_id(id)
        except NotFound as error:
            return Response(
                {'message': 'Validation failed', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(status_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatusCreateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = StatusCreateUpdateSerializer

    @swagger_auto_schema(
        operation_summary='Create a new status',
        operation_description='Creates a new transaction status with '
        'the specified name. Requires admin privileges.',
        security=[{'Bearer': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='Completed')
            },
        ),
        responses={
            201: openapi.Response(
                description='Status created successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Completed'
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

        status_obj = create_status(name=serializer.validated_data.get('name'))
        return Response(
            StatusDetailSerializer(status_obj).data,
            status=status.HTTP_201_CREATED,
        )


class StatusUpdateView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = StatusCreateUpdateSerializer

    @swagger_auto_schema(
        operation_summary='Update a status',
        operation_description='Updates an existing status with '
        'new information. Requires admin privileges.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Status ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='In Progress')
            },
        ),
        security=[{'Bearer': []}],
        responses={
            200: openapi.Response(
                description='Status updated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING, example='In Progress'
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
                            example={'name': ['Invalid status name.']},
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(
                description='Status not found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation failed'
                        ),
                        'errors': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Status with ID 999 not found',
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
            updated_status = update_status(
                status_id=id,
                name=serializer.validated_data.get('name'),
            )
        except NotFound as error:
            return Response(
                {'message': 'Validation failed', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            StatusDetailSerializer(updated_status).data,
            status=status.HTTP_200_OK,
        )


class StatusDeleteView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary='Delete a status',
        operation_description='Deletes a status by ID. Requires admin privileges.',
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='Status ID',
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            204: openapi.Response(description='Status deleted successfully'),
            401: openapi.Response(
                description='Authentication credentials not provided'
            ),
            404: openapi.Response(
                description='Status not found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING, example='Validation failed'
                        ),
                        'errors': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Status with ID 999 not found',
                        ),
                    },
                ),
            ),
        },
    )
    def delete(self, request: Request, id: int):
        try:
            delete_status(id)
        except NotFound as error:
            return Response(
                {'message': 'Validation failed', 'errors': error.detail},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {'message': 'Status deleted successfully'},
            status=status.HTTP_204_NO_CONTENT,
        )
