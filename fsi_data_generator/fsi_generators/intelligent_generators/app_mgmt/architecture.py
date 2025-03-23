import datetime
import random
from typing import Any, Dict

import anthropic

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

architecture_names: [str] = []


def generate_random_architecture(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt architecture record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (app_mgmt_architecture_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated architecture data (without ID fields or FK fields)
    """
    # Use generate_unique_json_array to get architecture names
    global architecture_names

    if not architecture_names:
        architecture_names = [
            "Microservice Architecture",
            "Event-Driven Architecture",
            "Layered Architecture",
            "Service-Oriented Architecture",
            "API-First Architecture",
            "Cloud-Native Architecture",
            "Serverless Architecture",
            "Domain-Driven Architecture",
            "Hexagonal Architecture",
            "CQRS Architecture",
            "Pipeline Architecture",
            "Modular Monolith Architecture",
            "Message-Based Architecture",
            "Multi-Tenant Architecture",
            "Zero-Trust Architecture",
            "Banking Integration Architecture",
            "Distributed Systems Architecture",
            "Regulatory Compliance Architecture",
            "Data Lake Architecture",
            "High-Availability Banking Architecture"
        ]
        try:
            architecture_names = architecture_names + generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='app_mgmt.architectures.architecture_name',
                count=50,
                cache_key='architecture_name_prefixes'
            )
        except anthropic.APIStatusError:
            pass

    random.shuffle(architecture_names)

    # Get statuses from the enum in DBML
    architecture_statuses = [
        "approved", "deprecated", "proposed"
    ]

    # Generate a name for the architecture
    architecture_name = architecture_names.pop()

    # Generate documentation URLs or use defaults
    documentation_urls = [
        "https://confluence.bank.internal/architecture/design-patterns",
        "https://docs.bank.internal/architecture/reference",
        "https://wiki.bank.internal/architecture/standards",
        "https://sharepoint.bank.internal/architecture/guidelines"
    ]
    try:
        documentation_urls = documentation_urls + generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='app_mgmt.architectures.documentation_url',
            count=10,
            cache_key='architecture_documentation_urls'
        )
    except anthropic.APIStatusError:
        pass

    documentation_url = random.choice(documentation_urls)

    # Generate architecture description
    descriptions = [
        f"A {architecture_name.lower()} designed for scalable and resilient financial applications. Provides secure API gateway patterns and data storage mechanisms compliant with banking regulations.",
        f"Enterprise-grade {architecture_name.lower()} for secure banking operations. Implements zero-trust security model with proper separation of concerns and audit capabilities.",
        f"Standardized {architecture_name.lower()} that follows industry best practices for high-availability financial systems. Includes resilient data storage, caching, and message broker patterns.",
        f"Modern {architecture_name.lower()} optimized for cloud deployment. Provides patterns for stateless services, data encryption, and secure API communications.",
        f"Robust {architecture_name.lower()} with focus on regulatory compliance. Includes patterns for comprehensive logging, monitoring, and data lineage tracking."
    ]
    description = random.choice(descriptions)

    # Generate random date in the past for approval
    today = datetime.date.today()
    days_ago = random.randint(30, 1095)  # Between 1 month and 3 years ago
    approval_date = today - datetime.timedelta(days=days_ago)

    # Determine status based on approval date
    # Newer architectures are more likely to be approved or proposed
    # Older architectures are more likely to be deprecated
    if days_ago < 180:  # Less than 6 months old
        status_weights = [0.7, 0.05, 0.25]  # approved, deprecated, proposed
    elif days_ago < 730:  # Less than 2 years old
        status_weights = [0.8, 0.15, 0.05]  # approved, deprecated, proposed
    else:  # Older than 2 years
        status_weights = [0.6, 0.4, 0.0]  # approved, deprecated, proposed

    status = random.choices(architecture_statuses, weights=status_weights, k=1)[0]

    # Create the architecture record (content fields only)
    architecture = {
        "architecture_name": architecture_name,
        "description": description,
        "approval_date": approval_date,
        "documentation_url": documentation_url,
        "status": status
    }

    return architecture
