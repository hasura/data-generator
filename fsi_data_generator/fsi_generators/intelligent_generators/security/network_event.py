from data_generator import DataGenerator
from faker import Faker
from typing import Any, Dict

import datetime
import random

fake = Faker()


def generate_random_network_event(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.network_events record.

    Args:
        _id_fields: Dictionary containing predetermined ID fields (these will be ignored in the output)
        _dg: DataGenerator instance

    Returns:
        Dict containing a random network event record
    """

    protocols = ["TCP", "UDP", "ICMP", "HTTP2", "TLS", "QUIC", "SIP"]
    statuses = ["success", "failure", "blocked", "timeout", "reset"]

    # Get TCP flag from the enum
    tcp_flags = ["SYN", "ACK", "FIN", "RST", "PSH", "URG", "ECE", "CWR"]

    # Get current time
    now = datetime.datetime.now()
    timestamp = now - datetime.timedelta(minutes=random.randint(0, 1440))  # Random time in the last 24 hours

    # Generate random IPs
    source_ip = fake.ipv4()
    dest_ip = fake.ipv4()

    # Generate ports
    source_port = random.randint(1024, 65535)
    dest_port = random.choice([80, 443, 22, 21, 25, 53, 3306, 5432] + [random.randint(1024, 65535)])

    # Determine protocol and TCP-specific fields
    protocol = random.choice(protocols)
    tcp_flag = None
    sequence = None
    ack = None
    window_size = None

    if protocol == "TCP":
        tcp_flag = random.choice(tcp_flags)
        sequence = random.randint(0, 2 ** 32 - 1)
        ack = random.randint(0, 2 ** 32 - 1)
        window_size = random.choice([8192, 16384, 32768, 65535])

    # Generate random data sizes
    length = random.randint(64, 8192)
    bytes_sent = random.randint(0, length)
    bytes_received = length - bytes_sent

    # Create log message
    action = "allowed" if random.random() > 0.3 else "blocked"
    log_message = f"{protocol} connection from {source_ip}:{source_port} to {dest_ip}:{dest_port} was {action}"
    created_at = timestamp + datetime.timedelta(seconds=random.uniform(0.1, 5.0))

    # Construct the network event record (without ID fields)
    network_event = {
        "timestamp": timestamp.isoformat(),
        "source_ip": source_ip,
        "source_port": source_port,
        "dest_ip": dest_ip,
        "dest_port": dest_port,
        "protocol": protocol,
        "status": random.choice(statuses),
        "tcp_flag": tcp_flag,
        "sequence": sequence,
        "ack": ack,
        "window_size": window_size,
        "length": length,
        "bytes_sent": bytes_sent,
        "bytes_received": bytes_received,
        "log_message": log_message,
        "created_at": created_at.isoformat()
    }

    return network_event
