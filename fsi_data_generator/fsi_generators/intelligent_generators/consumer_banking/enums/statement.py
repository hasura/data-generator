from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class StatementFormat(BaseEnum):
    """Formats for account statements."""
    PDF = auto()
    HTML = auto()
    TEXT = auto()
    CSV = auto()
    XML = auto()
    JSON = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        50.0,  # PDF
        20.0,  # HTML
        10.0,  # TEXT
        15.0,  # CSV
        3.0,   # XML
        2.0    # JSON
    ]


class CommunicationMethod(BaseEnum):
    """Methods for delivering account statements."""
    EMAIL = auto()
    MAIL = auto()
    PORTAL = auto()
    MOBILE_APP = auto()
    SMS_NOTIFICATION = auto()
    BRANCH_PICKUP = auto()
    MULTIPLE = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        45.0,  # EMAIL
        15.0,  # MAIL
        25.0,  # PORTAL
        10.0,  # MOBILE_APP
        2.0,   # SMS_NOTIFICATION
        1.0,   # BRANCH_PICKUP
        2.0    # MULTIPLE
    ]
