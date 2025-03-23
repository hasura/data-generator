import logging
import random
from typing import Any, Dict

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

logger = logging.getLogger(__name__)


def generate_random_team(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt team record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (app_mgmt_team_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated team data (without ID fields or FK fields)
    """
    # Default fallback values for team names
    team_names = [
        "Enterprise Architecture", "Core Banking Platform", "Digital Channels",
        "Risk Technology", "Compliance Systems", "Payment Solutions",
        "API & Integration", "DevOps & Cloud", "Security Engineering",
        "Data & Analytics", "Mobile Development", "Customer Experience",
        "Core Infrastructure", "Banking Technology", "Regulatory Systems",
        "Product Development", "Quality Assurance", "Fraud Prevention",
        "Financial Systems", "Loan Origination", "Card Management",
        "Investment Platforms", "Enterprise Integration", "Operations Technology",
        "Digital Transformation", "Platform Engineering", "Banking Solutions"
    ]

    # Try to use generate_unique_json_array for team names
    try:
        generated_names = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='app_mgmt.teams.team_name - Banking technology teams including platform engineering, digital channels, core banking, payment systems, risk technology, compliance systems, banking security, and enterprise architecture',
            count=50,
            cache_key='team_names'
        )
        if generated_names:
            team_names = generated_names
    except Exception as e:
        logger.error(f"Error generating team names: {e}")
        # Continue with fallback values
        pass

    # Select a team name
    team_name = random.choice(team_names)

    # Generate team descriptions based on the team name
    descriptions = {
        "Enterprise Architecture": "Defines technology standards and architectural patterns for the bank's systems",
        "Core Banking Platform": "Maintains and enhances the bank's core account processing systems",
        "Digital Channels": "Develops customer-facing web and mobile banking solutions",
        "Risk Technology": "Implements systems for credit, market, and operational risk management",
        "Compliance Systems": "Builds and maintains regulatory compliance technology solutions",
        "Payment Solutions": "Develops and supports payment processing systems and integrations",
        "API & Integration": "Creates and manages APIs and integration patterns across the bank",
        "DevOps & Cloud": "Manages cloud infrastructure and continuous delivery pipelines",
        "Security Engineering": "Implements security controls and systems across banking applications",
        "Data & Analytics": "Develops data warehousing and business intelligence solutions",
        "Mobile Development": "Creates mobile apps and frameworks for banking services",
        "Customer Experience": "Implements customer-facing technology solutions and journeys",
        "Core Infrastructure": "Manages bank-wide technology infrastructure and networking",
        "Banking Technology": "Develops specialized banking software solutions and platforms",
        "Regulatory Systems": "Builds systems for regulatory reporting and compliance monitoring",
        "Product Development": "Creates new technology-enabled banking products",
        "Quality Assurance": "Ensures software quality and test automation",
        "Fraud Prevention": "Develops systems to detect and prevent financial fraud",
        "Financial Systems": "Implements financial management and reporting solutions",
        "Loan Origination": "Develops technology for loan application and processing",
        "Card Management": "Creates systems for credit and debit card processing",
        "Investment Platforms": "Builds technology for investment and wealth management",
        "Enterprise Integration": "Manages system integration and data exchange patterns",
        "Operations Technology": "Supports bank operational processes with technology",
        "Digital Transformation": "Leads technology modernization initiatives",
        "Platform Engineering": "Develops shared technology platforms and services",
        "Banking Solutions": "Implements specialized banking applications and services"
    }

    # Generate a description based on team name or use a generic one
    if team_name in descriptions:
        description = descriptions[team_name]
    else:
        descriptions_generic = [
            f"Responsible for {team_name.lower()} systems and services across the bank",
            f"Develops and maintains {team_name.lower()} applications and infrastructure",
            f"Specialized team focused on {team_name.lower()} technology solutions",
            f"Builds and supports {team_name.lower()} platforms for the organization",
            f"Creates technology solutions for {team_name.lower()} capabilities"
        ]
        description = random.choice(descriptions_generic)

    # Create the team record (content fields only)
    team = {
        "team_name": team_name,
        "description": description
    }

    return team
