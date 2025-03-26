from .auto_name import AutoName
from .enum_utilities import EnumUtilities


class BaseEnum(EnumUtilities, AutoName):
    """
    Base class for Enums that combines auto() functionality
    (name-as-value) with utility methods (e.g., get_random()).
    """
    pass
