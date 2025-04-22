import json
import random
from typing import Any, Dict, List


def generate_random_validation_error(id_fields: Dict[str, Any], dg: Any = None) -> Dict[str, Any]:
    """
    Generate a random data quality validation error with plausible values that are consistent
    with the parent validation run.

    Args:
        id_fields: Dictionary containing the required ID fields (validation_error_id, validation_run_id)
        dg: DataGenerator instance (optional)

    Returns:
        Dictionary containing randomly generated validation error data
    """
    # Get database connection if available
    conn = None
    if dg is not None:
        conn = dg.conn

    # Check required ID fields
    if 'validation_run_id' not in id_fields:
        raise ValueError("validation_run_id is required in id_fields")

    # Fetch parent validation run data if database connection is available
    parent_run = None
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT 
                    query, 
                    validation_schema, 
                    operation_name,
                    variables,
                    total_errors
                FROM 
                    data_quality.validation_run
                WHERE 
                    validation_run_id = %s
            """, (id_fields['validation_run_id'],))

            result = cursor.fetchone()
            if result:
                parent_run = {
                    'query': result[0],
                    'validation_schema': result[1],
                    'operation_name': result[2],
                    'variables': result[3],
                    'total_errors': result[4]
                }
        except Exception as e:
            print(f"Warning: Could not fetch parent validation run: {e}")
        finally:
            cursor.close()

    # If we have the parent run data, make errors consistent with it
    # Otherwise, generate plausible errors for GraphQL validations
    if parent_run:
        validation_error = _generate_consistent_error(id_fields, parent_run)
    else:
        validation_error = _generate_random_graphql_error(id_fields)

    return validation_error


def _generate_consistent_error(id_fields: Dict[str, Any], parent_run: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a validation error consistent with the parent validation run.

    Args:
        id_fields: Dictionary containing ID fields
        parent_run: Dictionary containing parent validation run data

    Returns:
        Dictionary containing validation error data
    """
    # Parse the validation schema to understand its structure
    try:
        schema = json.loads(parent_run['validation_schema'])
    except (json.JSONDecodeError, TypeError):
        # If schema parsing fails, fall back to random error
        return _generate_random_graphql_error(id_fields)

    # Get operation name from parent run
    operation_name = parent_run.get('operation_name', 'query')
    operation_name_lower = operation_name.lower() if operation_name else 'query'

    # Extract entity type from operation name (e.g., getAccount -> Account)
    entity_type = _extract_entity_from_operation(operation_name)

    # Find possible schema paths and error keywords based on the schema
    schema_paths = []
    error_keywords = []

    # Start building schema paths based on typical GraphQL response structure
    if 'properties' in schema and 'data' in schema['properties']:
        data_schema = schema['properties']['data']
        if 'properties' in data_schema and operation_name_lower in data_schema['properties']:
            entity_schema = data_schema['properties'][operation_name_lower]

            # Add basic schema path patterns
            schema_paths.append(f"#/properties/data/properties/{operation_name_lower}")

            # Add property-specific schema paths
            if 'properties' in entity_schema:
                for prop_name in entity_schema['properties']:
                    schema_paths.append(f"#/properties/data/properties/{operation_name_lower}/properties/{prop_name}")

                    prop_schema = entity_schema['properties'][prop_name]
                    if isinstance(prop_schema, dict):
                        # Add error keyword based on property type
                        if 'type' in prop_schema:
                            error_keywords.append('type')
                        if 'format' in prop_schema:
                            error_keywords.append('format')
                        if 'minimum' in prop_schema:
                            error_keywords.append('minimum')
                        if 'enum' in prop_schema:
                            error_keywords.append('enum')

    # If we couldn't extract paths from the schema, use generic paths
    if not schema_paths:
        schema_paths = [
            "#/properties/data",
            "#/properties/data/properties/query",
            "#/properties/data/required",
            "#/properties/data/type"
        ]

    # If we couldn't extract error keywords, use common ones
    if not error_keywords:
        error_keywords = ['type', 'required', 'format', 'minimum', 'enum', 'additionalProperties']

    # Instance paths - where in the result data the error occurred
    instance_paths = [
        "",  # Root
        "/data",
        f"/data/{operation_name_lower}",
        f"/data/{operation_name_lower}/id",
    ]

    # Add some entity-specific paths if we have the entity type
    if entity_type:
        properties = _generate_entity_properties(entity_type)
        for prop in properties:
            instance_paths.append(f"/data/{operation_name_lower}/{prop}")

            # If prop might be an object itself, add a subpath
            if prop in ['owner', 'transactions', 'statements']:
                instance_paths.append(f"/data/{operation_name_lower}/{prop}/id")

    # Select a schema path and instance path
    schema_path = random.choice(schema_paths)
    instance_path = random.choice(instance_paths)
    error_keyword = random.choice(error_keywords)

    # Create error data based on the chosen error_keyword
    error_data = _generate_error_for_keyword(error_keyword, instance_path, entity_type)

    # Create the validation error
    validation_error = {
        "validation_error_id": id_fields["validation_error_id"],
        "validation_run_id": id_fields["validation_run_id"],
        "instance_path": error_data["instance_path"],
        "schema_path": schema_path,
        "error_keyword": error_keyword,
        "error_message": error_data["error_message"],
        "failed_data": error_data["failed_data"],
        "error_params": json.dumps(error_data["error_params"]) if error_data.get("error_params") else None,
        "error_schema_detail": None,  # Usually not populated for simpler errors
        "error_parent_schema_detail": None  # Usually not populated for simpler errors
    }

    return validation_error


def _generate_entity_properties(entity_type: str) -> List[str]:
    """
    Generate appropriate properties for a given entity type.

    Args:
        entity_type: The entity type (e.g., Account, Transaction)

    Returns:
        List of property names
    """
    if entity_type == "Account":
        return ["id", "accountNumber", "status", "balance", "availableBalance", "createdAt", "currencyCode", "owner"]
    elif entity_type == "Transaction":
        return ["id", "amount", "date", "description", "status", "category", "merchantName"]
    elif entity_type == "Customer":
        return ["id", "firstName", "lastName", "email", "phoneNumber", "dateOfBirth"]
    elif entity_type == "Card":
        return ["id", "cardNumber", "expirationDate", "status", "cardHolderName"]
    else:
        # Generic properties
        return ["id", "name", "status", "createdAt", "updatedAt"]


def _extract_entity_from_operation(operation_name: str) -> str:
    """
    Extract the entity type from an operation name.

    Args:
        operation_name: GraphQL operation name (e.g., getAccount, updateCustomer)

    Returns:
        Entity type (e.g., Account, Customer)
    """
    if not operation_name:
        return ""

    # Common prefixes in GraphQL operations
    prefixes = ["get", "find", "search", "update", "create", "delete", "query", "mutation"]

    # Remove the prefix and get the entity name
    for prefix in prefixes:
        if operation_name.lower().startswith(prefix):
            # Extract and capitalize the first letter
            entity = operation_name[len(prefix):]
            if entity:
                if entity.endswith('s') and len(entity) > 2:
                    # Handle plurals (e.g., searchAccounts -> Account)
                    entity = entity[:-1]
                return entity

    # If no prefix found, return the original name
    return operation_name


def _generate_error_for_keyword(error_keyword: str, instance_path: str, entity_type: str) -> Dict[str, Any]:
    """
    Generate error details specific to a validation keyword.

    Args:
        error_keyword: The JSON Schema keyword that failed
        instance_path: Path to the instance that failed validation
        entity_type: Type of entity being validated

    Returns:
        Dictionary with error details
    """
    result: dict = {
        "instance_path": instance_path,
        "error_message": "",
        "failed_data": "",
        "error_params": {}
    }

    if error_keyword == "type":
        # Type errors occur when the data type is wrong
        expected_type = random.choice(["string", "number", "boolean", "object", "array"])
        actual_type = random.choice(
            [t for t in ["string", "number", "boolean", "object", "array"] if t != expected_type])

        if actual_type == "string":
            if expected_type == "number":
                result["failed_data"] = '"12345"'
            elif expected_type == "boolean":
                result["failed_data"] = '"true"'
            else:
                result["failed_data"] = '"Some Value"'
        elif actual_type == "number":
            result["failed_data"] = "123.45"
        elif actual_type == "boolean":
            result["failed_data"] = "true"
        elif actual_type == "object":
            result["failed_data"] = "{}"
        elif actual_type == "array":
            result["failed_data"] = "[]"

        result["error_message"] = f"must be {expected_type}"
        result["error_params"] = {"type": expected_type}

    elif error_keyword == "required":
        # Required errors occur when a required property is missing
        prop_name = "id"
        if entity_type:
            props = _generate_entity_properties(entity_type)
            if props:
                prop_name = random.choice(props)

        result["error_message"] = f"must have required property '{prop_name}'"
        result["error_params"] = {"missingProperty": prop_name}

    elif error_keyword == "format":
        # Format errors occur when a string doesn't match the expected format
        format_name = random.choice(["date-time", "email", "uri", "uuid"])

        if format_name == "date-time":
            result["failed_data"] = '"2023-13-45T25:70:99Z"'  # Invalid date-time
            result["error_message"] = "must match format \"date-time\""
        elif format_name == "email":
            result["failed_data"] = '"not-an-email"'
            result["error_message"] = "must match format \"email\""
        elif format_name == "uri":
            result["failed_data"] = '"not-a-url"'
            result["error_message"] = "must match format \"uri\""
        elif format_name == "uuid":
            result["failed_data"] = '"not-a-uuid"'
            result["error_message"] = "must match format \"uuid\""

        result["error_params"] = {"format": format_name}

    elif error_keyword == "minimum":
        # Minimum errors occur when a number is below the minimum
        minimum = random.randint(1, 100)
        actual = random.randint(-100, minimum - 1)

        result["failed_data"] = str(actual)
        result["error_message"] = f"must be >= {minimum}"
        result["error_params"] = {"minimum": minimum}

    elif error_keyword == "enum":
        # Enum errors occur when a value isn't in the allowed set
        enum_values = ["ACTIVE", "INACTIVE", "PENDING"]
        actual = "UNKNOWN"

        result["failed_data"] = f'"{actual}"'
        result["error_message"] = "must be equal to one of the allowed values"
        result["error_params"] = {"allowedValues": enum_values}

    elif error_keyword == "additionalProperties":
        # Additional property errors occur when unexpected properties exist
        prop_name = "unknownProperty"

        result["error_message"] = f"must NOT have additional properties, found '{prop_name}'"
        result["error_params"] = {"additionalProperty": prop_name}

    else:
        # Generic error for other keywords
        result["error_message"] = f"failed {error_keyword} validation"

    return result


def _generate_random_graphql_error(id_fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a plausible but random GraphQL validation error when parent data is not available.

    Args:
        id_fields: Dictionary containing ID fields

    Returns:
        Dictionary containing validation error data
    """
    # Common GraphQL error patterns
    error_types = [
        {"keyword": "type", "schema_path": "#/properties/data/properties/query/properties/id/type",
         "message": "must be string", "instance_path": "/data/query/id", "failed_data": "123"},
        {"keyword": "required", "schema_path": "#/properties/data/required",
         "message": "must have required property 'query'", "instance_path": "/data", "failed_data": "{}"},
        {"keyword": "format", "schema_path": "#/properties/data/properties/query/properties/createdAt/format",
         "message": "must match format \"date-time\"", "instance_path": "/data/query/createdAt",
         "failed_data": "\"not-a-date\""},
        {"keyword": "enum", "schema_path": "#/properties/data/properties/query/properties/status/enum",
         "message": "must be equal to one of the allowed values", "instance_path": "/data/query/status",
         "failed_data": "\"UNKNOWN\""},
        {"keyword": "minimum", "schema_path": "#/properties/data/properties/query/properties/balance/minimum",
         "message": "must be >= 0", "instance_path": "/data/query/balance", "failed_data": "-10.5"},
    ]

    # Choose a random error pattern
    error_type = random.choice(error_types)

    # Build the error
    validation_error = {
        "validation_run_id": id_fields["validation_run_id"],
        "instance_path": error_type["instance_path"],
        "schema_path": error_type["schema_path"],
        "error_keyword": error_type["keyword"],
        "error_message": error_type["message"],
        "failed_data": error_type["failed_data"],
        "error_params": None,
        "error_schema_detail": None,
        "error_parent_schema_detail": None
    }

    # Add error params for some error types
    if error_type["keyword"] == "type":
        validation_error["error_params"] = json.dumps({"type": "string"})
    elif error_type["keyword"] == "required":
        validation_error["error_params"] = json.dumps({"missingProperty": "query"})
    elif error_type["keyword"] == "format":
        validation_error["error_params"] = json.dumps({"format": "date-time"})
    elif error_type["keyword"] == "enum":
        validation_error["error_params"] = json.dumps({"allowedValues": ["ACTIVE", "INACTIVE", "PENDING"]})
    elif error_type["keyword"] == "minimum":
        validation_error["error_params"] = json.dumps({"minimum": 0})

    return validation_error
