from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class HmdaLoanPurpose(BaseEnum):
    HOME_PURCHASE = "1"  # Home purchase
    HOME_IMPROVEMENT = "2"  # Home improvement
    REFINANCING = "3"  # Refinancing
    CASH_OUT_REFINANCING = "4"  # Cash-out refinancing
    OTHER_PURPOSE = "5"  # Other purpose
    REVERSE_MORTGAGE = "31"  # Reverse mortgage
    LINE_OF_CREDIT = "32"  # Open-end line of credit
    OTHER = "999"  # Other purpose not listed


class HmdaPreapproval(BaseEnum):
    REQUESTED = "1"  # Preapproval requested
    NOT_REQUESTED = "2"  # Preapproval not requested
    NOT_APPLICABLE = "3"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 0]


class HmdaConstructionMethod(BaseEnum):
    SITE_BUILT = "1"  # Site-built
    MANUFACTURED_HOME = "2"  # Manufactured home


class HmdaOccupancyType(BaseEnum):
    PRINCIPAL_RESIDENCE = "1"  # Principal residence
    SECOND_RESIDENCE = "2"  # Second residence
    INVESTMENT_PROPERTY = "3"  # Investment property


class HmdaActionTaken(BaseEnum):
    LOAN_ORIGINATED = "1"  # Loan originated
    APPLICATION_APPROVED_BUT_NOT_ACCEPTED = "2"  # Application approved but not accepted
    APPLICATION_DENIED = "3"  # Application denied
    APPLICATION_WITHDRAWN = "4"  # Application withdrawn by applicant
    FILE_CLOSED_FOR_INCOMPLETENESS = "5"  # File closed for incompleteness
    PURCHASED_LOAN = "6"  # Purchased loan
    PREAPPROVAL_REQUEST_DENIED = "7"  # Preapproval request denied
    PREAPPROVAL_REQUEST_APPROVED_BUT_NOT_ACCEPTED = "8"  # Preapproval request approved but not accepted


class HmdaDenialReason(BaseEnum):
    DEBT_INCOME_RATIO = "1"  # Debt-to-income ratio
    EMPLOYMENT_HISTORY = "2"  # Employment history
    CREDIT_HISTORY = "3"  # Credit history
    COLLATERAL = "4"  # Collateral
    INSUFFICIENT_CASH = "5"  # Insufficient cash
    UNVERIFIABLE_INFORMATION = "6"  # Unverifiable information
    CREDIT_APPLICATION_INCOMPLETE = "7"  # Credit application incomplete
    MORTGAGE_INSURANCE_DENIED = "8"  # Mortgage insurance denied
    OTHER = "9"  # Other
    NOT_APPLICABLE = "10"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0.0]


class HmdaHoepaStatus(BaseEnum):
    HIGH_COST_MORTGAGE = "1"  # High-cost mortgage
    NOT_HIGH_COST_MORTGAGE = "2"  # Not a high-cost mortgage
    NOT_APPLICATION = "3"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 0]


class HmdaLienStatus(BaseEnum):
    SECURED_BY_FIRST_LIEN = "1"  # Secured by a first lien
    SECURED_BY_SUBORDINATE_LIEN = "2"  # Secured by a subordinate lien
    NOT_SECURED_BY_LIEN = "3"  # Not secured by a lien
    NOT_APPLICABLE = "4"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 1, 0.0]


class HmdaCreditScoreModel(BaseEnum):
    EQUIFAX = "1"  # Equifax
    EXPERIAN = "2"  # Experian
    TRANSUNION = "3"  # TransUnion
    FICO = "4"  # FICO
    COUNTERSCORE = "5"  # CounterScore
    GSGL = "6"  # GS/GL
    LOANPERFORMANCE = "7"  # LoanPerformance
    OTHER = "8"  # Other credit scoring model
    NOT_APPLICABLE = "9"  # Not applicable
    PURCHASED_LOAN = "1111"  # Purchased loan: credit score not available


class HmdaSubmissionStatus(BaseEnum):
    PENDING = "PENDING"  # Ready for submission but not yet sent
    SUBMITTED = "SUBMITTED"  # Submitted to regulatory agency
    ACCEPTED = "ACCEPTED"  # Accepted by regulatory agency
    REJECTED = "REJECTED"  # Rejected by regulatory agency, needs correction
    EXEMPTED = "EXEMPTED"  # Exempted from reporting requirements

    _DEFAULT_WEIGHTS = [0.15, 0.20, 0.40, 0.10, 0.15]


class HmdaBalloonPayment(BaseEnum):
    YES = "1"  # Yes, loan has balloon payment feature
    NO = "2"  # No, loan does not have balloon payment feature


class HmdaInterestOnly(BaseEnum):
    YES = "1"  # Yes, loan has interest-only payments
    NO = "2"  # No, loan does not have interest-only payments


class HmdaNegativeAmortization(BaseEnum):
    YES = "1"  # Yes, loan allows negative amortization
    NO = "2"  # No, loan does not allow negative amortization


class HmdaOtherNonAmortizing(BaseEnum):
    YES = "1"  # Yes, loan has other non-amortizing features
    NO = "2"  # No, loan does not have other non-amortizing features


class HmdaManufacturedHomeType(BaseEnum):
    MANUFACTURED_HOME_AND_LAND = "1"  # Manufactured home and land
    MANUFACTURED_HOME_ONLY = "2"  # Manufactured home only
    NOT_APPLICABLE = "3"  # Not applicable

    _DEFAULT_WEIGHTS = [0.5, 0.5, 0.0]


class HmdaManufacturedLandPropertyInterest(BaseEnum):
    DIRECT_OWNERSHIP = "1"  # Direct ownership
    INDIRECT_OWNERSHIP = "2"  # Indirect ownership
    PAID_LEASEHOLD = "3"  # Paid leasehold
    UNPAID_LEASEHOLD = "4"  # Unpaid leasehold
    NOT_APPLICABLE = "5"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 1, 1, 0.0]


class HmdaSubmissionMethod(BaseEnum):
    DIRECT_SUBMISSION = "1"  # Direct submission
    NOT_DIRECT_SUBMISSION = "2"  # Not direct submission
    NOT_APPLICABLE = "3"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 0]


class HmdaAus(BaseEnum):
    DU = "1"  # Desktop Underwriter (DU)
    LP = "2"  # Loan Prospector (LP) or Loan Product Advisor
    TOTAL = "3"  # Technology Open to Approved Lenders (TOTAL) Scorecard
    GUS = "4"  # Guaranteed Underwriting System (GUS)
    AUS = "5"  # Other AUS
    NOT_APPLICABLE = "6"  # Not applicable
    INTERNAL = "7"  # Internal proprietary system
    PURCHASE_LOAN = "1111"  # Purchased loan: AUS data not available


class HmdaReverseMortgage(BaseEnum):
    YES = "1"  # Yes, reverse mortgage
    NO = "2"  # No, not a reverse mortgage
    PURCHASED_LOAN = "1111"  # Purchased loan: reverse mortgage status not available


class HmdaOpenEndLineOfCredit(BaseEnum):
    YES = "1"  # Yes, open-end line of credit
    NO = "2"  # No, not an open-end line of credit
    PURCHASED_LOAN = "1111"  # Purchased loan: open-end line of credit status not available


class HmdaBusinessOrCommercialPurpose(BaseEnum):
    CODE_1 = "1"  # Yes, primarily for a business or commercial purpose
    CODE_2 = "2"  # No, not primarily for a business or commercial purpose
    PURCHASED_LOAN = "1111"  # Purchased loan: business or commercial purpose not available


class HmdaRecordEditStatus(BaseEnum):
    NOT_STARTED = "NOT_STARTED"  # Edits check has not been initiated
    IN_PROGRESS = "IN_PROGRESS"  # Edits check is currently running
    VALID = "VALID"  # Passed all required edits
    INVALID = "INVALID"  # Failed one or more validity edits
    QUALITY_ISSUES = "QUALITY_ISSUES"  # Passed all validity edits but has quality issues
    MACRO_ISSUES = "MACRO_ISSUES"  # Passed all validity and quality edits but has macro issues


class HmdaEditType(BaseEnum):
    SYNTACTICAL = auto()
    VALIDITY = auto()
    QUALITY = auto()
    MACRO = auto()


class HmdaEditStatus(BaseEnum):
    OPEN = auto()
    VERIFIED = auto()
    CORRECTED = auto()
    IN_PROGRESS = auto()
    WAIVED = auto()

    _DEFAULT_WEIGHTS = [0.5, 0.1, 0.2, 0.1, 0.1]


class HmdaReportingPeriod(BaseEnum):
    ANNUAL = "ANNUAL"  # Annual filing covering January 1 to December 31 data
    QUARTERLY_Q1 = "QUARTERLY_Q1"  # First quarter filing covering January 1 to March 31 data
    QUARTERLY_Q2 = "QUARTERLY_Q2"  # Second quarter filing covering April 1 to June 30 data
    QUARTERLY_Q3 = "QUARTERLY_Q3"  # Third quarter filing covering July 1 to September 30 data

    _DEFAULT_WEIGHTS = [7, 1, 1, 1]


class HmdaSubmissionStatusDetail(BaseEnum):
    NO_DATA_UPLOADED = "1"  # No data has been uploaded yet
    UPLOAD_IN_PROGRESS = "2"  # File upload in progress
    UPLOADED_NOT_PARSED = "3"  # File uploaded but not yet parsed
    PARSING_IN_PROGRESS = "4"  # Parsing in progress
    PARSED_WITH_ERRORS = "5"  # File parsed with errors
    PARSED_NO_ERRORS = "6"  # File parsed, no errors
    VALIDATING = "7"  # Validating file
    VALIDATION_ERRORS = "8"  # File has validation errors
    VALIDATED_WITH_VERIFICATION_NEEDED = "9"  # File passed validation with errors that need verification
    VALIDATION_ERRORS_REQUIRE_CORRECTION = "10"  # File has validation errors that require correction
    VALIDATED_READY_FOR_VERIFICATION = "11"  # File passed validation, ready for verification
    VERIFICATION_IN_PROGRESS = "12"  # Verification in progress
    MACRO_EDITS_NEED_REVIEW = "13"  # Data has macro edits that need review
    READY_FOR_SUBMISSION = "14"  # Data is ready for submission
    SUBMISSION_ACCEPTED = "15"  # Submission has been accepted
