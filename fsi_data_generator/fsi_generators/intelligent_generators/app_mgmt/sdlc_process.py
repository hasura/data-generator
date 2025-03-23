import logging
import random
from typing import Any, Dict

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

logger = logging.getLogger(__name__)


def generate_random_sdlc_process(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt SDLC process record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (app_mgmt_sdlc_process_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated SDLC process data (without ID fields or FK fields)
    """
    # Define common SDLC process names
    default_process_names = [
        "Agile Banking Development Framework",
        "Financial Regulatory Compliance Process",
        "Secure Banking DevOps Pipeline",
        "Enterprise Waterfall for Core Banking",
        "Hybrid Financial Systems Development",
        "Banking Microservices CI/CD Process",
        "Risk-Based Testing Framework",
        "Secure Application Development Lifecycle",
        "Financial Data Governance Process",
        "Regulated Systems Development Process",
        "Compliance-First Development Framework",
        "Core Banking Systems Delivery Process",
        "Payment Systems Development Lifecycle",
        "Fintech Integration Process",
        "Audit-Ready Development Pipeline",
        "Digital Banking Experience Framework",
        "Enterprise Security Development Lifecycle",
        "Customer Data Protection Process",
        "Financial Services Feature Delivery",
        "Card Processing Systems Development"
    ]

    # Try to use generate_unique_json_array for process names
    try:
        process_names = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='app_mgmt.sdlc_processes.process_name - Banking-specific software development methodologies including regulatory compliance integration, security-focused development, and financial data handling procedures',
            count=50,
            cache_key='sdlc_process_names'
        )
        if not process_names:
            process_names = default_process_names
    except Exception as e:
        logger.error(f"Error generating process names: {e}")
        process_names = default_process_names

    # Generate process name
    process_name = random.choice(process_names)

    # Generate process description based on the name
    if "Agile" in process_name:
        description = f"""
            A sprint-based development process tailored for financial applications. 
            Incorporates regulatory compliance checks at each sprint review and 
            emphasizes secure development practices. Features two-week sprints, 
            daily stand-ups, and mandatory security reviews before deployment.
            Includes special provisions for financial data handling and audit trails.
        """
    elif "Waterfall" in process_name:
        description = f"""
            A structured phase-gate approach designed for highly regulated 
            financial applications. Provides comprehensive documentation at each phase 
            to support audit requirements. Phases include Requirements, Design, 
            Implementation, Verification, and Maintenance, with formal sign-off 
            required between each transition.
        """
    elif "DevOps" in process_name or "CI/CD" in process_name:
        description = f"""
            An automated pipeline that integrates security scanning, compliance 
            checks, and audit logging. Provides continuous delivery with gated 
            deployments requiring approval for production financial systems. 
            Features automated testing for regulatory compliance and data protection.
        """
    elif "Security" in process_name:
        description = f"""
            A security-first development process that embeds threat modeling, 
            code analysis, and penetration testing throughout the lifecycle. 
            Designed for financial applications handling sensitive data with 
            specific controls for PCI-DSS, GDPR, and other regulatory frameworks.
        """
    elif "Compliance" in process_name or "Regulatory" in process_name:
        description = f"""
            A development process optimized for maintaining regulatory compliance 
            in financial services. Integrates compliance requirements into the 
            development workflow with automated checks, documentation generation, 
            and audit-ready reports. Includes specific gates for legal review.
        """
    else:
        description = f"""
            A balanced software development lifecycle process that addresses the 
            unique needs of financial applications. Combines iterative development 
            with structured compliance validation. Provides templates for required 
            documentation and automated security testing.
        """

    # Clean up the description (remove indentation and extra whitespace)
    description = ' '.join(line.strip() for line in description.split('\n')).strip()

    # Generate version with common versioning schemes
    major = random.randint(1, 5)
    minor = random.randint(0, 9)
    version_formats = [
        f"{major}.{minor}",  # e.g., 2.3
        f"{major}.{minor}.0",  # e.g., 2.3.0
        f"v{major}.{minor}",  # e.g., v2.3
        f"Version {major}.{minor}",  # e.g., Version 2.3
        f"{major}{chr(96 + minor)}",  # e.g., 2c (for financial institutions that use letter notation)
    ]
    version = random.choice(version_formats)

    # Generate documentation URL
    doc_domains = ["confluence.bank.internal", "docs.bank.internal", "wiki.bank.internal", "sharepoint.bank.internal"]
    doc_domain = random.choice(doc_domains)
    process_slug = process_name.lower().replace(" ", "-").replace("/", "-")
    documentation_url = f"https://{doc_domain}/sdlc/{process_slug}"

    # Create the SDLC process record (content fields only)
    sdlc_process = {
        "process_name": process_name,
        "description": description,
        "version": version,
        "documentation_url": documentation_url
    }

    return sdlc_process
