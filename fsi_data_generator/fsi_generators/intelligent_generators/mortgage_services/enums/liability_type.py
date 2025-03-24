from fsi_data_generator.fsi_generators.helpers import BaseEnum


class LiabilityType(BaseEnum):
    CREDIT_CARD = "CREDIT_CARD"  # Revolving credit card debt
    AUTO_LOAN = "AUTO_LOAN"  # Loan for vehicle purchase
    STUDENT_LOAN = "STUDENT_LOAN"  # Educational loan
    PERSONAL_LOAN = "PERSONAL_LOAN"  # Unsecured personal loan
    MORTGAGE = "MORTGAGE"  # Home mortgage loan
    HOME_EQUITY_LOAN = "HOME_EQUITY_LOAN"  # Loan secured by home equity
    HOME_EQUITY_LINE_OF_CREDIT = "HOME_EQUITY_LINE_OF_CREDIT"  # Revolving line of credit secured by home equity
    MEDICAL_DEBT = "MEDICAL_DEBT"  # Outstanding medical bills or healthcare-related debt
    BUSINESS_LOAN = "BUSINESS_LOAN"  # Loan for business purposes
    RETAIL_CREDIT = "RETAIL_CREDIT"  # Credit account with a retailer
    INSTALLMENT_LOAN = "INSTALLMENT_LOAN"  # Fixed-term loan with regular payments
    PAYDAY_LOAN = "PAYDAY_LOAN"  # Short-term, high-interest loan
    TAX_DEBT = "TAX_DEBT"  # Outstanding tax liabilities
    OTHER = "OTHER"  # Liability type not covered by standard categories

