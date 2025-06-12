from django.urls import include, path

from apps.reference.views.category import (
    CategoryDetailView,
    CategoryListCreateView,
)

category_patterns = [
    path(
        'categories/',
        include(
            [
                path('', CategoryListCreateView.as_view(), name='category-list-create'),
                path('<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
            ]
        ),
        name='category',
    )
]
