from fsi_data_generator.fsi_generators.text_list import text_list
from fsi_data_generator.fsi_text.consumer_banking__beneficiaries__supplementary_data import \
    consumer_banking__beneficiaries__supplementary_data
from fsi_data_generator.fsi_text.consumer_banking__products__product_type import \
    consumer_banking__products__product_type
from fsi_data_generator.fsi_text.consumer_banking__standing_orders__supplementary_data import \
    consumer_banking__standing_orders__supplementary_data
from fsi_data_generator.fsi_text.consumer_banking__statement__descriptions import \
    consumer_banking__statement__descriptions
from fsi_data_generator.fsi_text.consumer_banking__transactions__category_purpose_code import \
    consumer_banking__transactions__category_purpose_code
from fsi_data_generator.fsi_text.consumer_banking__transactions__payment_purpose_code import \
    consumer_banking__transactions__payment_purpose_code
from faker import Faker
fake = Faker()

def consumer_banking(_dg):
    return [
        ('consumer_banking\\.accounts', '^status$', text_list([
            "Active",
            "Inactive",
            "Frozen",
            "Closed"
        ])),
        ('consumer_banking\\.statement_descriptions', '^description$', text_list(consumer_banking__statement__descriptions)),
        ('consumer_banking\\.beneficiaries', '^supplementary_data$', text_list(consumer_banking__beneficiaries__supplementary_data)),
        ('consumer_banking\\.transactions', '^category_purpose_code$', text_list(consumer_banking__transactions__category_purpose_code)),
        ('consumer_banking\\.transactions', '^payment_purpose_code$', text_list(consumer_banking__transactions__payment_purpose_code)),
        ('consumer_banking\\.transactions', '^status$', text_list([
                "PENDING",
                "BOOKED",
                "REJECTED",
                "CANCELLED",
                "FAILED",
                "AUTHORIZED",
                "REVERSED",
                "REFUNDED"
            ])),
        ('consumer_banking\\.transactions', '^status$', text_list([
                "PENDING",
                "BOOKED",
                "REJECTED",
                "CANCELLED",
                "FAILED",
                "AUTHORIZED",
                "REVERSED",
                "REFUNDED"
            ])),
        ('consumer_banking\\.transactions', '^transaction_mutability$', text_list([
                "MUTABLE",
                "IMMUTABLE"
            ])),
        ('consumer_banking.standing_orders', '^supplementary_data$', text_list(consumer_banking__standing_orders__supplementary_data)),
        ('consumer_banking\\.products', '^product_type$', text_list(consumer_banking__products__product_type)),
        ('consumer_banking\\.account_access_consents', '^status$', text_list(["Active", "Revoked"])),
    ]
