# from data_generator import DataGenerator
from faker import Faker

from fsi_data_generator.fsi_generators.helpers import apply_schema_to_regex, random_record
from fsi_data_generator.fsi_generators.helpers.consumer_banking_generate_transaction_fee import \
    consumer_banking_generate_transaction_fee
from fsi_data_generator.fsi_generators.helpers.generate_transactions_and_balances import (
    generate_fake_balance, generate_fake_transaction)
from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_generators.helpers.unique_list import unique_list
from fsi_data_generator.fsi_generators.intelligent_generators.consumer_banking.account import generate_random_account
from fsi_data_generator.fsi_generators.intelligent_generators.consumer_banking.account_access_consent import \
    generate_random_account_access_consent
from fsi_data_generator.fsi_text.consumer_banking.consumer_banking__beneficiaries__supplementary_data import \
    consumer_banking__beneficiaries__supplementary_data
from fsi_data_generator.fsi_text.consumer_banking.consumer_banking__customer_interactions__description import \
    consumer_banking__customer_interactions__description
from fsi_data_generator.fsi_text.consumer_banking.consumer_banking__customer_interactions__resolution import \
    consumer_banking__customer_interactions__resolution
from fsi_data_generator.fsi_text.consumer_banking.consumer_banking__products__product_type import \
    consumer_banking__products__product_type
from fsi_data_generator.fsi_text.consumer_banking.consumer_banking__standing_orders__supplementary_data import \
    consumer_banking__standing_orders__supplementary_data
from fsi_data_generator.fsi_text.consumer_banking.consumer_banking__statement__descriptions import \
    consumer_banking__statement__descriptions
from fsi_data_generator.fsi_text.consumer_banking.consumer_banking__transactions__category_purpose_code import \
    consumer_banking__transactions__category_purpose_code
from fsi_data_generator.fsi_text.consumer_banking.consumer_banking__transactions__payment_purpose_code import \
    consumer_banking__transactions__payment_purpose_code

fake = Faker()


def get_product_type_by_account_id(conn, account_id):
    """
    Fetches the product_type associated with a given consumer_banking_account_id.

    :param conn: A psycopg2 database connection object.
    :param account_id: The consumer_banking_account_id to look up.
    :return: The product_type as a string.
    :raises Exception: If the product_type is not found or an error occurs.
    """
    try:
        # Create a new cursor
        with conn.cursor() as cursor:
            # SQL query to fetch the product_type
            query = """
                SELECT p.product_type
                FROM consumer_banking.accounts a
                JOIN consumer_banking.products p
                ON a.consumer_banking_product_id = p.consumer_banking_product_id
                WHERE a.consumer_banking_account_id = %s;
            """

            # Execute the query and fetch the result
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()

            # Check if a result was found
            if result is None:
                raise Exception(f"No product_type found for account_id {account_id}")

            # Return the product_type
            return result.get('product_type')

    except Exception as e:
        # Reraise any exceptions that occur
        raise Exception(f"Error fetching product_type for account_id {account_id}: {str(e)}")


def get_consumer_balance(dg):
    def get_balance(a, _b, _c):
        conn = dg.conn
        account_id = a.get('consumer_banking_account_id')
        product_type = "CHECKING"
        if account_id:
            try:
                product_type = get_product_type_by_account_id(conn, account_id)
            except:
                pass
        value = generate_fake_balance(product_type=product_type)
        return value

    return get_balance


def get_consumer_transaction(dg):
    def get_transaction(a, _b, _c):
        conn = dg.conn
        account_id = a.get('consumer_banking_account_id')
        product_type = "CHECKING"
        if account_id:
            try:
                product_type = get_product_type_by_account_id(conn, account_id)
            except:
                pass
        value = generate_fake_transaction(product_type=product_type)
        return value

    return get_transaction


def consumer_banking(dg):
    return apply_schema_to_regex('consumer_banking', [
        ('account_access_consents', random_record(dg, generate_random_account_access_consent)),
        ('accounts', random_record(dg, generate_random_account)),
        ('transactions', 'charge_amount', consumer_banking_generate_transaction_fee),
        ('transactions', 'charge_currency', lambda a, b, c: 'USD'),
        ('transactions', 'merchant_address', lambda a, b, c: fake.address()),
        ('customer_interactions', 'resolution',
         text_list(consumer_banking__customer_interactions__resolution)),
        ('customer_interactions', 'description',
         text_list(consumer_banking__customer_interactions__description)),
        ('transactions', 'amount', get_consumer_transaction(dg)),
        ('balances', 'amount', get_consumer_balance(dg)),
        ('customer_interactions', 'priority', text_list(["high," "medium," "low"])),
        ('customer_interactions', 'status',
         text_list(["open," "resolved", "not resolved", "pending"])),
        ('customer_interactions', 'interaction_type',
         text_list(["phone call," "email," "chat," "in-person," "online form," "ATM interaction"])),
        ('customer_interactions', 'channel',
         text_list(["phone," "email," "web," "branch," "mobile app"])),
        ('statement_descriptions', 'description',
         text_list(consumer_banking__statement__descriptions)),
        ('beneficiaries', 'supplementary_data',
         text_list(consumer_banking__beneficiaries__supplementary_data)),
        ('transactions', 'category',
         text_list(consumer_banking__transactions__category_purpose_code)),
        ('transactions', 'transaction_type',
         text_list(consumer_banking__transactions__payment_purpose_code)),
        ('transactions', 'status', text_list([
            "pending",
            "completed",
            "rejected",
            "cancelled",
            "failed",
            "authorized",
            "reversed",
            "refunded"
        ])),
        ('transactions', 'transaction_mutability', text_list([
            "mutable",
            "immutable"
        ])),
        ('standing_orders', 'supplementary_data',
         text_list(consumer_banking__standing_orders__supplementary_data)),
        ('products', 'product_type', unique_list(tuple(consumer_banking__products__product_type))),
    ])
