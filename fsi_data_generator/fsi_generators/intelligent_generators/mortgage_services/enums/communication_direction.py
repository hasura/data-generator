from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class CommunicationDirection(BaseEnum):
    INBOUND = auto()
    OUTBOUND = auto()
    INTERNAL = auto()
