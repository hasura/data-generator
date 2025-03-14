import logging
import random

from faker import Faker

from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_applications__status import \
    consumer_lending__loan_applications__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_applications__application_type import \
    consumer_lending__loan_applications__application_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__application_applicants__relationship_to_primary import \
    consumer_lending__application_applicants__relationship_to_primary
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__application_applicants__applicant_type import \
    consumer_lending__application_applicants__applicant_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicants__housing_status import \
    consumer_lending__applicants__housing_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicants__citizenship_status import \
    consumer_lending__applicants__citizenship_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicants__marital_status import \
    consumer_lending__applicants__marital_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicant_employments__employment_type import \
    consumer_lending__applicant_employments__employment_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicant_incomes__verification_status import \
    consumer_lending__applicant_incomes__verification_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicant_incomes__frequency import \
    consumer_lending__applicant_incomes__frequency
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicant_incomes__income_type import \
    consumer_lending__applicant_incomes__income_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicant_assets__verification_status import \
    consumer_lending__applicant_assets__verification_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicant_liabilities__verification_status import \
    consumer_lending__applicant_liabilities__verification_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__applicant_liabilities__liability_type import \
    consumer_lending__applicant_liabilities__liability_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_products__disbursement_options import \
    consumer_lending__loan_products__disbursement_options
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_products__late_fee_type import \
    consumer_lending__loan_products__late_fee_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_products__origination_fee_type import \
    consumer_lending__loan_products__origination_fee_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_products__interest_rate_type import \
    consumer_lending__loan_products__interest_rate_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_products__loan_type import \
    consumer_lending__loan_products__loan_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__product_eligibility_criteria__criteria_type import \
    consumer_lending__product_eligibility_criteria__criteria_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__risk_based_pricing_tiers__tier_name import \
    consumer_lending__risk_based_pricing_tiers__tier_name
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__credit_reports__status import \
    consumer_lending__credit_reports__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__credit_reports__bureau_name import \
    consumer_lending__credit_reports__bureau_name
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__credit_reports__report_type import \
    consumer_lending__credit_reports__report_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__credit_report_tradelines__worst_delinquency import \
    consumer_lending__credit_report_tradelines__worst_delinquency
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__credit_report_tradelines__payment_status import \
    consumer_lending__credit_report_tradelines__payment_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__credit_report_tradelines__account_type import \
    consumer_lending__credit_report_tradelines__account_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__decision_models__model_type import \
    consumer_lending__decision_models__model_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__public_records__status import \
    consumer_lending__public_records__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__public_records__record_type import \
    consumer_lending__public_records__record_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__credit_inquiries__inquiry_type import \
    consumer_lending__credit_inquiries__inquiry_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_accounts__payment_frequency import \
    consumer_lending__loan_accounts__payment_frequency
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_accounts__status import \
    consumer_lending__loan_accounts__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__vehicles__vehicle_type import \
    consumer_lending__vehicles__vehicle_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__adverse_action_notices__status import \
    consumer_lending__adverse_action_notices__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__adverse_action_notices__delivery_method import \
    consumer_lending__adverse_action_notices__delivery_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__application_decisions__decision_result import \
    consumer_lending__application_decisions__decision_result
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__application_decisions__decision_type import \
    consumer_lending__application_decisions__decision_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_collateral__collateral_type import \
    consumer_lending__loan_collateral__collateral_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_fees__fee_status import \
    consumer_lending__loan_fees__fee_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_fees__fee_type import \
    consumer_lending__loan_fees__fee_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_payments__payment_status import \
    consumer_lending__loan_payments__payment_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_payments__payment_method import \
    consumer_lending__loan_payments__payment_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__disbursements__disbursement_method import \
    consumer_lending__disbursements__disbursement_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__payment_schedules__status import \
    consumer_lending__payment_schedules__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_statements__delivery_method import \
    consumer_lending__loan_statements__delivery_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_communications__status import \
    consumer_lending__loan_communications__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_communications__direction import \
    consumer_lending__loan_communications__direction
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_communications__communication_type import \
    consumer_lending__loan_communications__communication_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_documents__status import \
    consumer_lending__loan_documents__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_documents__document_type import \
    consumer_lending__loan_documents__document_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_applications__application_channel import \
    consumer_lending__loan_applications__application_channel
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_applications__referral_source import \
    consumer_lending__loan_applications__referral_source
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_payments__payment_type import \
    consumer_lending__loan_payments__payment_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__disbursements__disbursement_status import \
    consumer_lending__disbursements__disbursement_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__collection_accounts__resolution_type import \
    consumer_lending__collection_accounts__resolution_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__collection_accounts__priority import \
    consumer_lending__collection_accounts__priority
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__collection_accounts__status import \
    consumer_lending__collection_accounts__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_insurance__status import \
    consumer_lending__loan_insurance__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_insurance__premium_frequency import \
    consumer_lending__loan_insurance__premium_frequency
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_insurance__insurance_type import \
    consumer_lending__loan_insurance__insurance_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_modifications__status import \
    consumer_lending__loan_modifications__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__loan_modifications__modification_type import \
    consumer_lending__loan_modifications__modification_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__payment_arrangements__payment_frequency import \
    consumer_lending__payment_arrangements__payment_frequency
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__payment_arrangements__status import \
    consumer_lending__payment_arrangements__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__collection_actions__action_result import \
    consumer_lending__collection_actions__action_result
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__collection_actions__action_type import \
    consumer_lending__collection_actions__action_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__compliance_exceptions__status import \
    consumer_lending__compliance_exceptions__status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__compliance_exceptions__severity import \
    consumer_lending__compliance_exceptions__severity
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__compliance_exceptions__regulation import \
    consumer_lending__compliance_exceptions__regulation
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__compliance_exceptions__exception_type import \
    consumer_lending__compliance_exceptions__exception_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__high_cost_mortgage_tests__test_type import \
    consumer_lending__high_cost_mortgage_tests__test_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__military_lending_checks__military_status import \
    consumer_lending__military_lending_checks__military_status
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__military_lending_checks__verification_method import \
    consumer_lending__military_lending_checks__verification_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__appraisal_disclosures__delivery_method import \
    consumer_lending__appraisal_disclosures__delivery_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__appraisal_disclosures__disclosure_type import \
    consumer_lending__appraisal_disclosures__disclosure_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__reg_b_notices__delivery_method import \
    consumer_lending__reg_b_notices__delivery_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__reg_b_notices__notice_type import \
    consumer_lending__reg_b_notices__notice_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__fairlending_analysis__analysis_type import \
    consumer_lending__fairlending_analysis__analysis_type
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__ecoa_monitoring__action_taken import \
    consumer_lending__ecoa_monitoring__action_taken
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__ecoa_monitoring__information_method import \
    consumer_lending__ecoa_monitoring__information_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__adverse_action_details__credit_bureau_name import \
    consumer_lending__adverse_action_details__credit_bureau_name
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__reg_z_disclosures__delivery_method import \
    consumer_lending__reg_z_disclosures__delivery_method
from fsi_data_generator.fsi_text.consumer_lending.consumer_lending__reg_z_disclosures__disclosure_type import \
    consumer_lending__reg_z_disclosures__disclosure_type
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
        ('consumer_lending\\.compliance_exceptions', '^root_cause$',  text_list(consumer_lending__compliance_exceptions__root_cause)),
        ('consumer_lending\\.compliance_exceptions', '^remediation_plan$',  text_list(consumer_lending__compliance_exceptions__remediation_plan)),
        ('consumer_lending\\.compliance_exceptions', '^preventive_action$',  text_list(consumer_lending__compliance_exceptions__preventive_action)),
        ('consumer_lending\\.compliance_exceptions', '^description$',  text_list(consumer_lending__compliance_exceptions__description)),
        ('consumer_lending\\.high_cost_mortgage_tests', '^notes$',  text_list(consumer_lending__high_cost__mortgage_tests__notes)),
        ('consumer_lending\\.fairlending_analysis', '^findings$',  text_list(consumer_lending__fairlending_analysis__findings)),
        ('consumer_lending\\.fairlending_analysis', '^controls_applied$',  text_list(consumer_lending__fairlending_analysis__controls_applied)),
        ('consumer_lending\\.adverse_action_details', '^credit_score_factors$',  text_list(consumer_lending__adverse_action_details__credit_score_factors)),
        ('consumer_lending\\.reg_z_disclosures', '^security_interest$', text_list(consumer_lending__reg_z_disclosures__security_interest)),
        ('consumer_lending\\.payment_arrangements', '^notes$', text_list(consumer_lending__payment_arrangements__notes)),
        ('consumer_lending\\.collection_actions', '^notes$', text_list(consumer_lending__collection_actions__notes)),
        ('consumer_lending\\.loan_communications', '^content$', subject_content),
        ('consumer_lending\\.loan_communications', '^subject$',  text_list(consumer_lending__loan_communications__subject)),
        ('consumer_lending\\.disbursements', '^notes$', text_list(consumer_lending__disbursements__notes)),
        ('consumer_lending\\.decision_models', '^description$',  text_list(consumer_lending__decision_models__description)),
        ('consumer_lending\\.product_eligibility_criteria', '^description$',  text_list(consumer_lending__product_eligibility_criteria__description)),
        ('consumer_lending\\.reg_z_disclosures', '^disclosure_type$',  text_list(
            consumer_lending__reg_z_disclosures__disclosure_type)),
        ('consumer_lending\\.reg_z_disclosures', '^delivery_method$',  text_list(
            consumer_lending__reg_z_disclosures__delivery_method)),
        ('consumer_lending\\.adverse_action_details', '^credit_bureau_name$',  text_list(
            consumer_lending__adverse_action_details__credit_bureau_name)),
        ('consumer_lending\\.ecoa_monitoring', '^information_method$',  text_list(
            consumer_lending__ecoa_monitoring__information_method)),
        ('consumer_lending\\.ecoa_monitoring', '^action_taken$',  text_list(
            consumer_lending__ecoa_monitoring__action_taken)),
        ('consumer_lending\\.fairlending_analysis', '^analysis_type$',  text_list(
            consumer_lending__fairlending_analysis__analysis_type)),
        ('consumer_lending\\.fairlending_analysis', '^action_recommend$',  text_list(consumer_lending__fairlending_analysis__action_recommended)),
        ('consumer_lending\\.reg_b_notices', '^notice_type$',  text_list(consumer_lending__reg_b_notices__notice_type)),
        ('consumer_lending\\.reg_b_notices', '^delivery_method$', text_list(
            consumer_lending__reg_b_notices__delivery_method)),
        ('consumer_lending\\.appraisal_disclosures', '^disclosure_type$',  text_list(
            consumer_lending__appraisal_disclosures__disclosure_type)),
        ('consumer_lending\\.appraisal_disclosures', '^delivery_method$', text_list(
            consumer_lending__appraisal_disclosures__delivery_method)),
        ('consumer_lending\\.military_lending_checks', '^verification_method$',  text_list(
            consumer_lending__military_lending_checks__verification_method)),
        ('consumer_lending\\.military_lending_checks', '^military_status$',  text_list(
            consumer_lending__military_lending_checks__military_status)),
        ('consumer_lending\\.high_cost_mortgage_tests', '^test_type$', text_list(
            consumer_lending__high_cost_mortgage_tests__test_type)),
        ('consumer_lending\\.compliance_exceptions', '^exception_type$', text_list(
            consumer_lending__compliance_exceptions__exception_type)),
        ('consumer_lending\\.compliance_exceptions', '^regulation$', text_list(
            consumer_lending__compliance_exceptions__regulation)),
        ('consumer_lending\\.compliance_exceptions', '^severity$', text_list(
            consumer_lending__compliance_exceptions__severity)),
        ('consumer_lending\\.compliance_exceptions', '^status$', text_list(
            consumer_lending__compliance_exceptions__status)),
        ('consumer_lending\\.collection_actions', '^action_type$', text_list(
            consumer_lending__collection_actions__action_type)),
        ('consumer_lending\\.collection_actions', '^action_result$', text_list(
            consumer_lending__collection_actions__action_result)),
        ('consumer_lending\\.payment_arrangements', '^status$', text_list(
            consumer_lending__payment_arrangements__status)),
        ('consumer_lending\\.payment_arrangements', '^payment_frequency$', text_list(
            consumer_lending__payment_arrangements__payment_frequency)),
        ('consumer_lending\\.loan_modifications', '^modification_type$', text_list(
            consumer_lending__loan_modifications__modification_type)),
        ('consumer_lending\\.loan_modifications', '^status$', text_list(consumer_lending__loan_modifications__status)),
        ('consumer_lending\\.loan_insurance', '^insurance_type$', text_list(
            consumer_lending__loan_insurance__insurance_type)),
        ('consumer_lending\\.loan_insurance', '^premium_frequency$', text_list(
            consumer_lending__loan_insurance__premium_frequency)),
        ('consumer_lending\\.loan_insurance', '^status$', text_list(consumer_lending__loan_insurance__status)),
        ('consumer_lending\\.loan_documents', '^document_type$', text_list(
            consumer_lending__loan_documents__document_type)),
        ('consumer_lending\\.loan_documents', '^status$', text_list(consumer_lending__loan_documents__status)),
        ('consumer_lending\\.loan_communications', '^communication_type$', text_list(
            consumer_lending__loan_communications__communication_type)),
        ('consumer_lending\\.loan_communications', '^direction$', text_list(
            consumer_lending__loan_communications__direction)),
        ('consumer_lending\\.loan_communications', '^status$', text_list(consumer_lending__loan_communications__status)),
        ('consumer_lending\\.loan_statements', '^delivery_method$', text_list(
            consumer_lending__loan_statements__delivery_method)),
        ('consumer_lending\\.collection_accounts', '^status$', text_list(consumer_lending__collection_accounts__status)),
        ('consumer_lending\\.collection_accounts', '^priority$', text_list(
            consumer_lending__collection_accounts__priority)),
        ('consumer_lending\\.collection_accounts', '^resolution_type$', text_list(
            consumer_lending__collection_accounts__resolution_type)),
        ('consumer_lending\\.payment_schedules', '^status$', text_list(consumer_lending__payment_schedules__status)),
        ('consumer_lending\\.disbursements', '^disbursement_method$', text_list(
            consumer_lending__disbursements__disbursement_method)),
        ('consumer_lending\\.disbursements', '^disbursement_status$', text_list(
            consumer_lending__disbursements__disbursement_status)),
        ('consumer_lending\\.loan_payments', '^payment_type$', text_list(consumer_lending__loan_payments__payment_type)),
        ('consumer_lending\\.loan_payments', '^payment_method$', text_list(
            consumer_lending__loan_payments__payment_method)),
        ('consumer_lending\\.loan_payments', '^payment_status$', text_list(
            consumer_lending__loan_payments__payment_status)),
        ('consumer_lending\\.loan_fees', '^fee_type$', text_list(consumer_lending__loan_fees__fee_type)),
        ('consumer_lending\\.loan_fees', '^fee_status$', text_list(consumer_lending__loan_fees__fee_status)),
        ('consumer_lending\\.loan_collateral', '^collateral_type$', text_list(
            consumer_lending__loan_collateral__collateral_type)),
        ('consumer_lending\\.application_decisions', '^decision_type$', text_list(
            consumer_lending__application_decisions__decision_type)),
        ('consumer_lending\\.application_decisions', '^decision_result$',  text_list(
            consumer_lending__application_decisions__decision_result)),
        ('consumer_lending\\.adverse_action_notices', '^delivery_method$', text_list(
            consumer_lending__adverse_action_notices__delivery_method)),
        ('consumer_lending\\.adverse_action_notices', '^status$', text_list(
            consumer_lending__adverse_action_notices__status)),
        ('consumer_lending\\.vehicles', '^vehicle_type$', text_list(consumer_lending__vehicles__vehicle_type)),
        ('consumer_lending\\.loan_accounts', '^status$',  text_list(consumer_lending__loan_accounts__status)),
        ('consumer_lending\\.loan_accounts', '^payment_frequency$', text_list(
            consumer_lending__loan_accounts__payment_frequency)),
        ('consumer_lending\\.credit_inquiries', '^inquiry_type$', text_list(
            consumer_lending__credit_inquiries__inquiry_type)),
        ('consumer_lending\\.public_records', '^record_type$', text_list(consumer_lending__public_records__record_type)),
        ('consumer_lending\\.public_records', '^status$', text_list(consumer_lending__public_records__status)),
        ('consumer_lending\\.decision_models', '^model_type$',  text_list(
            consumer_lending__decision_models__model_type)),
        ('consumer_lending\\.credit_report_tradelines', '^account_type$',  text_list(
            consumer_lending__credit_report_tradelines__account_type)),
        ('consumer_lending\\.credit_report_tradelines', '^payment_status$', text_list(
            consumer_lending__credit_report_tradelines__payment_status)),
        ('consumer_lending\\.credit_report_tradelines', '^worst_delinquency$',  text_list(
            consumer_lending__credit_report_tradelines__worst_delinquency)),
        ('consumer_lending\\.credit_reports', '^report_type$', text_list(consumer_lending__credit_reports__report_type)),
        ('consumer_lending\\.credit_reports', '^bureau_name$', text_list(consumer_lending__credit_reports__bureau_name)),
        ('consumer_lending\\.credit_reports', '^status$', text_list(consumer_lending__credit_reports__status)),
        ('consumer_lending\\.risk_based_pricing_tiers', '^tier_name$',  text_list(
            consumer_lending__risk_based_pricing_tiers__tier_name)),
        ('consumer_lending\\.product_eligibility_criteria', '^criteria_type$',  text_list(
            consumer_lending__product_eligibility_criteria__criteria_type)),
        ('consumer_lending\\.loan_products', '^loan_type$', text_list(consumer_lending__loan_products__loan_type)),
        ('consumer_lending\\.loan_products', '^interest_rate_type$', text_list(
            consumer_lending__loan_products__interest_rate_type)),
        ('consumer_lending\\.loan_products', '^origination_fee_type$', text_list(
            consumer_lending__loan_products__origination_fee_type)),
        ('consumer_lending\\.loan_products', '^late_fee_type$', text_list(
            consumer_lending__loan_products__late_fee_type)),
        ('consumer_lending\\.loan_products', '^disbursement_options$',  text_list(
            consumer_lending__loan_products__disbursement_options)),
        ('consumer_lending\\.applicant_liabilities', '^liability_type$',  text_list(
            consumer_lending__applicant_liabilities__liability_type)),
        ('consumer_lending\\.applicant_liabilities', '^verification_status$',  text_list(
            consumer_lending__applicant_liabilities__verification_status)),
        ('consumer_lending\\.applicant_assets', '^verification_status$',  text_list(
            consumer_lending__applicant_assets__verification_status)),
        ('consumer_lending\\.applicant_incomes', '^income_type$', text_list(
            consumer_lending__applicant_incomes__income_type)),
        ('consumer_lending\\.applicant_incomes', '^frequency$',  text_list(
            consumer_lending__applicant_incomes__frequency)),
        ('consumer_lending\\.applicant_incomes', '^verification_status$',  text_list(
            consumer_lending__applicant_incomes__verification_status)),
        ('consumer_lending\\.applicant_employments', '^employment_type$',  text_list(
            consumer_lending__applicant_employments__employment_type)),
        ('consumer_lending\\.applicants', '^marital_status$', text_list(consumer_lending__applicants__marital_status)),
        ('consumer_lending\\.applicants', '^citizenship_status$',  text_list(
            consumer_lending__applicants__citizenship_status)),
        ('consumer_lending\\.applicants', '^housing_status$', text_list(consumer_lending__applicants__housing_status)),
        ('consumer_lending\\.application_applicants', '^applicant_type$',  text_list(
            consumer_lending__application_applicants__applicant_type)),
        ('consumer_lending\\.application_applicants', '^relationship_to_primary$', text_list(
            consumer_lending__application_applicants__relationship_to_primary)),
        ('consumer_lending\\.loan_applications', '^decision_reason$',  text_list(consumer_lending__loan_applications__decision_reasons)),
        ('consumer_lending\\.loan_applications', '^application_type$', text_list(
            consumer_lending__loan_applications__application_type)),
        ('consumer_lending\\.loan_applications', '^status$',  text_list(consumer_lending__loan_applications__status)),
        ('consumer_lending\\.loan_applications', '^application_channel$',  text_list(
            consumer_lending__loan_applications__application_channel)),
        ('consumer_lending\\.loan_applications', '^referral_source$', text_list(
            consumer_lending__loan_applications__referral_source)),
        ('consumer_lending\\.application_applicants', 'consumer_lending_application_id',  lambda a, b, c: loan_applications(dg)),
        ('consumer_lending\\.application_applicants', 'consumer_lending_applicant_id',  lambda a, b, c: loan_applicants(dg)),
    ]
