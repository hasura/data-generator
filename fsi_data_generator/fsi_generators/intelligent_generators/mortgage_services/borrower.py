import logging
import random
from typing import Any, Dict

from data_generator import DataGenerator

# Set up logging
logger = logging.getLogger(__name__)


def generate_random_borrower(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random mortgage services borrower record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_party_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated borrower data (without ID fields)
    """

    # Generate years in school (between 12 and 20)
    years_in_school = random.randint(12, 20)

    # Generate dependent count (0 to 5, weighted)
    dependent_weights = [0.4, 0.3, 0.2, 0.07, 0.02, 0.01]  # Weights for 0, 1, 2, 3, 4, 5 dependents
    dependent_count = random.choices(range(6), weights=dependent_weights, k=1)[0]

    # Create the borrower record
    borrower = {
        "years_in_school": years_in_school,
        "dependent_count": dependent_count
    }

    return borrower
