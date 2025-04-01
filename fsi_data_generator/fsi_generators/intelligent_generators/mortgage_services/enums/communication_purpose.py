from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class CommunicationPurpose(BaseEnum):
    PAYMENT_REMINDER = auto()
    PAYMENT_CONFIRMATION = auto()
    ESCROW_ANALYSIS = auto()
    FORBEARANCE = auto()
    MODIFICATION = auto()
    DOCUMENT_REQUEST = auto()
    DOCUMENT_RECEIPT = auto()
    STATEMENT = auto()
    INSURANCE = auto()
    TAXES = auto()
    DEFAULT_NOTICE = auto()
    FORECLOSURE = auto()
    LOSS_MITIGATION = auto()
    GENERAL_INQUIRY = auto()
    COMPLAINT = auto()
    WELCOME = auto()
    REGULATORY = auto()
    OTHER = auto()
