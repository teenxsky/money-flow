from django.urls import include, path

from apps.reference.views.subcategory import (
    SubcategoryDetailView,
    SubcategoryListCreateView,
)

subcategory_patterns = [
    path(
        'subcategories/',
        include(
            [
                path(
                    '',
                    SubcategoryListCreateView.as_view(),
                    name='subcategory-list-create',
                ),
                path(
                    '<int:id>/',
                    SubcategoryDetailView.as_view(),
                    name='subcategory-detail',
                ),
            ]
        ),
        name='subcategory',
    )
]
