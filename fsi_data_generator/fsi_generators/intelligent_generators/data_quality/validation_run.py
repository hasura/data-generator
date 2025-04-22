from __future__ import annotations

import json
import random
from datetime import datetime
from typing import Any, Dict, List


def generate_random_validation_run(id_fields: Dict[str, Any], dg: Any = None) -> Dict[str, Any]:
    """
    Generate a random data quality validation run with plausible values for GraphQL API validation.

    Args:
        id_fields: Dictionary containing the required ID fields (validation_run_id will be included)
        dg: DataGenerator instance (optional)

    Returns:
        Dictionary containing randomly generated validation run data
    """
    # Get database connection if available
    conn = None
    if dg is not None:
        conn = dg.conn

    # Use the timestamp from id_fields or current time
    run_timestamp = id_fields.get('run_timestamp', datetime.now())

    # Random source systems
    source_systems = [
        "consumer_banking.api",
        "credit_cards.api",
        "mortgage_services.api",
        "small_business_banking.api",
        "openbanking.api",
        None  # Sometimes no source is specified
    ]

    # Common GraphQL operations
    operations = [
        "getAccountDetails",
        "getTransactionHistory",
        "getCustomerProfile",
        "searchTransactions",
        "getStatements",
        "updateAccountSettings",
        "getCardsForAccount",
        None  # Sometimes no operation is specified
    ]

    # Instead of hardcoded roles, fetch roles from security system if connection available
    # Otherwise fall back to sample roles
    roles: List[str | None] = []
    if conn:
        cursor = conn.cursor()
        try:
            # Query roles from the security.roles table
            cursor.execute("""
                SELECT role_name 
                FROM security.roles 
                WHERE status = 'ACTIVE'
                ORDER BY RANDOM()
                LIMIT 20
            """)
            roles = [row[0] for row in cursor.fetchall()]

            # If no roles found, use fallback roles
            if not roles:
                roles = _get_fallback_roles()

        except Exception as e:
            # If query fails, use fallback roles
            print(f"Warning: Could not fetch roles from database: {e}")
            roles = _get_fallback_roles()
        finally:
            cursor.close()
    else:
        # No connection available, use fallback roles
        roles = _get_fallback_roles()

    # Add None as a possibility (sometimes no role is specified)
    roles.append(None)

    # Common entity types for GraphQL schemas
    entity_types = ["Account", "Transaction", "Customer", "Card", "Statement", "Payment", "Balance"]

    # Generate random GraphQL query
    entity = random.choice(entity_types)

    # Add some basic fields
    base_fields = ["id", "createdAt", "updatedAt"]

    # Add entity-specific fields
    if entity == "Account":
        entity_fields = ["accountNumber", "status", "accountType", "balance", "availableBalance", "currencyCode"]
    elif entity == "Transaction":
        entity_fields = ["amount", "date", "description", "category", "status", "merchantName", "transactionType"]
    elif entity == "Customer":
        entity_fields = ["firstName", "lastName", "email", "phoneNumber", "dateOfBirth", "customerNumber"]
    elif entity == "Card":
        entity_fields = ["cardNumber", "cardType", "expirationDate", "status", "cardHolderName", "cvv"]
    elif entity == "Statement":
        entity_fields = ["statementDate", "dueDate", "startDate", "endDate", "totalDue", "minimumDue"]
    elif entity == "Payment":
        entity_fields = ["paymentDate", "amount", "method", "status", "confirmationNumber", "paymentType"]
    elif entity == "Balance":
        entity_fields = ["currentBalance", "availableBalance", "pendingTransactions", "lastUpdated"]
    else:
        entity_fields = []

    # Select a random subset of entity fields
    selected_fields = random.sample(base_fields, k=min(len(base_fields), random.randint(1, len(base_fields))))
    selected_fields.extend(random.sample(entity_fields, k=min(len(entity_fields), random.randint(2, 5))))

    # Add nested objects with their own fields (30% chance)
    if random.random() < 0.3:
        if entity == "Account":
            nested_entity = random.choice(["owner", "transactions", "statements"])
            nested_fields = ["id"]
            if nested_entity == "owner":
                nested_fields.extend(["firstName", "lastName", "email"])
            elif nested_entity == "transactions":
                nested_fields.extend(["amount", "date", "description"])
            elif nested_entity == "statements":
                nested_fields.extend(["statementDate", "totalDue"])

            nested_selection = " ".join(nested_fields)
            selected_fields.append(f"{nested_entity} {{ {nested_selection} }}")

    # Format the fields for the query
    fields_selection = "\n      ".join(selected_fields)

    # Choose a query or mutation
    operation_type = "query" if random.random() < 0.8 else "mutation"

    # Generate variables for later use
    variables = {}

    # Generate parameters
    if operation_type == "query":
        operation_name = random.choice([f"get{entity}", f"find{entity}", f"search{entity}s"])
        param_name = "id" if random.random() < 0.7 else entity.lower() + "Id"
        param_value = str(random.randint(1000, 9999))

        # Build the query - properly using param_name in the query
        query = f"""{operation_type} {operation_name}(${param_name}: ID!) {{
  {operation_name.lower()}({param_name}: ${param_name}) {{
      {fields_selection}
  }}
}}"""

        # Update the variables to use the correct parameter name
        variables = {
            param_name: param_value
        }

    else:  # mutation
        operation_name = random.choice([f"update{entity}", f"create{entity}", f"delete{entity}"])
        param_name = "id" if random.random() < 0.7 else entity.lower() + "Id"
        param_value = str(random.randint(1000, 9999))

        if "create" in operation_name or "update" in operation_name:
            # Add some input fields for the GraphQL query
            input_fields = []

            if entity == "Account":
                input_fields = ["accountType: $accountType", "currencyCode: $currencyCode"]
                # Add corresponding variables
                variables["accountType"] = "CHECKING"
                variables["currencyCode"] = "USD"
            elif entity == "Transaction":
                input_fields = ["amount: $amount", "description: $description"]
                # Add corresponding variables
                variables["amount"] = round(random.uniform(1, 1000), 2)
                variables["description"] = "Online Purchase"
            elif entity == "Customer":
                input_fields = ["firstName: $firstName", "lastName: $lastName", "email: $email"]
                # Add corresponding variables
                variables["firstName"] = "John"
                variables["lastName"] = "Doe"
                variables["email"] = "john.doe@example.com"

            input_selection = ", ".join(input_fields)

            # Build the mutation with proper parameter usage
            query = f"""{operation_type} {operation_name}(${param_name}: ID!, $accountType: String, $currencyCode: String) {{
  {operation_name.lower()}({param_name}: ${param_name}, input: {{ {input_selection} }}) {{
      {fields_selection}
  }}
}}"""
        else:
            # Simple delete-type mutation
            query = f"""{operation_type} {operation_name}(${param_name}: ID!) {{
  {operation_name.lower()}({param_name}: ${param_name}) {{
      {fields_selection}
  }}
}}"""

        # Always add the ID parameter to variables
        variables[param_name] = param_value

    # Generate schema for validation
    schema = {
        "type": "object",
        "required": ["data"],
        "properties": {
            "data": {
                "type": "object",
                "required": [operation_name.lower()],
                "properties": {
                    operation_name.lower(): {
                        "type": "object",
                        "required": ["id"],
                        "properties": {
                            "id": {"type": "string"}
                        }
                    }
                }
            }
        }
    }

    # Add property validations based on selected fields
    entity_property = schema["properties"]["data"]["properties"][operation_name.lower()]

    for field in selected_fields:
        if '{' not in field:  # Skip nested fields
            if field in ["id", "accountNumber", "cardNumber", "confirmationNumber"]:
                entity_property["properties"][field] = {"type": "string"}
            elif field in ["amount", "balance", "availableBalance", "totalDue", "minimumDue"]:
                entity_property["properties"][field] = {"type": "number", "minimum": 0}
            elif field in ["status", "accountType", "transactionType", "cardType"]:
                entity_property["properties"][field] = {"type": "string", "enum": ["ACTIVE", "INACTIVE", "PENDING"]}
            elif field in ["createdAt", "updatedAt", "date", "statementDate", "dueDate"]:
                entity_property["properties"][field] = {"type": "string", "format": "date-time"}
            elif field in ["firstName", "lastName", "email", "description", "merchantName"]:
                entity_property["properties"][field] = {"type": "string"}

    # Random error count (often 0, sometimes more)
    error_distribution = [0] * 7 + [1] * 2 + [2] + [random.randint(3, 10)]
    total_errors = random.choice(error_distribution)

    # Create the validation run record
    validation_run = {
        # Include the ID field from id_fields
        "run_timestamp": run_timestamp,
        "source_identifier": random.choice(source_systems),
        "run_user": _get_random_user(conn) if conn else f"user_{random.randint(1000, 9999)}",
        "run_role": random.choice(roles),
        "operation_name": operation_name,
        "variables": json.dumps(variables),
        "validation_config_data": random.choice([True, False]),
        "validation_config_verbose": random.choice([True, False, False, False]),  # Less likely to be verbose
        "validation_config_all_errors": random.choice([True, True, False]),  # More likely to show all errors
        "validation_config_strict": random.choice([True, False, False]),  # Less likely to be strict
        "query": query,
        "validation_schema": json.dumps(schema),
        "total_errors": total_errors
    }

    return validation_run


def _get_fallback_roles():
    """Provides fallback roles if database query fails"""
    return [
        "SYSTEM",
        "API_CLIENT",
        "EXTERNAL_APP",
        "MOBILE_APP",
        "WEB_PORTAL",
        "THIRD_PARTY_SERVICE",
        "DATA_ANALYST",
        "LOAN_OFFICER",
        "CUSTOMER_SERVICE_REP",
        "ADMIN"
    ]


def _get_random_user(conn):
    """Get a random username from the security system"""
    if not conn:
        return f"user_{random.randint(1000, 9999)}"

    cursor = conn.cursor()
    try:
        # Try to get a random identity name from the security system
        cursor.execute("""
            SELECT name 
            FROM security.identities 
            WHERE inactive = FALSE
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()
        if result:
            return result[0]

        # If no identities found, try accounts
        cursor.execute("""
            SELECT name 
            FROM security.accounts 
            WHERE disabled = FALSE
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()
        if result:
            return result[0]

        # Fallback
        return f"user_{random.randint(1000, 9999)}"
    except Exception as e:
        print(f"Warning: Could not fetch users from database: {e}")
        return f"user_{random.randint(1000, 9999)}"
    finally:
        cursor.close()
