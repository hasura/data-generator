import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict

from data_generator import DataGenerator, SkipRowGenerationError

# Set up logger
logger = logging.getLogger(__name__)


def generate_random_installed_application(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.installed_applications record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_host_id, app_mgmt_application_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random installed application record
    """

    # Get the required IDs from id_fields
    host_id = id_fields.get('security_host_id')
    application_id = id_fields.get('app_mgmt_application_id')

    if not host_id or not application_id:
        logger.error("Both host_id and application_id are required to generate an installed application record")
        raise SkipRowGenerationError("Missing required IDs")

    # Fetch application information from app_mgmt
    application_info = _fetch_application_info(application_id, dg)

    # Generate realistic version number, possibly using the version from app_mgmt
    base_version = application_info.get('version')
    version = _generate_version_number(
        application_info.get('application_name', ''),
        base_version
    )

    # Generate installation date (within the last 2 years, but not after the app's deployment date)
    now = datetime.now()
    max_days_ago = 365 * 2  # 2 years

    # If we have the application's deployment date, use that as the earliest possible install date
    app_deploy_date = application_info.get('date_deployed')
    if app_deploy_date and isinstance(app_deploy_date, datetime):
        days_since_deploy = (now - app_deploy_date).days
        if days_since_deploy < max_days_ago:
            max_days_ago = days_since_deploy

    # Make sure we don't try to install after retirement
    app_retire_date = application_info.get('date_retired')
    install_cutoff_date = app_retire_date if app_retire_date and isinstance(app_retire_date, datetime) else now

    # Generate a random installation date
    installation_date = install_cutoff_date - timedelta(
        days=random.randint(0, max_days_ago),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    # Construct the installed application record
    installed_app = {
        "security_host_id": host_id,
        "app_mgmt_application_id": application_id,
        "application_version": version,
        "installation_date": installation_date
    }

    return installed_app


def _fetch_application_info(application_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch application information from the app_mgmt.applications table

    Args:
        application_id: UUID of the application
        dg: DataGenerator instance

    Returns:
        Dictionary with application information, or empty dict if not found
    """
    if not application_id:
        return {}

    try:
        # Try to query the application information from app_mgmt
        query = """
        SELECT application_name, description, application_type, vendor, version, 
               deployment_environment, lifecycle_status, date_deployed, date_retired
        FROM app_mgmt.applications
        WHERE app_mgmt_application_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (application_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        # Log the error
        logger.error(f"Error fetching application info for ID {application_id}: {str(e)}")

    return {}


def _generate_version_number(application_name: str, base_version: str = None) -> str:
    """
    Generate a realistic version number for the given application

    Args:
        application_name: Name of the application
        base_version: Base version from app_mgmt.applications to use as a starting point

    Returns:
        String containing a realistic version number
    """
    # If we have a base version, use that or a slight variation
    if base_version and random.random() < 0.7:  # 70% chance to use base version
        # Sometimes use exact base version
        if random.random() < 0.5:
            return base_version

        # Otherwise, generate a patch or minor update to base version
        try:
            # Parse semantic versioning (major.minor.patch)
            parts = base_version.split('.')
            if len(parts) >= 3:
                # Increment patch version
                patch = int(parts[2]) + random.randint(0, 3)
                return f"{parts[0]}.{parts[1]}.{patch}"
            elif len(parts) == 2:
                # Increment minor version or add patch
                if random.random() < 0.5:
                    minor = int(parts[1]) + random.randint(0, 2)
                    return f"{parts[0]}.{minor}"
                else:
                    return f"{parts[0]}.{parts[1]}.{random.randint(1, 10)}"
            else:
                # Just use as is
                return base_version
        except (ValueError, IndexError):
            # If parsing fails, just use the base version
            return base_version

    # Common version patterns
    patterns = [
        # Semantic versioning (major.minor.patch)
        lambda: f"{random.randint(1, 20)}.{random.randint(0, 50)}.{random.randint(0, 99)}",

        # Two-part versioning (major.minor)
        lambda: f"{random.randint(1, 20)}.{random.randint(0, 99)}",

        # Year-based versioning
        lambda: f"{random.randint(2015, 2025)}",

        # Year.release versioning
        lambda: f"{random.randint(2015, 2025)}.{random.randint(1, 4)}",

        # Version with build number
        lambda: f"{random.randint(1, 15)}.{random.randint(0, 30)}.{random.randint(0, 99)}.{random.randint(1000, 9999)}"
    ]

    # Some applications have specific versioning patterns
    specific_patterns = {
        "Windows": lambda: f"{random.choice(['7', '8.1', '10', '11', '10 Enterprise', '10 Pro'])}",
        "Office": lambda: f"{random.choice(['2016', '2019', '2021', '365'])}",
        "Ubuntu": lambda: f"{random.choice(['18.04', '20.04', '22.04', '23.10'])}" + random.choice(['', ' LTS']),
        "Chrome": lambda: f"{random.randint(70, 120)}.0.{random.randint(1000, 9999)}.{random.randint(10, 200)}",
        "Firefox": lambda: f"{random.randint(60, 120)}.{random.randint(0, 9)}",
        "Java": lambda: f"{random.randint(8, 17)}.0.{random.randint(1, 352)}",
        "Python": lambda: f"{random.choice(['2.7', '3.6', '3.7', '3.8', '3.9', '3.10', '3.11', '3.12'])}",
        "Excel": lambda: f"{random.choice(['2016', '2019', '2021', '365'])}",
        "Word": lambda: f"{random.choice(['2016', '2019', '2021', '365'])}",
        "Adobe": lambda: f"{random.randint(11, 25)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "SQL Server": lambda: f"{random.choice(['2016', '2017', '2019', '2022'])}",
        "Oracle": lambda: f"{random.choice(['11g', '12c', '18c', '19c', '21c'])}",
        "PostgreSQL": lambda: f"{random.randint(9, 15)}.{random.randint(0, 7)}",
        "MySQL": lambda: f"{random.randint(5, 8)}.{random.randint(0, 9)}.{random.randint(10, 35)}",
        "Nginx": lambda: f"{random.randint(1, 1)}.{random.randint(18, 24)}.{random.randint(0, 3)}",
        "Apache": lambda: f"{random.randint(2, 2)}.{random.randint(2, 4)}.{random.randint(30, 50)}"
    }

    # Check if we have a specific pattern for this application
    for app_name, pattern in specific_patterns.items():
        if app_name.lower() in application_name.lower():
            return pattern()

    # Use a random general pattern
    return random.choice(patterns)()
