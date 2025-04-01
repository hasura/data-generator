from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class ClosingType(BaseEnum):
    IN_PERSON = auto()
    HYBRID = auto()
    REMOTE = auto()
    MAIL_AWAY = auto()
    ESCROW = auto()
    POWER_OF_ATTORNEY = auto()
    DRY_CLOSING = auto()
    WET_CLOSING = auto()
