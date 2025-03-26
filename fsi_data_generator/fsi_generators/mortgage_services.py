from faker import Faker

from .helpers.apply_schema_to_regex import apply_schema_to_regex
from .helpers.random_record import random_record
from .intelligent_generators.mortgage_services.application import \
    generate_random_application
from .intelligent_generators.mortgage_services.application_borrower import \
    generate_random_application_borrower
from .intelligent_generators.mortgage_services.appraisal import \
    generate_random_appraisal
from .intelligent_generators.mortgage_services.asset import \
    generate_borrower_asset
from .intelligent_generators.mortgage_services.borrower import \
    generate_random_borrower
from .intelligent_generators.mortgage_services.borrower_income import \
    generate_random_borrower_income
from .intelligent_generators.mortgage_services.borrower_liability import \
    generate_random_borrower_liability
from .intelligent_generators.mortgage_services.closed_loan import \
    generate_random_closed_loan
from .intelligent_generators.mortgage_services.closing_appointment import \
    generate_random_closing_appointment
from .intelligent_generators.mortgage_services.closing_disclosure import \
    generate_random_closing_disclosure
from .intelligent_generators.mortgage_services.condition import \
    generate_random_condition
from .intelligent_generators.mortgage_services.credit_report import \
    generate_random_credit_report
from .intelligent_generators.mortgage_services.customer_communication import \
    generate_random_customer_communication
from .intelligent_generators.mortgage_services.document import \
    generate_random_document
from .intelligent_generators.mortgage_services.employment import \
    generate_random_borrower_employment
from .intelligent_generators.mortgage_services.escrow_analysis import \
    generate_random_escrow_analysis
from .intelligent_generators.mortgage_services.escrow_disbursement import \
    generate_random_escrow_disbursement
from .intelligent_generators.mortgage_services.hmda_applicant_demographics import \
    generate_random_hmda_applicant_demographics
from .intelligent_generators.mortgage_services.hmda_edit import \
    generate_random_hmda_edit
from .intelligent_generators.mortgage_services.hmda_record import \
    generate_random_hmda_record
from .intelligent_generators.mortgage_services.hmda_submission import \
    generate_random_hmda_submission
from .intelligent_generators.mortgage_services.insurance_policy import \
    generate_random_insurance_policy
from .intelligent_generators.mortgage_services.loan_modification import \
    generate_random_loan_modification
from .intelligent_generators.mortgage_services.loan_product import \
    generate_random_loan_product
from .intelligent_generators.mortgage_services.loan_rate_lock import \
    generate_random_loan_rate_lock
from .intelligent_generators.mortgage_services.mortgage import \
    generate_random_mortgage
from .intelligent_generators.mortgage_services.payment import \
    generate_random_payment
from .intelligent_generators.mortgage_services.property import \
    generate_random_property
from .intelligent_generators.mortgage_services.servicing_account import \
    generate_random_servicing_account

fake = Faker()


def mortgage_services(dg):
    return apply_schema_to_regex('mortgage_services', [
        ('customer_communications', random_record(dg, generate_random_customer_communication)),
        ('loan_modifications', random_record(dg, generate_random_loan_modification)),
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
        ('application_borrowers', random_record(dg, generate_random_application_borrower)),
        ('borrower_employments', random_record(dg, generate_random_borrower_employment)),
        ('borrower_incomes', random_record(dg, generate_random_borrower_income)),
        ('borrower_assets', random_record(dg, generate_borrower_asset)),
        ('loan_products', random_record(dg, generate_random_loan_product)),
        ('applications', random_record(dg, generate_random_application)),
        ('properties', random_record(dg, generate_random_property)),
        ('loans', random_record(dg, generate_random_mortgage)),
        ('hmda_records', random_record(dg, generate_random_hmda_record)),
        ('hmda_edits', random_record(dg, generate_random_hmda_edit)),
        ('hmda_applicant_demographics', random_record(dg, generate_random_hmda_applicant_demographics)),
        ('hmda_submissions', random_record(dg, generate_random_hmda_submission))
    ])
