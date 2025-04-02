from ....helpers import BaseEnum
from enum import auto


class DependencyType(BaseEnum):
    """
    Enum representing the types of dependencies in an application.
    """
    RUNTIME = auto()
    BUILD = auto()
    TEST = auto()
    DEVELOPMENT = auto()
    OPTIONAL = auto()
    PROVIDED = auto()
    SYSTEM = auto()
    IMPORT = auto()
    COMPILE = auto()
    ANNOTATION_PROCESSOR = auto()

    _DEFAULT_WEIGHTS = [
        30.0,  # RUNTIME
        20.0,  # BUILD
        15.0,  # TEST
        10.0,  # DEVELOPMENT
        5.0,   # OPTIONAL
        5.0,   # PROVIDED
        5.0,   # SYSTEM
        4.0,   # IMPORT
        4.0,   # COMPILE
        2.0    # ANNOTATION_PROCESSOR
    ]
