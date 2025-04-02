import random
from typing import Any, Dict

from data_generator import DataGenerator
from .enums import RelationshipType, CriticalityLevel


def generate_random_application_relationship(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt application_relationship record with reasonable values.

    This creates a relationship between two applications without generating any ID fields
    or foreign keys.

    Args:
        _id_fields: Dictionary containing the required ID fields
                  (app_mgmt_application_relationship_id, application_id_1, application_id_2)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated application relationship data
        (without ID fields or FK fields)
    """
    # Generate relationship descriptions based on the relationship type
    descriptions = {
        RelationshipType.AUTHORIZATION: [
            "Validates user permissions for accessing restricted functionality",
            "Provides role-based access control for sensitive operations",
            "Handles authorization tokens and permissions checking"
        ],
        RelationshipType.AUTHENTICATION: [
            "Verifies user identities through multi-factor authentication",
            "Manages user login and session management",
            "Provides single sign-on capabilities across applications"
        ],
        RelationshipType.DATA_ACCESS: [
            "Retrieves customer financial data required for processing",
            "Provides backend data access to core banking records",
            "Acts as the system of record for account information"
        ],
        RelationshipType.SERVICE_DEPENDENCY: [
            "Delivers core business logic for transaction processing",
            "Provides essential services for compliance checking",
            "Handles critical calculations for financial operations"
        ],
        RelationshipType.API_INTEGRATION: [
            "Exposes REST APIs consumed by this application",
            "Provides data interface through GraphQL endpoints",
            "Handles API authentication and rate limiting"
        ],
        RelationshipType.CONFIGURATION_PROVIDER: [
            "Delivers centralized configuration settings",
            "Manages environment-specific application parameters",
            "Controls feature flags and system behaviors"
        ],
        RelationshipType.LOGGING_SERVICE: [
            "Centralizes application logging for auditing purposes",
            "Maintains required regulatory log records",
            "Stores transaction logs with PII protections"
        ],
        RelationshipType.MONITORING_SERVICE: [
            "Tracks application health metrics and alerts on issues",
            "Provides real-time monitoring of system performance",
            "Detects anomalies in transaction patterns"
        ],
        RelationshipType.CACHING_SERVICE: [
            "Provides high-speed caching to improve performance",
            "Reduces database load through distributed caching",
            "Manages session state information"
        ],
        RelationshipType.MESSAGING_QUEUE: [
            "Handles asynchronous communication between services",
            "Ensures reliable message delivery for critical operations",
            "Manages work queues for batch processing"
        ],
        RelationshipType.REPORTING_SERVICE: [
            "Generates regulatory compliance reports",
            "Provides business intelligence dashboards",
            "Creates customer-facing account statements"
        ],
        RelationshipType.DATA_PROCESSING: [
            "Performs ETL operations on transaction data",
            "Handles real-time data transformation",
            "Processes raw data into actionable information"
        ],
        RelationshipType.UI_EMBEDDING: [
            "Provides UI components embedded within the application",
            "Delivers front-end widgets for customer interactions",
            "Integrates visual elements seamlessly into dashboard"
        ],
        RelationshipType.WORKFLOW_TRIGGER: [
            "Initiates business process workflows",
            "Triggers approval processes for high-value transactions",
            "Starts scheduled batch operations automatically"
        ],
        RelationshipType.EVENT_SUBSCRIPTION: [
            "Receives event notifications for account status changes",
            "Subscribes to transaction events for fraud detection",
            "Listens for system alerts and notifications"
        ],
        RelationshipType.NOTIFICATION_SERVICE: [
            "Delivers customer alerts and notifications",
            "Sends transaction confirmations via email and SMS",
            "Manages staff alerts for critical system events"
        ],
        RelationshipType.IDENTITY_MANAGEMENT: [
            "Manages customer identity information",
            "Maintains employee user profiles and credentials",
            "Handles secure identity verification"
        ],
        RelationshipType.PAYMENT_PROCESSING: [
            "Processes customer payment transactions",
            "Handles merchant payment gateway integrations",
            "Manages recurring payment schedules"
        ],
        RelationshipType.STORAGE_SERVICE: [
            "Provides secure document storage capabilities",
            "Maintains encrypted file storage for sensitive documents",
            "Handles temporary file storage needs"
        ],
        RelationshipType.SEARCH_SERVICE: [
            "Delivers high-performance search functionality",
            "Indexes transaction and customer records for quick retrieval",
            "Provides advanced search capabilities for compliance investigations"
        ],
        RelationshipType.SECURITY_SCANNING: [
            "Performs vulnerability scanning on code and configurations",
            "Scans for potential security issues in real-time",
            "Manages security validation processes"
        ],
        RelationshipType.AUDIT_LOGGING: [
            "Records detailed audit trails for regulatory compliance",
            "Maintains immutable logs of all security-relevant events",
            "Provides tamper-evident logging of sensitive operations"
        ],
        RelationshipType.RESOURCE_MANAGEMENT: [
            "Manages access to shared computing resources",
            "Controls database connection pooling",
            "Allocates system resources efficiently"
        ],
        RelationshipType.TASK_SCHEDULING: [
            "Schedules and executes background processing tasks",
            "Manages recurring batch processes",
            "Handles distributed task scheduling across environments"
        ],
        RelationshipType.CONTENT_DELIVERY: [
            "Serves static content and assets to end users",
            "Manages content distribution for customer-facing interfaces",
            "Optimizes delivery of media and document content"
        ]
    }

    # Get random values from enums using weighted selection
    relationship_type = RelationshipType.get_random()
    criticality = CriticalityLevel.get_random()

    # Generate a description based on relationship type
    if relationship_type in descriptions:
        description = random.choice(descriptions[relationship_type])
    else:
        description = f"Integrates with {relationship_type.name} functionality"

    # Create the application relationship record (content fields only)
    application_relationship = {
        "relationship_type": relationship_type.name,
        "description": description,
        "criticality": criticality.name
    }

    return application_relationship
