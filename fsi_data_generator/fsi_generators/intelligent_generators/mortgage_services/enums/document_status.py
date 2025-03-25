from fsi_data_generator.fsi_generators.helpers import BaseEnum


class DocumentStatus(BaseEnum):
    """
    Status values for mortgage document processing.
    Matches the DBML enum 'mortgage_services.document_status'.
    """
    PENDING = "PENDING"
    REVIEWED = "REVIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REQUIRES_REVISION = "REQUIRES_REVISION"
    IN_REVIEW = "IN_REVIEW"
    ARCHIVED = "ARCHIVED"
    EXPIRED = "EXPIRED"
    OTHER = "OTHER"
