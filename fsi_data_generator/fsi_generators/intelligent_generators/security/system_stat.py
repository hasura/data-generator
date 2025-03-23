import logging
import random
import sys
from datetime import datetime, timedelta
from typing import Any, Dict

import psycopg2
from faker import Faker

from data_generator import DataGenerator

fake = Faker()
logger = logging.getLogger(__name__)


def generate_random_system_stat(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.system_stats record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_system_stat_id, security_host_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random system stats record
        (without ID fields)
    """
    # We need security_host_id to generate system stats
    security_host_id = id_fields.get('security_host_id')
    if not security_host_id:
        raise ValueError("security_host_id is required")

    # Get host information to generate appropriate stats
    host_info = get_host_info(security_host_id, dg)

    # Generate timestamp
    # System stats are typically recent (within the last 24 hours)
    now = datetime.now()
    timestamp = now - timedelta(minutes=random.randint(0, 1440))  # Up to 24 hours ago

    # Determine if system is server or workstation based on host info
    is_server = False
    if host_info and 'system_type' in host_info:
        is_server = host_info['system_type'].upper() in ['SERVER', 'VIRTUAL_MACHINE']

    # Generate CPU usage percentage
    # Servers typically have higher average CPU usage than workstations
    if is_server:
        # Servers have more consistent, higher utilization
        cpu_usage_percent = random.choices(
            [random.randint(5, 30), random.randint(30, 70), random.randint(70, 95)],
            weights=[0.3, 0.5, 0.2],
            k=1
        )[0]
    else:
        # Workstations/laptops have more variance, often idle or spiking
        cpu_usage_percent = random.choices(
            [random.randint(1, 10), random.randint(10, 40), random.randint(40, 100)],
            weights=[0.5, 0.3, 0.2],
            k=1
        )[0]

    # Generate memory stats
    # Servers typically have more memory than workstations/laptops
    if is_server:
        memory_total_gb = random.choice([16, 32, 64, 128, 256, 512])
    else:
        memory_total_gb = random.choice([4, 8, 16, 32, 64])

    # Generate memory usage
    # More variability in usage percentage
    memory_usage_percentage = random.uniform(0.1, 0.9)
    memory_usage_gb = round(memory_total_gb * memory_usage_percentage, 1)

    # Generate disk stats
    # Servers typically have more disk space than workstations/laptops
    if is_server:
        disk_total_gb = random.choice([500, 1000, 2000, 4000, 8000])
    else:
        disk_total_gb = random.choice([128, 256, 512, 1000, 2000])

    # Generate disk usage - typically more full than memory
    disk_usage_percentage = random.uniform(0.3, 0.9)
    disk_free_gb = int(disk_total_gb * (1 - disk_usage_percentage))

    # Adjust stats based on host status if available
    if host_info and 'agent_status' in host_info:
        agent_status = host_info['agent_status']

        # If agent is inactive, stats might be stale or irregular
        if agent_status.upper() != 'ACTIVE':
            # Generate older timestamp
            timestamp = now - timedelta(days=random.randint(1, 30))

            # Stats might be more extreme (very high or very low)
            if random.random() < 0.5:
                cpu_usage_percent = random.randint(90, 100)
                memory_usage_gb = round(memory_total_gb * random.uniform(0.9, 0.99), 1)
                disk_free_gb = int(disk_total_gb * random.uniform(0.01, 0.1))
            else:
                cpu_usage_percent = random.randint(0, 5)
                memory_usage_gb = round(memory_total_gb * random.uniform(0.01, 0.1), 1)

    # Construct the system stats record
    system_stat = {
        "security_host_id": security_host_id,  # Include this reference for clarity
        "cpu_usage_percent": cpu_usage_percent,
        "memory_usage_gb": memory_usage_gb,
        "memory_total_gb": memory_total_gb,
        "disk_free_gb": disk_free_gb,
        "disk_total_gb": disk_total_gb,
        "timestamp": timestamp.isoformat()
    }

    return system_stat


def get_host_info(host_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Get host information using the PK
    """
    try:
        query = """
        SELECT hostname, system_type, agent_status
        FROM security.hosts
        WHERE security_host_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (host_id,))
            result = cursor.fetchone()

        if result:
            return {
                'hostname': result[0],
                'system_type': result[1],
                'agent_status': result[2]
            }
    except psycopg2.ProgrammingError as e:
        # Log the critical error
        logger.critical(f"Programming error detected in the SQL query: {e}")

        # Exit the program immediately with a non-zero status code
        sys.exit(1)

    # If no result or error, return empty dict
    return {}
