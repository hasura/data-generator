import random
from typing import Any, Dict

import anthropic

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array


def generate_random_enhanced_entitlement(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.enhanced_entitlements record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields
                   (security_entitlement_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated enhanced entitlement data
        (without ID fields)
    """
    # Generate unique entitlement names
    entitlement_names = [
        "read_customer_data",
        "write_transaction_records",
        "view_account_balances",
        "modify_user_profiles",
        "access_financial_reports",
        "dashboard_admin",
        "create_new_application",
        "manage_user_roles",
        "configure_system_settings",
        "audit_system_logs",
        "security_policy_management",
        "identity_verification",
        "access_control_configuration",
        "compliance_reporting",
        "security_incident_response",
        "mortgage_application_review",
        "credit_card_limit_adjustment",
        "loan_origination_access",
        "risk_assessment_management",
        "regulatory_compliance_review"
    ]
    try:
        entitlement_names = entitlement_names + generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='security.enhanced_entitlements.entitlement_name',
            count=100,
            cache_key='enhanced_entitlement_names'
        )
    except anthropic.APIStatusError:
        pass

    # Status options matching the enum
    status_options = [
        "ACTIVE",  # Higher weight for active entitlements
        "ACTIVE",  # Double weight to make it more common
        "INACTIVE",  # Some inactive entitlements
        "DEPRECATED",  # Few deprecated entitlements
        "DRAFT"  # Rare draft entitlements
    ]

    # Status selection with weighted probabilities
    status_weights = [0.6, 0.2, 0.1, 0.1]
    status = random.choices(status_options[:4], weights=status_weights)[0]

    # Prepare display names and descriptions
    entitlement_name = random.choice(entitlement_names)
    display_name = entitlement_name.replace('_', ' ').title()

    # Generate descriptions based on entitlement name
    descriptions = {
        "read_customer_data": "Grants read-only access to customer profile information",
        "write_transaction_records": "Allows modification of transaction log entries",
        "view_account_balances": "Permission to view financial account balances",
        "modify_user_profiles": "Ability to update and modify user account details",
        "access_financial_reports": "Access to generate and view financial reporting documents",
        "dashboard_admin": "Full administrative access to system dashboards",
        "create_new_application": "Permission to initiate new application deployments",
        "manage_user_roles": "Ability to assign and modify user role permissions",
        "configure_system_settings": "Access to modify core system configuration parameters",
        "audit_system_logs": "Permission to view and analyze system audit logs"
    }

    description = descriptions.get(
        entitlement_name,
        f"Entitlement for managing {display_name} access and operations"
    )

    # Create the enhanced entitlement record
    enhanced_entitlement = {
        "entitlement_name": entitlement_name,
        "display_name": display_name,
        "description": description,
        "status": status
    }

    return enhanced_entitlement
