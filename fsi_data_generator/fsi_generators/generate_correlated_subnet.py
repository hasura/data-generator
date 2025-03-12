import random


def generate_correlated_subnet(a,_b,_c):
    ipv4_address = a.get('ip_address')
    # Split the IP into its octets
    octets = list(map(int, ipv4_address.split(".")))

    # Determine the IP class based on the first octet
    first_octet = octets[0]
    if 0 <= first_octet <= 127:
        # Class A
        min_cidr, max_cidr = 8, 15  # Allow more specific subnets within Class A
    elif 128 <= first_octet <= 191:
        # Class B
        min_cidr, max_cidr = 16, 23  # Subnets within Class B
    elif 192 <= first_octet <= 223:
        # Class C
        min_cidr, max_cidr = 24, 30  # Subnets within Class C
    else:
        # Class D or E (Uncommon, return None or default to Class C for fake generation)
        return "/24", "255.255.255.0"

    # Randomly select a CIDR within the range for the IP class
    cidr_prefix = random.randint(min_cidr, max_cidr)

    # Compute the subnet mask in binary form
    binary_mask = ("1" * cidr_prefix).ljust(32, "0")

    # Convert the binary form into dotted decimal
    dotted_decimal = ".".join(str(int(binary_mask[i:i + 8], 2)) for i in range(0, 32, 8))

    return f"/{cidr_prefix}", dotted_decimal
