import uuid
from datetime import datetime, timedelta
from typing import Any, Dict

import anthropic
from faker import Faker

from data_generator import DataGenerator, SkipRowGenerationError
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from fsi_data_generator.fsi_generators.intelligent_generators.security.agent_status import \
    AgentStatus
from fsi_data_generator.fsi_generators.intelligent_generators.security.compliance_status import \
    ComplianceStatus
from fsi_data_generator.fsi_generators.intelligent_generators.security.patch_status import \
    PatchStatus
from fsi_data_generator.fsi_generators.intelligent_generators.security.system_status import \
    SystemType

# Track previously generated hostnames for uniqueness
prev_hostnames = set()

import random


def generate_random_host(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "security.hosts" record.

    Args:
        _id_fields: Dictionary containing predetermined ID fields
                  (security_host_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random host record
        (without ID fields)
    """
    fake = Faker()

    # Try to get hostname patterns from DBML if available
    hostname_patterns = []
    try:
        hostname_patterns = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='security.hosts.hostname',
            count=20,
            cache_key='host_hostnames'
        )
    except anthropic.APIStatusError:
        # Fallback hostname patterns if not found in DBML
        hostname_patterns = [
            "srv-{dept}-{num:03d}",
            "ws-{dept}-{num:03d}",
            "{dept}{num:03d}-{loc}",
            "{dept}-{role}-{num:02d}",
            "srv-{loc}-{num:02d}",
            "vm-{project}-{env}{num:02d}",
            "app-{app}-{env}-{num:02d}",
            "db-{db_type}-{env}-{num:02d}"
        ]

    # Generate hostname
    for _ in range(10):  # Try up to 10 times to generate a unique hostname
        if not hostname_patterns:
            hostname = fake.hostname()
        else:
            hostname_pattern = random.choice(hostname_patterns)

            # Fill in the template variables
            hostname = hostname_pattern.format(
                dept=random.choice(['fin', 'hr', 'it', 'dev', 'ops', 'sec', 'sales', 'mkt']),
                num=random.randint(1, 999),
                loc=random.choice(['nyc', 'sfo', 'lon', 'tok', 'sgp', 'syd']),
                role=random.choice(['web', 'app', 'db', 'file', 'mail', 'proxy', 'auth']),
                project=random.choice(['core', 'billing', 'crm', 'api', 'ui', 'data']),
                env=random.choice(['dev', 'test', 'qa', 'prod']),
                app=random.choice(['web', 'api', 'auth', 'payment', 'billing']),
                db_type=random.choice(['sql', 'pg', 'mongo', 'oracle', 'mysql'])
            )

        # Check if hostname is unique
        global prev_hostnames
        if hostname not in prev_hostnames:
            prev_hostnames.add(hostname)
            break
    else:
        # If we couldn't generate a unique hostname after 10 tries, skip this row
        raise SkipRowGenerationError("Could not generate a unique hostname")

    # Generate agent identifier (UUIDv4 format)
    agent_identifier = str(uuid.uuid4())

    # Generate IP addresses
    ip_address_internal = fake.ipv4_private()

    # 70% chance of having an external IP
    has_external_ip = random.random() < 0.7
    ip_address_external = fake.ipv4_public() if has_external_ip else None

    # Generate MAC address
    mac_address = ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])

    # Determine system type using the enum
    system_type = SystemType.get_random()

    # Select OS based on system type
    os_types = {
        SystemType.SERVER: ["Windows Server 2019", "Windows Server 2022", "Ubuntu Server 20.04",
                            "Red Hat Enterprise Linux 8", "CentOS 7"],
        SystemType.WORKSTATION: ["Windows 10", "Windows 11", "Ubuntu Desktop 22.04", "macOS Monterey"],
        SystemType.LAPTOP: ["Windows 10", "Windows 11", "macOS Ventura", "macOS Monterey", "Ubuntu Desktop 22.04"],
        SystemType.VIRTUAL_MACHINE: ["Windows Server 2019", "Ubuntu Server 20.04", "CentOS 7", "Debian 11"],
        SystemType.CONTAINER: ["Alpine Linux", "Ubuntu 20.04", "Debian 11"],
        SystemType.APPLIANCE: ["Cisco IOS", "Palo Alto PAN-OS", "FortiOS", "Custom Linux"]
    }

    os = random.choice(os_types.get(system_type, ["Windows 10", "Ubuntu 20.04"]))

    # Generate OS version based on OS
    os_version_map = {
        "Windows 10": ["21H2", "22H1", "22H2"],
        "Windows 11": ["21H2", "22H2"],
        "Windows Server 2019": ["1809", "1903", "1909", "2004"],
        "Windows Server 2022": ["21H2"],
        "Ubuntu Server 20.04": ["20.04.4 LTS", "20.04.5 LTS"],
        "Ubuntu Desktop 22.04": ["22.04.1 LTS", "22.04.2 LTS"],
        "Red Hat Enterprise Linux 8": ["8.4", "8.5", "8.6"],
        "CentOS 7": ["7.9.2009"],
        "Debian 11": ["11.5", "11.6"],
        "macOS Monterey": ["12.5", "12.6"],
        "macOS Ventura": ["13.0", "13.1"],
        "Alpine Linux": ["3.16", "3.17"],
        "Cisco IOS": ["15.2(7)", "16.9(3)"],
        "Palo Alto PAN-OS": ["10.1.6", "10.2.0"],
        "FortiOS": ["6.4.8", "7.0.5"],
        "Custom Linux": ["4.19", "5.15"]
    }

    os_version = random.choice(os_version_map.get(os, ["Unknown"]))

    # Generate timestamps
    now = datetime.now()

    # Last seen: Between now and 30 days ago, weighted toward recent
    days_ago = random.choices(
        range(31),  # 0 to 30 days ago
        weights=[30 - i for i in range(31)],  # Weight decreases as days ago increases
        k=1
    )[0]

    last_seen = now - timedelta(days=days_ago,
                                hours=random.randint(0, 23),
                                minutes=random.randint(0, 59))

    # Generate agent version
    agent_versions = ["1.2.3", "1.3.0", "1.3.1", "1.4.0", "2.0.1"]
    agent_version = random.choice(agent_versions)

    # Determine agent status using the enum
    agent_status = AgentStatus.get_random()

    # Days since last patched: between 0 and 180 days
    days_since_patched = random.choices(
        range(181),  # 0 to 180 days
        weights=[180 - i for i in range(181)],  # Weight decreases as days increases
        k=1
    )[0]

    last_patched = now - timedelta(days=days_since_patched)

    # Determine patch status using the enum
    patch_status = PatchStatus.from_days(days_since_patched)

    # Determine compliance using the enum
    compliance = ComplianceStatus.calculate(patch_status, agent_status)

    # Checkout info for laptops and some workstations
    checked_out_date = None
    asset_owner_name = None
    asset_owner_email = None

    if system_type in [SystemType.LAPTOP, SystemType.WORKSTATION] and random.random() < 0.8:
        # Checkout date between 1 and 365 days ago
        checkout_days_ago = random.randint(1, 365)
        checked_out_date = (now - timedelta(days=checkout_days_ago)).date()

        # Generate owner info
        first_name = fake.first_name()
        last_name = fake.last_name()
        asset_owner_name = f"{first_name} {last_name}"
        asset_owner_email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"

    # Determine if patch update is available
    patch_update_available = None
    if patch_status in [PatchStatus.OUTDATED, PatchStatus.CRITICAL]:
        patch_update_available = True
    elif patch_status == PatchStatus.CURRENT:
        patch_update_available = False
    elif patch_status == PatchStatus.UP_TO_DATE:
        patch_update_available = random.random() < 0.3  # 30% chance of update available

    # Generate patch level
    if "Windows" in os:
        patch_level = f"KB{random.randint(4000000, 5999999)}"
    elif "Ubuntu" in os or "Debian" in os or "Linux" in os:
        patch_level = f"{'.'.join(str(random.randint(0, 20)) for _ in range(3))}-{random.randint(1, 50)}"
    else:
        patch_level = f"{random.randint(10, 20)}.{random.randint(1, 9)}.{random.randint(1, 20)}"

    # Construct the host record
    host = {
        "hostname": hostname,
        "agent_identifier": agent_identifier,  # Changed from agent_id to agent_identifier
        "ip_address_internal": ip_address_internal,
        "ip_address_external": ip_address_external,
        "mac_address": mac_address,
        "system_type": system_type.value,  # Convert enum to string value
        "os": os,
        "os_version": os_version,
        "last_seen": last_seen.isoformat(),
        "agent_version": agent_version,
        "agent_status": agent_status.value,  # Convert enum to string value
        "patch_status": patch_status.value,  # Convert enum to string value
        "last_patched": last_patched.isoformat(),
        "compliance": compliance.value,  # Convert enum to string value
        "checked_out_date": checked_out_date.isoformat() if checked_out_date else None,
        "asset_owner_name": asset_owner_name,
        "asset_owner_email": asset_owner_email,
        "patch_level": patch_level,
        "patch_update_available": patch_update_available
    }

    return host
