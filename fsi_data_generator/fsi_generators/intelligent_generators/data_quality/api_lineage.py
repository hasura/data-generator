import logging
import random
from typing import Any, Dict
from datetime import datetime, timedelta

import psycopg2
from faker import Faker

from data_generator import DataGenerator, SkipRowGenerationError

logger = logging.getLogger(__name__)
fake = Faker()  # Initialize Faker

# Dictionary to track unique API paths per application to avoid duplicates
api_paths_per_app = {}


def generate_random_api_lineage(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "data_quality"."api_lineage" record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (api_lineage_id, app_mgmt_application_id, security_host_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated API lineage data
    """
    # Get connection for fetching related data
    conn = dg.conn

    # Extract the application ID from _id_fields
    app_mgmt_application_id_host_id = _id_fields.get("host_app_mgmt_application_id")

    if app_mgmt_application_id_host_id is None:
        # If no application ID is provided, we can't generate a valid record
        raise SkipRowGenerationError("No application ID provided")

    (related_host_id, app_mgmt_application_id) = app_mgmt_application_id_host_id

    # Override the security_host_id in _id_fields with our related host
    _id_fields["security_host_id"] = related_host_id
    _id_fields["app_mgmt_application_id"] = app_mgmt_application_id
    _id_fields["host_app_mgmt_application_id"] = None

    # Fetch application info including hostname
    app_info = _get_application_info(conn, app_mgmt_application_id, related_host_id)

    if not app_info or not app_info.get("hostname"):
        # If no host name is available, skip row generation
        raise SkipRowGenerationError("No host name available for this application")

    # Get server name from the application's hostname
    server_name = app_info["hostname"]

    # Generate a business function-oriented REST API endpoint for this application
    api_details = _generate_unique_rest_endpoint(app_mgmt_application_id, server_name,
                                                 app_info.get("application_type", "WEB"))

    api_call = api_details["endpoint"]
    base_name = api_details["base_name"]

    # Generate version numbers - consider the application's history
    # Check if we already have versions for this base endpoint
    existing_versions = _get_existing_versions(base_name, app_mgmt_application_id, api_paths_per_app)

    version_info = _generate_version_info(existing_versions)
    major_version = version_info["major_version"]
    minor_version = version_info["minor_version"]

    # Generate a GraphQL query as the internal representation (kept from original)
    query = _generate_graphql_query(api_call, app_info.get("application_type", "WEB"))

    # Generate dates with proper versioning logic
    date_info = _generate_versioned_dates(existing_versions, version_info["is_latest"])
    start_date = date_info["start_date"]
    end_date = date_info["end_date"]
    updated_at = date_info["updated_at"]

    # Create the API lineage record
    api_lineage = {
        "host_app_mgmt_application_id": None,
        "app_mgmt_application_id": _id_fields["app_mgmt_application_id"],
        "security_host_id": _id_fields["security_host_id"],
        "server_name": server_name,
        "major_version": major_version,
        "minor_version": minor_version,
        "api_call": api_call,
        "query": query,
        "description": _generate_api_description(api_call, app_info.get("application_type", "WEB")),
        "start_date": start_date,
        "end_date": end_date,
        "updated_at": updated_at,
        "base_name": base_name  # Add base_name for tracking versions (can be removed if not needed in DB)
    }

    # Track this version in our global dictionary
    if base_name not in api_paths_per_app.get(app_mgmt_application_id, {}):
        if app_mgmt_application_id not in api_paths_per_app:
            api_paths_per_app[app_mgmt_application_id] = {}
        api_paths_per_app[app_mgmt_application_id][base_name] = []

    api_paths_per_app[app_mgmt_application_id][base_name].append({
        "major_version": major_version,
        "minor_version": minor_version,
        "start_date": start_date,
        "end_date": end_date,
        "is_latest": version_info["is_latest"]
    })

    # Remove the base_name field since it's not in the database schema
    api_lineage.pop("base_name", None)

    return api_lineage


def _get_application_info(conn, app_mgmt_application_id, host_id=None):
    """
    Get application information including hostname from the database.

    Args:
        conn: PostgreSQL connection object
        app_mgmt_application_id: UUID of the application
        host_id: UUID of the host to use for finding hostname

    Returns:
        Dictionary containing application information or None if not found
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.application_name, a.application_type
            FROM app_mgmt.applications a
            WHERE a.app_mgmt_application_id = %s
            LIMIT 1
        """, (app_mgmt_application_id,))

        result1 = cursor.fetchone()

        cursor.execute("""
                    SELECT a.security_host_id, a.hostname
                    FROM security.hosts a
                    WHERE a.security_host_id = %s
                    LIMIT 1
                """, (host_id,))

        result2 = cursor.fetchone()
        cursor.close()

        if result1 and result2:
            return result1 | result2

        # If we didn't find a host, get just the application info
        cursor = conn.cursor()
        cursor.execute("""
            SELECT application_name, application_type
            FROM app_mgmt.applications
            WHERE app_mgmt_application_id = %s
        """, (app_mgmt_application_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return result

        return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching application information: {error}")
        return None


def _get_existing_versions(base_name, app_id, api_paths_dict):
    """
    Get existing versions for a base API endpoint.

    Args:
        base_name: Base name of the API endpoint
        app_id: Application ID
        api_paths_dict: Dictionary tracking API versions

    Returns:
        List of existing versions or empty list if none
    """
    if app_id in api_paths_dict and base_name in api_paths_dict[app_id]:
        return api_paths_dict[app_id][base_name]
    return []


def _generate_version_info(existing_versions):
    """
    Generate version information for an API endpoint.

    Args:
        existing_versions: List of existing versions

    Returns:
        Dictionary with major_version, minor_version and is_latest flag
    """
    is_latest = True

    if not existing_versions:
        # First version of this API
        major_version = 1
        minor_version = 0
    else:
        # Determine if we should create a new major or minor version
        latest_versions = sorted(
            existing_versions,
            key=lambda x: (x["major_version"], x["minor_version"]),
            reverse=True
        )

        latest = latest_versions[0]

        # For APIs with many versions, increase chance of major version bump
        version_count = len(existing_versions)
        major_version_probability = min(0.2 + (version_count * 0.05), 0.5)  # Max 50% chance

        # Higher chance of major version bump if we already have several minor versions
        if latest["minor_version"] >= 3:
            major_version_probability += 0.2  # Add 20% more chance after 3+ minor versions

        # 20-70% chance of creating a new major version depending on history
        if random.random() < major_version_probability and len(existing_versions) > 0:
            major_version = latest["major_version"] + 1
            minor_version = 0
        else:
            # Create a new minor version
            major_version = latest["major_version"]
            minor_version = latest["minor_version"] + 1

        # Mark all previous versions as no longer latest
        for ver in existing_versions:
            if ver.get("is_latest", False):
                ver["is_latest"] = False

    return {
        "major_version": major_version,
        "minor_version": minor_version,
        "is_latest": is_latest
    }


def _generate_versioned_dates(existing_versions, is_latest):
    """
    Generate dates for API versioning with proper progression.

    Args:
        existing_versions: List of existing versions
        is_latest: Whether this is the latest version

    Returns:
        Dictionary with start_date, end_date and updated_at
    """
    if not existing_versions:
        # First version starts sometime in the past 2 years
        start_date = fake.date_time_between(start_date="-2y", end_date="-6m")
    else:
        # Find the latest version's end date to use as our start date
        latest_versions = sorted(
            existing_versions,
            key=lambda x: (x["major_version"], x["minor_version"]),
            reverse=True
        )

        # For the latest existing version, make sure it has an end date
        # This ensures proper versioning as a new version is being created
        if latest_versions and latest_versions[0].get("is_latest", False):
            previous_latest = latest_versions[0]
            if previous_latest.get("end_date") is None:
                # Set an end date for the previous latest version
                # Make it between 1-3 months ago
                previous_latest["end_date"] = fake.date_time_between(start_date="-3m", end_date="-1m")
                previous_latest["is_latest"] = False

        # Get the most recent end date as our start date
        latest_end_dates = [v.get("end_date") for v in latest_versions if v.get("end_date") is not None]

        if latest_end_dates:
            # Use the most recent end date plus a small gap (1-5 days) as our start date
            most_recent_end = max(latest_end_dates)
            start_date = most_recent_end + timedelta(days=random.randint(1, 5))
        else:
            # No end dates found, use a recent date
            start_date = fake.date_time_between(start_date="-6m", end_date="-1m")

    # Latest versions typically have no end date (still active)
    # 80% of latest versions are still active
    if is_latest and random.random() < 0.8:
        end_date = None
    else:
        # For non-latest or deprecated versions, set an end date
        # Make sure it's at least 30 days after start_date
        min_end_date = start_date + timedelta(days=30)
        # If min_end_date is in the future, use today as the end_date
        if min_end_date > datetime.now():
            # 50% chance of having no end date for recent endpoints
            if random.random() < 0.5:
                end_date = None
            else:
                end_date = datetime.now()
        else:
            end_date = fake.date_time_between(start_date=min_end_date, end_date="now")

    # Updated at is always after start date and before end date (if exists)
    if end_date:
        updated_at = fake.date_time_between(start_date=start_date, end_date=end_date)
    else:
        updated_at = fake.date_time_between(start_date=start_date, end_date="now")

    return {
        "start_date": start_date,
        "end_date": end_date,
        "updated_at": updated_at
    }


def _generate_unique_rest_endpoint(app_id, server_name, app_type):
    """
    Generate a unique REST API endpoint path for the application.

    Args:
        app_id: Application ID
        server_name: Server hostname
        app_type: Type of application

    Returns:
        Dictionary containing the endpoint string and base name
    """
    # Initialize tracking dictionary for this app if not exists
    if app_id not in api_paths_per_app:
        api_paths_per_app[app_id] = {}

    # REST APIs use various HTTP methods
    methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    method = random.choice(methods)

    # Generate business function based endpoints
    if server_name and "banking" in server_name.lower():
        domains = ["accounts", "transfers", "statements", "payments", "beneficiaries"]
        resources = {
            "accounts": ["balances", "transactions", "details", "status", "preferences"],
            "transfers": ["domestic", "international", "scheduled", "recurring", "status"],
            "statements": ["monthly", "annual", "custom", "pdf", "csv"],
            "payments": ["scheduled", "recurring", "bill", "p2p", "status"],
            "beneficiaries": ["domestic", "international", "favorites", "recent", "status"]
        }
        domain = random.choice(domains)

        # Determine if we're creating a collection or specific resource endpoint
        is_collection = random.choice([True, False])

        if is_collection:
            base_name = f"banking-{domain}"
            path = f"/api/banking/{domain}"

            # For collection endpoints, GET is most common
            if method not in ["GET", "POST"]:
                method = "GET"
        else:
            resource = random.choice(resources[domain])
            base_name = f"banking-{domain}-{resource}"

            if method in ["GET", "PUT", "DELETE"]:
                path = f"/api/banking/{domain}/{{id}}/{resource}"
            else:
                path = f"/api/banking/{domain}/{resource}"

    elif server_name and "credit" in server_name.lower():
        domains = ["cards", "rewards", "statements", "payments", "applications"]
        resources = {
            "cards": ["transactions", "limits", "activation", "pin", "security"],
            "rewards": ["points", "cashback", "redemption", "catalog", "history"],
            "statements": ["current", "previous", "pdf", "dispute", "breakdown"],
            "payments": ["due", "minimum", "schedule", "history", "methods"],
            "applications": ["status", "documents", "approval", "offers", "prequalify"]
        }
        domain = random.choice(domains)

        # Determine if we're creating a collection or specific resource endpoint
        is_collection = random.choice([True, False])

        if is_collection:
            base_name = f"cards-{domain}"
            path = f"/api/cards/{domain}"

            # For collection endpoints, GET is most common
            if method not in ["GET", "POST"]:
                method = "GET"
        else:
            resource = random.choice(resources[domain])
            base_name = f"cards-{domain}-{resource}"

            if method in ["GET", "PUT", "DELETE"]:
                path = f"/api/cards/{domain}/{{id}}/{resource}"
            else:
                path = f"/api/cards/{domain}/{resource}"

    elif server_name and "mortgage" in server_name.lower():
        domains = ["loans", "applications", "payments", "documents", "properties"]
        resources = {
            "loans": ["details", "schedule", "balance", "history", "options"],
            "applications": ["status", "documents", "preapproval", "closing", "requirements"],
            "payments": ["schedule", "history", "extra", "escrow", "breakdown"],
            "documents": ["statements", "tax", "insurance", "closing", "agreement"],
            "properties": ["valuation", "insurance", "taxes", "liens", "details"]
        }
        domain = random.choice(domains)

        # Determine if we're creating a collection or specific resource endpoint
        is_collection = random.choice([True, False])

        if is_collection:
            base_name = f"mortgage-{domain}"
            path = f"/api/mortgage/{domain}"

            # For collection endpoints, GET is most common
            if method not in ["GET", "POST"]:
                method = "GET"
        else:
            resource = random.choice(resources[domain])
            base_name = f"mortgage-{domain}-{resource}"

            if method in ["GET", "PUT", "DELETE"]:
                path = f"/api/mortgage/{domain}/{{id}}/{resource}"
            else:
                path = f"/api/mortgage/{domain}/{resource}"

    elif app_type == "MICROSERVICE":
        domains = ["data", "auth", "config", "metrics", "notifications"]
        resources = {
            "data": ["query", "transform", "sync", "backup", "validate"],
            "auth": ["tokens", "permissions", "roles", "sessions", "users"],
            "config": ["env", "features", "settings", "defaults", "overrides"],
            "metrics": ["performance", "usage", "errors", "latency", "health"],
            "notifications": ["email", "sms", "webhooks", "events", "templates"]
        }
        domain = random.choice(domains)

        # Determine if we're creating a collection or specific resource endpoint
        is_collection = random.choice([True, False])

        if is_collection:
            base_name = f"service-{domain}"
            path = f"/api/service/{domain}"

            # For collection endpoints, GET is most common
            if method not in ["GET", "POST"]:
                method = "GET"
        else:
            resource = random.choice(resources[domain])
            base_name = f"service-{domain}-{resource}"

            if method in ["GET", "PUT", "DELETE"]:
                path = f"/api/service/{domain}/{{id}}/{resource}"
            else:
                path = f"/api/service/{domain}/{resource}"

    else:
        # Generic REST API
        domains = ["users", "products", "orders", "reports", "settings"]
        resources = {
            "users": ["profile", "preferences", "permissions", "history", "devices"],
            "products": ["inventory", "pricing", "categories", "reviews", "images"],
            "orders": ["status", "history", "details", "shipment", "return"],
            "reports": ["daily", "monthly", "custom", "export", "dashboard"],
            "settings": ["account", "notifications", "security", "billing", "features"]
        }
        domain = random.choice(domains)

        # Determine if we're creating a collection or specific resource endpoint
        is_collection = random.choice([True, False])

        if is_collection:
            base_name = f"api-{domain}"
            path = f"/api/{domain}"

            # For collection endpoints, GET is most common
            if method not in ["GET", "POST"]:
                method = "GET"
        else:
            resource = random.choice(resources[domain])
            base_name = f"api-{domain}-{resource}"

            if method in ["GET", "PUT", "DELETE"]:
                path = f"/api/{domain}/{{id}}/{resource}"
            else:
                path = f"/api/{domain}/{resource}"

    endpoint = f"{method} {path}"

    # No need to check for uniqueness as we're tracking by base_name now
    return {
        "endpoint": endpoint,
        "base_name": base_name
    }


def _generate_graphql_query(api_path, app_type):
    """
    Generate a realistic GraphQL query based on the API path and application type.
    This is kept as internal representation of the data that will be exposed via REST.

    Args:
        api_path: The API endpoint path
        app_type: Type of application

    Returns:
        A GraphQL query string
    """
    # Create appropriate query based on endpoint path and app type
    if "banking" in api_path.lower():
        return """query GetAccounts($customerId: ID!) {
  customer(id: $customerId) {
    accounts {
      id
      accountNumber
      accountType
      balance
      currency
      status
      availableBalance
      transactions(limit: 5) {
        id
        date
        amount
        description
      }
    }
  }
}"""
    elif "card" in api_path.lower():
        return """query GetCardDetails($customerId: ID!) {
  customer(id: $customerId) {
    cards {
      id
      cardNumber
      cardType
      expirationDate
      status
      creditLimit
      availableCredit
      currentBalance
      rewards {
        points
        cashbackBalance
      }
    }
  }
}"""
    elif "mortgage" in api_path.lower():
        return """query GetMortgageLoans($customerId: ID!) {
  customer(id: $customerId) {
    mortgageLoans {
      id
      loanNumber
      originalAmount
      currentBalance
      interestRate
      term
      paymentAmount
      nextPaymentDate
      property {
        address
        value
        type
      }
    }
  }
}"""
    elif app_type == "MICROSERVICE":
        return """query GetServiceData($serviceId: ID!, $parameters: ParameterInput) {
  service(id: $serviceId) {
    status
    version
    metrics {
      uptime
      responseTime
      errorRate
    }
    data(parameters: $parameters) {
      results
      pagination {
        total
        page
        pageSize
      }
    }
  }
}"""
    else:
        # Generic GraphQL query
        return """query GetData($id: ID!, $filter: FilterInput) {
  data(id: $id, filter: $filter) {
    id
    name
    description
    created
    modified
    attributes {
      key
      value
    }
    status
    metadata {
      version
      createdBy
      lastUpdated
    }
  }
}"""


def _generate_api_description(api_path, app_type):
    """
    Generate a description for the API endpoint.

    Args:
        api_path: The API endpoint path
        app_type: Type of application

    Returns:
        A description string
    """
    # Extract HTTP method and path for context
    parts = api_path.split(maxsplit=1)
    method = parts[0] if len(parts) > 0 else ""
    path = parts[1] if len(parts) > 1 else ""

    # Define some standard response formats for REST APIs
    response_formats = ["JSON", "HAL+JSON", "JSON:API", "XML"]
    response_format = random.choice(response_formats)

    # Common authentication methods
    auth_methods = [
        "OAuth 2.0", "JWT tokens", "API keys", "Basic authentication",
        "OpenID Connect", "SAML", "Mutual TLS"
    ]
    auth_method = random.choice(auth_methods)

    # Create appropriate descriptions based on the HTTP method, endpoint path and app type
    if "banking" in path.lower():
        if "accounts" in path.lower():
            if method == "GET" and "{id}" in path:
                return f"REST API endpoint that retrieves detailed information for a specific banking account in {response_format} format. Returns account balance, status, transaction history, and customer details. Requires {auth_method} authentication. Used by {random.choice(['online banking portal', 'mobile banking app', 'customer service representatives', 'financial advisors'])}."
            elif method == "GET":
                return f"REST API endpoint that lists all banking accounts for an authenticated customer in {response_format} format. Supports pagination, filtering by account type, and sorting by balance. Requires {auth_method} authentication. Used by {random.choice(['account dashboard', 'financial overview', 'wealth management tools', 'account aggregation services'])}."
            elif method == "POST":
                return f"REST API endpoint that creates a new banking account with {response_format} request and response format. Validates customer eligibility, initiates account opening workflow, and returns the newly created account details. Requires {auth_method} authentication with elevated privileges. Used by {random.choice(['account opening workflow', 'new customer onboarding', 'product recommendation engine', 'promotional campaigns'])}."
            elif method == "PUT":
                return f"REST API endpoint that updates account details or preferences using {response_format} request and response format. Supports partial updates with validation for specific account settings. Requires {auth_method} authentication. Used by {random.choice(['account management services', 'profile management', 'customer preferences center', 'settings management'])}."
            else:
                return f"REST API endpoint for banking account management with {response_format} data exchange. Provides {random.choice(['account access', 'transaction history', 'statement generation', 'balance information'])} capabilities. Requires {auth_method} authentication."
        elif "transfers" in path.lower():
            if method == "POST":
                return f"REST API endpoint that initiates fund transfers between accounts using {response_format} request and response format. Validates sufficient funds, processes the transfer, and returns confirmation details. Requires {auth_method} authentication with transaction privileges. Used by {random.choice(['fund transfer module', 'payment processing system', 'scheduled transfers service', 'mobile banking app'])}."
            elif method == "GET" and "status" in path:
                return f"REST API endpoint that checks transfer status in {response_format} format. Returns processing stage, confirmation details, and estimated completion time. Requires {auth_method} authentication. Used by {random.choice(['transfer tracking interface', 'payment confirmation services', 'transaction monitoring', 'support tools'])}."
            else:
                return f"REST API endpoint for fund transfer operations with {response_format} data exchange. Provides {random.choice(['transfer initiation', 'status tracking', 'history viewing', 'beneficiary management'])} functionality. Requires {auth_method} authentication."
        else:
            return f"Banking REST API endpoint supporting {method} operations with {response_format} format for {path.split('/')[-1]} functionality. Requires {auth_method} authentication. Used within the retail banking ecosystem for customer-facing operations."

    elif "card" in path.lower():
        if "cards" in path.lower():
            if method == "GET" and "{id}" in path:
                return f"REST API endpoint that retrieves credit card information in {response_format} format. Returns current balance, available credit, transaction history, and reward status. Requires {auth_method} authentication. Used by {random.choice(['card management portal', 'mobile banking app', 'customer service representatives', 'fraud detection systems'])}."
            elif method == "GET":
                return f"REST API endpoint that lists all credit cards for a customer in {response_format} format. Supports pagination and filtering by card type or status. Requires {auth_method} authentication. Used by {random.choice(['card dashboard', 'financial overview', 'account summary views', 'wallet applications'])}."
            elif method == "POST":
                return f"REST API endpoint that processes credit card applications with {response_format} request and response format. Performs credit checks, validates customer information, and returns application status. Requires {auth_method} authentication with elevated privileges. Used by {random.choice(['card application workflow', 'instant approval system', 'promotional campaigns', 'cross-selling initiatives'])}."
            else:
                return f"REST API endpoint for credit card management with {response_format} data exchange. Provides {random.choice(['card details', 'transaction history', 'statement access', 'reward information'])} capabilities. Requires {auth_method} authentication."
        elif "rewards" in path.lower():
            if method == "GET":
                return f"REST API endpoint that retrieves reward program information in {response_format} format. Returns point balances, redemption options, and program details. Requires {auth_method} authentication. Used by {random.choice(['rewards portal', 'loyalty program interface', 'mobile banking rewards section', 'marketing campaigns'])}."
            elif method == "POST" and "redemption" in path:
                return f"REST API endpoint that processes reward redemptions with {response_format} request and response format. Validates point balance, applies the redemption, and returns confirmation. Requires {auth_method} authentication. Used by {random.choice(['rewards redemption workflow', 'points management system', 'benefits portal', 'customer engagement platform'])}."
            else:
                return f"REST API endpoint for credit card reward program with {response_format} data exchange. Supports {random.choice(['points tracking', 'redemption options', 'promotion eligibility', 'special offers'])} features. Requires {auth_method} authentication."
        else:
            return f"Card services REST API endpoint supporting {method} operations with {response_format} format for {path.split('/')[-1]} functionality. Requires {auth_method} authentication. Used within the credit card ecosystem for customer account management."

    elif "mortgage" in path.lower():
        if "loans" in path.lower():
            if method == "GET" and "{id}" in path:
                return f"REST API endpoint that retrieves mortgage loan details in {response_format} format. Returns current balance, payment schedule, loan terms, and property information. Requires {auth_method} authentication. Used by {random.choice(['mortgage servicing portal', 'loan management system', 'customer account overview', 'financial advisors'])}."
            elif method == "GET":
                return f"REST API endpoint that lists all mortgage loans for a customer in {response_format} format. Supports pagination and filtering by loan status or type. Requires {auth_method} authentication. Used by {random.choice(['loan dashboard', 'financial overview', 'account summary views', 'wealth management applications'])}."
            else:
                return f"REST API endpoint for mortgage loan management with {response_format} data exchange. Provides {random.choice(['loan details', 'payment history', 'amortization schedules', 'escrow information'])} capabilities. Requires {auth_method} authentication."
        elif "payments" in path.lower():
            if method == "POST":
                return f"REST API endpoint that processes mortgage payments with {response_format} request and response format. Validates payment amount, applies the payment with proper allocation, and returns confirmation. Requires {auth_method} authentication with transaction privileges. Used by {random.choice(['payment processing system', 'automatic payment service', 'online banking portal', 'mobile banking app'])}."
            elif method == "GET" and "history" in path:
                return f"REST API endpoint that retrieves mortgage payment history in {response_format} format. Returns payment dates, amounts, breakdowns, and application details. Supports pagination and date range filtering. Requires {auth_method} authentication. Used by {random.choice(['payment history interface', 'account statements', 'tax preparation tools', 'customer service representatives'])}."
            else:
                return f"REST API endpoint for mortgage payment operations with {response_format} data exchange. Supports {random.choice(['payment scheduling', 'additional principal payments', 'payment history tracking', 'escrow management'])} functionality. Requires {auth_method} authentication."
        else:
            return f"Mortgage services REST API endpoint supporting {method} operations with {response_format} format for {path.split('/')[-1]} functionality. Requires {auth_method} authentication. Used within the mortgage lending ecosystem for loan servicing and management."

    elif app_type == "MICROSERVICE":
        if "metrics" in path.lower():
            return f"Internal REST API endpoint for microservice metrics in {response_format} format. Provides performance statistics, operational data, and health information. Requires {auth_method} authentication with service account privileges. Used by {random.choice(['monitoring systems', 'dashboards', 'alerting services', 'devops tools', 'SRE teams'])}."
        elif "config" in path.lower():
            return f"Internal REST API endpoint for configuration management with {response_format} data exchange. Manages service settings, feature flags, and environment variables. Requires {auth_method} authentication with elevated privileges. Used by {random.choice(['service configuration management', 'deployment pipelines', 'feature flag controls', 'A/B testing frameworks'])}."
        elif "auth" in path.lower():
            return f"Internal REST API endpoint for authentication services with {response_format} format. Handles token validation, permission verification, and identity management. Requires {auth_method} authentication. Used by {random.choice(['API gateways', 'service mesh', 'identity providers', 'security monitoring tools'])}."
        else:
            return f"Internal microservice REST API endpoint supporting {method} operations with {response_format} format for {path.split('/')[-1]} functionality. Requires {auth_method} authentication. Used for {random.choice(['service-to-service communication', 'data synchronization', 'operational management', 'system integration'])}."

    else:
        # Generic API descriptions based on HTTP method
        if method == "GET" and "{id}" in path:
            resources = ["record", "entity", "resource", "item", "object"]
            return f"REST API endpoint that retrieves a specific {random.choice(resources)} in {response_format} format from the {path.split('/')[-2]} collection. Includes all properties and related resource references. Requires {auth_method} authentication. Used by {random.choice(['user interfaces', 'reporting systems', 'integration services', 'administrative tools'])}."
        elif method == "GET":
            return f"REST API endpoint that lists items from the {path.split('/')[-1]} collection in {response_format} format. Supports pagination, filtering, and sorting. Requires {auth_method} authentication. Used by {random.choice(['data retrieval services', 'reporting dashboards', 'search interfaces', 'administrative consoles'])}."
        elif method == "POST":
            return f"REST API endpoint that creates a new entry in the {path.split('/')[-1]} collection with {response_format} request and response format. Validates input data, persists the entity, and returns the created resource. Requires {auth_method} authentication. Used by {random.choice(['data entry forms', 'import tools', 'integration services', 'automated processes'])}."
        elif method == "PUT":
            return f"REST API endpoint that performs full updates to an entry in the {path.split('/')[-1]} collection using {response_format} format. Requires all fields to be provided, validates the data, and returns the updated resource. Requires {auth_method} authentication. Used by {random.choice(['edit interfaces', 'data management tools', 'synchronization services', 'administrative consoles'])}."
        elif method == "DELETE":
            return f"REST API endpoint that removes an entry from the {path.split('/')[-1]} collection. Returns a {response_format} status response. Performs validation before deletion and may archive rather than permanently delete. Requires {auth_method} authentication with elevated privileges. Used by {random.choice(['data cleanup processes', 'user-initiated deletions', 'archiving services', 'compliance tools'])}."
        elif method == "PATCH":
            return f"REST API endpoint that performs partial updates to an entry in the {path.split('/')[-1]} collection using {response_format} format. Accepts specific fields to update, validates the data, and returns the modified resource. Requires {auth_method} authentication. Used by {random.choice(['field-level updates', 'status changes', 'property modifications', 'incremental changes'])}."
        else:
            return f"REST API endpoint supporting {method} operations with {response_format} format for {path.split('/')[-1]} functionality within the {app_type.lower() if app_type else 'application'} ecosystem. Requires {auth_method} authentication."
