from faker import Faker

from fsi_data_generator.fsi_generators.helpers.generate_account_number import \
    fake_account_numbers
from fsi_data_generator.fsi_generators.helpers.generate_ein import fake_eins
from fsi_data_generator.fsi_generators.helpers.generate_product_code import \
    fake_product_codes
from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__account_signatories__signatory_level import \
    small_business_banking__account_signatories__signatory_level
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__accounts__account_type import \
    small_business_banking__accounts__account_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__accounts__status import \
    small_business_banking__accounts__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__adverse_action_notices__delivery_method import \
    small_business_banking__adverse_action_notices__delivery_method
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__adverse_action_notices__primary_reason import \
    small_business_banking__adverse_action_notices__primary_reason
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__adverse_action_notices__score_factors import \
    small_business_banking__adverse_action_notices__score_factors
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__adverse_action_notices__secondary_reasons import \
    small_business_banking__adverse_action_notices__secondary_reasons
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__beneficial_owner_verification__id_type import \
    small_business_banking__beneficial_owner_verification__id_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__beneficial_owner_verification__notes import \
    small_business_banking__beneficial_owner_verification__notes
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__beneficial_owner_verification__screening_results import \
    small_business_banking__beneficial_owner_verification__screening_results
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__beneficial_owner_verification__verification_method import \
    small_business_banking__beneficial_owner_verification__verification_method
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__beneficial_owner_verification__verification_status import \
    small_business_banking__beneficial_owner_verification__verification_status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_card_accounts__account_type import \
    small_business_banking__business_card_accounts__account_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_card_accounts__expense_category_setup import \
    small_business_banking__business_card_accounts__expense_category_setup
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_card_accounts__liability_type import \
    small_business_banking__business_card_accounts__liability_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_card_accounts__ownership_type import \
    small_business_banking__business_card_accounts__ownership_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_card_users__merchant_category_restrictions import \
    small_business_banking__business_card_users__merchant_category_restrictions
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_card_users__role import (
    small_business_banking__accounts__statement_frequency,
    small_business_banking__business_card_users__role)
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__approval_status import \
    small_business_banking__business_due_diligence__approval_status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__diligence_type import \
    small_business_banking__business_due_diligence__diligence_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__expected_activity import \
    small_business_banking__business_due_diligence__expected_activity
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__high_risk_factors import \
    small_business_banking__business_due_diligence__high_risk_factors
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__notes import \
    small_business_banking__business_due_diligence__notes
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__review_frequency import \
    small_business_banking__business_due_diligence__review_frequency
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__risk_rating import \
    small_business_banking__business_due_diligence__risk_rating
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__screening_results import \
    small_business_banking__business_due_diligence__screening_results
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__site_visit_notes import \
    small_business_banking__business_due_diligence__site_visit_notes
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_due_diligence__verification_method import \
    small_business_banking__business_due_diligence__verification_method
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_owners__role import \
    small_business_banking__business_owners__role
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_risk_assessments__assessment_type import \
    small_business_banking__business_risk_assessments__assessment_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_risk_assessments__mitigating_factors import \
    small_business_banking__business_risk_assessments__mitigating_factors
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_risk_assessments__rationale import \
    small_business_banking__business_risk_assessments__rationale
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_risk_assessments__recommended_actions import \
    small_business_banking__business_risk_assessments__recommended_actions
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__business_risk_assessments__risk_rating import \
    small_business_banking__business_risk_assessments__risk_rating
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__businesses__business_type import \
    small_business_banking__businesses__business_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__businesses__status import \
    small_business_banking__businesses__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__collateral__collateral_type import (
    small_business_banking__collateral__collateral_type,
    small_business_banking__collateral__valuation_type)
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__collateral__description import \
    small_business_banking__collateral__description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__collateral__status import \
    small_business_banking__collateral__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_cases__case_type import \
    small_business_banking__compliance_cases__case_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_cases__description import \
    small_business_banking__compliance_cases__description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_cases__escalation_reason import \
    small_business_banking__compliance_cases__escalation_reason
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_cases__priority import \
    small_business_banking__compliance_cases__priority
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_cases__resolution import \
    small_business_banking__compliance_cases__resolution
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_cases__source import \
    small_business_banking__compliance_cases__source
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_cases__status import \
    small_business_banking__compliance_cases__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_requirements__business_impact import \
    small_business_banking__compliance_requirements__business_impact
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_requirements__control_measures import \
    small_business_banking__compliance_requirements__control_measures
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_requirements__description import \
    small_business_banking__compliance_requirements__description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_requirements__verification_frequency import \
    small_business_banking__compliance_requirements__verification_frequency
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__compliance_requirements__verification_procedure import \
    small_business_banking__compliance_requirements__verification_procedure
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__credit_decisions__decision_factors import \
    small_business_banking__credit_decisions__decision_factors
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__credit_decisions__decision_outcome import \
    small_business_banking__credit_decisions__decision_outcome
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__credit_decisions__decision_type import \
    small_business_banking__credit_decisions__decision_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__credit_decisions__exception_reason import \
    small_business_banking__credit_decisions__exception_reason
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__credit_lines__interest_type import \
    small_business_banking__credit_lines__interest_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__credit_lines__status import \
    small_business_banking__credit_lines__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__documents__document_type import \
    small_business_banking__documents__document_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__documents__status import \
    small_business_banking__documents__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loan_fair_lending__action_taken import \
    small_business_banking__loan_fair_lending__action_taken
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loan_fair_lending__denial_reason_1 import \
    small_business_banking__loan_fair_lending__denial_reason_1
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loan_fair_lending__denial_reason_2 import \
    small_business_banking__loan_fair_lending__denial_reason_2
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loan_fair_lending__denial_reason_3 import \
    small_business_banking__loan_fair_lending__denial_reason_3
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loan_fair_lending__denial_reason_4 import \
    small_business_banking__loan_fair_lending__denial_reason_4
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loan_fair_lending__loan_type import \
    small_business_banking__loan_fair_lending__loan_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loans__interest_type import \
    small_business_banking__loans__interest_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loans__payment_frequency import \
    small_business_banking__loans__payment_frequency
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loans__purpose import \
    small_business_banking__loans__purpose
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__loans__status import \
    small_business_banking__loans__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__payments__payment_method import \
    small_business_banking__payments__payment_method
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__payments__payment_type import \
    small_business_banking__payments__payment_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__payments__status import \
    small_business_banking__payments__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__products__description import \
    small_business_banking__products__description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__products__product_type import \
    small_business_banking__products__product_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_findings__corrective_action_description import \
    small_business_banking__regulatory_findings__corrective_action_description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_findings__description import \
    small_business_banking__regulatory_findings__description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_findings__finding_type import \
    small_business_banking__regulatory_findings__finding_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_findings__resolution_description import \
    small_business_banking__regulatory_findings__resolution_description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_findings__severity import \
    small_business_banking__regulatory_findings__severity
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_findings__source import \
    small_business_banking__regulatory_findings__source
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_findings__status import \
    small_business_banking__regulatory_findings__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_reports__notes import \
    small_business_banking__regulatory_reports__notes
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_reports__regulatory_agency import \
    small_business_banking__regulatory_reports__regulatory_agency
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_reports__report_type import \
    small_business_banking__regulatory_reports__report_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__regulatory_reports__status import \
    small_business_banking__regulatory_reports__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__report_submissions__response_status import \
    small_business_banking__report_submissions__response_status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__report_submissions__submission_method import \
    small_business_banking__report_submissions__submission_method
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__suspicious_activity_reports__law_enforcement_contact_name import \
    small_business_banking__suspicious_activity_reports__law_enforcement_contact_name
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__suspicious_activity_reports__other_description import \
    small_business_banking__suspicious_activity_reports__other_description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__suspicious_activity_reports__supporting_documentation import \
    small_business_banking__suspicious_activity_reports__supporting_documentation
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__suspicious_activity_reports__suspicious_activity_description import \
    small_business_banking__suspicious_activity_reports__suspicious_activity_description
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__suspicious_activity_reports__suspicious_activity_type import \
    small_business_banking__suspicious_activity_reports__suspicious_activity_type
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__transactions__status import \
    small_business_banking__transactions__status
from fsi_data_generator.fsi_text.small_business_banking.small_business_banking__transactions__transaction_type import \
    small_business_banking__transactions__transaction_type

fake = Faker()


def small_business_banking(dg):
    return [
        ('small_business_banking\\.suspicious_activity_reports', '^law_enforcement_contact_name$',
         text_list(small_business_banking__suspicious_activity_reports__law_enforcement_contact_name)),
        ('small_business_banking\\.beneficial_owner_verification', '^notes$',
         text_list(small_business_banking__beneficial_owner_verification__notes)),
        ('small_business_banking\\.beneficial_owner_verification', '^screening_results$',
         text_list(small_business_banking__beneficial_owner_verification__screening_results)),
        ('small_business_banking\\.beneficial_owner_verification', '^verification_method$',
         text_list(small_business_banking__beneficial_owner_verification__verification_method)),
        ('small_business_banking\\.business_due_diligence', '^notes$',
         text_list(small_business_banking__business_due_diligence__notes)),
        ('small_business_banking\\.business_due_diligence', '^site_visit_notes$',
         text_list(small_business_banking__business_due_diligence__site_visit_notes)),
        ('small_business_banking\\.business_due_diligence', '^screening_results$',
         text_list(small_business_banking__business_due_diligence__screening_results)),
        ('small_business_banking\\.business_due_diligence', '^expected_activity$',
         text_list(small_business_banking__business_due_diligence__expected_activity)),
        ('small_business_banking\\.business_due_diligence', '^high_risk_factors$',
         text_list(small_business_banking__business_due_diligence__high_risk_factors)),
        ('small_business_banking\\.adverse_action_notices', '^score_factors$',
         text_list(small_business_banking__adverse_action_notices__score_factors)),
        ('small_business_banking\\.adverse_action_notices', '^secondary_reasons$',
         text_list(small_business_banking__adverse_action_notices__secondary_reasons)),
        ('small_business_banking\\.adverse_action_notices', '^primary_reason$',
         text_list(small_business_banking__adverse_action_notices__primary_reason)),
        ('small_business_banking\\.credit_decisions', '^exception_reason$',
         text_list(small_business_banking__credit_decisions__exception_reason)),
        ('small_business_banking\\.credit_decisions', '^decision_factors$',
         text_list(small_business_banking__credit_decisions__decision_factors)),
        ('small_business_banking\\.loan_fair_lending', '^denial_reason_1$',
         text_list(small_business_banking__loan_fair_lending__denial_reason_1)),
        ('small_business_banking\\.loan_fair_lending', '^denial_reason_2$',
         text_list(small_business_banking__loan_fair_lending__denial_reason_2)),
        ('small_business_banking\\.loan_fair_lending', '^denial_reason_3$',
         text_list(small_business_banking__loan_fair_lending__denial_reason_3)),
        ('small_business_banking\\.loan_fair_lending', '^denial_reason_4$',
         text_list(small_business_banking__loan_fair_lending__denial_reason_4)),
        ('small_business_banking\\.credit_lines', '^credit_line_number$',
         lambda a, b, c: 'CL' + fake.unique.random_element(tuple(fake_product_codes))),
        ('small_business_banking\\.loans', '^loan_number$',
         lambda a, b, c: 'LN' + fake.unique.random_element(tuple(fake_product_codes))),
        ('small_business_banking\\.products', '^product_code$',
         lambda a, b, c: fake.unique.random_element(tuple(fake_product_codes))),
        ('small_business_banking\\.accounts', '^account_number$',
         lambda a, b, c: fake.unique.random_element(tuple(fake_account_numbers))),
        ('small_business_banking\\.businesses', '^tax_id$',
         lambda a, b, c: fake.unique.random_element(tuple(fake_eins))),
        ('small_business_banking\\.business_card_users', '^merchant_category_restrictions$',
         text_list(small_business_banking__business_card_users__merchant_category_restrictions)),
        ('small_business_banking\\.suspicious_activity_reports', '^supporting_documentation$',
         text_list(small_business_banking__suspicious_activity_reports__supporting_documentation)),
        ('small_business_banking\\.business_card_accounts', '^card_account_id$',
         lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['credit_cards.card_accounts']))),
        ('small_business_banking\\.loan_collateral', '^consumer_lending_collateral_id$',
         lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['small_business_banking\\.collateral']))),
        ('small_business_banking\\.business_card_users', '^enterprise_party_id$',
         lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['enterprise.parties']))),
        ('small_business_banking\\.business_owners', '^enterprise_party_id$',
         lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['enterprise.parties']))),
        ('small_business_banking\\.account_signatories', '^enterprise_party_id$',
         lambda a, b, c: fake.unique.random_element(tuple(dg.inserted_pks['enterprise.parties']))),
        ('small_business_banking\\.suspicious_activity_reports', '^other_description$',
         text_list(small_business_banking__suspicious_activity_reports__other_description)),
        ('small_business_banking\\.suspicious_activity_reports', '^suspicious_activity_description$',
         text_list(small_business_banking__suspicious_activity_reports__suspicious_activity_description)),
        ('small_business_banking\\.business_risk_assessments', '^recommended_actions$',
         text_list(small_business_banking__business_risk_assessments__recommended_actions)),
        ('small_business_banking\\.business_risk_assessments', '^mitigating_factors$',
         text_list(small_business_banking__business_risk_assessments__mitigating_factors)),
        ('small_business_banking\\.business_risk_assessments', '^rationale$',
         text_list(small_business_banking__business_risk_assessments__rationale)),
        ('small_business_banking\\.compliance_requirements', '^control_measures$',
         text_list(small_business_banking__compliance_requirements__control_measures)),
        ('small_business_banking\\.compliance_requirements', '^verification_procedure$',
         text_list(small_business_banking__compliance_requirements__verification_procedure)),
        ('small_business_banking\\.compliance_requirements', '^business_impact$',
         text_list(small_business_banking__compliance_requirements__business_impact)),
        ('small_business_banking\\.compliance_requirements', '^description$',
         text_list(small_business_banking__compliance_requirements__description)),
        ('small_business_banking\\.compliance_cases', '^escalation_reason$',
         text_list(small_business_banking__compliance_cases__escalation_reason)),
        ('small_business_banking\\.compliance_cases', '^resolution$',
         text_list(small_business_banking__compliance_cases__resolution)),
        ('small_business_banking\\.compliance_cases', '^description$',
         text_list(small_business_banking__compliance_cases__description)),
        ('small_business_banking\\.regulatory_findings', '^resolution_description$',
         text_list(small_business_banking__regulatory_findings__resolution_description)),
        ('small_business_banking\\.regulatory_findings', '^corrective_action_description$',
         text_list(small_business_banking__regulatory_findings__corrective_action_description)),
        ('small_business_banking\\.regulatory_findings', '^description$',
         text_list(small_business_banking__regulatory_findings__description)),
        ('small_business_banking\\.regulatory_reports', '^notes$',
         text_list(small_business_banking__regulatory_reports__notes)),
        ('small_business_banking\\.collateral', '^description$',
         text_list(small_business_banking__collateral__description)),
        ('small_business_banking\\.products', '^description$',
         text_list(small_business_banking__products__description)),
        ('small_business_banking\\.loans', '^purpose$',
         text_list(small_business_banking__loans__purpose)),
        ('small_business_banking\\.business_card_accounts', '^ownership_type$',
         text_list(small_business_banking__business_card_accounts__ownership_type)),
        ('small_business_banking\\.business_card_accounts', '^liability_type$',
         text_list(small_business_banking__business_card_accounts__liability_type)),
        ('small_business_banking\\.business_card_accounts', '^expense_category_setup$',
         text_list(small_business_banking__business_card_accounts__expense_category_setup)),
        ('small_business_banking\\.business_due_diligence', '^verification_method$',
         text_list(small_business_banking__business_due_diligence__verification_method)),
        ('small_business_banking\\.business_due_diligence', '^review_frequency$',
         text_list(small_business_banking__business_due_diligence__review_frequency)),
        ('small_business_banking\\.business_due_diligence', '^approval_status$',
         text_list(small_business_banking__business_due_diligence__approval_status)),
        ('small_business_banking\\.beneficial_owner_verification', '^id_type$',
         text_list(small_business_banking__beneficial_owner_verification__id_type)),
        ('small_business_banking\\.beneficial_owner_verification', '^verification_status$',
         text_list(small_business_banking__beneficial_owner_verification__verification_status)),
        ('small_business_banking\\.suspicious_activity_reports', '^suspicious_activity_type$',
         text_list(small_business_banking__suspicious_activity_reports__suspicious_activity_type)),
        ('small_business_banking\\.loan_fair_lending', '^loan_type$',
         text_list(small_business_banking__loan_fair_lending__loan_type)),
        ('small_business_banking\\.loan_fair_lending', '^action_taken$',
         text_list(small_business_banking__loan_fair_lending__action_taken)),
        ('small_business_banking\\.credit_decisions', '^product_type$',
         text_list(small_business_banking__products__product_type)),
        ('small_business_banking\\.business_due_diligence', '^risk_rating$',
         text_list(small_business_banking__business_due_diligence__risk_rating)),
        ('small_business_banking\\.business_due_diligence', '^diligence_type$',
         text_list(small_business_banking__business_due_diligence__diligence_type)),
        ('small_business_banking\\.credit_decisions', '^decision_type$',
         text_list(small_business_banking__credit_decisions__decision_type)),
        ('small_business_banking\\.credit_decisions', '^decision_outcome$',
         text_list(small_business_banking__credit_decisions__decision_outcome)),
        ('small_business_banking\\.adverse_action_notices', '^delivery_method$',
         text_list(small_business_banking__adverse_action_notices__delivery_method)),
        ('small_business_banking\\.compliance_cases', '^priority$',
         text_list(small_business_banking__compliance_cases__priority)),
        ('small_business_banking\\.compliance_cases', '^status$',
         text_list(small_business_banking__compliance_cases__status)),
        ('small_business_banking\\.compliance_cases', '^source$',
         text_list(small_business_banking__compliance_cases__source)),
        ('small_business_banking\\.compliance_requirements', '^regulatory_authority$',
         text_list(small_business_banking__regulatory_reports__regulatory_agency)),
        ('small_business_banking\\.compliance_requirements', '^verification_frequency$',
         text_list(small_business_banking__compliance_requirements__verification_frequency)),
        ('small_business_banking\\.\\business_risk_assessments', '^assessment_type$',
         text_list(small_business_banking__business_risk_assessments__assessment_type)),
        ('small_business_banking\\.business_risk_assessments', '^risk_rating$',
         text_list(small_business_banking__business_risk_assessments__risk_rating)),
        ('small_business_banking\\.regulatory_reports', '^report_type$',
         text_list(small_business_banking__regulatory_reports__report_type)),
        ('small_business_banking\\.regulatory_reports', '^status$',
         text_list(small_business_banking__regulatory_reports__status)),
        ('small_business_banking\\.regulatory_reports', '^regulatory_agency$',
         text_list(small_business_banking__regulatory_reports__regulatory_agency)),
        ('small_business_banking\\.report_submissions', '^submission_method$',
         text_list(small_business_banking__report_submissions__submission_method)),
        ('small_business_banking\\.report_submissions', '^response_status$',
         text_list(small_business_banking__report_submissions__response_status)),
        ('small_business_banking\\.regulatory_findings', '^source$',
         text_list(small_business_banking__regulatory_findings__source)),
        ('small_business_banking\\.regulatory_findings', '^finding_type$',
         text_list(small_business_banking__regulatory_findings__finding_type)),
        ('small_business_banking\\.regulatory_findings', '^severity$',
         text_list(small_business_banking__regulatory_findings__severity)),
        ('small_business_banking\\.regulatory_findings', '^status$',
         text_list(small_business_banking__regulatory_findings__status)),
        ('small_business_banking\\.compliance_cases', '^case_type$',
         text_list(small_business_banking__compliance_cases__case_type)),
        ('small_business_banking\\.transactions', '^transaction_type$',
         text_list(small_business_banking__transactions__transaction_type)),
        ('small_business_banking\\.transactions', '^status$', text_list(small_business_banking__transactions__status)),
        ('small_business_banking\\.payments', '^payment_method$',
         text_list(small_business_banking__payments__payment_method)),
        ('small_business_banking\\.payments', '^payment_type$',
         text_list(small_business_banking__payments__payment_type)),
        ('small_business_banking\\.payments', '^status$', text_list(small_business_banking__payments__status)),
        ('small_business_banking\\.documents', '^document_type$',
         text_list(small_business_banking__documents__document_type)),
        ('small_business_banking\\.documents', '^status$', text_list(small_business_banking__documents__status)),
        ('small_business_banking\\.credit_lines', '^status$',
         text_list(small_business_banking__credit_lines__status, lower=True)),
        ('small_business_banking\\.collateral', '^collateral_type$',
         text_list(small_business_banking__collateral__collateral_type, lower=True)),
        ('small_business_banking\\.collateral', '^valuation_type$',
         text_list(small_business_banking__collateral__valuation_type, lower=True)),
        ('small_business_banking\\.collateral', '^status$',
         text_list(small_business_banking__collateral__status, lower=True)),
        ('small_business_banking\\.business_card_accounts', '^account_type$',
         text_list(small_business_banking__business_card_accounts__account_type, lower=True)),
        ('small_business_banking\\.business_card_accounts', '^business_structure$',
         text_list(small_business_banking__businesses__business_type, lower=True)),
        ('small_business_banking\\.business_card_accounts', '^ownership_type$',
         text_list(small_business_banking__business_card_accounts__ownership_type, lower=True)),
        ('small_business_banking\\.business_card_accounts', '^liability_type$',
         text_list(small_business_banking__business_card_accounts__liability_type, lower=True)),
        ('small_business_banking\\.business_card_accounts', '^expense_category_setup$',
         text_list(small_business_banking__business_card_accounts__expense_category_setup, lower=True)),
        ('small_business_banking\\.business_card_users', '^role$',
         text_list(small_business_banking__business_card_users__role, lower=True)),
        ('small_business_banking\\.accounts', '^account_type$',
         text_list(small_business_banking__accounts__account_type)),
        ('small_business_banking\\.accounts', '^status$',
         text_list(small_business_banking__accounts__status, lower=True)),
        ('small_business_banking\\.accounts', '^statement_frequency$',
         text_list(small_business_banking__accounts__statement_frequency, lower=True)),
        ('small_business_banking\\.products', '^product_type$',
         text_list(small_business_banking__products__product_type, lower=True)),
        ('small_business_banking\\.account_signatories', '^signatory_level$',
         text_list(small_business_banking__account_signatories__signatory_level, lower=True)),
        ('small_business_banking\\.loans', '^interest_type$',
         text_list(small_business_banking__loans__interest_type, lower=True)),
        ('small_business_banking\\.loans', '^payment_frequency$',
         text_list(small_business_banking__loans__payment_frequency, lower=True)),
        ('small_business_banking\\.loans', '^status$', text_list(small_business_banking__loans__status, lower=True)),
        ('small_business_banking\\.credit_lines', '^interest_type$',
         text_list(small_business_banking__credit_lines__interest_type, lower=True)),
        ('small_business_banking\\.businesses', '^business_type$',
         text_list(small_business_banking__businesses__business_type, lower=True)),
        ('small_business_banking\\.businesses', '^status$',
         text_list(small_business_banking__businesses__status, lower=True)),
        ('small_business_banking\\.business_owners', '^role$',
         text_list(small_business_banking__business_owners__role, lower=True)),
        ('small_business_banking\\.accounts', '^account_type$',
         text_list(small_business_banking__accounts__account_type, lower=True)),
        ('small_business_banking\\.accounts', '^status$',
         text_list(small_business_banking__accounts__status, lower=True)),
        ('small_business_banking\\.accounts', '^statement_frequency$',
         text_list(small_business_banking__accounts__statement_frequency, lower=True)),
    ]
