from fsi_data_generator.fsi_generators.helpers import BaseEnum


class ApplicationStatus(BaseEnum):
    """Enum for mortgage application statuses."""
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    ADDITIONAL_INFO_REQUIRED = "ADDITIONAL_INFO_REQUIRED"
    CONDITIONAL_APPROVAL = "CONDITIONAL_APPROVAL"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    WITHDRAWN = "WITHDRAWN"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"
