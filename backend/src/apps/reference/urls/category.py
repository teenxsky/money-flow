from django.urls import include, path

from apps.reference.views.category import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
)

category_patterns = [
    path(
        'categories/',
        include(
            [
                path('', CategoryListView.as_view(), name='category-list'),
                path('create/', CategoryCreateView.as_view(), name='category-create'),
                path('<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
                path(
                    '<int:id>/update/',
                    CategoryUpdateView.as_view(),
                    name='category-update',
                ),
                path(
                    '<int:id>/delete/',
                    CategoryDeleteView.as_view(),
                    name='category-delete',
                ),
            ]
        ),
        name='category',
    )
]
