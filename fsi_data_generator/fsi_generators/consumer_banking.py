from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.consumer_banking_generate_transaction_fee import \
    consumer_banking_generate_transaction_fee
from fsi_data_generator.fsi_generators.helpers.generate_transactions_and_balances import generate_fake_balance, \
    generate_fake_transaction
from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_generators.helpers.unique_list import unique_list
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
from faker import Faker
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
            return result[0]

    except Exception as e:
        # Reraise any exceptions that occur
        raise Exception(f"Error fetching product_type for account_id {account_id}: {str(e)}")

def get_consumer_balance(dg: DataGenerator):
    def get_balance(a,_b,_c):
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

def get_consumer_transaction(dg: DataGenerator):
    def get_transaction(a,_b,_c):
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
    return [
        ('consumer_banking\\.transactions', '^charge_amount$', consumer_banking_generate_transaction_fee),
        ('consumer_banking\\.transactions', '^charge_currency$', lambda a,b,c: 'USD'),
        ('consumer_banking\\.transactions', '^merchant_address$', lambda a,b,c: fake.address()),
        ('consumer_banking\\.customer_interactions', '^resolution$', text_list(consumer_banking__customer_interactions__resolution)),
        ('consumer_banking\\.customer_interactions', '^description$', text_list(consumer_banking__customer_interactions__description)),
        ('consumer_banking\\.transactions', '^amount$', get_consumer_transaction(dg)),
        ('consumer_banking\\.balances', '^amount$', get_consumer_balance(dg)),
        ('consumer_banking\\.customer_interactions', '^priority$', text_list(["high," "medium," "low"])),
        ('consumer_banking\\.customer_interactions', '^status$', text_list(["open," "resolved", "not resolved", "pending"])),
        ('consumer_banking\\.customer_interactions', '^interaction_type$', text_list(["phone call," "email," "chat," "in-person," "online form," "ATM interaction"])),
        ('consumer_banking\\.customer_interactions','^channel$', text_list(["phone," "email," "web," "branch," "mobile app"])),
        ('consumer_banking\\.accounts', '^status$', text_list([
            "active",
            "Inactive",
            "Frozen",
            "Closed"
        ], lower=True)),
        ('consumer_banking\\.statement_descriptions', '^description$', text_list(consumer_banking__statement__descriptions)),
        ('consumer_banking\\.beneficiaries', '^supplementary_data$', text_list(consumer_banking__beneficiaries__supplementary_data)),
        ('consumer_banking\\.transactions', '^category$', text_list(consumer_banking__transactions__category_purpose_code)),
        ('consumer_banking\\.transactions', '^transaction_type$', text_list(consumer_banking__transactions__payment_purpose_code)),
        ('consumer_banking\\.transactions', '^status$', text_list([
                "pending",
                "completed",
                "rejected",
                "cancelled",
                "failed",
                "authorized",
                "reversed",
                "refunded"
            ])),
        ('consumer_banking\\.transactions', '^transaction_mutability$', text_list([
                "mutable",
                "immutable"
            ])),
        ('consumer_banking\\.standing_orders', '^supplementary_data$', text_list(consumer_banking__standing_orders__supplementary_data)),
        ('consumer_banking\\.products', '^product_type$', unique_list(tuple(consumer_banking__products__product_type))),
        ('consumer_banking\\.account_access_consents', '^status$', text_list(["active", "revoked"])),
    ]
