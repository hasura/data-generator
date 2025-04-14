from ....helpers import BaseEnum
from enum import auto


class OccupationCategory(BaseEnum):
    """Occupation categories for demographic classification."""
    MANAGEMENT = auto()  # Executive, administrative, and managerial occupations
    BUSINESS_FINANCIAL = auto()  # Business and financial operations occupations
    COMPUTER_MATHEMATICAL = auto()  # Computer and mathematical occupations
    ARCHITECTURE_ENGINEERING = auto()  # Architecture and engineering occupations
    SCIENCE = auto()  # Life, physical, and social science occupations
    COMMUNITY_SOCIAL_SERVICE = auto()  # Community and social service occupations
    LEGAL = auto()  # Legal occupations
    EDUCATION = auto()  # Educational instruction and library occupations
    ARTS_ENTERTAINMENT = auto()  # Arts, design, entertainment, sports, and media occupations
    HEALTHCARE_PRACTITIONERS = auto()  # Healthcare practitioners and technical occupations
    HEALTHCARE_SUPPORT = auto()  # Healthcare support occupations
    PROTECTIVE_SERVICE = auto()  # Protective service occupations
    FOOD_SERVICE = auto()  # Food preparation and serving related occupations
    BUILDING_MAINTENANCE = auto()  # Building and grounds cleaning and maintenance occupations
    PERSONAL_CARE = auto()  # Personal care and service occupations
    SALES = auto()  # Sales and related occupations
    OFFICE_ADMIN = auto()  # Office and administrative support occupations
    FARMING_FISHING_FORESTRY = auto()  # Farming, fishing, and forestry occupations
    CONSTRUCTION = auto()  # Construction and extraction occupations
    INSTALLATION_MAINTENANCE_REPAIR = auto()  # Installation, maintenance, and repair occupations
    PRODUCTION = auto()  # Production occupations
    TRANSPORTATION = auto()  # Transportation and material moving occupations
    MILITARY = auto()  # Military specific occupations
    RETIRED = auto()  # Retired from work force
    STUDENT = auto()  # Full-time student
    HOMEMAKER = auto()  # Full-time homemaker
    UNEMPLOYED = auto()  # Currently unemployed
    OTHER = auto()  # Other occupation not listed
    UNKNOWN = auto()  # Occupation is unknown or not provided

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        6.0,   # MANAGEMENT
        5.0,   # BUSINESS_FINANCIAL
        3.5,   # COMPUTER_MATHEMATICAL
        2.0,   # ARCHITECTURE_ENGINEERING
        1.5,   # SCIENCE
        2.0,   # COMMUNITY_SOCIAL_SERVICE
        1.5,   # LEGAL
        3.5,   # EDUCATION
        2.0,   # ARTS_ENTERTAINMENT
        3.0,   # HEALTHCARE_PRACTITIONERS
        2.5,   # HEALTHCARE_SUPPORT
        2.0,   # PROTECTIVE_SERVICE
        5.0,   # FOOD_SERVICE
        3.0,   # BUILDING_MAINTENANCE
        3.0,   # PERSONAL_CARE
        7.0,   # SALES
        7.0,   # OFFICE_ADMIN
        1.5,   # FARMING_FISHING_FORESTRY
        4.0,   # CONSTRUCTION
        3.5,   # INSTALLATION_MAINTENANCE_REPAIR
        4.0,   # PRODUCTION
        5.0,   # TRANSPORTATION
        1.0,   # MILITARY
        6.0,   # RETIRED
        4.0,   # STUDENT
        3.0,   # HOMEMAKER
        4.0,   # UNEMPLOYED
        2.5,   # OTHER
        2.0    # UNKNOWN
    ]
