from faker import Faker

from fsi_data_generator.fsi_generators.helpers.text_list import text_list
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__closing__appointments_notes import \
    mortgage_services__closing__appointments_notes
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__closing_appointments__notes import \
    mortgage_services__closing_appointments__notes
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__conditions__description import \
    mortgage_services__conditions__description
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__content import \
    mortgage_services__customer_communications__content
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__documents__notes import \
    mortgage_services__documents__notes
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_application_demographics__ethnicity_free_form import \
    mortgage_services__hmda_application_demographics__ethnicity_free_form
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_application_demographics__ethnicity_observed import \
    mortgage_services__hmda_application_demographics__ethnicity_observed
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_application_demographics__race_free_form import \
    mortgage_services__hmda_application_demographics__race_free_form
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_application_demographics__race_observed import \
    mortgage_services__hmda_application_demographics__race_observed
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_application_demographics__sex import \
    mortgage_services__hmda_application_demographics__sex
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_application_demographics__sex_observed import \
    mortgage_services__hmda_application_demographics__sex_observed
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_edits__edit_description import \
    mortgage_services__hmda_edits__edit_description
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_edits__resolution_notes import \
    mortgage_services__hmda_edits__resolution_notes
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_submissions__submission_notes import \
    mortgage_services__hmda_submissions__submission_notes
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_modifications__reason import \
    mortgage_services__loan_modifications__reason
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_products__description import \
    mortgage_services__loan_products__description
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__applications__loan_purpose import \
    mortgage_services__applications__loan_purpose
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__applications__status import \
    mortgage_services__applications__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__applications__referral_source import \
    mortgage_services__applications__referral_source
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__applications__application_type import \
    mortgage_services__applications__application_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_service__application_borrowers__relationship_to_primary import \
    mortgage_service__application_borrowers__relationship_to_primary
from fsi_data_generator.fsi_text.mortgage_services.mortgage_service__application_borrowers__borrower_type import \
    mortgage_service__application_borrowers__borrower_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__borrower_citizenships__citizenship_status import \
    mortgage_services__borrower_citizenships__citizenship_status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__borrower_incomes__verification_status import \
    mortgage_services__borrower_incomes__verification_status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__borrower_incomes__frequency import \
    mortgage_services__borrower_incomes__frequency
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__borrower_employments__employment_type import \
    mortgage_services__borrower_employments__employment_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__borrower_incomes__income_type import \
    mortgage_services__borrower_incomes__income_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__borrower_assets__verification_status import \
    mortgage_services__borrower_assets__verification_status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__borrower_assets__asset_type import \
    mortgage_services__borrower_assets__asset_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__borrower_liabilities__liability_type import \
    mortgage_services__borrower_liabilities__liability_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__properties__occupancy_type import \
    mortgage_services__properties__occupancy_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__properties__property_type import \
    mortgage_services__properties__property_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_products__interest_rate_type import \
    mortgage_services__loan_products__interest_rate_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_products__loan_type import \
    mortgage_services__loan_products__loan_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_rate_locks__status import \
    mortgage_services__loan_rate_locks__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__documents__status import \
    mortgage_services__documents__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__documents__document_type import \
    mortgage_services__documents__document_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__conditions__status import \
    mortgage_services__conditions__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__conditions__condition_type import \
    mortgage_services__conditions__condition_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__appraisals__status import \
    mortgage_services__appraisals__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__appraisals__appraisal_type import \
    mortgage_services__appraisals__appraisal_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__credit_reports__status import \
    mortgage_services__credit_reports__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__credit_reports__report_type import \
    mortgage_services__credit_reports__report_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__closing_disclosures__disclosure_type import \
    mortgage_services__closing_disclosures__disclosure_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__closing_appointments__status import \
    mortgage_services__closing_appointments__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__servicing_accounts__status import \
    mortgage_services__servicing_accounts__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__payments__payment_type import \
    mortgage_services__payments__payment_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__payments__status import \
    mortgage_services__payments__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__payments__payment_method import \
    mortgage_services__payments__payment_method
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__escrow_disbursements__status import \
    mortgage_services__escrow_disbursements__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__escrow_disbursements__disbursement_type import \
    mortgage_services__escrow_disbursements__disbursement_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__escrow_analyses__status import \
    mortgage_services__escrow_analyses__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__insurance_policies__status import \
    mortgage_services__insurance_policies__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__insurance_policies__insurance_type import \
    mortgage_services__insurance_policies__insurance_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_modification__status import \
    mortgage_services__loan_modification__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__loan_modification__modification_type import \
    mortgage_services__loan_modification__modification_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__related_to import \
    mortgage_services__customer_communications__related_to
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__status import \
    mortgage_services__customer_communications__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__direction import \
    mortgage_services__customer_communications__direction
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__customer_communications__communication_type import \
    mortgage_services__customer_communications__communication_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__edit_status import \
    mortgage_services__hmda_records__edit_status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__submission_status import \
    mortgage_services__hmda_records__submission_status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__aus1 import \
    mortgage_services__hmda_records__aus1
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__yes_no import \
    mortgage_services__hmda_records__yes_no
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__submission_of_application import \
    mortgage_services__hmda_records__submission_of_application
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__manufactured_home_land_property_interest import \
    mortgage_services__hmda_records__manufactured_home_land_property_interest
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__manufactured_home_secured_property_type import \
    mortgage_services__hmda_records__manufactured_home_secured_property_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__denial_reason1 import \
    mortgage_services__hmda_records__denial_reason1
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__credit_score_model import \
    mortgage_services__hmda_records__credit_score_model
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__action_taken import \
    mortgage_services__hmda_records__action_taken
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__occupancy_type import \
    mortgage_services__hmda_records__occupancy_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__construction_method import \
    mortgage_services__hmda_records__construction_method
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__loan_purpose import \
    mortgage_services__hmda_records__loan_purpose
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_records__loan_type import \
    mortgage_services__hmda_records__loan_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__sex_observed import \
    mortgage_services__hmda_applicant_demographics__sex_observed
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__sex import \
    mortgage_services__hmda_applicant_demographics__sex
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__race_observed import \
    mortgage_services__hmda_applicant_demographics__race_observed
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__race_4 import \
    mortgage_services__hmda_applicant_demographics__race_4
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__race_3 import \
    mortgage_services__hmda_applicant_demographics__race_3
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__race_2 import \
    mortgage_services__hmda_applicant_demographics__race_2
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__race_1 import \
    mortgage_services__hmda_applicant_demographics__race_1
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__ethnicity_observed import \
    mortgage_services__hmda_applicant_demographics__ethnicity_observed
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__ethnicity_3 import \
    mortgage_services__hmda_applicant_demographics__ethnicity_3
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__ethnicity_2 import \
    mortgage_services__hmda_applicant_demographics__ethnicity_2
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__ethnicity_1 import \
    mortgage_services__hmda_applicant_demographics__ethnicity_1
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_applicant_demographics__applicant_type import \
    mortgage_services__hmda_applicant_demographics__applicant_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_edits__status import \
    mortgage_services__hmda_edits__status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_edits__edit_type import \
    mortgage_services__hmda_edits__edit_type
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_submissions__submission_status import \
    mortgage_services__hmda_submissions__submission_status
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__hmda_submissions__reporting_period import \
    mortgage_services__hmda_submissions__reporting_period

fake = Faker()


def mortgage_services(_dg):
    return [
        ('mortgage_services\\.hmda_submissions', '^submission_notes$', text_list(
            mortgage_services__hmda_submissions__submission_notes)),
        ('mortgage_services\\.hmda_submissions', '^reporting_period$',
         text_list(mortgage_services__hmda_submissions__reporting_period, lower=True)),
        ('mortgage_services\\.hmda_submissions', '^submission_status$',
         text_list(mortgage_services__hmda_submissions__submission_status, lower=True)),
        ('mortgage_services\\.hmda_edits', '^resolution_notes$',
         text_list(mortgage_services__hmda_edits__resolution_notes)),
        ('mortgage_services\\.hmda_edits', '^edit_type$',
         text_list(mortgage_services__hmda_edits__edit_type, lower=True)),
        ('mortgage_services\\.hmda_edits', '^status$', text_list(mortgage_services__hmda_edits__status, lower=True)),
        ('mortgage_services\\.hmda_applicant_demographics', '^applicant_type$',
         text_list(mortgage_services__hmda_applicant_demographics__applicant_type, lower=True)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_1$',
         text_list(mortgage_services__hmda_applicant_demographics__ethnicity_1)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_2$',
         text_list(mortgage_services__hmda_applicant_demographics__ethnicity_2)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_3$',
         text_list(mortgage_services__hmda_applicant_demographics__ethnicity_3)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_4$',
         text_list(mortgage_services__hmda_applicant_demographics__ethnicity_3)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_5$',
         text_list(mortgage_services__hmda_applicant_demographics__ethnicity_3)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_observed$',
         text_list(mortgage_services__hmda_applicant_demographics__ethnicity_observed, lower=True)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_1$',
         text_list(mortgage_services__hmda_applicant_demographics__race_1)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_2$',
         text_list(mortgage_services__hmda_applicant_demographics__race_2)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_3$',
         text_list(mortgage_services__hmda_applicant_demographics__race_3)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_4$',
         text_list(mortgage_services__hmda_applicant_demographics__race_4)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_5$',
         text_list(mortgage_services__hmda_applicant_demographics__race_4)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_observed$',
         text_list(mortgage_services__hmda_applicant_demographics__race_observed)),
        ('mortgage_services\\.hmda_applicant_demographics', '^sex$',
         text_list(mortgage_services__hmda_applicant_demographics__sex)),
        ('mortgage_services\\.hmda_applicant_demographics', '^sex_observed$',
         text_list(mortgage_services__hmda_applicant_demographics__sex_observed)),
        ('mortgage_services\\.hmda_records', '^loan_type$',
         text_list(mortgage_services__hmda_records__loan_type, lower=True)),
        ('mortgage_services\\.hmda_records', '^loan_purpose$',
         text_list(mortgage_services__hmda_records__loan_purpose, lower=True)),
        ('mortgage_services\\.hmda_records', '^construction_method$',
         text_list(mortgage_services__hmda_records__construction_method, lower=True)),
        ('mortgage_services\\.hmda_records', '^occupancy_type$',
         text_list(mortgage_services__hmda_records__occupancy_type, lower=True)),
        ('mortgage_services\\.hmda_records', '^action_taken$',
         text_list(mortgage_services__hmda_records__action_taken, lower=True)),
        ('mortgage_services\\.hmda_records', '^hoepa_status$', text_list([
            1, 2
        ])),
        ('mortgage_services\\.hmda_records', '^lien_status$', text_list([
            1, 2
        ])),
        ('mortgage_services\\.hmda_records', '^credit_score_model$',
         text_list(mortgage_services__hmda_records__credit_score_model)),
        ('mortgage_services\\.hmda_records', '^denial_reason(1|2|3|4)$',
         text_list(mortgage_services__hmda_records__denial_reason1, lower=True)),
        ('mortgage_services\\.hmda_records', 'manufactured_home_secured_property_type',
         text_list(mortgage_services__hmda_records__manufactured_home_secured_property_type, lower=True)),
        ('mortgage_services\\.hmda_records', 'manufactured_home_land_property_interest',
         text_list(mortgage_services__hmda_records__manufactured_home_land_property_interest, lower=True)),
        ('mortgage_services\\.hmda_records', '^submission_of_application$',
         text_list(mortgage_services__hmda_records__submission_of_application, lower=True)),
        ('mortgage_services\\.hmda_records',
         '^reverse_mortgage|business_or_commercial_purpose|initially_payable_to_institution|preapproval|negative_amortization|other_non_amortizing_features|balloon_payment|interest_only_payment|initially_payable_to_institution|reverse_mortgage|open_end_line_of_credit$',
         text_list(mortgage_services__hmda_records__yes_no, lower=True)),
        ('mortgage_services\\.hmda_records', '^aus(1|2|3|4|5)$', text_list(mortgage_services__hmda_records__aus1)),
        ('mortgage_services\\.hmda_records', '^submission_status$',
         text_list(mortgage_services__hmda_records__submission_status, lower=True)),
        ('mortgage_services\\.hmda_records', '^edit_status$',
         text_list(mortgage_services__hmda_records__edit_status, lower=True)),
        ('mortgage_services\\.customer_communications', '^communication_type$',
         text_list(mortgage_services__customer_communications__communication_type)),
        ('mortgage_services\\.customer_communications', '^direction$',
         text_list(mortgage_services__customer_communications__direction, lower=True)),
        ('mortgage_services\\.customer_communications', '^status$',
         text_list(mortgage_services__customer_communications__status, lower=True)),
        ('mortgage_services\\.customer_communications', '^related_to$',
         text_list(mortgage_services__customer_communications__related_to, lower=True)),
        ('mortgage_services\\.loan_modification', '^modification_type$',
         text_list(mortgage_services__loan_modification__modification_type, lower=True)),
        ('mortgage_services\\.loan_modification', '^reason$', text_list(
            mortgage_services__loan_modifications__reason)),
        ('mortgage_services\\.loan_modification', '^status$',
         text_list(mortgage_services__loan_modification__status, lower=True)),
        ('mortgage_services\\.insurance_policies', '^insurance_type$',
         text_list(mortgage_services__insurance_policies__insurance_type, lower=True)),
        ('mortgage_services\\.insurance_policies', '^agent_name$', lambda a, b, c: fake.name()),
        ('mortgage_services\\.insurance_policies', '^carrier_name$', lambda a, b, c: fake.company()),
        ('mortgage_services\\.insurance_policies', '^status$',
         text_list(mortgage_services__insurance_policies__status, lower=True)),
        ('mortgage_services\\.escrow_analyses', '^status$',
         text_list(mortgage_services__escrow_analyses__status, lower=True)),
        ('mortgage_services\\.escrow_disbursements', '^disbursement_type$',
         text_list(mortgage_services__escrow_disbursements__disbursement_type)),
        ('mortgage_services\\.escrow_disbursements', '^status$',
         text_list(mortgage_services__escrow_disbursements__status, lower=True)),
        ('mortgage_services\\.payments', '^payment_method$', text_list(mortgage_services__payments__payment_method)),
        ('mortgage_services\\.payments', '^status$', text_list(mortgage_services__payments__status, lower=True)),
        ('mortgage_services\\.payments', '^payment_type$',
         text_list(mortgage_services__payments__payment_type, lower=True)),
        ('mortgage_services\\.servicing_accounts', '^status$',
         text_list(mortgage_services__servicing_accounts__status, lower=True)),
        ('mortgage_services\\.closed_loans', '^settlement_agent$', lambda a, b, c: fake.name()),
        ('mortgage_services\\.closed_loans', '^settlement_company$', lambda a, b, c: fake.company()),
        ('mortgage_services\\.closing_appointments', '^notes$',
         text_list(mortgage_services__closing__appointments_notes)),
        ('.*', '^closing_agent$', lambda a, b, c: fake.name()),
        ('.*', '^closing_company$', lambda a, b, c: fake.company()),
        ('mortgage_services\\.closing_appointments', '^status$',
         text_list(mortgage_services__closing_appointments__status, lower=True)),
        ('mortgage_services\\.closing_disclosures', '^disclosure_type$',
         text_list(mortgage_services__closing_disclosures__disclosure_type, lower=True)),
        ('mortgage_services\\.credit_reports', '^report_type$',
         text_list(mortgage_services__credit_reports__report_type, lower=True)),
        ('mortgage_services\\.credit_reports', '^status$',
         text_list(mortgage_services__credit_reports__status, lower=True)),
        ('mortgage_services\\.appraisals', '^appraisal_type$',
         text_list(mortgage_services__appraisals__appraisal_type, lower=True)),
        ('mortgage_services\\.appraisals', '^appraiser_name$', lambda a, b, c: fake.name()),
        ('mortgage_services\\.(appraisals|credit_reports)', '^report_path$', lambda a, b, c: fake.file_path()),
        ('mortgage_services\\.appraisals', '^appraisal_company$', lambda a, b, c: fake.company()),
        ('mortgage_services\\.appraisals', '^status$', text_list(mortgage_services__appraisals__status, lower=True)),
        ('mortgage_services\\.conditions', '^condition_type$',
         text_list(mortgage_services__conditions__condition_type, lower=True)),
        ('mortgage_services\\.conditions', '^status$', text_list(mortgage_services__conditions__status, lower=True)),
        ('.*', '^document_name$', lambda a, b, c: fake.file_name()),
        ('.*', '^.*_path$', lambda a, b, c: fake.file_path()),
        ('mortgage_services\\.documents', '^document_type$', text_list(mortgage_services__documents__document_type)),
        ('mortgage_services\\.documents', '^status$', text_list(mortgage_services__documents__status, lower=True)),
        ('mortgage_services\\.loan_rate_locks', '^status$',
         text_list(mortgage_services__loan_rate_locks__status, lower=True)),
        ('mortgage_services\\.loan_products', '^loan_type$', text_list(mortgage_services__loan_products__loan_type)),
        ('mortgage_services\\.loans', '^loan_type$', text_list(mortgage_services__loan_products__loan_type)),
        ('mortgage_services\\.loan_products', '^interest_rate_type$',
         text_list(mortgage_services__loan_products__interest_rate_type, lower=True)),
        ('mortgage_services\\.properties', '^property_type$',
         text_list(mortgage_services__properties__property_type, lower=True)),
        ('mortgage_services\\.properties', '^occupancy_type$',
         text_list(mortgage_services__properties__occupancy_type, lower=True)),
        ('mortgage_services\\.borrower_liabilities', '^liability_type$',
         text_list(mortgage_services__borrower_liabilities__liability_type, lower=True)),
        ('.*', '^asset_type$', text_list(mortgage_services__borrower_assets__asset_type)),
        ('mortgage_services\\.borrower_(assets|liabilities)', '^verification_status$',
         text_list(mortgage_services__borrower_assets__verification_status, lower=True)),
        ('.*', '^income_type$', text_list(mortgage_services__borrower_incomes__income_type, lower=True)),
        ('.*', '^employment_type$', text_list(mortgage_services__borrower_employments__employment_type, lower=True)),
        ('mortgage_services\\.borrower_incomes', '^frequency$',
         text_list(mortgage_services__borrower_incomes__frequency, lower=True)),
        ('mortgage_services\\.borrower_incomes', '^verification_status$',
         text_list(mortgage_services__borrower_incomes__verification_status, lower=True)),
        ('.*', '^citizenship_status$', text_list(mortgage_services__borrower_citizenships__citizenship_status)),
        ('mortgage_service.application_borrowers', '^borrower_type$',
         text_list(mortgage_service__application_borrowers__borrower_type, lower=True)),
        (
            'mortgage_service.application_borrowers', '^relationship_to_primary$',
            text_list(mortgage_service__application_borrowers__relationship_to_primary, lower=True)),
        ('mortgage_services\\.applications', '^application_type$',
         text_list(mortgage_services__applications__application_type)),
        ('.*', '^referral_source$', text_list(mortgage_services__applications__referral_source, lower=True)),
        (
        'mortgage_services\\.applications', '^status$', text_list(mortgage_services__applications__status, lower=True)),
        ('mortgage_services\\.applications', '^loan_purpose$',
         text_list(mortgage_services__applications__loan_purpose, lower=True)),
        ('mortgage_services\\.hmda_edits', '^edit_description$',
         text_list(mortgage_services__hmda_edits__edit_description)),
        ('mortgage_services\\.hmda_applicant_demographics', '^sex_observed$',
         text_list(mortgage_services__hmda_application_demographics__sex_observed)),
        ('mortgage_services\\.hmda_applicant_demographics', '^sex$',
         text_list(mortgage_services__hmda_application_demographics__sex)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_observed$',
         text_list(mortgage_services__hmda_application_demographics__race_observed)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_free_form$',
         text_list(mortgage_services__hmda_application_demographics__race_free_form)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_free_form$',
         text_list(mortgage_services__hmda_application_demographics__ethnicity_free_form)),
        ('mortgage_services\\.hmda_applicant_demographics', 'ethnicity_observed',
         text_list(mortgage_services__hmda_application_demographics__ethnicity_observed)),
        ('mortgage_services\\.customer_communications', '^content$',
         text_list(mortgage_services__customer_communications__content)),
        ('mortgage_services\\.closing_appointments', '^notes$',
         text_list(mortgage_services__closing_appointments__notes)),
        ('mortgage_services\\.conditions', '^description$', text_list(mortgage_services__conditions__description)),
        ('mortgage_services\\.documents', '^notes$', text_list(mortgage_services__documents__notes)),
        (
        'mortgage_services\\.loan_products', '^description$', text_list(mortgage_services__loan_products__description)),
    ]
