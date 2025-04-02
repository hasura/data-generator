from ....helpers import BaseEnum
from enum import auto


class RelationshipType(BaseEnum):
    """
    Enum representing the types of relationships between applications.
    """
    AUTHORIZATION = auto()
    AUTHENTICATION = auto()
    DATA_ACCESS = auto()
    SERVICE_DEPENDENCY = auto()
    API_INTEGRATION = auto()
    CONFIGURATION_PROVIDER = auto()
    LOGGING_SERVICE = auto()
    MONITORING_SERVICE = auto()
    CACHING_SERVICE = auto()
    MESSAGING_QUEUE = auto()
    REPORTING_SERVICE = auto()
    DATA_PROCESSING = auto()
    UI_EMBEDDING = auto()
    WORKFLOW_TRIGGER = auto()
    EVENT_SUBSCRIPTION = auto()
    NOTIFICATION_SERVICE = auto()
    IDENTITY_MANAGEMENT = auto()
    PAYMENT_PROCESSING = auto()
    STORAGE_SERVICE = auto()
    SEARCH_SERVICE = auto()
    SECURITY_SCANNING = auto()
    AUDIT_LOGGING = auto()
    RESOURCE_MANAGEMENT = auto()
    TASK_SCHEDULING = auto()
    CONTENT_DELIVERY = auto()

    _DEFAULT_WEIGHTS = [
        8.0,   # AUTHORIZATION
        10.0,  # AUTHENTICATION
        15.0,  # DATA_ACCESS
        12.0,  # SERVICE_DEPENDENCY
        15.0,  # API_INTEGRATION
        5.0,   # CONFIGURATION_PROVIDER
        7.0,   # LOGGING_SERVICE
        7.0,   # MONITORING_SERVICE
        5.0,   # CACHING_SERVICE
        8.0,   # MESSAGING_QUEUE
        6.0,   # REPORTING_SERVICE
        8.0,   # DATA_PROCESSING
        4.0,   # UI_EMBEDDING
        4.0,   # WORKFLOW_TRIGGER
        5.0,   # EVENT_SUBSCRIPTION
        5.0,   # NOTIFICATION_SERVICE
        6.0,   # IDENTITY_MANAGEMENT
        4.0,   # PAYMENT_PROCESSING
        7.0,   # STORAGE_SERVICE
        4.0,   # SEARCH_SERVICE
        3.0,   # SECURITY_SCANNING
        5.0,   # AUDIT_LOGGING
        5.0,   # RESOURCE_MANAGEMENT
        4.0,   # TASK_SCHEDULING
        3.0    # CONTENT_DELIVERY
    ]
