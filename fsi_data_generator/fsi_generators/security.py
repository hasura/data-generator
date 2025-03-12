from faker import Faker

from fsi_data_generator.fsi_generators.generate_correlated_subnet import generate_correlated_subnet
from fsi_data_generator.fsi_generators.get_random_port_with_popular_bias import get_random_port_with_popular_bias
from fsi_data_generator.fsi_generators.text_list import text_list

fake = Faker()


def security(dg):
    return [
        ('security\\.identity_roles', '^identity_id$',
         lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['security\\.identities']))),
        ('security\\.identity_roles', '^role_id',
         lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['security\\.roles']))),
        ('security\\..*', '^subnet$', generate_correlated_subnet),
        ('security\\..*', '^.*port$', get_random_port_with_popular_bias),
        ('security\\..*', '^tcp_flag', text_list([
            'SYN',
            'ACK',
            'FIN',
            'RST',
            'PSH',
            'URG',
            'ECE',
            'CWR'])),
    ]
