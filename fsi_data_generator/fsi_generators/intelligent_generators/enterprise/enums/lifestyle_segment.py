from ....helpers import BaseEnum
from enum import auto


class LifestyleSegment(BaseEnum):
    """Lifestyle segment categories for demographic and marketing classification."""
    URBAN_PROFESSIONAL = auto()  # Urban-dwelling professionals with high earning potential
    SUBURBAN_FAMILY = auto()  # Family-oriented individuals living in suburban areas
    RURAL_TRADITIONAL = auto()  # Individuals living in rural areas with traditional values
    BUDGET_CONSCIOUS = auto()  # Individuals who are particularly sensitive to price and value
    LUXURY_SEEKER = auto()  # Individuals who prefer premium products and experiences
    ECO_CONSCIOUS = auto()  # Individuals who prioritize environmental sustainability
    TECH_SAVVY = auto()  # Early adopters of technology and digital services
    EXPERIENTIAL = auto()  # Individuals who value experiences over material possessions
    HEALTH_FOCUSED = auto()  # Individuals who prioritize health and wellness
    CONVENIENCE_SEEKER = auto()  # Individuals who prioritize convenience in products and services
    TRADITIONAL_BANKING = auto()  # Individuals who prefer traditional banking methods and in-person service
    DIGITAL_FIRST = auto()  # Individuals who prefer digital banking and fintech solutions
    COMMUNITY_ORIENTED = auto()  # Individuals who value community involvement and local businesses
    CREDIT_REBUILDER = auto()  # Individuals working to rebuild or establish credit
    WEALTH_BUILDER = auto()  # Individuals focused on building long-term wealth
    RETIREMENT_FOCUSED = auto()  # Individuals primarily focused on retirement planning
    OTHER = auto()  # Other lifestyle segment
    UNKNOWN = auto()  # Lifestyle segment is unknown or not provided

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        12.0,  # URBAN_PROFESSIONAL
        15.0,  # SUBURBAN_FAMILY
        8.0,   # RURAL_TRADITIONAL
        10.0,  # BUDGET_CONSCIOUS
        3.0,   # LUXURY_SEEKER
        5.0,   # ECO_CONSCIOUS
        8.0,   # TECH_SAVVY
        6.0,   # EXPERIENTIAL
        7.0,   # HEALTH_FOCUSED
        8.0,   # CONVENIENCE_SEEKER
        5.0,   # TRADITIONAL_BANKING
        7.0,   # DIGITAL_FIRST
        4.0,   # COMMUNITY_ORIENTED
        3.0,   # CREDIT_REBUILDER
        4.0,   # WEALTH_BUILDER
        3.0,   # RETIREMENT_FOCUSED
        1.0,   # OTHER
        1.0    # UNKNOWN
    ]
