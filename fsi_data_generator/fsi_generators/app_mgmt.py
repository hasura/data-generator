from faker import Faker

from fsi_data_generator.fsi_generators.helpers.apply_schema_to_regex import \
    apply_schema_to_regex
from fsi_data_generator.fsi_generators.helpers.generate_composite_key import \
    generate_unique_composite_key
from fsi_data_generator.fsi_generators.helpers.random_record import \
    random_record
from fsi_data_generator.fsi_generators.intelligent_generators.app_mgmt import (
    generate_random_application, generate_random_application_component,
    generate_random_architecture, generate_random_component,
    generate_random_component_dependency, generate_random_sdlc_process,
    generate_random_team, get_license_data)
from fsi_data_generator.fsi_generators.intelligent_generators.app_mgmt.application_relationship import \
    generate_random_application_relationship
from fsi_data_generator.fsi_generators.intelligent_generators.app_mgmt.team_member import \
    generate_random_team_member

fake = Faker()


def app_mgmt(dg):
    return apply_schema_to_regex('app_mgmt', [
        ('team_members', random_record(dg, generate_random_team_member)),
        ('sdlc_processes', random_record(dg, generate_random_sdlc_process)),
        ('application_components', '.*_id', generate_unique_composite_key(dg, (
            'app_mgmt.applications.app_mgmt_application_id', 'app_mgmt.components.app_mgmt_component_id'), (
                                                                              'app_mgmt_application_id',
                                                                              'app_mgmt_component_id'),
                                                                          __name__ + "_application_components")),
        ('application_components', random_record(dg, generate_random_application_component)),
        ('teams', random_record(dg, generate_random_team)),
        ('application_relationships', random_record(dg, generate_random_application_relationship)),
        ('component_dependencies', '.*_id', generate_unique_composite_key(dg, (
            'app_mgmt.components.app_mgmt_component_id', 'app_mgmt.components.app_mgmt_component_id'),
                                                                          ('parent_component_id', 'child_component_id'),
                                                                          __name__ + '_component_dependencies')),
        ('component_dependencies', random_record(dg, generate_random_component_dependency)),
        ('applications', random_record(dg, generate_random_application)),
        ('components', random_record(dg, generate_random_component)),
        ('architectures', random_record(dg, generate_random_architecture)),
        ('team_members', '.*_id', generate_unique_composite_key(dg, (
            'app_mgmt.teams.app_mgmt_team_id', 'enterprise.associates.enterprise_associate_id'),
                                                                ('app_mgmt_team_id', 'enterprise_associate_id'),
                                                                __name__ + "_team_members")),
        ('application_licenses', '.*_id', generate_unique_composite_key(dg, (
            'app_mgmt.applications.app_mgmt_application_id', 'app_mgmt.licenses.app_mgmt_license_id'), (
                                                                            'app_mgmt_application_id',
                                                                            'app_mgmt_license_id'),
                                                                        __name__ + "_application_licenses")),
        ('licenses', 'license_type', get_license_data),
    ])
