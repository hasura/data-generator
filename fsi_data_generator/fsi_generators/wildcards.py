from datetime import datetime, timedelta

from faker import Faker

from fsi_data_generator.fsi_generators.helpers.generate_leis import \
    generate_leis
from fsi_data_generator.fsi_generators.helpers.generate_permission_name import \
    generate_all_permission_names
from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_text.wildcards.____direct_debit_status_code import \
    ____direct_debit_status_code
from fsi_data_generator.fsi_text.wildcards.____frequency_point_in_time import \
    ____frequency_point_in_time
from fsi_data_generator.fsi_text.wildcards.____frequency_type import \
    ____frequency_type
from fsi_data_generator.fsi_text.wildcards.____offer_type import ____offer_type
from fsi_data_generator.fsi_text.wildcards.____standing_order_status_code import \
    ____standing_order_status_code
from fsi_data_generator.fsi_text.wildcards.__balances__sub_type import \
    __balances__sub_type
from fsi_data_generator.fsi_text.wildcards.__balances__type import \
    __balances__type
from fsi_data_generator.fsi_text.wildcards.__statement__rate_type import \
    __statement__rate_type
from fsi_data_generator.fsi_text.wildcards.__statement_benefits__type import \
    __statement_benefits__type
from fsi_data_generator.fsi_text.wildcards.__statement_fees__frequency import \
    __statement_fees__frequency
from fsi_data_generator.fsi_text.wildcards.__statement_fees__type import \
    __statement_fees__type
from fsi_data_generator.fsi_text.wildcards.__statements__type import \
    __statements__type

fake = Faker()
fake_ca = Faker('en_CA')

fake_leis = generate_leis()
three_word_strings = [" ".join((fake.word(), fake.word(), fake.word())) for _ in range(10000)]
three_word_strings.append('')
three_word_tuple = tuple(three_word_strings)


def status_update_date_time(a, _b, _c):
    opening_date = a.get("opened_date")
    if opening_date is None:
        return fake.date_time_between_dates(datetime_start=timedelta(weeks=-10 * 52), datetime_end=datetime.now())
    return generate_random_date_between(opening_date)


wildcards = [
    # ('^.*\\.accounts', '^status_update_date_time$', status_update_date_time),
    # ('.*', '^mobile$', lambda a, b, c: fake.phone_number()),
    # ('.*', '^first_name$', lambda a, b, c: fake.first_name()),
    # ('.*', '^middle_name$', lambda a, b, c: fake.first_name()),
    # ('.*', '^last_name$', lambda a, b, c: fake.last_name()),
    # ('.*', '^surname$', lambda a, b, c: fake.last_name()),
    # ('.*', '^email$', generate_email),
    ('.*', '^standing_order_status_code$', text_list(____standing_order_status_code)),
    ('.*', '^permission_name$',
     lambda a, b, c: fake.unique.random_element(tuple(generate_all_permission_names()))),
    ('.*', '^entity_type$', text_list(
        ["customer", "borrower", "business", "vendor", "employee", "branch", "department", "subsidiary",
         "supplier",
         "partner", "shareholder", "legal_representative", "agent", "regulator", "government_agency"])),
    ('^.*\\.account_statement_preferences', '^frequency$', text_list(
        ["Daily", "Weekly", "Bi-Weekly", "Monthly", "Quarterly", "Annually", "Upon Request", "End of Month"],
        lower=True)),
    ('^.*\\.account_statement_preferences', '^format$',
     text_list(["PDF", "Paper", "CSV", "HTML", "XML", "Plain Text"])),
    ('^.*\\.account_statement_preferences', '^communication_method$',
     text_list(["EMAIL", "POSTAL", "ONLINE_BANKING", "MOBILE_APP", "SMS"])),
    ('.*', '^switch_status$', text_list(
        ["Initiated", "In Progress", "Completed", "Failed", "Cancelled", "Pending", "Awaiting Confirmation",
         "Validation Error", "Transferred", "Rejected"])),
    ('^.*\\.transaction_card_instruments', '^authorisation_type$', text_list([
        "PIN",
        "Signature",
        "Contactless",
        "Online",
        "CVV",
        "3D Secure",
        "Biometric",
        "Fallback",
        "Manual"
    ])),
    ('^.*\\.transaction_debtor_agents', '^name$', lambda a, b, c: fake.company()),
    ('.*', '^merchant_category_code$', lambda a, b, c: fake.merchant_category_code()),
    ('^.*\\.transaction_balances', '^type$', text_list([
        "Booked",
        "Available",
        "Hold",
        "Closing"
    ], lower=True)),
    ('^.*\\.transaction_bank_transaction_codes', '^code$', text_list([
        "PAYMENT",
        "TRANSFER",
        "DEPOSIT",
        "WITHDRAWAL",
        "FEE",
        "INTEREST",
        "ADJUSTMENT",
        "REVERSAL",
        "PURCHASE",
        "SALE",
        "CREDIT",
        "DEBIT",
        "DIRECT_DEBIT",
        "STANDING_ORDER",
        "ATM_TRANSACTION",
        "POINT_OF_SALE",
        "ONLINE_TRANSFER",
        "INTERNATIONAL_TRANSFER",
        "CHECK_DEPOSIT",
        "WIRE_TRANSFER",
        "CARD_PAYMENT",
        "CARD_WITHDRAWAL",
        "FX_TRADE",
        "SECURITY_TRADE",
        "DIVIDEND",
        "TAX"
    ], lower=True)),
    ('^.*\\.transaction_bank_transaction_codes', '^sub_code$', text_list([
        "DOMESTIC",
        "INTERNATIONAL",
        "INTERNAL",
        "EXTERNAL",
        "ATM",
        "ONLINE",
        "BRANCH",
        "POS",
        "DIRECT",
        "SCHEDULED",
        "IMMEDIATE",
        "RECURRING",
        "ONE_TIME",
        "CHECK",
        "WIRE",
        "CREDIT_CARD",
        "DEBIT_CARD",
        "SAVINGS",
        "CHECKING",
        "LOAN",
        "MORTGAGE",
        "INVESTMENT",
        "FX_SPOT",
        "FX_FORWARD",
        "EQUITY",
        "BOND",
        "MUTUAL_FUND",
        "GOVERNMENT",
        "CORPORATE",
        "RETAIL",
        "WHOLESALE",
        "SALARY",
        "RENT",
        "UTILITIES",
        "GROCERIES",
        "ENTERTAINMENT",
        "TRAVEL",
        "ELECTRONICS",
        "CLOTHING",
        "FUEL",
        "INSURANCE"
    ], lower=True)),
    ('.*', '^contract_identification$', lambda a, b, c: generate_random_forex_contract_id()),

    (
        '.*\\.statement_values', '^type$', text_list([
            "LOYALTY_POINTS",
            "TIER_LEVEL",
            "CREDIT_SCORE",
            "REWARD_STATUS",
            "ACCOUNT_STANDING",
            "CUSTOMER_SEGMENT"
        ], lower=True)
    ),
    (
        '^.*\\.statement_date_times', '^type$', text_list([
            "PAYMENT_DUE",
            "MINIMUM_PAYMENT_DUE",
            "CYCLE_END",
            "STATEMENT_GENERATED",
            "INTEREST_CALCULATED",
            "LAST_STATEMENT_DATE"
        ], lower=True)
    ),
    (
        '^.*\\.statement_rates', '^type$', text_list([
            "APR",
            "INTEREST",
            "EXCHANGE",
            "PROMOTIONAL",
            "PENALTY",
            "DISCOUNT",
            "BONUS"
        ], lower=True)
    ),
    (
        '^.*\\.statement_amounts', '^type$', text_list([
            "OPENING_BALANCE",
            "CLOSING_BALANCE",
            "PAYMENTS",
            "RECEIPTS",
            "INTEREST_EARNED",
            "INTEREST_CHARGED",
            "FEES_CHARGED",
            "REWARDS_EARNED",
            "TRANSFERS_IN",
            "TRANSFERS_OUT"
        ], lower=True)
    ),
    (
        '^.*\\.statement_amounts', '^sub_type$', text_list([
            "ATM_WITHDRAWAL",
            "ONLINE_TRANSFER",
            "CHECK_DEPOSIT",
            "DIRECT_DEBIT",
            "STANDING_ORDER"
        ], lower=True)
    ),
    (
        '^.*\\.statement_interests', '^type$', text_list([
            "DEPOSIT",
            "LOAN",
            "CREDIT_CARD",
            "MORTGAGE",
            "INVESTMENT"
        ], lower=True)
    ),
    (
        '^.*\\.statement_interests', '^rate_type$', text_list([
            "FIXED",
            "VARIABLE",
            "INTRODUCTORY",
            "PENALTY",
            "PROMOTIONAL"
        ], lower=True)
    ),
    (
        '^.*\\.statement_interests', '^frequency$', text_list([
            "DAILY",
            "WEEKLY",
            "MONTHLY",
            "QUARTERLY",
            "ANNUALLY"
        ], lower=True)
    ),
    (
        '^.*\\.statement_fees', '^frequency$', text_list(__statement_fees__frequency, lower=True)
    ),
    (
        '^.*\\.statement_.*$', '^rate_type$', text_list(__statement__rate_type, lower=True)
    ),
    (
        '^.*\\.statement_fees', '^type$', text_list(__statement_fees__type, lower=True)
    ),
    (
        '^.*\\.statement_benefits', '^type$', text_list(__statement_benefits__type, lower=True)
    ),
    (
        '^.*\\.statements', '^type$', text_list(__statements__type, lower=True)
    ),

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
        '.*', '^offer_type$', text_list(____offer_type, lower=True)
    ),
    (
        '.*', '^frequency_point_in_time$', text_list(____frequency_point_in_time, lower=True)
    ),
    (
        '.*', '^frequency_type$', text_list(____frequency_type, lower=True)
    ),
    (
        '.*', '^direct_debit_status_code$', text_list(____direct_debit_status_code, lower=True)
    ),
    (
        '.*', '^credit_debit_indicator$', text_list(["CR", "DR"])
    ),
    (
        '.*\\.balances', '^type$', text_list(__balances__type, lower=True)
    ),
    (
        '.*\\.balances', '^sub_type$', text_list(__balances__sub_type, lower=True)
    ),
    (
        '.*\\.(balances|transactions)', '^currency|source_currency|target_currency|unit_currency$', text_list([
            "USD",
            "EUR",
            "GBP",
            "JPY"
        ]
        ))
]
