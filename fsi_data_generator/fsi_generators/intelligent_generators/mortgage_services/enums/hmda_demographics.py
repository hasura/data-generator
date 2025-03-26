from fsi_data_generator.fsi_generators.helpers import BaseEnum


class HmdaEthnicity(BaseEnum):
    HISPANIC_OR_LATINO = "1"  # Hispanic or Latino
    NOT_HISPANIC_OR_LATINO = "2"  # Not Hispanic or Latino
    INFORMATION_NOT_PROVIDED = "3"  # Information not provided by applicant in mail, internet, or telephone application
    NOT_APPLICABLE = "4"  # Not applicable
    NO_CO_APPLICANT = "5"  # No co-applicant

    _DEFAULT_WEIGHTS = [1, 1, 1, 0, 1]


class HmdaEthnicityDetail(BaseEnum):
    MEXICAN = "1"  # Mexican
    PUERTO_RICAN = "2"  # Puerto Rican
    CUBAN = "3"  # Cuban
    OTHER_HISPANIC_OR_LATINO = "4"  # Other Hispanic or Latino
    NOT_HISPANIC_OR_LATINO = "5"  # Not Hispanic or Latino
    INFORMATION_NOT_PROVIDED = "6"  # Information not provided
    NOT_APPLICABLE = "7"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 1, 1, 1, 1, 0]


class HmdaRace(BaseEnum):
    AMERICAN_INDIAN_OR_ALASKA_NATIVE = "1"  # American Indian or Alaska Native
    ASIAN = "2"  # Asian
    BLACK_OR_AFRICAN_AMERICAN = "3"  # Black or African American
    NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER = "4"  # Native Hawaiian or Other Pacific Islander
    WHITE = "5"  # White
    INFORMATION_NOT_PROVIDED = "6"  # Information not provided by applicant in mail, internet, or telephone application
    NOT_APPLICABLE = "7"  # Not applicable
    NO_CO_APPLICANT = "8"  # No co-applicant

    _DEFAULT_WEIGHTS = [1, 1, 1, 1, 1, 1, 0, 1]


class HmdaRaceAsianDetail(BaseEnum):
    ASIAN_INDIAN = "1"  # Asian Indian
    CHINESE = "2"  # Chinese
    FILIPINO = "3"  # Filipino
    JAPANESE = "4"  # Japanese
    KOREAN = "5"  # Korean
    VIETNAMESE = "6"  # Vietnamese
    OTHER_ASIAN = "7"  # Other Asian

    _DEFAULT_WEIGHTS = [1, 1, 1, 1, 1, 1, 1]


class HmdaRacePacificIslanderDetail(BaseEnum):
    NATIVE_HAWAIIAN = "1"  # Native Hawaiian
    GUAMANIAN_OR_CHAMORRO = "2"  # Guamanian or Chamorro
    SAMOAN = "3"  # Samoan
    OTHER_PACIFIC_ISLANDER = "4"  # Other Pacific Islander

    _DEFAULT_WEIGHTS = [1, 1, 1, 1]


class HmdaSex(BaseEnum):
    MALE = "1"  # Male
    FEMALE = "2"  # Female
    INFORMATION_NOT_PROVIDED = "3"  # Information not provided by applicant in mail, internet, or telephone application
    NOT_APPLICABLE = "4"  # Not applicable
    NO_CO_APPLICANT = "5"  # No co-applicant
    APPLICANT_SELECTED_BOTH = "6"  # Applicant selected both male and female

    _DEFAULT_WEIGHTS = [1, 1, 1, 0, 1, 1]


class HmdaCollectionMethod(BaseEnum):
    VISUAL_OBSERVATION_OR_SURNAME = "1"  # Visual observation or surname
    NOT_COLLECTED_ON_VISUAL_OBSERVATION = "2"  # Not collected on the basis of visual observation or surname
    NOT_APPLICABLE = "3"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 0]


class HmdaAgeGroup(BaseEnum):
    LESS_THAN_25 = "1"  # Less than 25
    AGE_25_TO_34 = "2"  # 25-34
    AGE_35_TO_44 = "3"  # 35-44
    AGE_45_TO_54 = "4"  # 45-54
    AGE_55_TO_64 = "5"  # 55-64
    AGE_65_TO_74 = "6"  # 65-74
    GREATER_THAN_74 = "7"  # Greater than 74
    INFORMATION_NOT_PROVIDED = "8"  # Information not provided
    NOT_APPLICABLE = "9"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 1, 1, 1, 1, 1, 1, 0]


class HmdaApplicantPresent(BaseEnum):
    APPLICANT_PRESENT = "1"  # Applicant present
    NO_APPLICANT_PRESENT = "2"  # No applicant present (internet, mail, or telephone application)
    NOT_APPLICABLE = "3"  # Not applicable

    _DEFAULT_WEIGHTS = [1, 1, 0]


class HmdaApplicantType(BaseEnum):
    PRIMARY = "PRIMARY"  # Primary applicant for the mortgage
    CO_APPLICANT = "CO_APPLICANT"  # Co-applicant on the mortgage application
    BORROWER = "BORROWER"  # Main borrower after loan is originated
    CO_BORROWER = "CO_BORROWER"  # Secondary borrower after loan is originated
    GUARANTOR = "GUARANTOR"  # Person guaranteeing the loan but not a primary applicant

    _DEFAULT_WEIGHTS = [1, 1, 1, 1, 1]
