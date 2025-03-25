from fsi_data_generator.fsi_generators.helpers import BaseEnum


class SubmissionChannel(BaseEnum):
    """Enum for submission channels."""
    ONLINE = "ONLINE"
    MOBILE_APP = "MOBILE_APP"
    BRANCH = "BRANCH"
    PHONE = "PHONE"
    MAIL = "MAIL"
    REFERRAL = "REFERRAL"
    BROKER = "BROKER"
    EMAIL = "EMAIL"
    OTHER = "OTHER"
