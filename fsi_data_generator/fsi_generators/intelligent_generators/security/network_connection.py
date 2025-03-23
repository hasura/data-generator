import random
from datetime import datetime, timedelta
from typing import Any, Dict

from faker import Faker

from data_generator import DataGenerator

fake = Faker()


def generate_random_network_connection(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.network_connections record.

    Args:
        _id_fields: Dictionary containing predetermined ID fields
                  (security_network_connection_id, security_host_id, security_process_execution_id)
        _dg: DataGenerator instance

    Returns:
        Dict containing a random network connection record
        (without ID fields)
    """
    # Get current time
    now = datetime.now()

    # Define connection types (transport layer socket types)
    connection_types = ["TCP", "UDP", "RAW", "UNIX", "ICMP"]
    connection_type = random.choice(connection_types)

    # Use network_protocols enum values exactly as defined in DBML
    network_protocols = ["TCP", "UDP", "ICMP", "HTTP2", "TLS", "QUIC", "SIP"]

    # Protocol selection based on connection type for more realistic combinations
    if connection_type == "TCP":
        # Protocols that typically run over TCP
        protocol_options = ["TCP", "HTTP2", "TLS"]
    elif connection_type == "UDP":
        # Protocols that typically run over UDP
        protocol_options = ["UDP", "QUIC", "SIP"]
    elif connection_type == "ICMP":
        protocol_options = ["ICMP"]
    else:
        # For other connection types
        protocol_options = ["TCP", "UDP"]

    # Filter options to ensure we only use protocols defined in the enum
    valid_protocol_options = [p for p in protocol_options if p in network_protocols]
    protocol = random.choice(valid_protocol_options)

    # Generate IP addresses
    local_ip = fake.ipv4()
    remote_ip = fake.ipv4()

    # Generate ports based on protocol
    common_ports = {
        "HTTP2": [80, 443, 8080, 8443],
        "TLS": [443, 465, 636, 989, 990, 993, 995, 5061],
        "QUIC": [443, 80, 8443],
        "SIP": [5060, 5061],
        "TCP": [20, 21, 22, 23, 25, 53, 110, 143, 3306, 5432],
        "UDP": [53, 67, 68, 69, 123, 161, 162, 514]
    }

    # Default to random high ports if protocol not in common_ports
    default_ports = [random.randint(1024, 65535)]

    # Select remote port based on protocol
    if protocol in common_ports:
        remote_port = random.choice(common_ports[protocol] + [random.randint(1024, 65535)])
    else:
        remote_port = random.choice(default_ports)

    # For client connections, use ephemeral local ports
    if random.random() < 0.8:  # 80% chance this is a client connection
        local_port = random.randint(10000, 65535)
    else:
        # This might be a server accepting connections
        if protocol in common_ports:
            local_port = random.choice(common_ports[protocol])
        else:
            local_port = random.choice(default_ports)

    # Generate start time (between 1 and 30 days ago)
    start_time = now - timedelta(days=random.randint(1, 30),
                                 minutes=random.randint(0, 1440),
                                 seconds=random.randint(0, 3600))

    # Generate end time (some connections might still be open)
    is_open = random.random() < 0.1  # 10% chance connection is still open

    if is_open:
        end_time = None
    else:
        # Connection duration depends on protocol and typical usage patterns
        if protocol in ["HTTP2", "QUIC"]:
            # Web requests tend to be shorter
            duration_seconds = random.randint(1, 300)  # 1 second to 5 minutes
        elif protocol in ["TLS", "TCP"]:
            # Database or SSH connections can be longer
            duration_seconds = random.randint(60, 7200)  # 1 minute to 2 hours
        else:
            # Default duration
            duration_seconds = random.randint(1, 3600)  # 1 second to 1 hour

        end_time = start_time + timedelta(seconds=duration_seconds)

    # Construct the network connection record (without ID fields)
    network_connection = {
        "connection_type": connection_type,
        "protocol": protocol,
        "local_ip": local_ip,
        "local_port": local_port,
        "remote_ip": remote_ip,
        "remote_port": remote_port,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat() if end_time else None
    }

    return network_connection
