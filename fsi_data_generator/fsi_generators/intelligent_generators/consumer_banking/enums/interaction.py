from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class InteractionType(BaseEnum):
    """Types of customer interactions."""
    PHONE_CALL = auto()
    EMAIL = auto()
    CHAT = auto()
    IN_PERSON = auto()
    VIDEO_CALL = auto()
    ONLINE_FORM = auto()
    SOCIAL_MEDIA = auto()
    ATM_INTERACTION = auto()
    MOBILE_APP = auto()
    MAIL = auto()
    SMS = auto()
    FAX = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # PHONE_CALL
        25.0,  # EMAIL
        15.0,  # CHAT
        10.0,  # IN_PERSON
        5.0,   # VIDEO_CALL
        5.0,   # ONLINE_FORM
        3.0,   # SOCIAL_MEDIA
        2.0,   # ATM_INTERACTION
        3.0,   # MOBILE_APP
        1.0,   # MAIL
        1.0,   # SMS
        0.5    # FAX
    ]


class InteractionChannel(BaseEnum):
    """Channels through which customer interactions occur."""
    PHONE = auto()
    EMAIL = auto()
    WEB = auto()
    BRANCH = auto()
    MOBILE_APP = auto()
    ATM = auto()
    MAIL = auto()
    SOCIAL_MEDIA = auto()
    VIDEO = auto()
    SMS = auto()
    THIRD_PARTY = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # PHONE
        25.0,  # EMAIL
        15.0,  # WEB
        10.0,  # BRANCH
        8.0,   # MOBILE_APP
        4.0,   # ATM
        2.0,   # MAIL
        2.0,   # SOCIAL_MEDIA
        2.0,   # VIDEO
        1.5,   # SMS
        0.5    # THIRD_PARTY
    ]


class InteractionStatus(BaseEnum):
    """Status of customer interactions."""
    OPEN = auto()
    PENDING = auto()
    IN_PROGRESS = auto()
    RESOLVED = auto()
    ESCALATED = auto()
    TRANSFERRED = auto()
    CLOSED = auto()
    FOLLOW_UP = auto()
    REOPENED = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # OPEN
        15.0,  # PENDING
        20.0,  # IN_PROGRESS
        30.0,  # RESOLVED
        5.0,   # ESCALATED
        5.0,   # TRANSFERRED
        20.0,  # CLOSED
        5.0,   # FOLLOW_UP
        5.0    # REOPENED
    ]


class InteractionPriority(BaseEnum):
    """Priority levels for customer interactions."""
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    ROUTINE = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        5.0,   # CRITICAL
        15.0,  # HIGH
        40.0,  # MEDIUM
        30.0,  # LOW
        10.0   # ROUTINE
    ]
