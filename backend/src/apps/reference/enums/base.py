from enum import Enum


class BaseEnum(Enum):
    """
    Base Enum class that extends the standard Enum functionality.
    Provides additional utility methods for working with enumeration values.

    Supports a special `MAP` attribute for defining relationships between enum values.

    Example (Mapping of subcategories to categories):
        ```python
        MAP = {
            VPS: CategoryEnum.INFRASTRUCTURE,
            PROXY: CategoryEnum.INFRASTRUCTURE,
            FARPOST: CategoryEnum.MARKETING,
            AVITO: CategoryEnum.MARKETING,
        }
        ```
    """

    @classmethod
    def values(cls):
        """
        Returns an array of names for all enum members.
        Excludes any member named `MAP` from the resulting array.

        Returns:
            list: A list of names for each enum member.
        """

        return [i.value for i in cls if i.name != 'MAP']
