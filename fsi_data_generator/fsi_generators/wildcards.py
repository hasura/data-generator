from faker import Faker
from fsi_data_generator.fsi_generators.helpers.generate_leis import \
    generate_leis
from fsi_data_generator.fsi_generators.helpers.generate_permission_name import \
    generate_all_permission_names
from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_text.wildcards.____frequency_point_in_time import \
    ____frequency_point_in_time

fake = Faker()
fake_ca = Faker('en_CA')

fake_leis = generate_leis()
three_word_strings = [" ".join((fake.word(), fake.word(), fake.word())) for _ in range(10000)]
three_word_strings.append('')
three_word_tuple = tuple(three_word_strings)

wildcards = [
    ('.*', '^permission_name$',
     lambda a, b, c: fake.unique.random_element(tuple(generate_all_permission_names()))),
    ('.*', '^entity_type$', text_list(
        ["customer", "borrower", "business", "vendor", "employee", "branch", "department", "subsidiary",
         "supplier",
         "partner", "shareholder", "legal_representative", "agent", "regulator", "government_agency"])),
    ('.*', '^switch_status$', text_list(
        ["Initiated", "In Progress", "Completed", "Failed", "Cancelled", "Pending", "Awaiting Confirmation",
         "Validation Error", "Transferred", "Rejected"])),
    (
        '^.*', '^scheduled_type$', text_list([
            "SINGLE",
            "RECURRING"
        ], lower=True)
    ),
    (
        '.*', '^issuer|merchant_name$', lambda a, b, c: fake.company()
    ),
    (
        '.*', '^frequency_point_in_time$', text_list(____frequency_point_in_time, lower=True)
    ),

]
