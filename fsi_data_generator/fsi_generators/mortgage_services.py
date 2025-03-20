from decimal import Decimal
from typing import Dict

from faker import Faker

from data_generator import DataGenerator, SkipRowGenerationError
from fsi_data_generator.fsi_generators.helpers.generate_application_borrower_record import \
    generate_application_borrower_record
from fsi_data_generator.fsi_generators.helpers.generate_borrower_asset_record import generate_borrower_asset
from fsi_data_generator.fsi_generators.helpers.generate_borrower_employment import \
    generate_random_borrower_employment
from fsi_data_generator.fsi_generators.helpers.generate_borrower_income import generate_borrower_income
from fsi_data_generator.fsi_generators.helpers.generate_random_application import generate_random_application
from fsi_data_generator.fsi_generators.helpers.generate_random_appraisal import generate_random_appraisal
from fsi_data_generator.fsi_generators.helpers.generate_random_borrower import generate_random_borrower
from fsi_data_generator.fsi_generators.helpers.generate_random_borrower_liability import \
    generate_random_borrower_liability
from fsi_data_generator.fsi_generators.helpers.generate_random_closed_loan import generate_random_closed_loan
from fsi_data_generator.fsi_generators.helpers.generate_random_closing_appointment import \
    generate_random_closing_appointment
from fsi_data_generator.fsi_generators.helpers.generate_random_closing_disclosure import \
    generate_random_closing_disclosure
from fsi_data_generator.fsi_generators.helpers.generate_random_condition import generate_random_condition
from fsi_data_generator.fsi_generators.helpers.generate_random_credit_report import generate_random_credit_report
from fsi_data_generator.fsi_generators.helpers.generate_random_document import generate_random_document
from fsi_data_generator.fsi_generators.helpers.generate_random_escrow_analysis import generate_random_escrow_analysis
from fsi_data_generator.fsi_generators.helpers.generate_random_escrow_disbursement import \
    generate_random_escrow_disbursement
from fsi_data_generator.fsi_generators.helpers.generate_random_hmda_applicant_demographics import \
    generate_random_hmda_applicant_demographics
from fsi_data_generator.fsi_generators.helpers.generate_random_hmda_edit import generate_random_hmda_edit
from fsi_data_generator.fsi_generators.helpers.generate_random_hmda_record import generate_random_hmda_record
from fsi_data_generator.fsi_generators.helpers.generate_random_hmda_submission import generate_random_hmda_submission
from fsi_data_generator.fsi_generators.helpers.generate_random_insurance_policy import generate_random_insurance_policy
from fsi_data_generator.fsi_generators.helpers.generate_random_loan_product import generate_random_loan_product
from fsi_data_generator.fsi_generators.helpers.generate_random_loan_rate_lock import generate_random_loan_rate_lock
from fsi_data_generator.fsi_generators.helpers.generate_random_mortgage import generate_random_mortgage
from fsi_data_generator.fsi_generators.helpers.generate_random_payment import generate_random_payment
from fsi_data_generator.fsi_generators.helpers.generate_random_property import generate_random_property
from fsi_data_generator.fsi_generators.helpers.generate_random_servicing_account import \
    generate_random_servicing_account
from fsi_data_generator.fsi_generators.helpers.mod_tuples import mod_tuples
from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__communication_type import \
    mortgage_services__customer_communications__communication_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__content import \
    mortgage_services__customer_communications__content
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__direction import \
    mortgage_services__customer_communications__direction
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__related_to import \
    mortgage_services__customer_communications__related_to
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__status import \
    mortgage_services__customer_communications__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_modification__modification_type import \
    mortgage_services__loan_modification__modification_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_modification__status import \
    mortgage_services__loan_modification__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_modifications__reason import \
    mortgage_services__loan_modifications__reason

fake = Faker()

def generate_property(ids_dict, dg: DataGenerator):

    conn = dg.conn

    # Randomly choose an application ID
    application_id = ids_dict.get('mortgage_services_application_id')

    # SQL query to get the application details via the application_id
    query = """
            SELECT app.*
            FROM mortgage_services.applications AS app
            WHERE app.mortgage_services_application_id = %s
            """

    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(query, (application_id,))  # Parameterized query
        record = cursor.fetchone()  # Fetch the resulting record

    # If a record is found, convert it to a dictionary
    if record:
        record_dict = {desc[0]: value for desc, value in zip(cursor.description, record)}

        # Convert DECIMAL to float in the dictionary
        for key, value in record_dict.items():
            if isinstance(value, Decimal):
                record_dict[key] = float(value)
    else:
        raise ValueError(f"No loan application found for application_id: {application_id}")

    property_ = generate_random_property(record_dict)

    return property_



def generate_mortgage(ids_dict, dg: DataGenerator):

    conn = dg.conn

    # Randomly choose an application ID
    application_id = ids_dict.get('mortgage_services_application_id')

    # SQL query to get the loan product details via the application_id
    query = """
    SELECT lp.*
    FROM mortgage_services.applications AS app
    JOIN mortgage_services.loan_products AS lp
    ON app.mortgage_services_loan_product_id = lp.mortgage_services_loan_product_id
    WHERE app.mortgage_services_application_id = %s
    """

    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(query, (application_id,))  # Parameterized query
        record = cursor.fetchone()  # Fetch the resulting record

    # If a record is found, convert it to a dictionary
    if record:
        record_dict = {desc[0]: value for desc, value in zip(cursor.description, record)}

        # Convert DECIMAL to float in the dictionary
        for key, value in record_dict.items():
            if isinstance(value, Decimal):
                record_dict[key] = float(value)
    else:
        raise ValueError(f"No loan product found for application_id: {application_id}")

    loan_product = record_dict

    # SQL query to get the loan product details via the application_id
    query = """
            SELECT app.*
            FROM mortgage_services.applications AS app
            WHERE app.mortgage_services_application_id = %s
            """

    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(query, (application_id,))  # Parameterized query
        record = cursor.fetchone()  # Fetch the resulting record

    # If a record is found, convert it to a dictionary
    if record:
        record_dict = {desc[0]: value for desc, value in zip(cursor.description, record)}

        # Convert DECIMAL to float in the dictionary
        for key, value in record_dict.items():
            if isinstance(value, Decimal):
                record_dict[key] = float(value)
    else:
        raise ValueError(f"No application found for application_id: {application_id}")

    loan_application = record_dict

    # Do something with the retrieved data, e.g., update 'a'
    mortgage = generate_random_mortgage(loan_product=loan_product, loan_application=loan_application)

    # Optionally return something (e.g., application_id or the record_dict)
    interest_rate = mortgage.get('interest_rate')
    if not interest_rate:
        raise SkipRowGenerationError(f"No mortgage generated for application_id: {application_id}")
    return mortgage



def generate_application(ids_dict, dg: DataGenerator):

    conn = dg.conn

    # Randomly choose an application ID
    loan_product_id = ids_dict.get('mortgage_services_loan_product_id')

    # SQL query to get the loan product details via the application_id
    query = """
            SELECT lp.*
            FROM mortgage_services.loan_products AS lp
            WHERE lp.mortgage_services_loan_product_id = %s
            """
    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(query, (loan_product_id,))  # Parameterized query
        record = cursor.fetchone()  # Fetch the resulting record

    # If a record is found, convert it to a dictionary
    if record:
        record_dict = {desc[0]: value for desc, value in zip(cursor.description, record)}

        # Convert DECIMAL to float in the dictionary
        for key, value in record_dict.items():
            if isinstance(value, Decimal):
                record_dict[key] = float(value)
    else:
        raise ValueError(f"No loan product found for loan_product_id: {loan_product_id}")

    # Do something with the retrieved data, e.g., update 'a'
    loan_application = generate_random_application(loan_product=record_dict)


    # Optionally return something (e.g., application_id or the record_dict)
    return loan_application


def random_record(dg: DataGenerator, fn):
    def get_it(record: Dict, _b, field):
        record.update(fn(record, dg))
        return record.get(field)
    return get_it


def mortgage_services(dg):
    return mod_tuples('mortgage_services', [
        ('escrow_disbursements', random_record(dg, generate_random_escrow_disbursement)),
        ('escrow_analyses', random_record(dg, generate_random_escrow_analysis)),
        ('payments', random_record(dg, generate_random_payment)),
        ('insurance_policies', random_record(dg, generate_random_insurance_policy)),
        ('servicing_accounts', random_record(dg, generate_random_servicing_account)),
        ('closed_loans', random_record(dg, generate_random_closed_loan)),
        ('closing_appointments', random_record(dg, generate_random_closing_appointment)),
        ('closing_disclosures', random_record(dg, generate_random_closing_disclosure)),
        ('borrowers', random_record(dg, generate_random_borrower)),
        ('documents', random_record(dg, generate_random_document)),
        ('conditions', random_record(dg, generate_random_condition)),
        ('credit_reports', random_record(dg, generate_random_credit_report)),
        ('appraisals', random_record(dg, generate_random_appraisal)),
        ('loan_rate_locks', random_record(dg, generate_random_loan_rate_lock)),
        ('borrower_liabilities', random_record(dg, generate_random_borrower_liability)),
        ('application_borrowers', random_record(dg, generate_application_borrower_record)),
        ('borrower_employments', random_record(dg, generate_random_borrower_employment)),
        ('borrower_incomes', random_record(dg, generate_borrower_income)),
        ('borrower_assets', random_record(dg, generate_borrower_asset)),
        ('loan_products', random_record(dg, generate_random_loan_product)),
        ('applications', random_record(dg, generate_application)),
        ('properties', random_record(dg, generate_property)),
        ('loans', random_record(dg, generate_mortgage)),
        ('hmda_records', random_record(dg, generate_random_hmda_record)),
        ('hmda_edits', random_record(dg, generate_random_hmda_edit)),
        ('hmda_applicant_demographics', random_record(dg, generate_random_hmda_applicant_demographics)),
        ('hmda_submissions', random_record(dg, generate_random_hmda_submission)),
        ('customer_communications', 'communication_type',
         text_list(mortgage_services__customer_communications__communication_type)),
        ('customer_communications', 'direction',
         text_list(mortgage_services__customer_communications__direction, lower=True)),
        ('customer_communications', 'status',
         text_list(mortgage_services__customer_communications__status, lower=True)),
        ('customer_communications', 'related_to',
         text_list(mortgage_services__customer_communications__related_to, lower=True)),
        ('loan_modification', 'modification_type',
         text_list(mortgage_services__loan_modification__modification_type, lower=True)),
        ('loan_modification', 'reason', text_list(
            mortgage_services__loan_modifications__reason)),
        ('loan_modification', 'status',
         text_list(mortgage_services__loan_modification__status, lower=True)),
        ('.*', 'document_name', lambda a, b, c: fake.file_name()),
        ('.*', '.*_path', lambda a, b, c: fake.file_path()),
        ('customer_communications', 'content',
         text_list(mortgage_services__customer_communications__content)),
    ])
