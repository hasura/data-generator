import logging
import random
import sys
from typing import Any, Dict

import anthropic
import psycopg2

from data_generator import DataGenerator, SkipRowGenerationError
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

# Track previously generated rule names for uniqueness
prev_policy_rules = set()
logger = logging.getLogger(__name__)


def generate_random_policy_rule(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.policy_rules record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_policy_rule_id, security_policy_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random policy rule record
        (without ID fields)
    """

    # Try to fetch the related policy information
    policy_info = _fetch_policy_info(id_fields.get('security_policy_id'), dg)

    # Common rule categories for security policies
    rule_categories = {
        "authentication": [
            "password complexity enforcement",
            "multi-factor authentication",
            "biometric verification",
            "certificate-based authentication",
            "single sign-on requirement"
        ],
        "authorization": [
            "least privilege access",
            "separation of duties",
            "role-based access control",
            "attribute-based access control",
            "just-in-time access"
        ],
        "data protection": [
            "data encryption at rest",
            "data encryption in transit",
            "data masking requirement",
            "data retention limit",
            "secure data destruction"
        ],
        "network security": [
            "firewall configuration",
            "network segmentation",
            "intrusion detection",
            "traffic monitoring",
            "zero trust network"
        ],
        "compliance": [
            "audit logging requirement",
            "regulatory reporting",
            "privacy impact assessment",
            "regular compliance review",
            "third-party assessment"
        ],
        "incident response": [
            "security incident reporting",
            "breach notification procedure",
            "incident escalation process",
            "disaster recovery plan",
            "business continuity requirement"
        ]
    }

    # Select category based on policy info if available
    if policy_info and policy_info.get('name'):
        policy_name = policy_info.get('name', '').lower()
        policy_description = policy_info.get('description', '').lower()

        # Determine most relevant category based on policy info
        category_score = {}
        for category, _ in rule_categories.items():
            category_score[category] = 0
            if category in policy_name or category in policy_description:
                category_score[category] += 5

            # Additional keyword matching
            keywords = {
                "authentication": ["login", "password", "credential", "identity", "auth"],
                "authorization": ["access", "permission", "privilege", "role", "authorization"],
                "data protection": ["encrypt", "data", "protection", "retention", "mask"],
                "network security": ["network", "firewall", "intrusion", "traffic", "segmentation"],
                "compliance": ["compliance", "regulation", "audit", "report", "review"],
                "incident response": ["incident", "breach", "response", "recovery", "continuity"]
            }

            for keyword in keywords.get(category, []):
                if keyword in policy_name:
                    category_score[category] += 3
                if keyword in policy_description:
                    category_score[category] += 2

        # Select category with highest score, or random if tied
        top_categories = [k for k, v in category_score.items()
                          if v == max(category_score.values())]
        selected_category = random.choice(top_categories if top_categories else list(rule_categories.keys()))
    else:
        # Fallback to random category if no policy info
        selected_category = random.choice(list(rule_categories.keys()))

    # Select rule base from the chosen category
    rule_base = random.choice(rule_categories[selected_category])

    # Try to get unique rule names from DBML if available
    try:
        all_rules = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='security.policy_rules.rule_name',
            count=50,
            cache_key='policy_rule_names'
        )
        # Filter by category if possible
        filtered_rules = [rule for rule in all_rules
                          if selected_category in rule.lower()]
        if filtered_rules:
            rule_base = random.choice(filtered_rules)
    except anthropic.APIStatusError:
        # Already using fallback rule list
        pass

    # Enhance rule name with specificity
    specificity_elements = [
        f"for {random.choice(['internal', 'external', 'all'])} users",
        f"in {random.choice(['production', 'development', 'testing', 'all'])} environments",
        f"on {random.choice(['critical', 'sensitive', 'all'])} systems",
        f"with {random.choice(['immediate', 'standard', 'periodic'])} enforcement",
        f"requiring {random.choice(['automated', 'manual', 'hybrid'])} verification"
    ]

    # Decide whether to add specificity (70% chance)
    if random.random() < 0.7:
        specificity = random.choice(specificity_elements)
        rule_name = f"{rule_base} {specificity}"
    else:
        rule_name = rule_base

    # Capitalize rule name properly
    rule_name = rule_name.capitalize()

    # Generate rich rule description
    action_verbs = ["Enforce", "Require", "Implement", "Mandate", "Establish"]
    action_verb = random.choice(action_verbs)

    # Create base description
    rule_description = f"{action_verb} {rule_base} "

    # Add purpose
    purposes = [
        "to protect sensitive data from unauthorized access",
        "to maintain compliance with regulatory requirements",
        "to prevent security breaches and unauthorized activities",
        "to ensure system integrity and availability",
        "to mitigate risks associated with external threats",
        "to provide accountability and auditability of actions",
        "to enforce separation of duties within critical processes",
        "to enable rapid response to potential security incidents"
    ]
    rule_description += random.choice(purposes) + ". "

    # Add implementation detail (70% chance)
    if random.random() < 0.7:
        implementations = [
            f"This is implemented through {random.choice(['automated controls', 'manual procedures', 'technical safeguards', 'administrative processes'])}.",
            f"Compliance is verified through {random.choice(['periodic audits', 'automated monitoring', 'management review', 'continuous assessment'])}.",
            f"Exceptions require {random.choice(['senior management approval', 'formal risk acceptance', 'compensating controls', 'documented justification'])}.",
            f"This applies to {random.choice(['all systems', 'critical applications', 'customer-facing services', 'regulated data repositories'])}."
        ]
        rule_description += random.choice(implementations)

    # Ensure uniqueness of rule names per policy
    global prev_policy_rules
    check = (id_fields.get('security_policy_id'), rule_name)
    if check in prev_policy_rules:
        raise SkipRowGenerationError
    else:
        prev_policy_rules.add(check)

    # Construct the policy rule record (without ID fields)
    policy_rule = {
        "rule_name": rule_name,
        "rule_description": rule_description
    }

    return policy_rule


def _fetch_policy_info(policy_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch policy information from the database

    Args:
        policy_id: UUID of the policy
        dg: DataGenerator instance

    Returns:
        Dictionary with policy name and description, or empty dict if not found
    """
    if not policy_id:
        return {}

    try:
        # Try to query the policy information
        query = """
        SELECT name, description 
        FROM security.policies 
        WHERE security_policy_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (policy_id,))
            result = cursor.fetchone()

        if result:
            return {
                'name': result[0],
                'description': result[1]
            }

    except psycopg2.ProgrammingError as e:
        # Log the critical error
        logger.critical(f"Programming error detected in the SQL query: {e}")

        # Exit the program immediately with a non-zero status code
        sys.exit(1)

    return {}
