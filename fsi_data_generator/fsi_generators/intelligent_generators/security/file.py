import hashlib
import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict

from faker import Faker

from data_generator import DataGenerator, SkipRowGenerationError

# Set up logger
logger = logging.getLogger(__name__)


def generate_random_file(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.files record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_file_id, security_host_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random file record
    """
    fake = Faker()

    # Get the required IDs from id_fields
    host_id = id_fields.get('security_host_id')

    if not host_id:
        logger.error("Host ID is required to generate a file record")
        raise SkipRowGenerationError("Host ID is required")

    # Fetch host information to determine OS and file paths
    host_info = _fetch_host_info(host_id, dg)

    # Determine the OS and set appropriate file path patterns
    if not host_info:
        # Default to Windows if host info not available
        os_type = "Windows"
    else:
        os_type = host_info.get('os', 'Windows')
        if not os_type or 'windows' in os_type.lower():
            os_type = "Windows"
        elif 'linux' in os_type.lower() or 'ubuntu' in os_type.lower() or 'debian' in os_type.lower() or 'centos' in os_type.lower():
            os_type = "Linux"
        elif 'mac' in os_type.lower() or 'darwin' in os_type.lower():
            os_type = "MacOS"
        else:
            os_type = "Windows"  # Default to Windows for unknown OS

    # Generate appropriate file path based on OS
    file_path = _generate_file_path(os_type, fake)

    # Generate file size (weighted towards smaller files)
    file_size_weights = [
        (1024, 30),  # 1KB
        (10 * 1024, 25),  # 10KB
        (100 * 1024, 20),  # 100KB
        (1024 * 1024, 15),  # 1MB
        (10 * 1024 * 1024, 8),  # 10MB
        (100 * 1024 * 1024, 2)  # 100MB
    ]

    file_size = random.choices(
        [size[0] for size in file_size_weights],
        weights=[size[1] for size in file_size_weights],
        k=1
    )[0]

    # Add some randomness to the file size
    file_size = int(file_size * random.uniform(0.8, 1.2))

    # Generate a random file hash (SHA-256)
    file_hash = _generate_file_hash()

    # Generate a realistic last modified date (within the last year)
    last_modified = datetime.now() - timedelta(
        days=random.randint(0, 365),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    # Construct the file record
    file_record = {
        "security_host_id": host_id,
        "file_path": file_path,
        "file_hash": file_hash,
        "file_size": file_size,
        "last_modified": last_modified
    }

    return file_record


def _fetch_host_info(host_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch host information from the database

    Args:
        host_id: UUID of the host
        dg: DataGenerator instance

    Returns:
        Dictionary with host information, or empty dict if not found
    """
    if not host_id:
        return {}

    try:
        # Try to query the host information
        query = """
        SELECT hostname, system_type, os, os_version
        FROM security.hosts
        WHERE security_host_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (host_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        # Log the error
        logger.error(f"Error fetching host info for ID {host_id}: {str(e)}")

    return {}


def _generate_file_path(os_type: str, fake: Faker) -> str:
    """
    Generate a realistic file path based on OS type

    Args:
        os_type: Operating system type (Windows, Linux, MacOS)
        fake: Faker instance

    Returns:
        String containing a realistic file path
    """
    # Define common file extensions by category
    document_extensions = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt', 'md']
    spreadsheet_extensions = ['xls', 'xlsx', 'csv', 'ods']
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']
    audio_extensions = ['mp3', 'wav', 'flac', 'aac', 'm4a']
    video_extensions = ['mp4', 'avi', 'mov', 'wmv', 'mkv']
    code_extensions = ['py', 'java', 'js', 'cpp', 'h', 'c', 'cs', 'php', 'html', 'css', 'sql']
    archive_extensions = ['zip', 'rar', 'tar', 'gz', '7z']
    executable_extensions = ['exe', 'msi', 'dll', 'bin', 'sh', 'bat', 'cmd']
    financial_extensions = ['xlsx', 'csv', 'pdf', 'docx']

    # Weight the categories to make documents and spreadsheets more common in a financial context
    categories = [
        (document_extensions, 30),
        (spreadsheet_extensions, 25),
        (image_extensions, 10),
        (audio_extensions, 5),
        (video_extensions, 5),
        (code_extensions, 10),
        (archive_extensions, 8),
        (executable_extensions, 7),
        (financial_extensions, 0)  # Weight is 0 as we'll handle financial files separately
    ]

    # Choose a category based on weights
    chosen_category = random.choices(
        [cat[0] for cat in categories],
        weights=[cat[1] for cat in categories],
        k=1
    )[0]

    # 20% chance to generate a financial document
    if random.random() < 0.2:
        chosen_category = financial_extensions

    # Choose a random extension from the category
    extension = random.choice(chosen_category)

    # Generate a filename
    filename_patterns = [
        lambda: fake.word() + "_" + fake.word(),
        lambda: fake.word() + str(random.randint(1, 9999)),
        lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 10))),
        lambda: fake.company().replace(' ', '_').replace(',', '').replace('.', ''),
        lambda: fake.bs().replace(' ', '_')
    ]

    # For financial documents, use financial naming patterns
    if chosen_category == financial_extensions:
        fin_year = random.randint(datetime.now().year - 3, datetime.now().year)
        fin_month = random.randint(1, 12)
        fin_quarter = (fin_month - 1) // 3 + 1

        financial_filename_patterns = [
            lambda: f"Financial_Report_{fin_year}",
            lambda: f"Q{fin_quarter}_{fin_year}_Financials",
            lambda: f"Budget_{fin_year}",
            lambda: f"Invoice_{random.randint(10000, 99999)}",
            lambda: f"Tax_Return_{fin_year}",
            lambda: f"Balance_Sheet_{fin_year}_{fin_month:02d}",
            lambda: f"Profit_Loss_{fin_year}_Q{fin_quarter}",
            lambda: f"Expense_Report_{fake.last_name()}_{fin_year}_{fin_month:02d}",
            lambda: f"Payroll_{fin_year}_{fin_month:02d}",
            lambda: f"Audit_{fin_year}",
            lambda: f"Bank_Statement_{fin_year}_{fin_month:02d}"
        ]
        filename_patterns = financial_filename_patterns

    # Generate base filename
    base_filename = random.choice(filename_patterns)()
    filename = f"{base_filename}.{extension}"

    # Define path patterns based on OS
    if os_type == "Windows":
        system_dirs = [
            "C:\\Windows\\System32\\",
            "C:\\Windows\\",
            "C:\\Program Files\\",
            "C:\\Program Files (x86)\\",
        ]

        user_dirs = [
            "C:\\Users\\{username}\\Documents\\",
            "C:\\Users\\{username}\\Desktop\\",
            "C:\\Users\\{username}\\Downloads\\",
            "C:\\Users\\{username}\\Pictures\\",
            "C:\\Users\\{username}\\AppData\\Local\\",
            "C:\\Users\\{username}\\AppData\\Roaming\\"
        ]

        # Financial paths for Windows
        if chosen_category == financial_extensions:
            financial_dirs = [
                "C:\\Users\\{username}\\Documents\\Finance\\",
                "C:\\Users\\{username}\\Documents\\Accounting\\",
                "C:\\Users\\{username}\\Documents\\Tax\\",
                "C:\\Users\\{username}\\Documents\\Budgets\\",
                "C:\\Users\\{username}\\Documents\\Reports\\Financial\\",
                "C:\\Users\\{username}\\OneDrive\\Finance\\",
                "C:\\Finance\\",
                "C:\\Accounting\\",
                "C:\\Shared\\Finance\\"
            ]
            user_dirs.extend(financial_dirs)

        # 70% chance of user directory, 30% chance of system directory
        if random.random() < 0.7:
            path_template = random.choice(user_dirs)
            username = fake.user_name()
            path = path_template.format(username=username)

            # Maybe add 1-2 subdirectories
            depth = random.randint(0, 2)
            for _ in range(depth):
                path += fake.word() + "\\"
        else:
            path = random.choice(system_dirs)

            # Maybe add 1-2 subdirectories
            depth = random.randint(0, 2)
            for _ in range(depth):
                path += fake.word() + "\\"

    elif os_type == "Linux":
        system_dirs = [
            "/bin/",
            "/etc/",
            "/usr/bin/",
            "/usr/local/bin/",
            "/var/log/",
            "/opt/"
        ]

        user_dirs = [
            "/home/{username}/Documents/",
            "/home/{username}/Desktop/",
            "/home/{username}/Downloads/",
            "/home/{username}/Pictures/",
            "/home/{username}/.config/",
            "/home/{username}/.local/share/"
        ]

        # Financial paths for Linux
        if chosen_category == financial_extensions:
            financial_dirs = [
                "/home/{username}/Documents/Finance/",
                "/home/{username}/Documents/Accounting/",
                "/home/{username}/Documents/Tax/",
                "/home/{username}/Documents/Budgets/",
                "/home/{username}/Documents/Reports/Financial/",
                "/opt/finance/",
                "/var/finance/",
                "/shared/finance/"
            ]
            user_dirs.extend(financial_dirs)

        # 70% chance of user directory, 30% chance of system directory
        if random.random() < 0.7:
            path_template = random.choice(user_dirs)
            username = fake.user_name()
            path = path_template.format(username=username)

            # Maybe add 1-2 subdirectories
            depth = random.randint(0, 2)
            for _ in range(depth):
                path += fake.word() + "/"
        else:
            path = random.choice(system_dirs)

            # Maybe add 1-2 subdirectories
            depth = random.randint(0, 2)
            for _ in range(depth):
                path += fake.word() + "/"

    else:  # MacOS
        system_dirs = [
            "/Applications/",
            "/Library/",
            "/System/Library/",
            "/usr/bin/",
            "/usr/local/bin/"
        ]

        user_dirs = [
            "/Users/{username}/Documents/",
            "/Users/{username}/Desktop/",
            "/Users/{username}/Downloads/",
            "/Users/{username}/Pictures/",
            "/Users/{username}/Library/Application Support/",
            "/Users/{username}/Library/Preferences/"
        ]

        # Financial paths for MacOS
        if chosen_category == financial_extensions:
            financial_dirs = [
                "/Users/{username}/Documents/Finance/",
                "/Users/{username}/Documents/Accounting/",
                "/Users/{username}/Documents/Tax/",
                "/Users/{username}/Documents/Budgets/",
                "/Users/{username}/Documents/Reports/Financial/",
                "/Users/{username}/OneDrive/Finance/",
                "/Volumes/Shared/Finance/"
            ]
            user_dirs.extend(financial_dirs)

        # 70% chance of user directory, 30% chance of system directory
        if random.random() < 0.7:
            path_template = random.choice(user_dirs)
            username = fake.user_name()
            path = path_template.format(username=username)

            # Maybe add 1-2 subdirectories
            depth = random.randint(0, 2)
            for _ in range(depth):
                path += fake.word() + "/"
        else:
            path = random.choice(system_dirs)

            # Maybe add 1-2 subdirectories
            depth = random.randint(0, 2)
            for _ in range(depth):
                path += fake.word() + "/"

    # Combine path and filename
    return path + filename


def _generate_file_hash() -> str:
    """
    Generate a random SHA-256 hash string.

    Returns:
        String containing a valid SHA-256 hash
    """
    random_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=64))
    hash_object = hashlib.sha256(random_data.encode())
    return hash_object.hexdigest()
