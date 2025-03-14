import logging
import random

from faker import Faker

from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__adverse_action_details__credit_score_factors import \
    consumer_lending__adverse_action_details__credit_score_factors
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__collection_actions__notes import \
    consumer_lending__collection_actions__notes
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__compliance_exceptions__description import \
    consumer_lending__compliance_exceptions__description
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__compliance_exceptions__preventive_action import \
    consumer_lending__compliance_exceptions__preventive_action
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__compliance_exceptions__remediation_plan import \
    consumer_lending__compliance_exceptions__remediation_plan
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__compliance_exceptions__root_cause import \
    consumer_lending__compliance_exceptions__root_cause
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__decision_models__description import \
    consumer_lending__decision_models__description
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__disbursements__notes import consumer_lending__disbursements__notes
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__fairlending_analysis__action_recommended import \
    consumer_lending__fairlending_analysis__action_recommended
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__fairlending_analysis__controls_applied import \
    consumer_lending__fairlending_analysis__controls_applied
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__fairlending_analysis__findings import \
    consumer_lending__fairlending_analysis__findings
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__high_cost__mortgage_tests__notes import \
    consumer_lending__high_cost__mortgage_tests__notes
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_applications__decision_reasons import \
    consumer_lending__loan_applications__decision_reasons
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_communications__content import \
    consumer_lending__loan_communications__content
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_communications__content_dict import \
    consumer_lending__loan_communications__content_dict
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_communications__subject import \
    consumer_lending__loan_communications__subject
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__payment_arrangements__notes import \
    consumer_lending__payment_arrangements__notes
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__product_eligibility_criteria__description import \
    consumer_lending__product_eligibility_criteria__description
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__reg_z_disclosures__security_interest import \
    consumer_lending__reg_z_disclosures__security_interest

logger = logging.getLogger(__name__)
fake = Faker()

consumer_lending__loan_applicants_pks = None
consumer_lending__loan_applications_pks = None


def loan_applications(dg):
    global consumer_lending__loan_applications_pks
    if consumer_lending__loan_applications_pks is None:
        consumer_lending__loan_applications_pks = list(dg.inserted_pks['consumer_lending.loan_applications'])
        random.shuffle(consumer_lending__loan_applications_pks)
    if len(consumer_lending__loan_applications_pks) == 0:
        raise Exception('Not enough loan applications - increase # generated.')
    value = consumer_lending__loan_applications_pks.pop(0)
    logger.debug(f'loan_applications: {len(consumer_lending__loan_applications_pks)}/{value}')
    return value


def loan_applicants(dg):
    global consumer_lending__loan_applicants_pks
    if consumer_lending__loan_applicants_pks is None:
        consumer_lending__loan_applicants_pks = list(dg.inserted_pks['consumer_lending.applicants'])
        random.shuffle(consumer_lending__loan_applicants_pks)
    if len(consumer_lending__loan_applicants_pks) == 0:
        raise Exception('Not enough loan applicants - increase # generated.')
    value = consumer_lending__loan_applicants_pks.pop(0)
    logger.debug(f'loan_applicants: {len(consumer_lending__loan_applicants_pks)}/{value}')
    return value


def subject_content(a, _b, _c):
    subject = a.get("subject")
    content = consumer_lending__loan_communications__content_dict.get(subject)
    if content:
        return content

    return fake.random_element(consumer_lending__loan_communications__content)


def consumer_lending(dg):
    return [
        ('consumer_lending\\.compliance_exceptions', '^root_cause$',
         text_list(consumer_lending__compliance_exceptions__root_cause)),
        ('consumer_lending\\.compliance_exceptions', '^remediation_plan$',
         text_list(consumer_lending__compliance_exceptions__remediation_plan)),
        ('consumer_lending\\.compliance_exceptions', '^preventive_action$',
         text_list(consumer_lending__compliance_exceptions__preventive_action)),
        ('consumer_lending\\.compliance_exceptions', '^description$',
         text_list(consumer_lending__compliance_exceptions__description)),
        ('consumer_lending\\.high_cost_mortgage_tests', '^notes$',
         text_list(consumer_lending__high_cost__mortgage_tests__notes)),
        ('consumer_lending\\.fairlending_analysis', '^findings$',
         text_list(consumer_lending__fairlending_analysis__findings)),
        ('consumer_lending\\.fairlending_analysis', '^controls_applied$',
         text_list(consumer_lending__fairlending_analysis__controls_applied)),
        ('consumer_lending\\.adverse_action_details', '^credit_score_factors$',
         text_list(consumer_lending__adverse_action_details__credit_score_factors)),
        ('consumer_lending\\.reg_z_disclosures', '^security_interest$',
         text_list(consumer_lending__reg_z_disclosures__security_interest)),
        (
        'consumer_lending\\.payment_arrangements', '^notes$', text_list(consumer_lending__payment_arrangements__notes)),
        ('consumer_lending\\.collection_actions', '^notes$', text_list(consumer_lending__collection_actions__notes)),
        ('consumer_lending\\.loan_communications', '^content$', subject_content),
        ('consumer_lending\\.loan_communications', '^subject$',
         text_list(consumer_lending__loan_communications__subject)),
        ('consumer_lending\\.disbursements', '^notes$', text_list(consumer_lending__disbursements__notes)),
        ('consumer_lending\\.decision_models', '^description$',
         text_list(consumer_lending__decision_models__description)),
        ('consumer_lending\\.product_eligibility_criteria', '^description$',
         text_list(consumer_lending__product_eligibility_criteria__description)),
        ('consumer_lending\\.reg_z_disclosures', '^disclosure_type$',
         text_list(["initial TIL", "loan estimate", "closing disclosure", "change in terms"])),
        ('consumer_lending\\.reg_z_disclosures', '^delivery_method$',
         text_list(["email", "mail", "in person", "electronic"])),
        ('consumer_lending\\.adverse_action_details', '^credit_bureau_name$',
         text_list(["Equifax", "Experian", "TransUnion"])),
        ('consumer_lending\\.ecoa_monitoring', '^information_method$',
         text_list(["Self-reported", "Observed", "Not Provided"], lower=True)),
        ('consumer_lending\\.ecoa_monitoring', '^action_taken$',
         text_list(["Approved", "Denied", "Withdrawn", "Incomplete"], lower=True)),
        ('consumer_lending\\.fairlending_analysis', '^analysis_type$',
         text_list(["Pricing", "Underwriting", "Marketing", "Redlining", "Steering"], lower=True)),
        ('consumer_lending\\.fairlending_analysis', '^action_recommend$',
         text_list(consumer_lending__fairlending_analysis__action_recommended)),
        ('consumer_lending\\.reg_b_notices', '^notice_type$',
         text_list(["Incompleteness", "Counteroffer", "Notice of Action Taken"], lower=True)),
        ('consumer_lending\\.reg_b_notices', '^delivery_method$', text_list(["email", "mail", "electronic"], lower=True)),
        ('consumer_lending\\.appraisal_disclosures', '^disclosure_type$',
         text_list(["Initial Disclosure", "Final Disclosure"])),
        ('consumer_lending\\.appraisal_disclosures', '^delivery_method$', text_list(["email", "mail", "electronic"], lower=True)),
        ('consumer_lending\\.military_lending_checks', '^verification_method$',
         text_list(["MLA Database", "Credit Report Flag", "Self-reported", "Other"], lower=True)),
        ('consumer_lending\\.military_lending_checks', '^military_status$',
         text_list(["active Duty", "Dependent", "Veteran", "Retired Military", "Not Military"], lower=True)),
        ('consumer_lending\\.high_cost_mortgage_tests', '^test_type$', text_list(["APR Test", "Points and Fees Test"])),
        ('consumer_lending\\.compliance_exceptions', '^exception_type$', text_list(
            ["Documentation", "Disclosure", "Timing", "Data Integrity", "Process Error", "System Error", "Other"], lower=True)),
        ('consumer_lending\\.compliance_exceptions', '^regulation$',
         text_list(["Reg Z", "Reg B", "FCRA", "ECOA", "MLA", "HOEPA", "Other"])),
        ('consumer_lending\\.compliance_exceptions', '^severity$', text_list(["High", "Medium", "Low"], lower=True)),
        ('consumer_lending\\.compliance_exceptions', '^status$', text_list(["Open", "In Remediation", "Closed"], lower=True)),
        ('consumer_lending\\.collection_actions', '^action_type$',
         text_list(["Call", "Letter", "email", "Field Visit", "Text Message"], lower=True)),
        ('consumer_lending\\.collection_actions', '^action_result$', text_list(
            ["Contact Made", "Left Message", "No Answer", "Promise to Pay", "Refused to Pay", "Payment Arranged"], lower=True)),
        ('consumer_lending\\.payment_arrangements', '^status$', text_list(["active", "Completed", "Broken"], lower=True)),
        ('consumer_lending\\.payment_arrangements', '^payment_frequency$',
         text_list(["Weekly", "Bi-weekly", "Monthly"], lower=True)),
        ('consumer_lending\\.loan_modifications', '^modification_type$', text_list(
            ["Rate Reduction", "Term Extension", "Principal Reduction", "Payment Reduction", "Forbearance", "Other"], lower=True)),
        (
        'consumer_lending\\.loan_modifications', '^status$', text_list(["Pending", "Approved", "Denied", "Completed"], lower=True)),
        ('consumer_lending\\.loan_insurance', '^insurance_type$',
         text_list(["Auto", "Hazard", "Credit Life", "Disability"], lower=True)),
        ('consumer_lending\\.loan_insurance', '^premium_frequency$', text_list(["Annual", "Monthly"], lower=True)),
        ('consumer_lending\\.loan_insurance', '^status$', text_list(["active", "Lapsed", "Canceled"], lower=True)),
        ('consumer_lending\\.loan_documents', '^document_type$', text_list(
            ["Application", "Contract", "Statement", "Identification", "Income Verification", "Insurance", "Other"], lower=True)),
        ('consumer_lending\\.loan_documents', '^status$', text_list(["Pending", "Reviewed", "Accepted", "Rejected"], lower=True)),
        ('consumer_lending\\.loan_communications', '^communication_type$',
         text_list(["email", "Letter", "Phone Call", "Text"], lower=True)),
        ('consumer_lending\\.loan_communications', '^direction$', text_list(["Inbound", "Outbound"], lower=True)),
        ('consumer_lending\\.loan_communications', '^status$', text_list(["Sent", "Delivered", "Failed", "Received"], lower=True)),
        ('consumer_lending\\.loan_statements', '^delivery_method$', text_list(["email", "mail", "portal"], lower=True)),
        ('consumer_lending\\.collection_accounts', '^status$', text_list(["active", "Resolved", "Charged Off"], lower=True)),
        ('consumer_lending\\.collection_accounts', '^priority$', text_list(["High", "Medium", "Low"], lower=True)),
        ('consumer_lending\\.collection_accounts', '^resolution_type$',
         text_list(["Paid", "Settlement", "Modification", "Charge Off"], lower=True)),
        ('consumer_lending\\.payment_schedules', '^status$', text_list(["Scheduled", "Paid", "Past Due"], lower=True)),
        ('consumer_lending\\.disbursements', '^disbursement_method$', text_list(["ACH", "Check", "Wire"], lower=True)),
        ('consumer_lending\\.disbursements', '^disbursement_status$', text_list(["Pending", "Completed", "Failed"], lower=True)),
        ('consumer_lending\\.loan_payments', '^payment_type$', text_list(["Regular", "Extra Principal", "Late"], lower=True)),
        ('consumer_lending\\.loan_payments', '^payment_method$',
         text_list(["ACH", "Check", "Online", "Phone", "Money Order", "in person"], lower=True)),
        ('consumer_lending\\.loan_payments', '^payment_status$',
         text_list(["Pending", "Completed", "Returned", "Canceled"], lower=True)),
        ('consumer_lending\\.loan_fees', '^fee_type$',
         text_list(["Late Fee", "NSF fee", "origination fee", "prepayment penalty", "annual fee", "processing fee"])),
        ('consumer_lending\\.loan_fees', '^fee_status$', text_list(["Pending", "Charged", "Waived", "Paid"], lower=True)),
        ('consumer_lending\\.loan_collateral', '^collateral_type$',
         text_list(["Vehicle", "Property", "Deposit Account", "Savings Account", "Investment Account", "Other"], lower=True)),
        ('consumer_lending\\.application_decisions', '^decision_type$',
         text_list(["Prequalification", "Initial", "Final"], lower=True)),
        ('consumer_lending\\.application_decisions', '^decision_result$',
         text_list(["Approved", "Denied", "Pending Review"], lower=True)),
        ('consumer_lending\\.adverse_action_notices', '^delivery_method$', text_list(["email", "mail", "Portal"], lower=True)),
        ('consumer_lending\\.adverse_action_notices', '^status$', text_list(["Generated", "Sent", "Delivered"], lower=True)),
        ('consumer_lending\\.vehicles', '^vehicle_type$', text_list(["New", "Used"], lower=True)),
        ('consumer_lending\\.loan_accounts', '^status$',
         text_list(["active", "Paid Off", "Charged Off", "Delinquent", "Closed", "Default"], lower=True)),
        ('consumer_lending\\.loan_accounts', '^payment_frequency$', text_list(["Monthly", "Bi-weekly", "Weekly"], lower=True)),
        ('consumer_lending\\.credit_inquiries', '^inquiry_type$', text_list(["Hard inquiry", "Soft inquiry"], lower=True)),
        ('consumer_lending\\.public_records', '^record_type$', text_list(["Bankruptcy", "Lien", "Judgment"], lower=True)),
        ('consumer_lending\\.public_records', '^status$', text_list(["active", "Satisfied", "Discharged"], lower=True)),
        ('consumer_lending\\.decision_models', '^model_type$',
         text_list(["Credit Score", "Income Verification", "Fraud Detection"], lower=True)),
        ('consumer_lending\\.credit_report_tradelines', '^account_type$',
         text_list(["Mortgage", "Installment", "Revolving", "Open", "Closed"])),
        ('consumer_lending\\.credit_report_tradelines', '^payment_status$', text_list(
            ["Current", "30 days late", "60 days late", "90 days late", "120 days late", "Charged off", "Collection"], lower=True)),
        ('consumer_lending\\.credit_report_tradelines', '^worst_delinquency$',
         text_list(["30 days late", "60 days late", "90 days late", "120 days late", "Charged off", "Collection"], lower=True)),
        ('consumer_lending\\.credit_reports', '^report_type$', text_list(["Tri-merge", "Single Bureau"], lower=True)),
        ('consumer_lending\\.credit_reports', '^bureau_name$', text_list(["Equifax", "Experian", "TransUnion"])),
        ('consumer_lending\\.credit_reports', '^status$', text_list(["Completed", "Failed", "Pending"], lower=True)),
        ('consumer_lending\\.risk_based_pricing_tiers', '^tier_name$',
         text_list(["Platinum Plus", "Gold Star", "Silver Standard", "Bronze Basic", "Starter Tier"], lower=True)),
        ('consumer_lending\\.product_eligibility_criteria', '^criteria_type$',
         text_list(["credit score", "income", "DTI", "employment", "age", "citizenship", "collateral"])),
        ('consumer_lending\\.loan_products', '^loan_type$', text_list(
            ["Personal", "Auto", "Student", "Home Improvement", "Debt Consolidation", "Recreational Vehicle", "Boat",
             "Other"], lower=True)),
        ('consumer_lending\\.loan_products', '^interest_rate_type$', text_list(["Fixed", "Variable"], lower=True)),
        ('consumer_lending\\.loan_products', '^origination_fee_type$', text_list(["Flat", "Percentage"], lower=True)),
        ('consumer_lending\\.loan_products', '^late_fee_type$', text_list(["Flat", "Percentage"], lower=True)),
        ('consumer_lending\\.loan_products', '^disbursement_options$',
         text_list(["Direct Deposit", "Check", "Dealer Direct"], lower=True)),
        ('consumer_lending\\.applicant_liabilities', '^liability_type$',
         text_list(["Credit Card", "Auto Loan", "Student Loan", "Mortgage", "Personal Loan", "Medical Debt", "Other"], lower=True)),
        ('consumer_lending\\.applicant_liabilities', '^verification_status$',
         text_list(["Self-reported", "Verified", "Failed"], lower=True)),
        ('consumer_lending\\.applicant_assets', '^verification_status$',
         text_list(["Self-reported", "Verified", "Failed"], lower=True)),
        ('consumer_lending\\.applicant_incomes', '^income_type$', text_list(
            ["Salary", "Self-employment", "Rental", "Alimony", "Child Support", "Investment Income",
             "Retirement Income", "Social Security", "Disability", "Other"], lower=True)),
        ('consumer_lending\\.applicant_incomes', '^frequency$',
         text_list(["Weekly", "Bi-weekly", "Semi-monthly", "Monthly", "Quarterly", "Annual"], lower=True)),
        ('consumer_lending\\.applicant_incomes', '^verification_status$',
         text_list(["Self-reported", "Verified", "Failed"], lower=True)),
        ('consumer_lending\\.applicant_employments', '^employment_type$',
         text_list(["Full-time", "Part-time", "Self-employed", "Contract", "Temporary", "Retired", "Other"], lower=True)),
        ('consumer_lending\\.applicants', '^marital_status$', text_list(
            ["Single", "Married", "Divorced", "Widowed", "Separated", "Domestic Partnership", "Civil Union", "Other"], lower=True)),
        ('consumer_lending\\.applicants', '^citizenship_status$',
         text_list(["US Citizen", "Permanent Resident", "Visa Holder", "Other"], lower=True)),
        ('consumer_lending\\.applicants', '^housing_status$', text_list(["Own", "Rent", "Live with Parents", "Other"], lower=True)),
        ('consumer_lending\\.application_applicants', '^applicant_type$',
         text_list(["Primary", "Co-Applicant", "Guarantor"])),
        ('consumer_lending\\.application_applicants', '^relationship_to_primary$', text_list(
            ["Spouse", "Domestic Partner", "Parent", "Child", "Sibling", "Other Relative", "Friend", "Business Partner",
             "None"], lower=True)),
        ('consumer_lending\\.loan_applications', '^decision_reason$',
         text_list(consumer_lending__loan_applications__decision_reasons)),
        ('consumer_lending\\.loan_applications', '^application_type$', text_list(
            ["Personal", "Auto", "Student", "Home Improvement", "Debt Consolidation", "Recreational Vehicle", "Boat",
             "Other"], lower=True)),
        ('consumer_lending\\.loan_applications', '^status$',
         text_list(["Draft", "Submitted", "In Review", "Approved", "Denied", "Cancelled"], lower=True)),
        ('consumer_lending\\.loan_applications', '^application_channel$',
         text_list(["Online", "Mobile", "Branch", "Phone", "mail"], lower=True)),
        ('consumer_lending\\.loan_applications', '^referral_source$', text_list(
            ["Website", "Social Media", "Email Campaign", "Referral Program", "Partner Referral", "Direct Mail",
             "Television Ad", "Radio Ad", "Print Ad", "Other"], lower=True)),
        ('consumer_lending\\.application_applicants', 'consumer_lending_application_id',
         lambda a, b, c: loan_applications(dg)),
        ('consumer_lending\\.application_applicants', 'consumer_lending_applicant_id',
         lambda a, b, c: loan_applicants(dg)),
    ]
