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
from fsi_data_generator.fsi_text.mortgage_services.mortgage_services__documents__notes import mortgage_services__documents__notes
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

fake = Faker()

mortgage_services__hmda_submissions__reporting_period = ['annual', 'quarterly_q1', 'quarterly_q2', 'quarterly_q3']
mortgage_services__hmda_submissions__submission_status = ['pending', 'submitted', 'accepted', 'rejected', 'processing', 'completed', 'error']
mortgage_services__hmda_edits__resolution_notes = mortgage_services__hmda_edits__resolution_notes
mortgage_services__hmda_edits__edit_type = ['syntactical', 'validity', 'quality', 'macro']
mortgage_services__hmda_edits__status = ['open', 'verified', 'corrected']
mortgage_services__hmda_applicant_demographics__applicant_type = ['primary applicant', 'co-applicant']
mortgage_services__hmda_applicant_demographics__ethnicity_1 = ['Hispanic or Latino', 'Not Hispanic or Latino', 'Information not provided by applicant in mail, Internet, or telephone application', 'Not applicable']
mortgage_services__hmda_applicant_demographics__ethnicity_2 = ['Mexican', 'Puerto Rican', 'Cuban', 'Other Hispanic or Latino', 'Information not provided by applicant in mail, Internet, or telephone application', 'Not applicable']
mortgage_services__hmda_applicant_demographics__ethnicity_3 = ['Information not provided by applicant in mail, Internet, or telephone application', 'Not applicable']
mortgage_services__hmda_applicant_demographics__ethnicity_observed = ['Not applicable', 'Collected on the basis of visual observation or surname']
mortgage_services__hmda_applicant_demographics__race_1 = ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Native Hawaiian or Other Pacific Islander', 'White', 'Information not provided by applicant in mail, Internet, or telephone application', 'Not applicable']
mortgage_services__hmda_applicant_demographics__race_2 = ['Asian Indian', 'Chinese', 'Filipino', 'Japanese', 'Korean', 'Vietnamese', 'Other Asian', 'Information not provided by applicant in mail, Internet, or telephone application', 'Not applicable']
mortgage_services__hmda_applicant_demographics__race_3 = ['Native Hawaiian', 'Guamanian or Chamorro', 'Samoan', 'Other Pacific Islander', 'Information not provided by applicant in mail, Internet, or telephone application', 'Not applicable']
mortgage_services__hmda_applicant_demographics__race_4 = ['Information not provided by applicant in mail, Internet, or telephone application', 'Not applicable']
mortgage_services__hmda_applicant_demographics__race_observed = ['Not applicable', 'Collected on the basis of visual observation or surname']
mortgage_services__hmda_applicant_demographics__sex = ['Male', 'Female', 'Information not provided by applicant in mail, Internet, or telephone application', 'Not applicable']
mortgage_services__hmda_applicant_demographics__sex_observed = ['Not applicable', 'Collected on the basis of visual observation or surname']
mortgage_services__hmda_records__loan_type = ['Conventional', 'FHA', 'VA', 'USDA']
mortgage_services__hmda_records__loan_purpose = ['home purchase', 'home improvement', 'refinancing', 'cash-out refinancing', 'other purpose']
mortgage_services__hmda_records__construction_method = ['site-built', 'manufactured']
mortgage_services__hmda_records__occupancy_type = ['primary', 'secondary', 'investment']
mortgage_services__hmda_records__action_taken = ['originated', 'approved not accepted', 'denied', 'withdrawn by applicant', 'incomplete', 'preapproval request denied', 'preapproval request approved but not accepted']
mortgage_services__hmda_records__hoepa_status = [1, 2]
mortgage_services__hmda_records__lien_status = [1, 2]
mortgage_services__hmda_records__credit_score_model = ['Equifax Beacon 5.0', 'Experian/Fair Isaac Risk Model V2SM', 'TransUnion FICO Risk Score Classic 04', 'VantageScore 3.0']
mortgage_services__hmda_records__denial_reason1 = ['debt-to-income ratio', 'credit history', 'collateral', 'insufficient cash', 'unverifiable information', 'credit application incomplete', 'mortgage insurance denied', 'other']
mortgage_services__hmda_records__denial_reason2 = ['debt-to-income ratio', 'credit history', 'collateral', 'insufficient cash', 'unverifiable information', 'credit application incomplete', 'mortgage insurance denied', 'other']
mortgage_services__hmda_records__denial_reason3 = ['debt-to-income ratio', 'credit history', 'collateral', 'insufficient cash', 'unverifiable information', 'credit application incomplete', 'mortgage insurance denied', 'other']
mortgage_services__hmda_records__denial_reason4 = ['debt-to-income ratio', 'credit history', 'collateral', 'insufficient cash', 'unverifiable information', 'credit application incomplete', 'mortgage insurance denied', 'other']
mortgage_services__hmda_records__manufactured_home_secured_property_type = ['single-wide', 'double-wide', 'triple-wide', 'multi-wide']
mortgage_services__hmda_records__manufactured_home_land_property_interest = ['owned', 'leased', 'land contract']
mortgage_services__hmda_records__submission_of_application = ['direct', 'not direct']
mortgage_services__hmda_records__reverse_mortgage = ['yes', 'no']
mortgage_services__hmda_records__business_or_commercial_purpose = ['yes', 'no']
mortgage_services__hmda_records__initially_payable_to_institution = ['yes', 'no']
mortgage_services__hmda_records__preapproval = ['yes', 'no']
mortgage_services__hmda_records__negative_amortization = ['yes', 'no']
mortgage_services__hmda_records__other_non_amortizing_features = ['yes', 'no']
mortgage_services__hmda_records__balloon_payment = ['yes', 'no']
mortgage_services__hmda_records__interest_only_payment = ['yes', 'no']
mortgage_services__hmda_records__aus1 = ['Desktop Underwriter (DU)', 'Loan Prospector (LP)', 'Technology Open to Approved Lenders (TOTAL) Scorecard', 'Guaranteed Underwriting System (GUS)']
mortgage_services__hmda_records__aus2 = ['Desktop Underwriter (DU)', 'Loan Prospector (LP)', 'Technology Open to Approved Lenders (TOTAL) Scorecard', 'Guaranteed Underwriting System (GUS)']
mortgage_services__hmda_records__aus3 = ['Desktop Underwriter (DU)', 'Loan Prospector (LP)', 'Technology Open to Approved Lenders (TOTAL) Scorecard', 'Guaranteed Underwriting System (GUS)']
mortgage_services__hmda_records__aus4 = ['Desktop Underwriter (DU)', 'Loan Prospector (LP)', 'Technology Open to Approved Lenders (TOTAL) Scorecard', 'Guaranteed Underwriting System (GUS)']
mortgage_services__hmda_records__aus5 = ['Desktop Underwriter (DU)', 'Loan Prospector (LP)', 'Technology Open to Approved Lenders (TOTAL) Scorecard', 'Guaranteed Underwriting System (GUS)']
mortgage_services__hmda_records__submission_status = ['pending', 'submitted', 'accepted', 'rejected']
mortgage_services__hmda_records__edit_status = ['not_started', 'in_progress', 'completed', 'failed']
mortgage_services__customer_communications__communication_type = ['email', 'letter', 'phone', 'SMS', 'in person', 'secure message', 'fax']
mortgage_services__customer_communications__direction = ['incoming', 'outgoing']
mortgage_services__customer_communications__status = ['sent', 'delivered', 'opened', 'clicked', 'bounced', 'failed', 'draft', 'scheduled']
mortgage_services__customer_communications__related_to = ['application status', 'document request', 'payment reminder', 'escrow analysis', 'loan modification', 'insurance information', 'tax information', 'general inquiry', 'complaint', 'other']
mortgage_services__loan_modification__modification_type = ['rate reduction', 'term extension', 'principal reduction', 'payment reduction', 'forbearance plan', 'other']
mortgage_services__loan_modification__reason = mortgage_services__loan_modifications__reason
mortgage_services__loan_modification__status = ['requested', 'under review', 'approved', 'denied', 'completed', 'cancelled']
mortgage_services__insurance_policies__insurance_type = ['hazard', 'flood', 'windstorm', 'earthquake', 'liability', 'other']
mortgage_services__insurance_policies__status = ['active', 'expired', 'cancelled', 'pending renewal', 'lapsed']
mortgage_services__escrow_analyses__status = ['completed', 'pending review', 'approved', 'implemented', 'cancelled']
mortgage_services__escrow_disbursements__disbursement_type = ['property tax', 'homeowners insurance', 'mortgage insurance (PMI)', 'flood insurance', 'HOA fees', 'other']
mortgage_services__escrow_disbursements__status = ['pending', 'processed', 'cleared', 'failed', 'cancelled']
mortgage_services__payments__payment_method = ['ACH', 'check', 'online', 'phone', 'wire transfer', 'money order', 'in person']
mortgage_services__payments__status = ['pending', 'completed', 'failed', 'returned', 'cancelled', 'processing']
mortgage_services__payments__payment_type = ['regular', 'extra principal', 'escrow only', 'payoff', 'reinstatement', 'forbearance payment']
mortgage_services__servicing_accounts__status = ['active', 'paid off', 'delinquent', 'foreclosure', 'default', 'bankruptcy', 'forbearance', 'modification', 'transferred']
mortgage_services__closing_appointments__status = ['scheduled', 'rescheduled', 'completed', 'cancelled', 'pending']
mortgage_services__closing_disclosures__disclosure_type = ['closing disclosure', 'loan estimate', 'initial escrow statement', 'servicing transfer disclosure']
mortgage_services__credit_reports__report_type = ['single bureau', 'tri-merge']
mortgage_services__credit_reports__status = ['pulled', 'reviewed', 'expired', 'error']
mortgage_services__appraisals__appraisal_type = ['full appraisal', 'drive-by appraisal', 'desktop appraisal', 'hybrid appraisal']
mortgage_services__appraisals__status = ['ordered', 'scheduled', 'inspected', 'completed', 'reviewed', 'challenged', 'cancelled']
mortgage_services__conditions__condition_type = ['prior to approval', 'prior to closing', 'post closing']
mortgage_services__conditions__status = ['pending', 'cleared', 'waived', 'overdue', 'rejected']
mortgage_services__documents__document_type = ['W2', 'tax return', 'pay stub', 'bank statement', "driver's license", 'social security card', 'proof of residency', 'purchase agreement', 'appraisal', 'title report', 'insurance policy', 'gift letter', 'asset statement', 'liability statement', 'other']
mortgage_services__documents__status = ['uploaded', 'pending review', 'approved', 'rejected', 'requested', 'expired']
mortgage_services__loan_rate_locks__status = ['active', 'expired', 'extended', 'cancelled', 'completed']
mortgage_services__loan_products__loan_type = ['conventional', 'FHA', 'VA', 'USDA', 'jumbo', 'HELOC', 'reverse mortgage', 'construction loan']
mortgage_services__loans__loan_type = ['conventional', 'FHA', 'VA', 'USDA', 'jumbo', 'HELOC', 'reverse mortgage', 'construction loan']
mortgage_services__loans__interest_rate_type = ['fixed', 'adjustable']
mortgage_services__loan_products__interest_rate_type = ['fixed', 'adjustable']
mortgage_services__properties__property_type = ['single family', 'condominium', 'townhouse', 'multi-family', 'manufactured home', 'cooperative', 'other']
mortgage_services__properties__occupancy_type = ['primary residence', 'second home', 'investment property']
mortgage_services__borrower_liabilities__liability_type = ['credit card', 'auto loan', 'student loan', 'personal loan', 'mortgage', 'child support', 'alimony', 'medical debt', 'other']
mortgage_services__borrower_assets__asset_type = ['checking account', 'savings account', 'money market account', 'certificate of deposit (CD)', 'stocks', 'bonds', 'mutual funds', 'retirement account (401k, IRA)', 'real estate', 'vehicle', 'other']
mortgage_services__borrower_liabilities__asset_type = ['checking account', 'savings account', 'money market account', 'certificate of deposit (CD)', 'stocks', 'bonds', 'mutual funds', 'retirement account (401k, IRA)', 'real estate', 'vehicle', 'other']
mortgage_services__borrower_assets__verification_status = ['pending', 'verified', 'not verified', 'partial verification']
mortgage_services__borrower_liabilities__verification_status = ['pending', 'verified', 'not verified', 'partial verification']
mortgage_services__borrower_incomes__income_type = ['salary', 'hourly wages', 'self-employment', 'rental income', 'investment income', 'social security', 'pension', 'alimony', 'child support', 'disability income', 'other']
mortgage_services__borrower_employments__employment_type = ['full-time', 'part-time', 'self-employed', 'contract', 'temporary', 'retired', 'unemployed']
mortgage_services__borrower_incomes__frequency = ['weekly', 'bi-weekly', 'semi-monthly', 'monthly', 'annually', 'one-time']
mortgage_services__borrower_incomes__verification_status = ['pending', 'verified', 'not verified', 'partial verification']
mortgage_services__borrower_citizenships__citizenship_status = ['US citizen', 'permanent resident', 'non-permanent resident', 'other']
mortgage_service__application_borrowers__borrower_type = ['primary', 'co-borrower', 'guarantor', 'trust']
mortgage_service__application_borrowers__relationship_to_primary = ['spouse', 'domestic partner', 'parent', 'child', 'sibling', 'other relative', 'friend', 'business partner', 'none']
mortgage_services__applications__application_type = ['purchase', 'refinance', 'HELOC']
mortgage_services__applications__referral_source = ['online ad', 'referral', 'real estate agent', 'walk-in', 'direct mail', 'social media']
mortgage_services__applications__status = ['draft', 'submitted', 'under review', 'approved', 'denied', 'funded', 'cancelled', 'withdrawn']
mortgage_services__applications__loan_purpose = ['primary residence', 'second home', 'investment property']

def mortgage_services(_dg):
    return [
        ('mortgage_services\\.hmda_submissions', '^submission_notes$', text_list(
            mortgage_services__hmda_submissions__submission_notes)),
        ('mortgage_services\\.hmda_submissions', '^reporting_period$', text_list(mortgage_services__hmda_submissions__reporting_period, lower=True)),
        ('mortgage_services\\.hmda_submissions', '^submission_status$', text_list(mortgage_services__hmda_submissions__submission_status, lower=True)),
        ('mortgage_services\\.hmda_edits', '^resolution_notes$', text_list(mortgage_services__hmda_edits__resolution_notes)),
        ('mortgage_services\\.hmda_edits', '^edit_type$', text_list(mortgage_services__hmda_edits__edit_type, lower=True)),
        ('mortgage_services\\.hmda_edits', '^status$', text_list(mortgage_services__hmda_edits__status, lower=True)),
        ('mortgage_services\\.hmda_applicant_demographics', '^applicant_type$', text_list(mortgage_services__hmda_applicant_demographics__applicant_type, lower=True)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_1$', text_list(mortgage_services__hmda_applicant_demographics__ethnicity_1)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_2$', text_list(mortgage_services__hmda_applicant_demographics__ethnicity_2)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_3$', text_list(mortgage_services__hmda_applicant_demographics__ethnicity_3)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_4$', text_list(mortgage_services__hmda_applicant_demographics__ethnicity_3)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_5$', text_list(mortgage_services__hmda_applicant_demographics__ethnicity_3)),
        ('mortgage_services\\.hmda_applicant_demographics', '^ethnicity_observed$', text_list(mortgage_services__hmda_applicant_demographics__ethnicity_observed, lower=True)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_1$', text_list(mortgage_services__hmda_applicant_demographics__race_1)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_2$', text_list(mortgage_services__hmda_applicant_demographics__race_2)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_3$', text_list(mortgage_services__hmda_applicant_demographics__race_3)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_4$', text_list(mortgage_services__hmda_applicant_demographics__race_4)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_5$', text_list(mortgage_services__hmda_applicant_demographics__race_4)),
        ('mortgage_services\\.hmda_applicant_demographics', '^race_observed$', text_list(mortgage_services__hmda_applicant_demographics__race_observed)),
        ('mortgage_services\\.hmda_applicant_demographics', '^sex$', text_list(mortgage_services__hmda_applicant_demographics__sex)),
        ('mortgage_services\\.hmda_applicant_demographics', '^sex_observed$', text_list(mortgage_services__hmda_applicant_demographics__sex_observed)),
        ('mortgage_services\\.hmda_records', '^loan_type$', text_list([
            "Conventional",
            "FHA",
            "VA",
            "USDA"
        ])),
        ('mortgage_services\\.hmda_records', '^loan_purpose$', text_list([
            "Home purchase",
            "Home improvement",
            "Refinancing",
            "Cash-out refinancing",
            "Other purpose"
        ], lower=True)),
        ('mortgage_services\\.hmda_records', '^construction_method$', text_list([
            "Site-built",
            "Manufactured"
        ], lower=True)),
        ('mortgage_services\\.hmda_records', '^occupancy_type$', text_list([
            "Primary",
            "Secondary",
            "Investment"
        ], lower=True)),
        ('mortgage_services\\.hmda_records', '^action_taken$', text_list([
            "Originated",
            "Approved not accepted",
            "Denied",
            "Withdrawn by applicant",
            "Incomplete",
            "Preapproval request denied",
            "Preapproval request approved but not accepted"
        ], lower=True)),
        ('mortgage_services\\.hmda_records', '^hoepa_status$', text_list([
            1, 2
        ])),
        ('mortgage_services\\.hmda_records', '^lien_status$', text_list([
            1, 2
        ])),
        ('mortgage_services\\.hmda_records', '^credit_score_model$', text_list([
            "Equifax Beacon 5.0",
            "Experian/Fair Isaac Risk Model V2SM",
            "TransUnion FICO Risk Score Classic 04",
            "VantageScore 3.0"
        ])),
        ('mortgage_services\\.hmda_records', '^denial_reason(1|2|3|4)$', text_list([
            "Debt-to-income ratio",
            "Credit history",
            "Collateral",
            "Insufficient cash",
            "Unverifiable information",
            "Credit application incomplete",
            "Mortgage insurance denied",
            "Other"
        ], lower=True)),
        ('mortgage_services\\.hmda_records', 'manufactured_home_secured_property_type',
         text_list([
             "Single-wide",
             "Double-wide",
             "Triple-wide",
             "Multi-wide"
         ], lower=True)),
        ('mortgage_services\\.hmda_records', 'manufactured_home_land_property_interest',
         text_list([
             "Owned",
             "Leased",
             "Land contract"
         ], lower=True)),
        ('mortgage_services\\.hmda_records', '^submission_of_application$', text_list([
            "Direct",
            "Not direct"
        ], lower=True)),
        ('mortgage_services\\.hmda_records',
         '^reverse_mortgage|business_or_commercial_purpose|initially_payable_to_institution|preapproval|negative_amortization|other_non_amortizing_features|balloon_payment|interest_only_payment|initially_payable_to_institution|reverse_mortgage|open_end_line_of_credit$',
         text_list([
             "Yes",
             "No"
         ], lower=True)),
        ('mortgage_services\\.hmda_records', '^aus(1|2|3|4|5)$', text_list([
            "Desktop Underwriter (DU)",
            "Loan Prospector (LP)",
            "Technology Open to Approved Lenders (TOTAL) Scorecard",
            "Guaranteed Underwriting System (GUS)"
        ])),
        ('mortgage_services\\.hmda_records', '^submission_status$', text_list([
            "pending",
            "SUBMITTED",
            "ACCEPTED",
            "rejected"
        ], lower=True)),
        ('mortgage_services\\.hmda_records', '^edit_status$', text_list([
            "NOT_STARTED",
            "IN_PROGRESS",
            "completed",
            "failed"
        ], lower=True)),
        ('mortgage_services\\.customer_communications', '^communication_type$', text_list([
            "email",
            "letter",
            "phone",
            "SMS",
            "in person",
            "secure message",
            "fax"
        ])),
        ('mortgage_services\\.customer_communications', '^direction$', text_list([
            "Incoming",
            "Outgoing"
        ], lower=True)),
        ('mortgage_services\\.customer_communications', '^status$', text_list([
            "Sent",
            "Delivered",
            "Opened",
            "Clicked",
            "Bounced",
            "Failed",
            "Draft",
            "Scheduled"
        ], lower=True)),
        ('mortgage_services\\.customer_communications', '^related_to$', text_list([
            "Application Status",
            "Document Request",
            "Payment Reminder",
            "Escrow Analysis",
            "Loan Modification",
            "Insurance Information",
            "Tax Information",
            "General Inquiry",
            "Complaint",
            "Other"
        ], lower=True)),
        ('mortgage_services\\.loan_modification', '^modification_type$', text_list([
            "Rate Reduction",
            "Term Extension",
            "Principal Reduction",
            "Payment Reduction",
            "Forbearance Plan",
            "Other"
        ], lower=True)),
        ('mortgage_services\\.loan_modification', '^reason$', text_list(
            mortgage_services__loan_modifications__reason)),
        ('mortgage_services\\.loan_modification', '^status$', text_list([
            "Requested",
            "Under Review",
            "Approved",
            "Denied",
            "Completed",
            "Cancelled"
        ], lower=True)),
        ('mortgage_services\\.insurance_policies', '^insurance_type$', text_list([
            "Hazard",
            "Flood",
            "Windstorm",
            "Earthquake",
            "Liability",
            "Other"
        ], lower=True)),
        ('mortgage_services\\.insurance_policies', '^agent_name$', lambda a, b, c: fake.name()),
        ('mortgage_services\\.insurance_policies', '^carrier_name$', lambda a, b, c: fake.company()),
        ('mortgage_services\\.insurance_policies', '^status$', text_list([
            "active",
            "Expired",
            "Cancelled",
            "Pending Renewal",
            "Lapsed"
        ], lower=True)),
        ('mortgage_services\\.escrow_analyses', '^status$', text_list([
            "Completed",
            "Pending Review",
            "Approved",
            "Implemented",
            "Cancelled"
        ], lower=True)),
        ('mortgage_services\\.escrow_disbursements', '^disbursement_type$', text_list([
            "Property Tax",
            "Homeowners Insurance",
            "Mortgage Insurance (PMI)",
            "Flood Insurance",
            "HOA Fees",
            "Other"
        ])),
        ('mortgage_services\\.escrow_disbursements', '^status$', text_list([
            "Pending",
            "Processed",
            "Cleared",
            "Failed",
            "Cancelled"
        ], lower=True)),
        ('mortgage_services\\.payments', '^payment_method$', text_list([
            "ACH",
            "Check",
            "Online",
            "Phone",
            "Wire Transfer",
            "Money Order",
            "In Person"
        ])),
        ('mortgage_services\\.payments', '^status$', text_list([
            "Pending",
            "Completed",
            "Failed",
            "Returned",
            "Cancelled",
            "Processing"
        ], lower=True)),
        ('mortgage_services\\.payments', '^payment_type$', text_list([
            "Regular",
            "Extra Principal",
            "Escrow Only",
            "Payoff",
            "Reinstatement",
            "Forbearance Payment"
        ], lower=True)),
        ('mortgage_services\\.servicing_accounts', '^status$', text_list([
            "active",
            "Paid Off",
            "Delinquent",
            "Foreclosure",
            "Default",
            "Bankruptcy",
            "Forbearance",
            "Modification",
            "Transferred"
        ], lower=True)),
        ('mortgage_services\\.closed_loans', '^settlement_agent$', lambda a, b, c: fake.name()),
        ('mortgage_services\\.closed_loans', '^settlement_company$', lambda a, b, c: fake.company()),
        ('mortgage_services\\.closing_appointments', '^notes$',
         text_list(mortgage_services__closing__appointments_notes)),
        ('.*', '^closing_agent$', lambda a, b, c: fake.name()),
        ('.*', '^closing_company$', lambda a, b, c: fake.company()),
        ('mortgage_services\\.closing_appointments', '^status$', text_list([
            "Scheduled",
            "Rescheduled",
            "Completed",
            "Cancelled",
            "Pending"
        ], lower=True)),
        ('mortgage_services\\.closing_disclosures', '^disclosure_type$', text_list([
            "closing disclosure",
            "loan estimate",
            "Initial Escrow Statement",
            "Servicing Transfer Disclosure"
        ], lower=True)),
        ('mortgage_services\\.credit_reports', '^report_type$', text_list([
            "Single Bureau",
            "Tri-Merge"
        ], lower=True)),
        ('mortgage_services\\.credit_reports', '^status$', text_list([
            "Pulled",
            "Reviewed",
            "Expired",
            "Error"
        ], lower=True)),
        ('mortgage_services\\.appraisals', '^appraisal_type$', text_list([
            "Full Appraisal",
            "Drive-By Appraisal",
            "Desktop Appraisal",
            "Hybrid Appraisal"
        ], lower=True)),
        ('mortgage_services\\.appraisals', '^appraiser_name$', lambda a, b, c: fake.name()),
        ('mortgage_services\\.(appraisals|credit_reports)', '^report_path$', lambda a, b, c: fake.file_path()),
        ('mortgage_services\\.appraisals', '^appraisal_company$', lambda a, b, c: fake.company()),
        ('mortgage_services\\.appraisals', '^status$', text_list([
            "Ordered",
            "Scheduled",
            "Inspected",
            "Completed",
            "Reviewed",
            "Challenged",
            "Cancelled"
        ], lower=True)),
        ('mortgage_services\\.conditions', '^condition_type$', text_list([
            "Prior to Approval",
            "Prior to Closing",
            "Post Closing"
        ], lower=True)),
        ('mortgage_services\\.conditions', '^status$', text_list([
            "Pending",
            "Cleared",
            "Waived",
            "Overdue",
            "Rejected"
        ], lower=True)),
        ('.*', '^document_name$', lambda a, b, c: fake.file_name()),
        ('.*', '^.*_path$', lambda a, b, c: fake.file_path()),
        ('mortgage_services\\.documents', '^document_type$', text_list([
            "W2",
            "Tax Return",
            "Pay Stub",
            "Bank Statement",
            "Driver's License",
            "Social Security Card",
            "Proof of Residency",
            "Purchase Agreement",
            "Appraisal",
            "Title Report",
            "Insurance Policy",
            "Gift Letter",
            "Asset Statement",
            "Liability Statement",
            "Other"
        ])),
        ('mortgage_services\\.documents', '^status$', text_list([
            "Uploaded",
            "Pending Review",
            "Approved",
            "Rejected",
            "Requested",
            "Expired"
        ], lower=True)),
        ('mortgage_services\\.loan_rate_locks', '^status$', text_list([
            "active",
            "Expired",
            "Extended",
            "Cancelled",
            "Completed"
        ], lower=True)),
        ('mortgage_services\\.loan_products', '^loan_type$', text_list([
            "Conventional",
            "FHA",
            "VA",
            "USDA",
            "Jumbo",
            "HELOC",
            "Reverse Mortgage",
            "Construction Loan"
        ])),
        ('mortgage_services\\.loans', '^loan_type$', text_list([
            "Conventional",
            "FHA",
            "VA",
            "USDA",
            "Jumbo",
            "HELOC",
            "Reverse Mortgage",
            "Construction Loan"
        ])),
        ('mortgage_services\\.(loans|loan_products)', '^interest_rate_type$', text_list([
            "Fixed",
            "Adjustable"
        ], lower=True)),
        ('mortgage_services\\.properties', '^property_type$', text_list([
            "Single Family",
            "Condominium",
            "Townhouse",
            "Multi-Family",
            "Manufactured Home",
            "Cooperative",
            "Other"
        ], lower=True)),
        ('mortgage_services\\.properties', '^occupancy_type$', text_list([
            "Primary Residence",
            "Second Home",
            "Investment Property"
        ], lower=True)),
        ('mortgage_services\\.borrower_liabilities', '^liability_type$', text_list([
            "Credit Card",
            "Auto Loan",
            "Student Loan",
            "Personal Loan",
            "Mortgage",
            "Child Support",
            "Alimony",
            "Medical Debt",
            "Other"
        ], lower=True)),
        ('.*', '^asset_type$', text_list([
            "Checking Account",
            "Savings Account",
            "Money Market Account",
            "Certificate of Deposit (CD)",
            "Stocks",
            "Bonds",
            "Mutual Funds",
            "Retirement Account (401k, IRA)",
            "Real Estate",
            "Vehicle",
            "Other"
        ])),
        ('mortgage_services\\.borrower_(assets|liabilities)', '^verification_status$',
         text_list([
             "Pending",
             "Verified",
             "Not Verified",
             "Partial Verification"
         ], lower=True)),
        ('.*', '^income_type$', text_list([
            "Salary",
            "Hourly Wages",
            "Self-Employment",
            "Rental Income",
            "Investment Income",
            "Social Security",
            "Pension",
            "Alimony",
            "Child Support",
            "Disability Income",
            "Other"
        ], lower=True)),
        ('.*', '^employment_type$', text_list([
            "Full-Time",
            "Part-Time",
            "Self-Employed",
            "Contract",
            "Temporary",
            "Retired",
            "Unemployed"
        ], lower=True)),
        ('mortgage_services\\.borrower_incomes', '^frequency$', text_list([
            "Weekly",
            "Bi-Weekly",
            "Semi-Monthly",
            "Monthly",
            "Annually",
            "One-Time"
        ], lower=True)),
        ('mortgage_services\\.borrower_incomes', '^verification_status$', text_list([
            "Pending",
            "Verified",
            "Not Verified",
            "Partial Verification"
        ], lower=True)),
        ('.*', '^citizenship_status$', text_list([
            "US Citizen",
            "Permanent Resident",
            "Non-Permanent Resident",
            "Other"
        ])),
        ('mortgage_service.application_borrowers', '^borrower_type$', text_list([
            "Primary",
            "Co-Borrower",
            "Guarantor",
            "Trust"
        ], lower=True)),
        (
            'mortgage_service.application_borrowers', '^relationship_to_primary$',
            text_list([
                "Spouse",
                "Domestic Partner",
                "Parent",
                "Child",
                "Sibling",
                "Other Relative",
                "Friend",
                "Business Partner",
                "None"
            ], lower=True)),
        ('mortgage_services\\.applications', '^application_type$', text_list([
            "Purchase",
            "Refinance",
            "HELOC"
        ])),
        ('.*', '^referral_source$', text_list([
            "Online Ad",
            "Referral",
            "Real Estate Agent",
            "Walk-In",
            "Direct Mail",
            "Social Media"
        ], lower=True)),
        ('mortgage_services\\.applications', '^status$', text_list([
            "Draft",
            "Submitted",
            "Under Review",
            "Approved",
            "Denied",
            "Funded",
            "Cancelled",
            "Withdrawn"
        ], lower=True)),
        ('mortgage_services\\.applications', '^loan_purpose$', text_list([
            "Primary Residence",
            "Second Home",
            "Investment Property"
        ], lower=True)), ('mortgage_services\\.hmda_edits', '^edit_description$',
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
        (
        'mortgage_services\\.closing_appointments', '^notes$', text_list(mortgage_services__closing_appointments__notes)),
        ('mortgage_services\\.conditions', '^description$', text_list(mortgage_services__conditions__description)),
        ('mortgage_services\\.documents', '^notes$', text_list(mortgage_services__documents__notes)),
        ('mortgage_services\\.loan_products', '^description$', text_list(mortgage_services__loan_products__description)),
    ]
