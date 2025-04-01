from data_generator import DataGenerator
from datetime import datetime, timedelta
from typing import Any, Dict

import logging
import psycopg2
import random
import sys

logger = logging.getLogger(__name__)


def generate_random_usb_device_usage(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.usb_device_usage record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_usb_device_usage_id, security_system_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random USB device usage record
        (without ID fields)
    """
    # Get the system_id from id_fields (security_system_id will be used)
    system_id = id_fields.get('security_system_id')

    if not system_id:
        raise ValueError("security_system_id is required")

    # Get host information if possible to determine reasonable device types
    host_info = get_host_info(system_id, dg)

    # Generate device name and type based on host information
    device_name, device_type = generate_device_info(host_info)

    # Generate connection time (within last 90 days)
    now = datetime.now()
    connection_time = now - timedelta(days=random.randint(1, 90),
                                      hours=random.randint(0, 23),
                                      minutes=random.randint(0, 59))

    # Determine if the device has been disconnected
    is_disconnected = random.random() < 0.9  # 90% chance device has been disconnected

    # Generate disconnection time if device was disconnected
    disconnection_time = None
    if is_disconnected:
        # USB connections typically last between a few minutes and a few hours
        duration_minutes = random.choices(
            [
                random.randint(1, 10),  # Quick usage (1-10 minutes)
                random.randint(11, 60),  # Medium usage (11-60 minutes)
                random.randint(61, 480),  # Extended usage (1-8 hours)
                random.randint(481, 10080)  # Long-term connection (8 hours - 1 week)
            ],
            weights=[20, 40, 30, 10],  # Weighted toward medium usage
            k=1
        )[0]

        disconnection_time = connection_time + timedelta(minutes=duration_minutes)

        # Ensure disconnection time is not in the future
        if disconnection_time > now:
            disconnection_time = now

    # Construct the USB device usage record
    usb_device_usage = {
        "device_name": device_name,
        "device_type": device_type,
        "connection_time": connection_time.isoformat(),
        "disconnection_time": disconnection_time.isoformat() if disconnection_time else None
    }

    return usb_device_usage


def get_host_info(system_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Get host information using the system_id
    """
    try:
        query = """
        SELECT hostname, system_type, os
        FROM security.hosts
        WHERE security_host_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (system_id,))
            result = cursor.fetchone()

        return result

    except psycopg2.ProgrammingError as e:
        # Log the critical error
        logger.critical(f"Programming error detected in the SQL query: {e}")

        # Exit the program immediately with a non-zero status code
        sys.exit(1)

    except Exception as e:
        logger.error(f"Error fetching host info: {e}")

    # Return default values if query fails
    return {'system_type': 'WORKSTATION', 'os': 'Windows'}


def generate_device_info(host_info: Dict[str, Any]) -> tuple:
    """
    Generate appropriate USB device name and type based on host information
    """
    system_type = host_info.get('system_type', 'WORKSTATION').upper()

    # Common USB device types
    device_types = [
        "Storage",
        "Keyboard",
        "Mouse",
        "Camera",
        "Audio",
        "Printer",
        "Network",
        "Hub",
        "Card Reader",
        "Smart Card",
        "Biometric",
        "Mobile Device"
    ]

    # Brands and manufacturers
    brands = [
        "SanDisk", "Kingston", "Seagate", "Western Digital", "Lexar",
        "Logitech", "Microsoft", "Dell", "HP", "Corsair", "Sony",
        "Samsung", "Toshiba", "Anker", "PNY", "ADATA", "LaCie",
        "Verbatim", "Razer", "Belkin", "Canon", "Epson", "Transcend"
    ]

    # Adjust probabilities based on system type
    if system_type == 'SERVER':
        # Servers typically have fewer USB connections, mostly storage
        device_type = random.choices(
            device_types,
            weights=[50, 5, 5, 1, 1, 1, 20, 10, 5, 1, 1, 0],
            k=1
        )[0]
    elif system_type == 'LAPTOP' or system_type == 'WORKSTATION':
        # Laptops and workstations have a wider variety of USB connections
        device_type = random.choices(
            device_types,
            weights=[30, 15, 15, 10, 10, 5, 5, 5, 2, 1, 1, 1],
            k=1
        )[0]
    else:
        # Default for other system types
        device_type = random.choice(device_types)

    # Generate device name based on type
    brand = random.choice(brands)

    if device_type == "Storage":
        capacity = random.choice(["8GB", "16GB", "32GB", "64GB", "128GB", "256GB", "1TB", "2TB"])
        model = random.choice(["Ultra", "DataTraveler", "Cruzer", "Elements", "Extreme", "EVO", "Pro", "Elite"])
        device_name = f"{brand} {model} {capacity} USB Drive"

    elif device_type == "Keyboard":
        model = random.choice(["Wireless", "Mechanical", "Gaming", "Ergonomic", "Bluetooth", "Slim", "Compact", "Pro"])
        device_name = f"{brand} {model} Keyboard"

    elif device_type == "Mouse":
        model = random.choice(
            ["Wireless", "Gaming", "Bluetooth", "Ergonomic", "Precision", "Optical", "Trackball", "Laser"])
        device_name = f"{brand} {model} Mouse"

    elif device_type == "Camera":
        model = random.choice(
            ["Webcam", "HD Camera", "Conference Cam", "Streaming Camera", "Pro Camera", "Document Camera"])
        resolution = random.choice(["720p", "1080p", "4K", "8MP", "12MP"])
        device_name = f"{brand} {model} {resolution}"

    elif device_type == "Audio":
        model = random.choice(["Headset", "Microphone", "Speaker", "Headphones", "Sound Card", "Audio Interface"])
        device_name = f"{brand} {model} Audio Device"

    elif device_type == "Printer":
        model = random.choice(["LaserJet", "InkJet", "OfficeJet", "WorkForce", "EcoTank", "DeskJet"])
        series = f"{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}"
        device_name = f"{brand} {model} {series}"

    elif device_type == "Network":
        model = random.choice(["Ethernet Adapter", "WiFi Adapter", "Bluetooth Adapter", "LAN Card", "Network Dongle"])
        device_name = f"{brand} {model}"

    elif device_type == "Hub":
        ports = random.choice(["4-Port", "7-Port", "10-Port"])
        model = random.choice(["USB Hub", "USB-C Hub", "Powered Hub", "Data Hub", "Charging Hub"])
        device_name = f"{brand} {ports} {model}"

    elif device_type == "Card Reader":
        model = random.choice(["Multi-Card Reader", "SD Card Reader", "Memory Card Reader", "Smart Card Reader"])
        device_name = f"{brand} {model}"

    elif device_type == "Smart Card":
        model = random.choice(["Security Key", "Authentication Token", "Identity Card", "Access Card"])
        device_name = f"{brand} {model}"

    elif device_type == "Biometric":
        model = random.choice(["Fingerprint Reader", "Facial Recognition", "Iris Scanner", "Biometric Authenticator"])
        device_name = f"{brand} {model}"

    elif device_type == "Mobile Device":
        model = random.choice(["Smartphone", "Tablet", "iPhone", "Galaxy", "iPad", "Android Device"])
        device_name = f"{brand} {model}"

    else:
        # Generic device name
        device_name = f"{brand} USB Device"

    return device_name, device_type
