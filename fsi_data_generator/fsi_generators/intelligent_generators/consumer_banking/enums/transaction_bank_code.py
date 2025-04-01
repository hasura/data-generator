from ....helpers import BaseEnum
from enum import auto


class TransactionBankCode(BaseEnum):
    """Comprehensive bank transaction codes with categorization."""

    # Retail Categories
    RETAIL__CLOTHING_STORE = auto()
    RETAIL__ELECTRONICS = auto()
    RETAIL__DEPARTMENT_STORE = auto()
    RETAIL__ONLINE_SHOPPING = auto()
    RETAIL__GROCERY = auto()
    RETAIL__CONVENIENCE_STORE = auto()
    RETAIL__OTHER = auto()

    # Services Categories
    SERVICES__RESTAURANT = auto()
    SERVICES__ENTERTAINMENT = auto()
    SERVICES__TRAVEL = auto()
    SERVICES__CAR_RENTAL = auto()
    SERVICES__HOTEL = auto()
    SERVICES__PROFESSIONAL = auto()
    SERVICES__UTILITIES = auto()
    SERVICES__TELECOMMUNICATIONS = auto()
    SERVICES__OTHER = auto()

    # Financial Categories
    FINANCIAL__ATM_WITHDRAWAL = auto()
    FINANCIAL__BANK_TRANSFER = auto()
    FINANCIAL__LOAN_PAYMENT = auto()
    FINANCIAL__CREDIT_CARD_PAYMENT = auto()
    FINANCIAL__INVESTMENT = auto()
    FINANCIAL__INSURANCE_PAYMENT = auto()
    FINANCIAL__WIRE_TRANSFER = auto()
    FINANCIAL__OTHER = auto()

    # Regulatory Categories
    REGULATORY__BSA_REPORTING = auto()
    REGULATORY__AML_THRESHOLD = auto()
    REGULATORY__OFAC_SCREENING = auto()
    REGULATORY__CTR_REPORT = auto()
    REGULATORY__SUSPICIOUS_ACTIVITY = auto()
    REGULATORY__KYC_VERIFICATION = auto()
    REGULATORY__PEP_TRANSACTION = auto()
    REGULATORY__SANCTIONS_CHECK = auto()
    REGULATORY__TAX_REPORTING = auto()
    REGULATORY__FATCA_REPORTING = auto()
    REGULATORY__OTHER = auto()

    # Risk Management Categories
    RISK__HIGH_RISK_GEO = auto()
    RISK__UNUSUAL_PATTERN = auto()
    RISK__VELOCITY_CHECK = auto()
    RISK__LARGE_CASH_DEPOSIT = auto()
    RISK__CROSS_BORDER = auto()
    RISK__FIRST_TIME_MERCHANT = auto()
    RISK__DEVICE_ANOMALY = auto()
    RISK__REPEATED_DECLINED = auto()
    RISK__OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        # Retail Weights
        10.0,  # RETAIL__CLOTHING_STORE
        8.0,  # RETAIL__ELECTRONICS
        7.0,  # RETAIL__DEPARTMENT_STORE
        6.0,  # RETAIL__ONLINE_SHOPPING
        12.0,  # RETAIL__GROCERY
        5.0,  # RETAIL__CONVENIENCE_STORE
        2.0,  # RETAIL__OTHER

        # Services Weights
        8.0,  # SERVICES__RESTAURANT
        6.0,  # SERVICES__ENTERTAINMENT
        7.0,  # SERVICES__TRAVEL
        4.0,  # SERVICES__CAR_RENTAL
        5.0,  # SERVICES__HOTEL
        3.0,  # SERVICES__PROFESSIONAL
        9.0,  # SERVICES__UTILITIES
        6.0,  # SERVICES__TELECOMMUNICATIONS
        2.0,  # SERVICES__OTHER

        # Financial Weights
        8.0,  # FINANCIAL__ATM_WITHDRAWAL
        7.0,  # FINANCIAL__BANK_TRANSFER
        6.0,  # FINANCIAL__LOAN_PAYMENT
        9.0,  # FINANCIAL__CREDIT_CARD_PAYMENT
        5.0,  # FINANCIAL__INVESTMENT
        4.0,  # FINANCIAL__INSURANCE_PAYMENT
        3.0,  # FINANCIAL__WIRE_TRANSFER
        2.0,  # FINANCIAL__OTHER

        # Regulatory Weights
        6.0,  # REGULATORY__BSA_REPORTING
        5.0,  # REGULATORY__AML_THRESHOLD
        4.0,  # REGULATORY__OFAC_SCREENING
        3.0,  # REGULATORY__CTR_REPORT
        7.0,  # REGULATORY__SUSPICIOUS_ACTIVITY
        5.0,  # REGULATORY__KYC_VERIFICATION
        3.0,  # REGULATORY__PEP_TRANSACTION
        4.0,  # REGULATORY__SANCTIONS_CHECK
        5.0,  # REGULATORY__TAX_REPORTING
        3.0,  # REGULATORY__FATCA_REPORTING
        2.0,  # REGULATORY__OTHER

        # Risk Management Weights
        6.0,  # RISK__HIGH_RISK_GEO
        7.0,  # RISK__UNUSUAL_PATTERN
        5.0,  # RISK__VELOCITY_CHECK
        4.0,  # RISK__LARGE_CASH_DEPOSIT
        3.0,  # RISK__CROSS_BORDER
        3.0,  # RISK__FIRST_TIME_MERCHANT
        5.0,  # RISK__DEVICE_ANOMALY
        4.0,  # RISK__REPEATED_DECLINED
        2.0  # RISK__OTHER
    ]
