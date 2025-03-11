import random

from faker import Faker

from fsi_data_generator.fsi_generators.text_list import text_list

fake = Faker()

def get_random_port_with_popular_bias():
    """
    Generates a random plausible TCP port (0–65535) with higher probabilities
    for reserved ports (0–1023) and other popular non-reserved ports.
    Returns:
        int: A randomly selected plausible TCP port.
    """
    # Define popular reserved and non-reserved ports
    popular_reserved_ports = list(range(0, 1024))  # Reserved ports (0–1023)
    popular_non_reserved_ports = [
        3306, 5432, 8080, 8443, 6379, 27017  # Popular non-reserved ports
    ]
    all_other_ports = [port for port in range(1024, 65536) if port not in popular_non_reserved_ports]

    # Assign probabilities
    weights = {
        "reserved": 0.6,  # 60% chance for reserved ports (0–1023)
        "popular_non_reserved": 0.3,  # 30% for popular non-reserved ports
        "all_other": 0.1  # 10% for all other ports
    }

    # Decide the category based on weights
    choice = random.choices(
        population=["reserved", "popular_non_reserved", "all_other"],
        weights=[weights["reserved"], weights["popular_non_reserved"], weights["all_other"]],
        k=1
    )[0]

    # Generate a port based on the selected category
    if choice == "reserved":
        return random.choice(popular_reserved_ports)
    elif choice == "popular_non_reserved":
        return random.choice(popular_non_reserved_ports)
    else:
        return random.choice(all_other_ports)

def security(dg):
    return [
        ('security\\..*', '^.*port$', get_random_port_with_popular_bias()),
        ('security\\..*', '^tcp_flag', text_list([
            'SYN',
            'ACK',
            'FIN',
            'RST',
            'PSH',
            'URG',
            'ECE',
            'CWR'])),
    ]
