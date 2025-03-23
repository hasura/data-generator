import ipaddress
import random
from typing import Any, Dict

from data_generator import DataGenerator


def generate_random_device(id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.devices record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields
                   (security_device_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated device data
        (without ID fields)
    """
    # Device types
    device_types = [
        "router",
        "server",
        "workstation",
        "firewall",
        "switch",
        "load_balancer",
        "vpn_gateway",
        "network_attached_storage",
        "wireless_access_point",
        "printer"
    ]

    # Subnet configurations
    subnet_prefixes = [
        "10.0.",  # Private network
        "192.168.",  # Private network
        "172.16.",  # Private network
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23."
    ]

    # Hostname generation helpers
    hostname_prefixes = [
        "prod", "dev", "test", "stage",
        "web", "app", "db", "cache",
        "mail", "vpn", "internal"
    ]

    hostname_suffixes = [
        "01", "02", "03", "04", "05",
        "001", "002",
        "core", "edge", "backend",
        "primary", "secondary"
    ]

    # Generate IP address
    # Use the security_device_id (which should be an IP address) if provided
    if 'security_device_id' in id_fields and id_fields['security_device_id']:
        ip_address = id_fields['security_device_id']
    else:
        # Generate a random private IP address
        subnet = random.choice(subnet_prefixes)
        ip_octets = [int(x) for x in subnet.rstrip('.').split('.')]
        ip_octets.extend([random.randint(1, 254), random.randint(1, 254)])
        ip_address = '.'.join(map(str, ip_octets))

    # Validate IP address
    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        raise ValueError(f"Invalid IP address generated: {ip_address}")

    # Generate subnet
    subnet = f"{'.'.join(ip_address.split('.')[:2])}.0.0/16"

    # Generate hostname
    hostname_components = [
        random.choice(hostname_prefixes),
        random.choice(hostname_suffixes)
    ]
    hostname = '-'.join(hostname_components)

    # Device record
    device = {
        "device_type": random.choice(device_types),
        "subnet": subnet,
        "hostname": hostname
    }

    return device
