from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class AppointmentStatus(BaseEnum):
    SCHEDULED = auto()
    RESCHEDULED = auto()
    CONFIRMED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    MISSED = auto()
    PENDING = auto()
