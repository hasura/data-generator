from faker import Faker

from .helpers import (apply_schema_to_regex, generate_unique_composite_key,
                      random_record)
from .intelligent_generators.security import (
    generate_random_account, generate_random_device,
    generate_random_enhanced_entitlement, generate_random_entitlement_resource,
    generate_random_file, generate_random_file_access,
    generate_random_file_threat, generate_random_governance_group,
    generate_random_host, generate_random_iam_login, generate_random_identity,
    generate_random_identity_profile, generate_random_identity_role,
    generate_random_installed_application, generate_random_network_connection,
    generate_random_network_event, generate_random_open_port,
    generate_random_policy, generate_random_policy_attribute,
    generate_random_policy_rule, generate_random_process_execution,
    generate_random_resource_definition, generate_random_role_entitlement,
    generate_random_running_service, generate_random_security_role,
    generate_random_system_stat, generate_random_usb_device_usage)

fake = Faker()


def security(dg):
    return apply_schema_to_regex('security', [
        ('policies', random_record(dg, generate_random_policy)),
        ('usb_device_usage', random_record(dg, generate_random_usb_device_usage)),
        ('role_entitlements', random_record(dg, generate_random_role_entitlement)),
        ('identity_roles', random_record(dg, generate_random_identity_role)),
        ('system_stats', random_record(dg, generate_random_system_stat)),
        ('running_services', random_record(dg, generate_random_running_service)),
        ('hosts', random_record(dg, generate_random_host)),
        ('process_executions', random_record(dg, generate_random_process_execution)),
        ('open_ports', random_record(dg, generate_random_open_port)),
        ('network_connections', random_record(dg, generate_random_network_connection)),
        ('installed_applications', '.*_id',
         generate_unique_composite_key(
             dg,
             ('security.hosts.security_host_id', 'app_mgmt.applications.app_mgmt_application_id'),
             ('security_host_id', 'app_mgmt_application_id'),
             __name__ + '_security_identity_role')),
        ('installed_applications', random_record(dg, generate_random_installed_application)),
        ('files', random_record(dg, generate_random_file)),
        ('file_threats', random_record(dg, generate_random_file_threat)),
        ('file_accesses', random_record(dg, generate_random_file_access)),
        ('governance_groups', random_record(dg, generate_random_governance_group)),
        ('identity_profiles', random_record(dg, generate_random_identity_profile)),
        ('identities', random_record(dg, generate_random_identity)),
        ('iam_logins', random_record(dg, generate_random_iam_login)),
        ('accounts', random_record(dg, generate_random_account)),
        ('policy_rules', random_record(dg, generate_random_policy_rule)),
        ('policy_attributes', random_record(dg, generate_random_policy_attribute)),
        ('network_events', random_record(dg, generate_random_network_event)),
        ('devices', random_record(dg, generate_random_device)),
        ('enhanced_entitlements', random_record(dg, generate_random_enhanced_entitlement)),
        ('identity_roles', 'security_identity_id', generate_unique_composite_key(dg, (
            'security.identities.security_identity_id', 'security.roles.security_role_id'), ('security_identity_id',
                                                                                             'security_role_id'),
                                                                                 __name__ + '_security_identity_role')),
        ('role_entitlements', 'security_role_id', generate_unique_composite_key(dg, (
            'security.roles.security_role_id', 'security.enhanced_entitlements.security_entitlement_id'), (
                                                                                    'security_role_id',
                                                                                    'security_entitlement_id'),
                                                                                __name__ + '_security_role_entitlement')),
        ('entitlement_resources', random_record(dg, generate_random_entitlement_resource)),
        ('resource_definitions', random_record(dg, generate_random_resource_definition)),
        ('roles', random_record(dg, generate_random_security_role)),
    ])
