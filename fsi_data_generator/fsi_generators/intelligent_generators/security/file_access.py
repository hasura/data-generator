from data_generator import DataGenerator
from datetime import datetime, timedelta
from faker import Faker
from typing import Any, Dict

import logging
import random

# Set up logger
logger = logging.getLogger(__name__)


def generate_random_file_access(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.file_accesses record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_file_access_id, security_file_id, security_process_execution_id, security_system_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random file access record
        (without ID fields)
    """
    fake = Faker()

    # Get the process execution info if available (this is our link to the user/associate)
    process_info = _fetch_process_execution_info(id_fields.get('security_process_execution_id'), dg)

    # Try to fetch the file information if possible
    file_info = _fetch_file_info(id_fields.get('security_file_id'), dg)

    # Get system information
    system_info = _fetch_system_info(id_fields.get('security_system_id'), dg)

    # Generate access timestamp (within the last 90 days)
    now = datetime.now()
    access_time = now - timedelta(
        days=random.randint(0, 90),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    # If we have process info with a start time, make sure access is after process start
    if process_info and 'start_time' in process_info and process_info['start_time']:
        process_start = process_info['start_time']
        if isinstance(process_start, datetime) and process_start > access_time:
            # Adjust access time to be after process start (within 10 minutes)
            access_time = process_start + timedelta(
                seconds=random.randint(1, 600)  # 1 second to 10 minutes after process start
            )

    # Define access types with weighted probabilities
    access_types = [
        ("VIEW", 70),  # Most common: viewing files
        ("DOWNLOAD", 15),  # Less common: downloading files
        ("EDIT", 10),  # Even less common: editing files
        ("PRINT", 3),  # Rare: printing files
        ("SHARE", 2)  # Rarest: sharing files
    ]

    # Choose access type based on weights
    access_type = random.choices(
        [access[0] for access in access_types],
        weights=[access[1] for access in access_types],
        k=1
    )[0]

    # Determine if access was successful (most are, but some fail)
    # Higher chance of failure for more privileged operations
    failure_chance = {
        "VIEW": 0.02,  # 2% chance of view failure
        "DOWNLOAD": 0.05,  # 5% chance of download failure
        "EDIT": 0.08,  # 8% chance of edit failure
        "PRINT": 0.10,  # 10% chance of print failure
        "SHARE": 0.15  # 15% chance of share failure
    }

    access_successful = random.random() > failure_chance.get(access_type, 0.05)

    # Generate appropriate status message
    if access_successful:
        status_message = "Success"
    else:
        # Different failure reasons based on access type
        failure_reasons = {
            "VIEW": ["Insufficient permissions", "File encrypted", "File locked"],
            "DOWNLOAD": ["Download quota exceeded", "Network error", "File size too large"],
            "EDIT": ["File locked by another user", "Read-only file", "Version conflict"],
            "PRINT": ["Printer not found", "Out of paper", "Printer queue full"],
            "SHARE": ["Recipient not found", "Sharing disabled by policy", "External sharing restricted"]
        }
        status_message = random.choice(failure_reasons.get(access_type, ["Access denied"]))

    # Generate IP address (internal or external)
    # 80% chance it's an internal IP
    if random.random() < 0.8:
        # Internal IP (10.x.x.x or 192.168.x.x)
        if random.random() < 0.5:
            ip_address = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        else:
            ip_address = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
    else:
        # External IP (public)
        ip_address = fake.ipv4_public()

    # Determine access location based on IP (internal/external)
    if ip_address.startswith(("10.", "192.168.")):
        location = random.choice(["Corporate HQ", "Branch Office", "Data Center", "VPN"])
    else:
        # External location
        location = fake.city() + ", " + fake.country_code()

    # Generate device info
    devices = [
        "Windows Workstation", "MacBook Pro", "Linux Server",
        "iPhone", "Android Phone", "iPad", "Surface Pro",
        "Thin Client", "Terminal Server", "Remote Desktop"
    ]
    device_info = random.choice(devices)

    # Add the OS version for more realism
    if "Windows" in device_info:
        device_info += " (Windows " + random.choice(["10", "11", "Server 2019", "Server 2022"]) + ")"
    elif "Mac" in device_info:
        device_info += " (macOS " + random.choice(["Monterey", "Ventura", "Sonoma"]) + ")"
    elif "Linux" in device_info:
        device_info += " (" + random.choice(["Ubuntu 22.04", "RHEL 8", "CentOS 7", "Debian 11"]) + ")"
    elif "iPhone" in device_info or "iPad" in device_info:
        device_info += " (iOS " + str(random.randint(14, 17)) + "." + str(random.randint(0, 5)) + ")"
    elif "Android" in device_info:
        device_info += " (Android " + str(random.randint(10, 14)) + ")"

    # Construct the file access record
    file_access = {
        "access_time": access_time,
        "access_type": access_type,
        "successful": access_successful,
        "status_message": status_message,
        "ip_address": ip_address,
        "location": location,
        "device_info": device_info,
        "session_id": fake.uuid4(),
        "user_agent": fake.user_agent() if random.random() < 0.9 else None
    }

    # If we have host/system info, add it
    if system_info:
        file_access["system_name"] = system_info.get('hostname')
        file_access["system_type"] = system_info.get('system_type')
        file_access["os"] = system_info.get('os')

    # If we have process info, add additional context from it
    if process_info:
        file_access["process_name"] = process_info.get('process_name', 'Unknown Process')
        file_access["process_user"] = process_info.get('user_name')
        file_access["command_line"] = process_info.get('command_line')

        # If process has associate info (via username), get the associate details
        if process_info.get('user_name'):
            associate_info = _fetch_associate_by_username(process_info.get('user_name'), dg)
            if associate_info:
                file_access["associate_reference"] = associate_info.get('enterprise_associate_id')
                file_access[
                    "associate_name"] = f"{associate_info.get('first_name', '')} {associate_info.get('last_name', '')}"
                file_access["associate_department"] = associate_info.get('department')

    # Add contextual data based on file type if available
    if file_info and 'file_path' in file_info:
        file_path = file_info.get('file_path', '')
        file_name = file_path.split('/')[-1] if '/' in file_path else (
            file_path.split('\\')[-1] if '\\' in file_path else file_path)
        file_access["file_name"] = file_name
        file_access["file_path"] = file_path
        file_access["file_hash"] = file_info.get('file_hash', '')

        # Guess the file type from extension
        file_type = ""
        if '.' in file_name:
            extension = file_name.split('.')[-1].lower()
            file_access["file_extension"] = extension

            if extension in ['pdf', 'doc', 'docx', 'txt', 'rtf']:
                file_type = "document"
            elif extension in ['xls', 'xlsx', 'csv']:
                file_type = "spreadsheet"
            elif extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                file_type = "image"
            elif extension in ['mp3', 'wav', 'flac', 'aac']:
                file_type = "audio"
            elif extension in ['mp4', 'avi', 'mov', 'wmv']:
                file_type = "video"
            elif extension in ['zip', 'rar', 'tar', 'gz']:
                file_type = "archive"
            elif extension in ['exe', 'msi', 'dll', 'bin']:
                file_type = "executable"
            elif extension in ['js', 'py', 'java', 'cpp', 'h', 'cs', 'php', 'html', 'css']:
                file_type = "code"

            # Financial document detection
            if any(term in file_name.lower() for term in
                   ['financial', 'report', 'statement', 'tax', 'invoice', 'receipt',
                    'balance', 'ledger', 'account', 'budget', 'forecast']):
                if file_type:
                    file_type = "financial_" + file_type
                else:
                    file_type = "financial_document"

            file_access["file_type"] = file_type

            # Add finance-specific context for financial documents
            if file_type and 'financial' in file_type:
                # For financial files, track additional finance-specific metadata
                financial_contexts = [
                    "Quarterly Review", "Annual Audit", "Tax Preparation",
                    "Budget Planning", "Financial Analysis", "Compliance Check",
                    "Audit Trail", "Regulatory Filing"
                ]
                file_access["access_context"] = random.choice(financial_contexts)

                # For sensitive financial files, add a reason code
                if not access_successful or random.random() < 0.3:
                    reason_codes = [
                        "FIN-REV-001", "FIN-AUD-002", "TAX-PREP-003",
                        "BUD-PLAN-004", "REG-COM-005", "FIN-ANA-006"
                    ]
                    file_access["reason_code"] = random.choice(reason_codes)

    return file_access


def _fetch_system_info(system_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch system information from the database

    Args:
        system_id: UUID of the system/host
        dg: DataGenerator instance

    Returns:
        Dictionary with system information, or empty dict if not found
    """
    if not system_id:
        return {}

    try:
        # Try to query the system information
        query = """
        SELECT hostname, system_type, os, os_version
        FROM security.hosts
        WHERE security_host_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (system_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        # Log the error
        logger.error(f"Error fetching system info for ID {system_id}: {str(e)}")

    return {}


def _fetch_process_execution_info(process_execution_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch process execution information from the database

    Args:
        process_execution_id: UUID of the process execution
        dg: DataGenerator instance

    Returns:
        Dictionary with process execution information, or empty dict if not found
    """
    if not process_execution_id:
        return {}

    try:
        # Try to query the process execution information
        query = """
        SELECT process_name, process_id, parent_process_id, start_time, end_time, command_line, user_name
        FROM security.process_executions
        WHERE security_process_execution_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (process_execution_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        # Log the error
        logger.error(f"Error fetching process execution info for ID {process_execution_id}: {str(e)}")

    return {}


def _fetch_associate_by_username(username: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch associate information based on username

    Args:
        username: Username from the process execution
        dg: DataGenerator instance

    Returns:
        Dictionary with associate information, or empty dict if not found
    """
    if not username:
        return {}

    try:
        # Query the associate information - assuming username is stored in email field
        query = """
        SELECT enterprise_associate_id, first_name, last_name, email, job_title
        FROM enterprise.associates
        WHERE email = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (username,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        # Log the error
        logger.error(f"Error fetching associate info for username {username}: {str(e)}")

    return {}


def _fetch_file_info(file_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch file information from the database

    Args:
        file_id: UUID of the file
        dg: DataGenerator instance

    Returns:
        Dictionary with file information, or empty dict if not found
    """
    if not file_id:
        return {}

    try:
        # Try to query the file information from security.files table
        query = """
        SELECT file_path, file_hash, file_size, last_modified
        FROM security.files
        WHERE security_file_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (file_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        # Log the error
        logger.error(f"Error fetching file info from security.files for ID {file_id}: {str(e)}")

        # Try an alternative query if the first one fails
        try:
            # Let's try checking document.files as a fallback
            query = """
            SELECT file_name, file_path, content_type, created_by, created_at, sensitivity_level
            FROM document.files
            WHERE file_id = %s
            """

            with dg.conn.cursor() as cursor:
                cursor.execute(query, (file_id,))
                result = cursor.fetchone()

            return result

        except Exception as e:
            # Log the error from the second attempt
            logger.error(f"Error fetching file info from document.files for ID {file_id}: {str(e)}")

    return {}
