from faker import Faker

from .helpers import random_record
from .helpers.apply_schema_to_regex import apply_schema_to_regex
from .intelligent_generators.data_quality import generate_random_validation_run, generate_random_validation_error, \
    generate_random_api_lineage, generate_random_record_lineage, generate_random_field_lineage

fake = Faker()


def data_quality(dg):
    return apply_schema_to_regex('data_quality', [
        ('validation_run', random_record(dg, generate_random_validation_run)),
        ('validation_error', random_record(dg, generate_random_validation_error)),
        ('api_lineage', random_record(dg, generate_random_api_lineage)),
        ('record_lineage', random_record(dg, generate_random_record_lineage)),
        ('field_lineage', random_record(dg, generate_random_field_lineage))
    ])
