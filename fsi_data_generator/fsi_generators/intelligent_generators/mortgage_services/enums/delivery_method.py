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

    _DEFAULT_WEIGHTS = [0.4, 0.3, 0.1, 0.15, 0.03, 0.02, 0.0]  # Favor EMAIL and MAIL
