import logging
import random
from typing import Any, Dict

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

# Global set to track used role names across instances
used_role_names = set()
logger = logging.getLogger(__name__)


def generate_random_security_role(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security role record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (security_role_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated role data (without ID fields or FK fields)
    """
    global used_role_names

    # Default fallback values for role names
    role_name_templates = [
        "AccountAdmin", "TransactionApprover", "CustomerViewOnly",
        "LoanOfficer", "ComplianceReviewer", "SecurityAuditor",
        "SystemAdministrator", "ReportViewer", "DataAnalyst",
        "CustomerServiceRep", "BranchManager", "TreasuryManager",
        "RiskAnalyst", "PaymentProcessor", "FraudInvestigator",
        "CreditApprover", "AccountManager", "InvestmentAdvisor",
        "RegulatorAccess", "AuditReviewer", "MarketingAnalyst",
        "CollectionsAgent", "ServiceDesk", "BusinessIntelligence"
    ]

    status = random.choice(['ACTIVE', 'INACTIVE', 'DEPRECATED', 'RETIRED', 'DRAFT'])

    # Try to use generate_unique_json_array for role names
    try:
        generated_names = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='security.roles.role_name - Names of banking access control roles including account administrators, loan officers, transaction approvers, compliance reviewers, security auditors, and customer service representatives',
            count=100,
            cache_key='security_role_names'
        )
        if generated_names:
            role_name_templates = generated_names
    except Exception as e:
        logger.error(f"Error generating role names: {e}")
        # Continue with fallback values
        pass

    # Generate a unique role name
    role_name = None
    attempts = 0
    max_attempts = 100

    while role_name is None or role_name in used_role_names:
        if attempts >= max_attempts:
            # If we've tried too many times, add a uniquifier
            base_name = random.choice(role_name_templates)
            role_name = f"{base_name}_{random.randint(1000, 9999)}"
        else:
            # Potentially add a qualifier to the role name for variability
            base_name = random.choice(role_name_templates)

            # 30% chance to add a qualifier
            if random.random() < 0.3:
                qualifiers = ["Senior", "Junior", "Regional", "Global", "Lead",
                              "Corporate", "Branch", "Assistant", "Chief", "Deputy"]
                role_name = f"{random.choice(qualifiers)}{base_name}"
            else:
                role_name = base_name

        attempts += 1

    # Add the role name to the set of used names
    used_role_names.add(role_name)

    # Generate display name based on role name (more user-friendly)
    display_name = role_name.replace("_", " ")
    # Add spaces between camel case words
    import re
    display_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', display_name)

    # Generate role descriptions based on the role name
    descriptions = {
        "AccountAdmin": "Full administrative access to manage accounts, including creation, modification, and closure",
        "TransactionApprover": "Authority to approve transactions above threshold limits",
        "CustomerViewOnly": "Read-only access to customer information for support purposes",
        "LoanOfficer": "Access to loan application systems with authority to process and approve loans within limits",
        "ComplianceReviewer": "Access to review transactions and accounts for regulatory compliance",
        "SecurityAuditor": "Ability to audit security controls and access logs across systems",
        "SystemAdministrator": "Administrative access to configure and maintain banking systems",
        "ReportViewer": "Access to view and generate reports from banking data",
        "DataAnalyst": "Ability to query and analyze banking data for business insights",
        "CustomerServiceRep": "Access to customer information and basic transaction abilities for support",
        "BranchManager": "Elevated access for managing branch operations and approvals",
        "TreasuryManager": "Access to treasury management functions and high-value transfers",
        "RiskAnalyst": "Ability to assess and manage risk across accounts and transactions",
        "PaymentProcessor": "Access to payment processing systems and functions",
        "FraudInvestigator": "Specialized access to investigate potential fraudulent activity",
        "CreditApprover": "Authority to evaluate and approve credit applications",
        "AccountManager": "Access to manage customer accounts and provide services",
        "InvestmentAdvisor": "Access to investment platforms and customer portfolio data",
        "RegulatorAccess": "Specialized access provided to regulatory authorities for examinations",
        "AuditReviewer": "Access to conduct internal audits across banking functions",
        "MarketingAnalyst": "Access to customer data for marketing analysis and campaigns",
        "CollectionsAgent": "Access to manage past due accounts and collection activities",
        "ServiceDesk": "Basic access to help customers with account inquiries and issues",
        "BusinessIntelligence": "Access to analytics and reporting platforms for business insights"
    }

    # Find the closest base name to use for description
    base_for_description = None
    for base_name in descriptions.keys():
        if base_name in role_name:
            base_for_description = base_name
            break

    # Generate a description based on role name or use a generic one
    if base_for_description and base_for_description in descriptions:
        description = descriptions[base_for_description]
    else:
        descriptions_generic = [
            f"Provides access to {display_name.lower()} functionality within banking systems",
            f"Allows users to perform {display_name.lower()} operations according to bank policies",
            f"Specialized role for {display_name.lower()} with appropriate security restrictions",
            f"Grants permissions necessary for {display_name.lower()} duties in compliance with regulations",
            f"Role-based access control for staff performing {display_name.lower()} responsibilities"
        ]
        description = random.choice(descriptions_generic)

    # Create the role record (content fields only)
    role = {
        "role_name": role_name,
        "display_name": display_name,
        "description": description,
        "status": status
    }

    return role
