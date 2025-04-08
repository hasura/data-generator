from .helpers.apply_schema_to_regex import apply_schema_to_regex
from .helpers.random_record import random_record
from .intelligent_generators.enterprise import (
    generate_random_account, generate_random_enterprise_identifier,
    generate_random_address, generate_random_associate,
    generate_random_building, generate_random_department,
    generate_random_party, generate_random_party_entity_address,
    generate_random_party_relationship, generate_random_permission)
from faker import Faker

fake = Faker()


def enterprise(dg):
    return apply_schema_to_regex('enterprise', [
        ('identifiers', random_record(dg, generate_random_enterprise_identifier)),
        ('permissions', random_record(dg, generate_random_permission)),
        ('party_relationships', random_record(dg, generate_random_party_relationship)),
        ('party_entity_addresses', random_record(dg, generate_random_party_entity_address)),
        ('addresses', random_record(dg, generate_random_address)),
        ('departments', random_record(dg, generate_random_department)),
        ('buildings', random_record(dg, generate_random_building)),
        ('parties', random_record(dg, generate_random_party)),
        ('accounts', random_record(dg, generate_random_account)),
        ('associates', random_record(dg, generate_random_associate)),
    ])
