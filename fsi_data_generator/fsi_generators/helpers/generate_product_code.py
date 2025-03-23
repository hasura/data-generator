import random
import string
from typing import cast


def generate_product_code(length=20):
    """Generates a random product code containing uppercase letters and digits.

    Args:
      length: The desired length of the product code. Default is 20.

    Returns:
      A string representing the generated product code.
    """
    characters = string.ascii_uppercase + string.digits
    return cast(str, ''.join(random.choice(characters) for _ in range(length)))


def generate_product_codes(num_product_codes=10000):
    product_codes = set()
    for _ in range(num_product_codes):
        product_codes.add(generate_product_code())
    return list(product_codes)


fake_product_codes = generate_product_codes()
