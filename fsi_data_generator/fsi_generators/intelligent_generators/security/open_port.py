import random
from typing import Any, Dict

from faker import Faker

from data_generator import DataGenerator, SkipRowGenerationError

fake = Faker()

prev_ports = set()


def generate_random_open_port(id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.open_ports record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_host_id)
        _dg: DataGenerator instance

    Returns:
        Dict containing a random open port record
        (without ID fields)
    """
    # The composite key includes security_host_id, port_number, and protocol
    # security_host_id is provided in id_fields, we need to generate the other two

    # Common ports and their typical protocols
    common_port_mappings = {
        # Web servers
        80: ["TCP"],
        443: ["TCP"],
        8080: ["TCP"],
        8443: ["TCP"],

        # Email
        25: ["TCP"],
        587: ["TCP"],
        110: ["TCP"],
        143: ["TCP"],
        993: ["TCP"],
        995: ["TCP"],

        # File transfer
        20: ["TCP"],
        21: ["TCP"],
        22: ["TCP"],

        # Domain services
        53: ["UDP", "TCP"],

        # Database
        1433: ["TCP"],  # MSSQL
        3306: ["TCP"],  # MySQL
        5432: ["TCP"],  # PostgreSQL
        27017: ["TCP"],  # MongoDB

        # Remote access
        3389: ["TCP"],  # RDP
        5900: ["TCP"],  # VNC

        # DHCP
        67: ["UDP"],
        68: ["UDP"],

        # Other common services
        123: ["UDP"],  # NTP
        161: ["UDP"],  # SNMP
        162: ["UDP"],  # SNMP Trap
        389: ["TCP"],  # LDAP
        636: ["TCP"],  # LDAPS
        5060: ["UDP", "TCP"],  # SIP
        5061: ["TCP"],  # SIP over TLS
    }

    # Use the network_protocols enum from the DBML schema
    valid_protocols = ["TCP", "UDP", "ICMP", "HTTP2", "TLS", "QUIC", "SIP"]

    # Decide whether to use a common port or a random high port
    is_common_port = random.random() < 0.7  # 70% chance of being a common port

    if is_common_port:
        # Choose a random common port
        port_number = random.choice(list(common_port_mappings.keys()))

        # Get valid protocols for this port
        possible_protocols = common_port_mappings[port_number]

        # Ensure the protocol is in our valid_protocols list
        valid_possible_protocols = [p for p in possible_protocols if p in valid_protocols]

        # If none are valid, default to a common protocol
        if not valid_possible_protocols:
            protocol = random.choice(["TCP", "UDP"])
        else:
            protocol = random.choice(valid_possible_protocols)
    else:
        # Generate a random high port
        port_number = random.randint(10000, 65535)

        # For high ports, more likely to be TCP
        protocol = random.choices(
            ["TCP", "UDP", "HTTP2", "TLS", "QUIC"],
            weights=[0.6, 0.2, 0.1, 0.07, 0.03],
            k=1
        )[0]

    # Construct the open port record (without ID fields)
    # Note: security_host_id is part of the id_fields and not included here
    open_port = {
        "port_number": port_number,
        "protocol": protocol
    }

    key = (id_fields['security_host_id'], port_number, protocol)
    global prev_ports
    if key in prev_ports:
        raise SkipRowGenerationError

    prev_ports.add(key)

    return open_port
