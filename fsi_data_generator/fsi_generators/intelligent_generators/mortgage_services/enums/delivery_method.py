from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class DeliveryMethod(BaseEnum):
    EMAIL = auto()
    MAIL = auto()
    IN_PERSON = auto()
    ELECTRONIC_PORTAL = auto()
    COURIER = auto()
    FAX = auto()
    OTHER = auto()
