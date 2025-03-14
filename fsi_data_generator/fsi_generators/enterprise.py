from faker import Faker

from fsi_data_generator.fsi_generators.helpers.generate_random_date_between import generate_random_date_between
from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_generators.helpers.unique_list import unique_list
from fsi_data_generator.fsi_generators.wildcards import three_word_tuple, fake_leis
from fsi_data_generator.fsi_text.wildcards.____legal_structure import ____legal_structure
from fsi_data_generator.fsi_text.enterprise.enterprise__accounts__description import enterprise__accounts__description
from fsi_data_generator.fsi_text.enterprise.enterprise__accounts__description_dict import enterprise__accounts__description_dict
from fsi_data_generator.fsi_text.enterprise.enterprise__associates__job_title import enterprise__associates__job_title
from fsi_data_generator.fsi_text.enterprise.enterprise__associates__officer_title import enterprise__associates__officer_title
from fsi_data_generator.fsi_text.enterprise.enterprise__departments__department_name import \
    enterprise__departments__department_name

fake = Faker()


def release_date(a,_b,_c):
    status = a.get("status")
    hire_date = a.get("hire_date")
    if status in ["terminated", "retired"]:
        return generate_random_date_between(hire_date)
    return None

def party_name(a,_b,_c):
    party_type = a.get('party_type')
    if party_type == 'individual':
        return fake.name()
    return fake.company()

def full_business_legal_name(a,_b,_c):
    party_type = a.get('party_type')
    party_name = a.get('name')
    if party_type == 'organization':
        return party_name
    return ''

def lei(a,b,c):
    party_type = a.get('party_type')
    if party_type == 'organization':
        value = text_list(fake_leis)(a,b,c)
        return value
    return ''

def account_description(a,b,c):
    account_category = a.get('account_category')
    value = text_list(enterprise__accounts__description)(a,b,c)
    if account_category:
        alt_value = enterprise__accounts__description_dict[account_category]
        if alt_value:
            value = text_list(alt_value)(a,b,c)
            return value
    return value


def legal_structure(a,b,c):
    party_type = a.get('party_type')
    if party_type == 'organization':
        value = text_list(____legal_structure)(a,b,c)
        return value
    return ''

def enterprise(_dg):

    return [
        ('enterprise\\.lei', '^name$',lei),
        ('enterprise\\.parties', '^name$',party_name),
        ('enterprise\\.parties', '^legal_structure$', legal_structure),
        ('enterprise\\.parties', '^full_business_legal_name$',full_business_legal_name),
        ('enterprise\\.accounts', '^description$', account_description),
        ('enterprise\\.accounts', '^status$', text_list(["active", "closed"])),
        ('enterprise\\.accounts', '^account_category$', text_list(["personal", "business", "retirement"])),
        ('enterprise\\.associates', '^status$', text_list(["active", "terminated", "retired", "on-leave"])),
        ('enterprise\\.associates', '^job_title$', text_list(enterprise__associates__job_title)),
        ('enterprise\\.associates', '^officer_title$', text_list(enterprise__associates__officer_title)),
        ('enterprise\\.associates', '^status$', text_list(['active', 'terminated'])),
        ('enterprise\\.associates', '^release_date$', release_date),
        ('enterprise\\.buildings', '^building_name$', text_list(three_word_tuple)),
        ('enterprise\\.departments', '^department_name$', unique_list(tuple(enterprise__departments__department_name))),
    ]
