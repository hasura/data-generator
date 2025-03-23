# Global dictionary to store combinations keyed by (field_a, field_b)
from typing import TYPE_CHECKING

from fsi_data_generator.fsi_generators.helpers.generate_combinations_random import \
    generate_combinations_random

if TYPE_CHECKING:
    from data_generator import SkipRowGenerationError

global_entity_combinations = {}


def generate_unique_composite_key(dg, foreign_fields, local_fields, custom_cache_key=None):
    """
    Generates a generic method to assign combinations of entities from two schema.table.key fields.
    Each unique pair of fields will maintain its own set of combinations in a global cache.

    :param custom_cache_key:
    :param dg: Data generator object with inserted primary keys, keyed as schema.table.
    :param foreign_fields: The fully qualified field for the first and last entity FK, formatted as schema.table.key
                    (e.g., 'app_mgmt.applications.application_id').
    :param local_fields: tuple of composite key names
    :return: A function that assigns and returns combined entity IDs.
    """
    global global_entity_combinations  # Global cache

    field_a, field_b = foreign_fields
    local_key_a, local_key_b = local_fields

    # Parse schema and key parts from the fields
    schema_table_a, key_a = field_a.rsplit('.', 1)  # e.g., 'app_mgmt.applications.application_id'
    schema_table_b, key_b = field_b.rsplit('.', 1)  # e.g., 'app_mgmt.licenses.license_id'

    # Cache key for this entity combination
    if custom_cache_key is None:
        cache_key = (foreign_fields, local_fields)
    else:
        # Use the custom cache key if provided
        cache_key = (foreign_fields, local_fields, custom_cache_key)

    def get_combination(data_item, _b, _c):
        """
        Combines entities from the two schema tables and assigns the results.
        :param _c: param unused
        :param _b: not used
        :param data_item: The dictionary to which the second entity ID (entity_b_id) will be assigned.
        :return: The first entity ID (entity_a_id) from the combination.
        """

        # Validate schema_table_a and schema_table_b exist and contain valid data
        if not isinstance(dg.inserted_pks.get(schema_table_a), list):
            raise ValueError(f"{schema_table_a} must be a list, but got {type(dg.inserted_pks.get(schema_table_a))}")
        if not isinstance(dg.inserted_pks.get(schema_table_b), list):
            raise ValueError(f"{schema_table_b} must be a list, but got {type(dg.inserted_pks.get(schema_table_b))}")

        if not all(isinstance(item, (str, int, float)) for item in dg.inserted_pks[schema_table_a]):
            raise ValueError(f"{schema_table_a} must contain only strings, integers, or floats")
        if not all(isinstance(item, (str, int, float)) for item in dg.inserted_pks[schema_table_b]):
            raise ValueError(f"{schema_table_b} must contain only strings, integers, or floats")

        # Check if cached combinations already exist
        if cache_key not in global_entity_combinations:
            # Generate combinations if not in cache
            global_entity_combinations[cache_key] = generate_combinations_random(
                dg.inserted_pks[schema_table_a],  # Use string/number array directly
                dg.inserted_pks[schema_table_b]  # Use string/number array directly
            )

        # Handle pop from cached combinations
        if not global_entity_combinations[cache_key]:
            raise SkipRowGenerationError(f"No combinations left for the fields: {field_a}, {field_b}")

        # Access or pop combinations from the cache
        entity_combination = global_entity_combinations[cache_key]
        entity_a_id, entity_b_id = entity_combination.pop()

        # Assign the second entity ID to its corresponding key from field_b
        if _c == local_key_a:
            data_item[local_key_b] = entity_b_id
            return entity_a_id
        else:
            data_item[local_key_a] = entity_a_id
            return entity_b_id

    return get_combination
