from ....helpers import BaseEnum
from enum import auto


class TransactionStatus(BaseEnum):
    """Status of a banking transaction."""
    PENDING = auto()
    BOOKED = auto()
    CANCELLED = auto()
    REJECTED = auto()
    REVERSED = auto()
    HELD = auto()
    EXPIRED = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        25.0,  # PENDING
        50.0,  # BOOKED
        5.0,   # CANCELLED
        5.0,   # REJECTED
        5.0,   # REVERSED
        5.0,   # HELD
        3.0,   # EXPIRED
        2.0    # OTHER
    ]


class TransactionMutability(BaseEnum):
    """Mutability status of a transaction."""
    MUTABLE = auto()
    IMMUTABLE = auto()
    CONDITIONAL = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        20.0,  # MUTABLE
        70.0,  # IMMUTABLE
        10.0   # CONDITIONAL
    ]


class TransactionCategory(BaseEnum):
    """High-level categorization of banking transactions."""
    PAYMENT = auto()
    DEPOSIT = auto()
    WITHDRAWAL = auto()
    FEE = auto()
    INTEREST = auto()
    TRANSFER = auto()
    ATM = auto()
    POINT_OF_SALE = auto()
    CARD_PAYMENT = auto()
    DIRECT_DEBIT = auto()
    STANDING_ORDER = auto()
    CREDIT = auto()
    DEBIT = auto()
    REVERSAL = auto()
    ADJUSTMENT = auto()
    CHECK = auto()
    LOAN_DISBURSEMENT = auto()
    LOAN_PAYMENT = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # PAYMENT
        10.0,  # DEPOSIT
        10.0,  # WITHDRAWAL
        5.0,   # FEE
        5.0,   # INTEREST
        10.0,  # TRANSFER
        5.0,   # ATM
        10.0,  # POINT_OF_SALE
        10.0,  # CARD_PAYMENT
        5.0,   # DIRECT_DEBIT
        3.0,   # STANDING_ORDER
        2.0,   # CREDIT
        2.0,   # DEBIT
        2.0,   # REVERSAL
        2.0,   # ADJUSTMENT
        3.0,   # CHECK
        2.0,   # LOAN_DISBURSEMENT
        3.0,   # LOAN_PAYMENT
        1.0    # OTHER
    ]


class TransactionType(BaseEnum):
    """Specific type of banking transaction."""
    PURCHASE = auto()
    CASH_WITHDRAWAL = auto()
    REFUND = auto()
    BILL_PAYMENT = auto()
    SALARY = auto()
    SUBSCRIPTION = auto()
    DIVIDEND = auto()
    TAX_PAYMENT = auto()
    TAX_REFUND = auto()
    INTERNAL_TRANSFER = auto()
    EXTERNAL_TRANSFER = auto()
    MERCHANT_PAYMENT = auto()
    UTILITY_PAYMENT = auto()
    RENT_PAYMENT = auto()
    MORTGAGE_PAYMENT = auto()
    INVESTMENT = auto()
    INSURANCE_PREMIUM = auto()
    DONATION = auto()
    TRANSPORTATION = auto()
    FOOD_DINING = auto()
    HEALTHCARE = auto()
    EDUCATION = auto()
    ENTERTAINMENT = auto()
    TRAVEL = auto()
    RETAIL = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # PURCHASE
        8.0,   # CASH_WITHDRAWAL
        5.0,   # REFUND
        10.0,  # BILL_PAYMENT
        5.0,   # SALARY
        8.0,   # SUBSCRIPTION
        2.0,   # DIVIDEND
        3.0,   # TAX_PAYMENT
        2.0,   # TAX_REFUND
        5.0,   # INTERNAL_TRANSFER
        5.0,   # EXTERNAL_TRANSFER
        5.0,   # MERCHANT_PAYMENT
        5.0,   # UTILITY_PAYMENT
        3.0,   # RENT_PAYMENT
        3.0,   # MORTGAGE_PAYMENT
        2.0,   # INVESTMENT
        2.0,   # INSURANCE_PREMIUM
        1.0,   # DONATION
        3.0,   # TRANSPORTATION
        5.0,   # FOOD_DINING
        2.0,   # HEALTHCARE
        1.0,   # EDUCATION
        3.0,   # ENTERTAINMENT
        2.0,   # TRAVEL
        3.0,   # RETAIL
        1.0    # OTHER
    ]
