from faker import Faker

from fsi_data_generator.fsi_generators.helpers.apply_schema_to_regex import \
    apply_schema_to_regex
from fsi_data_generator.fsi_generators.helpers.random_record import \
    random_record
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.account import \
    generate_random_account
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.account_identifier import \
    generate_random_account_identifier
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.address import \
    generate_random_address
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.associate import \
    generate_random_associate
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.building import \
    generate_random_building
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.department import \
    generate_random_department
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.party import \
    generate_random_party
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.party_entity_address import \
    generate_random_party_entity_address
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.party_relationship import \
    generate_random_party_relationship
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.permission import \
    generate_random_permission

fake = Faker()


def enterprise(dg):
    return apply_schema_to_regex('enterprise', [
        ('account_identifiers', random_record(dg, generate_random_account_identifier)),
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
