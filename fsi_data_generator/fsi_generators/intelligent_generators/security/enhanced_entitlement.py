from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from typing import Any, Dict

import anthropic
import random


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
    # Generate unique entitlement names with more specific CRUD-based verbs
    entitlement_names = [
        # Read operations
        "read_customer_data",
        "view_account_balances",
        "view_financial_reports",
        "access_financial_reports",
        "view_system_logs",
        "view_user_roles",
        "read_security_policies",
        "view_compliance_reports",

        # Write/Create operations
        "create_transaction_records",
        "create_user_profiles",
        "create_applications",
        "create_security_policies",
        "create_compliance_reports",
        "create_risk_assessments",

        # Update operations
        "update_user_profiles",
        "update_transaction_records",
        "update_system_settings",
        "update_user_roles",
        "modify_security_policies",
        "update_compliance_reports",
        "adjust_credit_card_limits",

        # Delete operations
        "delete_user_profiles",
        "delete_applications",
        "delete_audit_records",
        "remove_system_settings",

        # Administrative operations (with specific verbs)
        "administer_dashboards",
        "configure_access_controls",
        "assign_user_roles",
        "review_mortgage_applications",
        "approve_loan_originations",
        "analyze_risk_assessments",
        "verify_identity",
        "monitor_security_incidents",
        "execute_compliance_reviews"
    ]
    try:
        # The "column name" is actually just the prompt to the model
        crud_prompt = "Generate unique entitlement names following the CRUD pattern (Create, Read, Update, Delete). " + \
                     "Each name should start with one of these verbs: " + \
                     "READ operations: read_, view_, access_, list_, search_, monitor_, export_ " + \
                     "WRITE operations: create_, add_, insert_, generate_, register_, submit_, execute_, approve_, " + \
                     "send_, publish_, activate_, deactivate_, process_, initiate_, schedule_, trigger_ " + \
                     "UPDATE operations: update_, modify_, edit_, adjust_, revise_, change_, extend_, renew_ " + \
                     "DELETE operations: delete_, remove_, archive_, purge_, cancel_, withdraw_ " + \
                     "Examples: create_customer_account, read_transaction_history, update_user_preferences, " + \
                     "delete_archived_records, view_audit_logs, approve_loan_applications, execute_payment_transfer, " + \
                     "register_new_device, send_notification, publish_report, schedule_maintenance, " + \
                     "withdraw_application, extend_credit_limit, archive_old_records."

        entitlement_names = entitlement_names + generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name=crud_prompt,
            count=100,
            cache_key='crud_enhanced_entitlement_names'
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

    # Generate descriptions based on entitlement name with more specific actions
    descriptions = {
        # Read operations
        "read_customer_data": "Grants read-only access to customer profile information",
        "view_account_balances": "Permission to view financial account balances",
        "view_financial_reports": "Permission to access and view financial reporting documents",
        "view_system_logs": "Permission to inspect system audit logs for analysis",

        # Write/Create operations
        "create_transaction_records": "Permission to create new transaction log entries",
        "create_user_profiles": "Ability to create new user account profiles",
        "create_applications": "Permission to initiate new application deployments",

        # Update operations
        "update_user_profiles": "Ability to modify existing user account details",
        "update_transaction_records": "Permission to modify existing transaction log entries",
        "update_system_settings": "Access to modify core system configuration parameters",
        "update_user_roles": "Ability to modify role assignments for users",

        # Delete operations
        "delete_user_profiles": "Permission to remove user account profiles from the system",
        "delete_applications": "Ability to remove deployed applications from the system",

        # Administrative operations
        "administer_dashboards": "Full administrative access to configure system dashboards",
        "configure_access_controls": "Ability to define and update access control settings",
        "assign_user_roles": "Permission to assign specific roles to system users",
        "verify_identity": "Authority to validate and confirm user identities",
        "monitor_security_incidents": "Permission to track and respond to security events"
    }

    description = descriptions.get(
        entitlement_name,
        f"Entitlement for {entitlement_name.replace('_', ' ')} operations"
    )

    # Create the enhanced entitlement record
    enhanced_entitlement = {
        "entitlement_name": entitlement_name,
        "display_name": display_name,
        "description": description,
        "status": status
    }

    return enhanced_entitlement
