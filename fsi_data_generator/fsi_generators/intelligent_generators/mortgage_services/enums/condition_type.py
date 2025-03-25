from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class ConditionType(BaseEnum):
    PRIOR_TO_APPROVAL = auto()
    PRIOR_TO_CLOSING = auto()
    PRIOR_TO_FUNDING = auto()
    PRIOR_TO_DOCS = auto()
    AT_CLOSING = auto()
    POST_CLOSING = auto()
    UNDERWRITER_REQUIREMENT = auto()
    AGENCY_REQUIREMENT = auto()
    OTHER = auto()
