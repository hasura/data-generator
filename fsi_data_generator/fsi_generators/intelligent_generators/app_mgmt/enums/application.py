from ....helpers import BaseEnum
from enum import auto


class ApplicationLifecycleStatus(BaseEnum):
    """
    Enum representing the lifecycle status of an application.
    """
    DEVELOPMENT = auto()
    PILOT = auto()
    PRODUCTION = auto()
    DEPRECATED = auto()
    DATA_MAINTENANCE = auto()
    DECOMMISSIONED = auto()
    ARCHIVED = auto()

    _DEFAULT_WEIGHTS = [
        20.0,  # DEVELOPMENT
        10.0,  # PILOT
        40.0,  # PRODUCTION
        15.0,  # DEPRECATED
        8.0,   # DATA_MAINTENANCE
        5.0,   # DECOMMISSIONED
        2.0    # ARCHIVED
    ]


class DeploymentEnvironment(BaseEnum):
    """
    Enum representing the environment where an application is deployed.
    """
    ON_PREMISES = auto()
    CLOUD_PUBLIC = auto()
    CLOUD_PRIVATE = auto()
    CLOUD_HYBRID = auto()
    CONTAINERIZED = auto()
    SERVERLESS = auto()
    EDGE = auto()

    _DEFAULT_WEIGHTS = [
        25.0,  # ON_PREMISES
        30.0,  # CLOUD_PUBLIC
        15.0,  # CLOUD_PRIVATE
        10.0,  # CLOUD_HYBRID
        12.0,  # CONTAINERIZED
        5.0,   # SERVERLESS
        3.0    # EDGE
    ]


class ApplicationType(BaseEnum):
    """
    Enum representing the type of application.
    """
    WEB = auto()
    MOBILE = auto()
    DESKTOP = auto()
    API = auto()
    BATCH = auto()
    MICROSERVICE = auto()
    LEGACY = auto()
    SAAS = auto()
    DATABASE = auto()
    MIDDLEWARE = auto()
    EMBEDDED = auto()

    _DEFAULT_WEIGHTS = [
        20.0,  # WEB
        15.0,  # MOBILE
        10.0,  # DESKTOP
        15.0,  # API
        8.0,   # BATCH
        12.0,  # MICROSERVICE
        5.0,   # LEGACY
        6.0,   # SAAS
        4.0,   # DATABASE
        3.0,   # MIDDLEWARE
        2.0    # EMBEDDED
    ]
