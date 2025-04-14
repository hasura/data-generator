from ....helpers import BaseEnum
from enum import auto


class EducationLevel(BaseEnum):
    """Education level categories for demographic classification."""
    NO_FORMAL_EDUCATION = auto()  # No formal educational credentials
    PRIMARY_EDUCATION = auto()  # Completed primary education
    SECONDARY_EDUCATION = auto()  # Completed secondary education (high school)
    VOCATIONAL_TRAINING = auto()  # Completed vocational or technical training
    ASSOCIATE_DEGREE = auto()  # Completed associate degree
    BACHELORS_DEGREE = auto()  # Completed bachelor's degree
    MASTERS_DEGREE = auto()  # Completed master's degree
    DOCTORATE = auto()  # Completed doctorate degree
    PROFESSIONAL_DEGREE = auto()  # Completed professional degree (MD, JD, etc.)
    OTHER = auto()  # Other educational qualification not listed
    UNKNOWN = auto()  # Education level is unknown or not provided

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        3.0,   # NO_FORMAL_EDUCATION
        5.0,   # PRIMARY_EDUCATION
        30.0,  # SECONDARY_EDUCATION
        10.0,  # VOCATIONAL_TRAINING
        12.0,  # ASSOCIATE_DEGREE
        25.0,  # BACHELORS_DEGREE
        8.0,   # MASTERS_DEGREE
        2.0,   # DOCTORATE
        2.0,   # PROFESSIONAL_DEGREE
        2.0,   # OTHER
        1.0    # UNKNOWN
    ]
