from typing import Any, Dict
import logging
import psycopg2
import random
from faker import Faker
from data_generator import DataGenerator, SkipRowGenerationError

logger = logging.getLogger(__name__)
fake = Faker()  # Initialize Faker

# Dictionary to track unique record lineage relationships to avoid duplicates
record_lineages_by_api = {}


def generate_random_record_lineage(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "data_quality"."record_lineage" record with reasonable values.
    Ensures consistency with parent api_lineage record.

    Args:
        _id_fields: Dictionary containing the required ID fields (record_lineage_id and api_lineage_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated record lineage data
    """
    # Get connection for fetching related data
    conn = dg.conn

    # Extract the API lineage ID from _id_fields
    api_lineage_id = _id_fields.get("api_lineage_id")

    if api_lineage_id is None:
        # If no API lineage ID is provided, we can't generate a valid record
        raise SkipRowGenerationError("No API lineage ID provided")

    # Fetch the API lineage information to ensure consistency
    api_info = _get_api_lineage_info(conn, api_lineage_id)

    if not api_info:
        # If API lineage information is not available, skip row generation
        raise SkipRowGenerationError("API lineage information not available")

    # Initialize tracking dictionary for this api if not exists
    if api_lineage_id not in record_lineages_by_api:
        record_lineages_by_api[api_lineage_id] = set()

    # Generate input and output types based on the API context
    input_type, output_type = _generate_consistent_types(api_info)

    # Create a unique key to check if this record lineage already exists
    record_lineage_key = f"{input_type}:{output_type}"

    # Check if this lineage already exists for this API
    attempt = 0
    original_key = record_lineage_key
    while record_lineage_key in record_lineages_by_api[api_lineage_id] and attempt < 10:
        # Add a suffix to make it unique
        suffix = f"_variant{attempt}"
        input_type = f"{input_type}{suffix}"
        output_type = f"{output_type}{suffix}"
        record_lineage_key = f"{input_type}:{output_type}"
        attempt += 1

    if attempt >= 10:
        # If we can't create a unique lineage after multiple attempts, skip it
        raise SkipRowGenerationError("Could not generate unique record lineage")

    # Add to tracking set
    record_lineages_by_api[api_lineage_id].add(record_lineage_key)

    # Generate appropriate primary key names based on the types
    pk_names = _generate_pk_names(input_type, output_type)

    # Create the record_lineage record
    record_lineage = {
        "input_type": input_type,
        "output_type": output_type,
        "description": _generate_lineage_description(input_type, output_type, api_info),
        "input_description": _generate_input_description(input_type, api_info),
        "output_description": _generate_output_description(output_type, api_info),
        "pk_names": pk_names
        # api_lineage_id will be handled by the framework
    }

    return record_lineage


def _get_api_lineage_info(conn, api_lineage_id):
    """
    Get API lineage information from the database.

    Args:
        conn: PostgreSQL connection object
        api_lineage_id: UUID of the API lineage record

    Returns:
        Dictionary containing API lineage information or None if not found
    """
    try:
        cursor = conn.cursor()

        # Query to fetch API lineage information
        cursor.execute("""
            SELECT al.server_name, al.major_version, al.minor_version, al.api_call, al.query, al.description,
                   a.application_name, a.application_type
            FROM data_quality.api_lineage al
            LEFT JOIN app_mgmt.applications a ON al.app_mgmt_application_id = a.app_mgmt_application_id
            WHERE al.api_lineage_id = %s
        """, (api_lineage_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "server_name": result[0],
                "major_version": result[1],
                "minor_version": result[2],
                "api_call": result[3],
                "query": result[4],
                "description": result[5],
                "application_name": result[6],
                "application_type": result[7]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching API lineage information: {error}")
        return None


def _generate_consistent_types(api_info):
    """
    Generate input and output types that are consistent with the API lineage.

    Args:
        api_info: Dictionary containing API lineage information

    Returns:
        Tuple of (input_type, output_type)
    """
    # Extract information to inform type generation
    api_call = api_info.get("api_call", "")
    server_name = api_info.get("server_name", "")
    app_type = api_info.get("application_type", "")
    query = api_info.get("query", "")

    # Generate domain-appropriate types based on the API context

    # Parse the GraphQL query to extract potential types
    query_types = _extract_types_from_query(query)

    if query_types and len(query_types) >= 2:
        # Use the first type as input and second as output if available
        return query_types[0], query_types[1]

    # If we couldn't extract from query, generate based on domain
    domain_types = []

    # Banking domain
    if "banking" in server_name.lower() or "account" in api_call.lower():
        domain_types = [
            "Customer", "Account", "Transaction", "Statement", "Payment",
            "Transfer", "CustomerProfile", "AccountSummary", "TransactionHistory",
            "PaymentInstruction", "TransferRequest", "BalanceDetails"
        ]

    # Credit card domain
    elif "credit" in server_name.lower() or "card" in api_call.lower():
        domain_types = [
            "Card", "CardAccount", "CardTransaction", "Reward", "Statement",
            "Payment", "CardHolder", "CreditLimit", "RewardsSummary",
            "TransactionDetail", "PaymentSchedule", "BillingCycle"
        ]

    # Mortgage domain
    elif "mortgage" in server_name.lower() or "loan" in api_call.lower():
        domain_types = [
            "LoanApplication", "Loan", "Property", "Borrower", "Document",
            "Payment", "Escrow", "InterestRate", "AmortizationSchedule",
            "PropertyValuation", "LoanTerms", "PaymentHistory"
        ]

    # Default domain if none of the above
    else:
        domain_types = [
            "User", "Profile", "Document", "Report", "Configuration",
            "Setting", "Metric", "AnalyticsResult", "UserProfile",
            "DocumentMetadata", "ReportData", "ConfigurationSetting"
        ]

    # Randomly select input and output types, ensuring they're different
    if len(domain_types) >= 2:
        input_type = random.choice(domain_types)
        # Make sure output_type is different from input_type
        remaining_types = [t for t in domain_types if t != input_type]
        output_type = random.choice(remaining_types)
    else:
        # Fallback if domain_types is too small
        input_type = "SourceData"
        output_type = "ProcessedData"

    return input_type, output_type


def _extract_types_from_query(query):
    """
    Extract potential data types from a GraphQL query.

    Args:
        query: GraphQL query string

    Returns:
        List of potential data types extracted from the query
    """
    if not query:
        return []

    types = []

    # Look for type names in query blocks
    lines = query.split('\n')
    for line in lines:
        # Look for query type definitions
        if "query" in line and "(" in line:
            # Extract the query name which often hints at the main type
            parts = line.split("query")
            if len(parts) > 1:
                query_name = parts[1].strip().split("(")[0].strip()
                # Clean up and extract type name
                if query_name.startswith("Get"):
                    type_name = query_name[3:]  # Remove "Get" prefix
                    # Handle plurals
                    if type_name.endswith("s"):
                        type_name = type_name[:-1]  # Remove plural 's'
                    types.append(type_name)

        # Look for field definitions that might indicate types
        if "{" in line and "}" not in line:
            field = line.strip().split("{")[0].strip()
            if field and not field.startswith("{") and field != "query":
                types.append(field[0].upper() + field[1:])  # Capitalize field name

        # Look for return type fields
        if ":" in line and "{" not in line and "(" not in line:
            field = line.strip().split(":")[0].strip()
            if field:
                types.append(field[0].upper() + field[1:])  # Capitalize field name

    # Remove duplicates and return
    return list(dict.fromkeys(types))


def _generate_pk_names(input_type, output_type):
    """
    Generate appropriate primary key field names based on the input and output types.

    Args:
        input_type: The input data type
        output_type: The output data type

    Returns:
        Comma-separated string of primary key field names
    """
    # Standard primary key naming patterns
    standard_pk_patterns = ["id", "code", "key", "uuid", "identifier"]

    # Generate primary key names based on the type
    input_pk = f"{input_type.lower()}_{random.choice(standard_pk_patterns)}"

    # Sometimes add a second PK field for composite keys
    if random.random() < 0.3:
        second_field = random.choice(["type", "category", "version", "sequence"])
        input_pk = f"{input_pk},{input_type.lower()}_{second_field}"

    return input_pk


def _generate_lineage_description(input_type, output_type, api_info):
    """
    Generate a description for the record lineage.

    Args:
        input_type: The input data type
        output_type: The output data type
        api_info: Dictionary containing API lineage information

    Returns:
        A description string
    """
    # Get context from API
    api_call = api_info.get("api_call", "")
    server_name = api_info.get("server_name", "")

    # Generate transformation descriptions
    transformations = [
        "Normalizes and enriches",
        "Transforms",
        "Processes and enhances",
        "Extracts and reorganizes",
        "Converts",
        "Maps",
        "Aggregates",
        "Summarizes",
        "Restructures",
        "Validates and formats"
    ]

    # Generate purposes
    purposes = [
        "for API consumption",
        "for downstream processing",
        "to meet response requirements",
        "for data integration",
        "to support business operations",
        "for customer-facing applications",
        "to support reporting functions",
        "for analytical processing",
        "to comply with data standards",
        "for efficient data access"
    ]

    # Create a contextual description
    context = ""
    if "banking" in server_name.lower() or "account" in api_call.lower():
        context = "in the banking domain"
    elif "credit" in server_name.lower() or "card" in api_call.lower():
        context = "in the credit card system"
    elif "mortgage" in server_name.lower() or "loan" in api_call.lower():
        context = "in the mortgage processing system"
    else:
        contexts = ["in the data pipeline", "within the processing workflow", "in the ETL process"]
        context = random.choice(contexts)

    return f"{random.choice(transformations)} {input_type} data into {output_type} format {context} {random.choice(purposes)}"


def _generate_input_description(input_type, api_info):
    """
    Generate a description for the input data type.

    Args:
        input_type: The input data type
        api_info: Dictionary containing API lineage information

    Returns:
        A description string
    """
    # Get context from API
    server_name = api_info.get("server_name", "")

    # Domain-specific descriptions
    if "banking" in server_name.lower():
        sources = [
            "core banking system",
            "account management system",
            "transaction processing system",
            "customer information system",
            "banking database"
        ]
    elif "credit" in server_name.lower():
        sources = [
            "card management system",
            "credit processing system",
            "rewards database",
            "transaction clearing system",
            "card activation system"
        ]
    elif "mortgage" in server_name.lower():
        sources = [
            "loan origination system",
            "property database",
            "borrower information system",
            "underwriting system",
            "mortgage servicing platform"
        ]
    else:
        sources = [
            "source database",
            "transactional system",
            "operational data store",
            "data warehouse",
            "third-party system"
        ]

    # Data characteristics
    characteristics = [
        "raw",
        "normalized",
        "validated",
        "structured",
        "unprocessed",
        "source-formatted"
    ]

    formats = [
        "JSON",
        "structured records",
        "relational data",
        "document format",
        "nested structure",
        "hierarchical format"
    ]

    return f"{input_type} data in {random.choice(characteristics)} {random.choice(formats)} format from the {random.choice(sources)}"


def _generate_output_description(output_type, api_info):
    """
    Generate a description for the output data type.

    Args:
        output_type: The output data type
        api_info: Dictionary containing API lineage information

    Returns:
        A description string
    """
    # Get context from API
    api_call = api_info.get("api_call", "")
    query = api_info.get("query", "")

    # Determine if this is likely a GraphQL response
    is_graphql = "graphql" in api_call.lower() or "query" in query.lower()

    # Output characteristics
    characteristics = [
        "enriched",
        "transformed",
        "validated",
        "normalized",
        "integrated",
        "optimized",
        "summarized",
        "structured"
    ]

    # Output destinations or purposes
    if is_graphql:
        destinations = [
            "GraphQL API response",
            "client application consumption",
            "frontend display",
            "UI rendering",
            "API client usage"
        ]

        return f"{output_type} data in {random.choice(characteristics)} format for {random.choice(destinations)}, conforming to GraphQL schema specifications"
    else:
        destinations = [
            "API response",
            "downstream system",
            "data lake",
            "reporting system",
            "analytics platform",
            "data warehouse"
        ]

        return f"{output_type} data in {random.choice(characteristics)} format for {random.choice(destinations)}, optimized for performance and usability"
