import random
from typing import Any, Dict

import anthropic

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array


def generate_random_component(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt component record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (app_mgmt_component_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated component data (without ID fields or FK fields)
    """
    # Define common component types
    component_types = [
        "java-library",
        "npm-package",
        "nuget-package",
        "python-module",
        "ruby-gem",
        "framework",
        "api",
        "dotnet-assembly",
        "docker-image",
        "gradle-plugin",
        "maven-plugin"
    ]

    # Use generate_unique_json_array for component names and vendors
    component_names = [
        "Spring Boot", "React", "Angular", "jQuery", "Bootstrap", "Hibernate",
        "Log4j", "Jackson", "Apache Commons", "Lombok", "Guava", "Redux",
        "Express", "Axios", "Jest", "Moment", "Lodash", "Material-UI",
        "Django", "Flask", "Requests", "NumPy", "Pandas", "TensorFlow",
        "Entity Framework", "ASP.NET Core", "Newtonsoft.Json", "Dapper",
        "SignalR", "LINQ", "Rails", "Sinatra", "ActiveRecord", "Nokogiri",
        "OWASP Security Headers", "Keycloak", "Auth0", "Sentry", "Prometheus",
        "Grafana", "Elastic APM", "Vault", "Consul", "NLog", "Log4Net",
        "Security Assertion Markup Language", "Financial Calculation Engine",
        "Banking API Client", "OAuth2 Client", "JWT Toolkit", "Encryption Library"
    ]
    try:
        component_names = component_names + generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='app_mgmt.components.component_name - Common software libraries, frameworks, APIs, and modules used in financial applications including security libraries, data processing frameworks, UI components, middleware, authentication systems, and financial calculation tools',
            count=100,
            cache_key='component_names'
        )
    except anthropic.APIStatusError:
        pass

    vendors = [
        "Apache", "Microsoft", "Google", "Facebook", "Oracle", "IBM",
        "Red Hat", "Pivotal", "JetBrains", "Mozilla", "Acme Corp",
        "Twitter", "Netflix", "Airbnb", "Amazon", "Salesforce",
        "SpringSource", "Palantir", "Square", "Elastic", "HashiCorp",
        "Financial Industry Technology", "Bank Core Systems Inc",
        "Fintech Solutions", "Enterprise Security Corp", "Open Banking Institute",
        "Compliance Systems", "Data Protection Technologies", "Secure Payment Systems"
    ]
    try:
        vendors = vendors + generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='app_mgmt.components.vendor - Major software vendors and organizations like Apache, Microsoft, Oracle, IBM, Google, Red Hat, Pivotal, Spring, Financial Industry Specific vendors, and popular open source maintainers',
            count=100,
            cache_key='component_vendors'
        )
    except anthropic.APIStatusError:
        pass

    # Select component name and type
    component_name = random.choice(component_names)
    component_type = random.choice(component_types)
    vendor = random.choice(vendors)

    # Generate version with semantic versioning (semver) format
    major = random.randint(0, 9)
    minor = random.randint(0, 20)
    patch = random.randint(0, 30)
    component_version = f"{major}.{minor}.{patch}"

    # For some components, add a qualifier like alpha, beta, RC
    if random.random() < 0.1:  # 10% chance
        qualifiers = ["-alpha", "-beta", "-RC1", "-RC2", "-M1", "-SNAPSHOT", "-RELEASE"]
        component_version += random.choice(qualifiers)

    # Generate a description based on the component name and type
    descriptions = [
        f"A {component_type.replace('-', ' ')} for {component_name} that provides essential functionality for financial applications.",
        f"Official {vendor} {component_type.replace('-', ' ')} for implementing {component_name} features securely and efficiently.",
        f"Enterprise-grade {component_name} {component_type.replace('-', ' ')} with comprehensive security features.",
        f"High-performance {component_name} implementation optimized for banking applications.",
        f"{component_name} {component_type.replace('-', ' ')} that ensures compliance with financial regulations and standards.",
        f"Security-focused {component_name} that assists with GDPR, PCI-DSS, and other regulatory compliance requirements.",
        f"Scalable {component_name} implementation for handling high-volume transaction processing.",
        f"Certified {component_name} module with built-in audit logging capabilities for financial operations."
    ]
    description = random.choice(descriptions)

    # Generate package_info based on component type
    if component_type == "java-library":
        group_id = vendor.lower().replace(" ", "").replace("-", "")
        artifact_id = component_name.lower().replace(" ", "-")
        package_info = f"{group_id}:{artifact_id}:{component_version}"
    elif component_type == "npm-package":
        package_name = component_name.lower().replace(" ", "-")
        package_info = f"{package_name}@{component_version}"
    elif component_type == "nuget-package":
        package_info = f"{component_name.replace(' ', '.')}.{component_version}"
    elif component_type == "python-module":
        package_info = component_name.lower().replace(" ", "_")
    else:
        package_info = f"{component_name}-{component_version}"

    # Generate repository URL based on component type
    domain = random.choice(["github.com", "gitlab.com", "bitbucket.org", "dev.azure.com"])
    org_name = vendor.lower().replace(" ", "-")
    repo_name = component_name.lower().replace(" ", "-")

    if component_type == "java-library":
        repository_url = f"https://mvnrepository.com/artifact/{org_name}/{repo_name}"
    elif component_type == "npm-package":
        repository_url = f"https://www.npmjs.com/package/{repo_name}"
    elif component_type == "nuget-package":
        repository_url = f"https://www.nuget.org/packages/{component_name.replace(' ', '.')}"
    else:
        repository_url = f"https://{domain}/{org_name}/{repo_name}"

    # Generate namespace or module
    namespace_prefixes = ["com", "org", "io", "net", "gov"]

    if component_type == "java-library":
        namespace_or_module = f"{random.choice(namespace_prefixes)}.{org_name}.{repo_name}"
    elif component_type == "python-module":
        namespace_or_module = repo_name
    elif component_type == "npm-package":
        namespace_or_module = f"@{org_name}/{repo_name}"
    elif component_type in ["nuget-package", "dotnet-assembly"]:
        namespace_or_module = f"{vendor.replace(' ', '')}.{component_name.replace(' ', '')}"
    else:
        namespace_or_module = None

    # Create the component record
    component = {
        "component_name": component_name,
        "component_version": component_version,
        "component_type": component_type,
        "vendor": vendor,
        "description": description,
        "package_info": package_info,
        "repository_url": repository_url,
        "namespace_or_module": namespace_or_module
    }

    return component
