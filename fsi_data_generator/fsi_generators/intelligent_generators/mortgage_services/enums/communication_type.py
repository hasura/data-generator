from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class CommunicationType(BaseEnum):
    EMAIL = auto()
    LETTER = auto()
    PHONE_CALL = auto()
    SMS = auto()
    IN_PERSON = auto()
    PORTAL_MESSAGE = auto()
    VOICEMAIL = auto()
    FAX = auto()
    VIDEO_CALL = auto()
    CHAT = auto()
    OTHER = auto()
