from enum import Enum


class BorrowRelationshipType(Enum):
    SPOUSE = "SPOUSE"
    PARENT = "PARENT"
    CHILD = "CHILD"
    SIBLING = "SIBLING"
    FRIEND = "FRIEND"
    BUSINESS_PARTNER = "BUSINESS_PARTNER"
    OTHER = "OTHER"
