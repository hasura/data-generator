from typing import Any, Dict
import logging
import psycopg2
import random
from faker import Faker
from data_generator import DataGenerator, SkipRowGenerationError

logger = logging.getLogger(__name__)
fake = Faker()  # Initialize Faker

# Dictionary to track field lineages per record lineage to avoid duplicates
field_lineages_by_record = {}


def generate_random_field_lineage(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "data_quality"."field_lineage" record with reasonable values.
    Ensures consistency with parent record_lineage.

    Args:
        _id_fields: Dictionary containing the required ID fields (field_lineage_id and record_lineage_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated field lineage data
    """
    # Get connection for fetching related data
    conn = dg.conn

    # Extract the record lineage ID from _id_fields
    record_lineage_id = _id_fields.get("record_lineage_id")

    if record_lineage_id is None:
        # If no record lineage ID is provided, we can't generate a valid record
        raise SkipRowGenerationError("No record lineage ID provided")

    # Fetch the record lineage information to ensure consistency
    record_info = _get_record_lineage_info(conn, record_lineage_id)

    if not record_info:
        # If record lineage information is not available, skip row generation
        raise SkipRowGenerationError("Record lineage information not available")

    # Initialize tracking dictionary for this record lineage if not exists
    if record_lineage_id not in field_lineages_by_record:
        field_lineages_by_record[record_lineage_id] = set()

    # Generate field name based on record lineage information
    field_name = _generate_field_name(record_info)

    # Check if this field lineage already exists for this record lineage
    attempt = 0
    original_field_name = field_name
    while field_name in field_lineages_by_record[record_lineage_id] and attempt < 10:
        # Add a suffix to make it unique
        field_name = f"{original_field_name}_{attempt}"
        attempt += 1

    if attempt >= 10:
        # If we can't create a unique field lineage after multiple attempts, skip it
        raise SkipRowGenerationError("Could not generate unique field lineage")

    # Add to tracking set
    field_lineages_by_record[record_lineage_id].add(field_name)

    # Generate input fields based on the field name and record types
    input_fields = _generate_input_fields(field_name, record_info)

    # Create the field_lineage record
    field_lineage = {
        "field_name": field_name,
        "description": _generate_field_description(field_name, input_fields, record_info),
        "input_fields": input_fields
        # record_lineage_id will be handled by the framework
    }

    return field_lineage


def _get_record_lineage_info(conn, record_lineage_id):
    """
    Get record lineage information from the database.

    Args:
        conn: PostgreSQL connection object
        record_lineage_id: ID of the record lineage record

    Returns:
        Dictionary containing record lineage information or None if not found
    """
    try:
        cursor = conn.cursor()

        # Query to fetch record lineage information
        cursor.execute("""
            SELECT rl.input_type, rl.output_type, rl.description, rl.pk_names,
                   al.server_name, al.api_call, al.query
            FROM data_quality.record_lineage rl
            LEFT JOIN data_quality.api_lineage al ON rl.api_lineage_id = al.api_lineage_id
            WHERE rl.record_lineage_id = %s
        """, (record_lineage_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "input_type": result[0],
                "output_type": result[1],
                "description": result[2],
                "pk_names": result[3],
                "server_name": result[4],
                "api_call": result[5],
                "query": result[6]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching record lineage information: {error}")
        return None


def _generate_field_name(record_info):
    """
    Generate a field name that is consistent with the record lineage information.

    Args:
        record_info: Dictionary containing record lineage information

    Returns:
        A field name string
    """
    output_type = record_info.get("output_type", "")

    # Extract field names from GraphQL query if available
    query = record_info.get("query", "")
    extracted_fields = _extract_fields_from_query(query)

    if extracted_fields:
        # Use an extracted field with 50% probability
        if random.random() < 0.5 and extracted_fields:
            return random.choice(extracted_fields)

    # If we didn't use an extracted field, generate a domain-specific one

    # Common field patterns by domain
    common_fields = []

    server_name = record_info.get("server_name", "").lower()

    # Banking domain fields
    if "banking" in server_name or "account" in output_type.lower():
        common_fields = [
            "accountNumber", "accountType", "balance", "availableBalance",
            "currency", "status", "customerId", "openedDate", "lastActivity",
            "overdraftLimit", "interestRate", "fees", "holderName", "branch"
        ]

    # Credit card domain fields
    elif "credit" in server_name or "card" in output_type.lower():
        common_fields = [
            "cardNumber", "expirationDate", "cardholderName", "cardType",
            "creditLimit", "availableCredit", "balance", "statementDate",
            "dueDate", "minimumPayment", "rewardsPoints", "cashbackAmount",
            "annualFee", "interestRate", "activationStatus"
        ]

    # Mortgage domain fields
    elif "mortgage" in server_name or "loan" in output_type.lower():
        common_fields = [
            "loanNumber", "loanAmount", "interestRate", "term", "monthlyPayment",
            "originationDate", "maturityDate", "principalBalance", "propertyAddress",
            "escrowBalance", "paymentDueDate", "paymentHistory", "loanType",
            "borrowerName", "loanStatus"
        ]

    # Default fields for any domain
    else:
        common_fields = [
            "id", "name", "description", "createdAt", "updatedAt", "status",
            "type", "category", "value", "code", "reference", "version",
            "isActive", "group", "sequence", "priority", "metadata", "attributes"
        ]

    # Sometimes create a nested field using dot notation
    if random.random() < 0.3:
        # Create parent field name
        parent_options = ["details", "metadata", "settings", "config", "properties", "info", "data", "attributes"]
        parent = random.choice(parent_options)
        child = random.choice(common_fields)
        return f"{parent}.{child}"

    # Regular field name
    return random.choice(common_fields)


def _extract_fields_from_query(query):
    """
    Extract field names from a GraphQL query.

    Args:
        query: GraphQL query string

    Returns:
        List of field names extracted from the query
    """
    if not query:
        return []

    fields = []

    # Parse the query to identify field names
    lines = query.split('\n')
    in_fields_block = False
    indent_level = 0

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            continue

        # Check for block opening
        if '{' in stripped:
            in_fields_block = True
            indent_level += stripped.count('{')

        # Check for block closing
        if '}' in stripped:
            indent_level -= stripped.count('}')
            if indent_level <= 0:
                in_fields_block = False

        # If we're in a fields block, look for fields
        if in_fields_block and indent_level > 0:
            # Remove all whitespace
            clean_line = stripped.strip()

            # Skip lines with block markers, parameters, or fragments
            if '{' in clean_line or '}' in clean_line or '(' in clean_line or \
                    ':' in clean_line or clean_line.startswith('...'):
                continue

            # What remains should be field names
            if clean_line:
                fields.append(clean_line)

    return fields


def _generate_input_fields(field_name, record_info):
    """
    Generate input fields that contribute to the output field.

    Args:
        field_name: The name of the output field
        record_info: Dictionary containing record lineage information

    Returns:
        Comma-separated string of input field names
    """
    input_type = record_info.get("input_type", "")

    # For simple pass-through fields (same name in input and output)
    if random.random() < 0.4:
        return field_name

    # For transformed or calculated fields
    num_input_fields = random.randint(1, 3)  # Most fields come from 1-3 source fields

    # Handle nested fields
    if '.' in field_name:
        parts = field_name.split('.')
        if len(parts) == 2:
            # If the field is something like "details.name", potential input fields could be:
            # - rawDetails.name
            # - detailsData.name
            # - details_name
            # - source.details.name
            parent, child = parts

            prefixes = [f"raw{parent[0].upper()}{parent[1:]}", f"{parent}Data", f"{parent}_", "source."]
            if random.random() < 0.5:
                # Use a transformed version of the same nested field
                return f"{random.choice(prefixes)}{child}"
            else:
                # Use multiple source fields
                return f"{parent}.{child}Raw, {parent}.{child}Source"

    # Standard field transformation patterns
    if num_input_fields == 1:
        # Simple transformations
        prefixes = ["raw", "source", "legacy", "original", "input"]
        suffixes = ["Raw", "Data", "Value", "Input", "Source"]

        if random.random() < 0.5:
            return f"{random.choice(prefixes)}{field_name}"
        else:
            return f"{field_name}{random.choice(suffixes)}"
    else:
        # Multiple input fields
        related_fields = []

        # Handle special common fields
        if field_name.lower() == "fullname":
            return "firstName, lastName, middleName"
        elif field_name.lower() == "address":
            return "street, city, state, postalCode, country"
        elif field_name.lower() == "fulladdress":
            return "addressLine1, addressLine2, city, state, postalCode"
        elif "amount" in field_name.lower() or "total" in field_name.lower():
            return f"base{field_name}, fee{field_name}, tax{field_name}"

        # Generate related fields based on context
        if "date" in field_name.lower():
            date_parts = ["year", "month", "day", "timestamp", "timezone"]
            selected = random.sample(date_parts, min(num_input_fields, len(date_parts)))
            return ", ".join([f"{field_name.replace('Date', '')}_{part}" for part in selected])

        # Default case: add prefixes to create related field names
        input_prefixes = ["raw", "source", "input", "base", "legacy", "original"]
        selected_prefixes = random.sample(input_prefixes, min(num_input_fields, len(input_prefixes)))

        for prefix in selected_prefixes:
            related_fields.append(f"{prefix}{field_name[0].upper()}{field_name[1:]}")

        return ", ".join(related_fields)


def _generate_field_description(field_name, input_fields, record_info):
    """
    Generate a description for the field lineage.

    Args:
        field_name: The name of the output field
        input_fields: Comma-separated string of input field names
        record_info: Dictionary containing record lineage information

    Returns:
        A description string
    """
    # Extract types for context
    input_type = record_info.get("input_type", "")
    output_type = record_info.get("output_type", "")

    # Determine the type of transformation
    transformation_type = ""

    # Same field name in input and output - likely a direct mapping or simple transformation
    if field_name in input_fields and ',' not in input_fields:
        transformation_types = [
            "Direct mapping of",
            "Type conversion for",
            "Formatting of",
            "Validation and normalization of",
            "Sanitization of",
            "Simple transformation of"
        ]
        transformation_type = random.choice(transformation_types)

        return f"{transformation_type} {field_name} from {input_type} to {output_type}"

    # Multiple input fields - likely a complex transformation
    elif ',' in input_fields:
        # Count number of input fields
        num_fields = len(input_fields.split(','))

        if num_fields > 1:
            complex_transformations = [
                f"Concatenation of {input_fields} into {field_name}",
                f"Calculated field derived from {input_fields}",
                f"Aggregated value combining {input_fields}",
                f"Conditional mapping based on {input_fields}",
                f"Business rule application using {input_fields}"
            ]

            # Specific transformations for certain field types
            if "date" in field_name.lower() or "time" in field_name.lower():
                return f"Date/time formatting combining {input_fields} into standardized {field_name} format"
            elif "name" in field_name.lower():
                return f"Name formatting by combining {input_fields} into properly formatted {field_name}"
            elif "address" in field_name.lower():
                return f"Address formatting by combining {input_fields} into standardized {field_name} representation"
            elif "amount" in field_name.lower() or "total" in field_name.lower() or "balance" in field_name.lower():
                return f"Calculated {field_name} by combining and processing {input_fields} with business rules"
            else:
                return random.choice(complex_transformations)

    # Different field name in input vs output - likely a rename or simple transformation
    else:
        rename_transformations = [
            f"Field renamed from {input_fields} to {field_name}",
            f"Standardized naming from legacy {input_fields} to {field_name}",
            f"Mapping from source system field {input_fields} to API field {field_name}",
            f"Normalized field name from {input_fields} to standard {field_name}"
        ]

        transform_descriptions = [
            f"Transform {input_fields} from {input_type} to {field_name} in {output_type}",
            f"Extract and process {input_fields} to create {field_name}",
            f"Apply business rules to {input_fields} resulting in {field_name}",
            f"Format and validate {input_fields} to produce {field_name}"
        ]

        # Select between rename or transformation
        if field_name.lower() == input_fields.lower() or random.random() < 0.3:
            return random.choice(rename_transformations)
        else:
            return random.choice(transform_descriptions)
