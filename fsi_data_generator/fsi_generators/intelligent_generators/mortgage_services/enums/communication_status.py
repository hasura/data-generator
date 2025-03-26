from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class CommunicationStatus(BaseEnum):
    SENT = auto()
    DELIVERED = auto()
    FAILED = auto()
    RECEIVED = auto()
    READ = auto()
    PENDING = auto()
    DRAFT = auto()
    CANCELLED = auto()
    RETURNED = auto()
    OTHER = auto()
