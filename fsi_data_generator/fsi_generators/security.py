from typing import cast

from faker import Faker

from fsi_data_generator.fsi_generators.helpers.generate_correlated_subnet import generate_correlated_subnet
from fsi_data_generator.fsi_generators.helpers.get_entity_combiner import get_entity_combiner
from fsi_data_generator.fsi_generators.helpers.get_random_port_with_popular_bias import get_random_port_with_popular_bias
from fsi_data_generator.fsi_generators.security__policies__name import security__policies__name
from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_generators.helpers.unique_list import unique_list
from fsi_data_generator.fsi_text.wildcards.____tcp_flag import ____tcp_flag
from fsi_data_generator.fsi_text.security.security__apps__name import security__apps__name
from fsi_data_generator.fsi_text.security.security__roles__name import security__roles__name

fake = Faker()

def security(dg):
    return [
        ('security\\.apps', '^name$', unique_list(security__apps__name)),
        ('security\\.roles', '^name$', unique_list(list(security__roles__name.keys()))),
        ('security\\.roles', '^display_name$',
         lambda a, b, c: security__roles__name[cast(str, a.get('name'))].get('display_name')),
        ('security\\.roles', '^description$',
         lambda a, b, c: security__roles__name[cast(str, a.get('name'))].get('responsibilities')),
        ('security\\.policies', '^name$', unique_list(list(security__policies__name.keys()))),
        ('security\\.identity_access_profiles', '^identity_id$',
         lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['security.identities']))),
        ('security\\.identity_roles', '^security_identity_id$', get_entity_combiner(dg, 'security.identities.security_identity_id', 'security.roles.security_role_id', '3')),
        ('security\\.identity_entitlements', '^security_identity_id$', get_entity_combiner(dg, 'security.identities.security_identity_id', 'security.entitlements.security_entitlement_id', '4')),
        ('security\\.identity_access_profiles', '^security_identity_id$', get_entity_combiner(dg, 'security.identities.security_identity_id', 'security.access_profiles.security_access_profile_id', '5')),
        ('security\\..*', '^subnet$', generate_correlated_subnet),
        ('security\\..*', '^.*port$', get_random_port_with_popular_bias),
        ('security\\..*', '^tcp_flag$', text_list(____tcp_flag)),
        ('security\\.open_ports', '^protocol', text_list([
            "TCP",
            "UDP",
            "ICMP",
            "HTTP2",
            "TLS",
            "QUIC",
            "SIP"]
        )),
        ('security\\.identities', '^environment$', text_list(["production", "development", "qa", "preproduction"])),
    ]
