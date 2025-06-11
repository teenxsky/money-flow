from django.urls import include, path

from apps.reference.views.subcategory import (
    SubcategoryCreateView,
    SubcategoryDeleteView,
    SubcategoryDetailView,
    SubcategoryListView,
    SubcategoryUpdateView,
)

subcategory_patterns = [
    path(
        'subcategories/',
        include(
            [
                path('', SubcategoryListView.as_view(), name='subcategory-list'),
                path(
                    'create/',
                    SubcategoryCreateView.as_view(),
                    name='subcategory-create',
                ),
                path(
                    '<int:id>/',
                    SubcategoryDetailView.as_view(),
                    name='subcategory-detail',
                ),
                path(
                    '<int:id>/update/',
                    SubcategoryUpdateView.as_view(),
                    name='subcategory-update',
                ),
                path(
                    '<int:id>/delete/',
                    SubcategoryDeleteView.as_view(),
                    name='subcategory-delete',
                ),
            ]
        ),
        name='subcategory',
    )
]
