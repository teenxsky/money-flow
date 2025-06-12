from apps.reference.urls.category import category_patterns
from apps.reference.urls.status import status_patterns
from apps.reference.urls.subcategories import subcategory_patterns
from apps.reference.urls.transaction_type import transaction_type_patterns

__all__ = ['urlpatterns']

urlpatterns = [
    *status_patterns,
    *category_patterns,
    *transaction_type_patterns,
    *subcategory_patterns,
]
