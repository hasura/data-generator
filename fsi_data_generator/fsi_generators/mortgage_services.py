from .helpers.apply_schema_to_regex import apply_schema_to_regex
from .helpers.random_record import random_record
from .intelligent_generators.mortgage_services import (
    generate_borrower_asset, generate_random_application,
    generate_random_application_borrower, generate_random_appraisal,
    generate_random_borrower, generate_random_borrower_employment,
    generate_random_borrower_income, generate_random_borrower_liability,
    generate_random_closed_loan, generate_random_closing_appointment,
    generate_random_closing_disclosure, generate_random_condition,
    generate_random_credit_report, generate_random_customer_communication,
    generate_random_document, generate_random_escrow_analysis,
    generate_random_escrow_disbursement,
    generate_random_hmda_applicant_demographics, generate_random_hmda_edit,
    generate_random_hmda_record, generate_random_hmda_submission,
    generate_random_insurance_policy, generate_random_loan_modification,
    generate_random_loan_product, generate_random_loan_rate_lock,
    generate_random_mortgage, generate_random_payment,
    generate_random_property, generate_random_servicing_account)
from faker import Faker

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
