from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class RelationshipType(BaseEnum):
    SPOUSE = auto()
    PARENT = auto()
    CHILD = auto()
    SIBLING = auto()
    FRIEND = auto()
    BUSINESS_PARTNER = auto()
    OTHER = auto()
