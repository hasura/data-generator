import random
from typing import cast

from faker import Faker

from fsi_data_generator.fsi_generators.generate_correlated_subnet import generate_correlated_subnet
from fsi_data_generator.fsi_generators.get_random_port_with_popular_bias import get_random_port_with_popular_bias
from fsi_data_generator.fsi_generators.security__policies__name import security__policies__name
from fsi_data_generator.fsi_generators.text_list import text_list
from fsi_data_generator.fsi_generators.unique_list import unique_list
from fsi_data_generator.fsi_text.____tcp_flag import ____tcp_flag
from fsi_data_generator.fsi_text.security__apps__name import security__apps__name
from fsi_data_generator.fsi_text.security__roles__name import security__roles__name
from itertools import product
fake = Faker()



def generate_combinations_random(list1, list2):
    """
    Generate all possible combinations of tuples from two lists of strings,
    ensure uniqueness, and shuffle them into random order.

    :param list1: First list of strings.
    :param list2: Second list of strings.
    :return: Randomized list of unique tuples representing all combinations.
    """
    # Generate all combinations and use a set to remove duplicates
    combinations = set(product(list1, list2))

    # Convert to a list for shuffling
    combinations_list = list(combinations)

    # Shuffle the list
    random.shuffle(combinations_list)

    return combinations_list

identity_role = []
identity_entitlement = []
identity_access_profile = []

def get_identity_role(dg):
    def get_it(a,b,c):
        global identity_role
        if not identity_role:
            identity_role = generate_combinations_random(dg.inserted_pks['security.identities'], dg.inserted_pks['security.roles'])
        identity_id, role_id = identity_role.pop()
        a['security_role_id'] = role_id
        return identity_id
    return get_it

def get_identity_access_profile(dg):
    def get_it(a,b,c):
        global identity_access_profile
        if not identity_access_profile:
            identity_access_profile = generate_combinations_random(dg.inserted_pks['security.identities'], dg.inserted_pks['security.access_profiles'])
        identity_id, access_profile_id = identity_access_profile.pop()
        a['security_access_profile_id'] = access_profile_id
        return identity_id
    return get_it

def get_identity_entitlement(dg):
    def get_it(a,b,c):
        global identity_entitlement
        if not identity_entitlement:
            identity_entitlement = generate_combinations_random(dg.inserted_pks['security.identities'], dg.inserted_pks['security.entitlements'])
        identity_id, entitlement_id = identity_entitlement.pop()
        a['security_entitlement_id'] = entitlement_id
        return identity_id
    return get_it

def security(dg):
    return [
        ('security\\.apps', '^name$', unique_list(security__apps__name)),
        ('security\\.roles','^name$', unique_list(list(security__roles__name.keys()))),
        ('security\\.roles','^display_name$', lambda a, b, c: security__roles__name[cast(str,a.get('name'))].get('display_name')),
        ('security\\.roles', '^description$', lambda a, b, c: security__roles__name[cast(str,a.get('name'))].get('responsibilities')),
        ('security\\.policies', '^name$', unique_list(list(security__policies__name.keys()))),
        ('security\\.identity_access_profiles', '^identity_id$', lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['security.identities']))),
        ('security\\.identity_roles', '^security_identity_id$', get_identity_role(dg)),
        ('security\\.identity_roles', '^security_role_id$', lambda a,b,c: a['security_role_id']),
        ('security\\.identity_entitlements', '^security_identity_id$', get_identity_entitlement(dg)),
        ('security\\.identity_entitlements', '^security_entitlement_id$', lambda a,b,c: a['security_entitlement_id']),
        ('security\\.identity_access_profiles', '^security_identity_id$', get_identity_access_profile(dg)),
        ('security\\.identity_access_profiles', '^security_access_profile_id$', lambda a,b,c: a['security_access_profile_id']),
        ('security\\..*', '^subnet$', generate_correlated_subnet),
        ('security\\..*', '^.*port$', get_random_port_with_popular_bias),
        ('security\\..*', '^tcp_flag$', text_list(____tcp_flag)),
        ('security\\.identities', '^environment$', text_list(["production", "development", "qa", "preproduction"])),
    ]
