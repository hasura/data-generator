import datetime
import logging
import random
import sys
from typing import Any, Dict

import psycopg2

from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.income_frequency import \
    IncomeFrequency
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.liability_type import \
    LiabilityType
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.verification_status import \
    VerificationStatus

logger = logging.getLogger(__name__)


def generate_random_borrower_liability(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services borrower liability record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (like mortgage_services_borrower_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated borrower liability data (without ID fields)
    """
    # Get database connection
    conn = dg.conn
    progress_through_loan = None

    # Define creditor names for different liability types
    creditor_names = {
        LiabilityType.CREDIT_CARD: ["Chase Bank", "Bank of America", "Capital One", "Discover", "American Express",
                                    "Citibank", "Wells Fargo", "Synchrony Bank", "Barclays", "U.S. Bank"],
        LiabilityType.AUTO_LOAN: ["Toyota Financial", "Honda Financial", "Ford Credit", "GM Financial",
                                  "BMW Financial Services", "Ally Financial", "Wells Fargo Auto", "Capital One Auto",
                                  "Chase Auto", "CarMax Auto Finance"],
        LiabilityType.STUDENT_LOAN: ["Sallie Mae", "Navient", "Great Lakes", "Nelnet", "FedLoan Servicing", "SoFi",
                                     "Earnest", "CommonBond", "LendKey", "MOHELA"],
        LiabilityType.PERSONAL_LOAN: ["Discover Personal Loans", "LendingClub", "Upstart", "Prosper", "Avant",
                                      "OneMain Financial", "Best Egg", "LightStream", "Upgrade",
                                      "Marcus by Goldman Sachs"],
        LiabilityType.MORTGAGE: ["Wells Fargo Home Mortgage", "Chase Home Lending", "Bank of America Home Loans",
                                 "Quicken Loans", "U.S. Bank Home Mortgage", "Caliber Home Loans", "PennyMac",
                                 "Freedom Mortgage", "Mr. Cooper", "Flagstar Bank"],
        LiabilityType.HOME_EQUITY_LOAN: ["Wells Fargo", "Bank of America", "Chase", "U.S. Bank", "Discover Home Loans",
                                         "Citizens Bank", "TD Bank", "Fifth Third Bank", "PNC Bank", "Flagstar Bank"],
        LiabilityType.HOME_EQUITY_LINE_OF_CREDIT: ["Wells Fargo", "Bank of America", "Chase", "U.S. Bank",
                                                   "Citizens Bank", "PNC Bank", "TD Bank", "BMO Harris", "Regions Bank",
                                                   "SunTrust Bank"],
        LiabilityType.MEDICAL_DEBT: ["Hospital Collection Dept.", "MedCredit Financial", "CareCredit",
                                     "Medical Financial Solutions", "NPAS Solutions", "Access One", "CCS Collections",
                                     "CMRE Financial Services", "Healthcare Receivables Group",
                                     "Medical Debt Resolution"],
        LiabilityType.BUSINESS_LOAN: ["Bank of America", "Chase Business Banking", "Wells Fargo Business", "U.S. Bank",
                                      "Capital One", "TD Bank", "PNC Bank", "Regions Bank", "Citizens Bank",
                                      "Huntington Bank"],
        LiabilityType.RETAIL_CREDIT: ["Amazon Store Card", "Best Buy Credit", "Home Depot Credit", "Lowe's Credit",
                                      "Macy's Credit", "Target RedCard", "Walmart Credit", "Kohl's Charge", "Gap Visa",
                                      "JCPenney Credit"],
        LiabilityType.INSTALLMENT_LOAN: ["Affirm", "Klarna", "Afterpay", "Sezzle", "PayPal Credit",
                                         "Progressive Leasing", "Acima", "Rent-A-Center", "Aaron's", "Snap Finance"],
        LiabilityType.PAYDAY_LOAN: ["Ace Cash Express", "Check 'n Go", "Speedy Cash", "CashNetUSA", "Advance America",
                                    "Check Into Cash", "RISE Credit", "LendUp", "MoneyKey", "Spotloan"],
        LiabilityType.TAX_DEBT: ["Internal Revenue Service", "State Tax Authority", "Local Tax Office",
                                 "Tax Resolution Services", "Tax Defense Network", "Optima Tax Relief",
                                 "Tax Hardship Center", "Tax Relief Center", "Community Tax", "StopIRSDebt"],
        LiabilityType.OTHER: ["Finance Company", "Credit Union", "Regional Bank", "Online Lender", "Family Loan",
                              "Employer Loan", "Credit Services", "Financial Institution", "Loan Company",
                              "Finance Corporation"]
    }

    # Get borrower income information to make liability data reasonable
    borrower_income = get_borrower_income(id_fields["mortgage_services_borrower_id"], conn)

    # Select a random liability type
    liability_type = LiabilityType.get_random()

    # Select an appropriate creditor for the liability type
    creditor_name = random.choice(creditor_names.get(liability_type, creditor_names[LiabilityType.OTHER]))

    # Generate a reasonable monthly payment based on borrower income and liability type
    # Typically, all debt payments should be less than 43% of income for mortgage qualification
    max_payment_percentages = {
        LiabilityType.CREDIT_CARD: 0.05,
        LiabilityType.AUTO_LOAN: 0.15,
        LiabilityType.STUDENT_LOAN: 0.10,
        LiabilityType.PERSONAL_LOAN: 0.08,
        LiabilityType.MORTGAGE: 0.28,
        LiabilityType.HOME_EQUITY_LOAN: 0.10,
        LiabilityType.HOME_EQUITY_LINE_OF_CREDIT: 0.08,
        LiabilityType.MEDICAL_DEBT: 0.05,
        LiabilityType.BUSINESS_LOAN: 0.15,
        LiabilityType.RETAIL_CREDIT: 0.03,
        LiabilityType.INSTALLMENT_LOAN: 0.07,
        LiabilityType.PAYDAY_LOAN: 0.10,
        LiabilityType.TAX_DEBT: 0.12,
        LiabilityType.OTHER: 0.08
    }

    max_percentage = max_payment_percentages.get(liability_type, 0.08)
    max_monthly_payment = borrower_income * max_percentage

    # Set minimum payment based on liability type
    min_payments = {
        LiabilityType.CREDIT_CARD: 25,
        LiabilityType.RETAIL_CREDIT: 15,
        LiabilityType.PAYDAY_LOAN: 50,
        LiabilityType.AUTO_LOAN: 200,
        LiabilityType.STUDENT_LOAN: 100,
        LiabilityType.PERSONAL_LOAN: 100,
        LiabilityType.MORTGAGE: 500,
        LiabilityType.HOME_EQUITY_LOAN: 150,
        LiabilityType.HOME_EQUITY_LINE_OF_CREDIT: 100,
        LiabilityType.MEDICAL_DEBT: 50,
        LiabilityType.BUSINESS_LOAN: 300,
        LiabilityType.INSTALLMENT_LOAN: 75,
        LiabilityType.TAX_DEBT: 200,
        LiabilityType.OTHER: 50
    }

    min_payment = min_payments.get(liability_type, 50)
    monthly_payment = round(random.uniform(min_payment, float(max_monthly_payment)), 2)

    # Generate term lengths based on liability type (in months)
    term_lengths = {
        LiabilityType.CREDIT_CARD: None,  # Revolving
        LiabilityType.RETAIL_CREDIT: None,  # Revolving
        LiabilityType.HOME_EQUITY_LINE_OF_CREDIT: None,  # Revolving
        LiabilityType.AUTO_LOAN: random.choice([36, 48, 60, 72, 84]),
        LiabilityType.STUDENT_LOAN: random.choice([120, 180, 240, 300]),
        LiabilityType.PERSONAL_LOAN: random.choice([12, 24, 36, 48, 60]),
        LiabilityType.MORTGAGE: random.choice([180, 240, 360]),
        LiabilityType.HOME_EQUITY_LOAN: random.choice([60, 120, 180, 240]),
        LiabilityType.MEDICAL_DEBT: random.choice([12, 24, 36, 48, 60]),
        LiabilityType.BUSINESS_LOAN: random.choice([12, 24, 36, 48, 60, 84, 120]),
        LiabilityType.INSTALLMENT_LOAN: random.choice([6, 12, 24, 36]),
        LiabilityType.PAYDAY_LOAN: random.choice([1, 2, 3, 6]),
        LiabilityType.TAX_DEBT: random.choice([12, 24, 36, 48, 60, 72]),
        LiabilityType.OTHER: random.choice([12, 24, 36, 48, 60])
    }

    # Generate reasonable amounts for other fields based on liability type and monthly payment
    term_length = term_lengths.get(liability_type)

    if term_length:
        # For installment loans, calculate current balance based on term and payment
        # Different liability types have different typical interest rate ranges
        if liability_type == LiabilityType.CREDIT_CARD:
            interest_rate = round(random.uniform(12.0, 24.99), 3)
        elif liability_type == LiabilityType.AUTO_LOAN:
            interest_rate = round(random.uniform(3.0, 8.0), 3)
        elif liability_type == LiabilityType.STUDENT_LOAN:
            interest_rate = round(random.uniform(4.0, 7.5), 3)
        elif liability_type == LiabilityType.PERSONAL_LOAN:
            interest_rate = round(random.uniform(6.0, 15.0), 3)
        elif liability_type == LiabilityType.MORTGAGE:
            interest_rate = round(random.uniform(2.5, 6.5), 3)
        elif liability_type in [LiabilityType.HOME_EQUITY_LOAN, LiabilityType.HOME_EQUITY_LINE_OF_CREDIT]:
            interest_rate = round(random.uniform(4.0, 8.0), 3)
        elif liability_type == LiabilityType.PAYDAY_LOAN:
            interest_rate = round(random.uniform(300.0, 500.0), 3)
        elif liability_type == LiabilityType.INSTALLMENT_LOAN:
            interest_rate = round(random.uniform(10.0, 30.0), 3)
        else:
            interest_rate = round(random.uniform(5.0, 12.0), 3)

        # Use a reasonable progress through the loan term to determine current balance
        progress_through_loan = random.uniform(0.0, 0.9)  # 0% to 90% through the loan
        remaining_months = term_length * (1 - progress_through_loan)

        # Simplified formula to estimate current balance
        current_balance = round(monthly_payment * (remaining_months - (remaining_months * interest_rate / 2400)), 2)

        # Make sure current balance is positive and reasonable
        current_balance = max(current_balance, monthly_payment)

        # Generate original amount (slightly higher than current balance)
        original_amount = round(current_balance / (1 - progress_through_loan), 2)
    else:
        # For revolving credit, use typical balance-to-payment ratios
        if liability_type == LiabilityType.CREDIT_CARD:
            current_balance = round(monthly_payment * random.uniform(10, 40), 2)
            interest_rate = round(random.uniform(12.0, 24.99), 3)
        elif liability_type == LiabilityType.HOME_EQUITY_LINE_OF_CREDIT:
            current_balance = round(monthly_payment * random.uniform(20, 100), 2)
            interest_rate = round(random.uniform(4.0, 8.0), 3)
        elif liability_type == LiabilityType.RETAIL_CREDIT:
            current_balance = round(monthly_payment * random.uniform(5, 20), 2)
            interest_rate = round(random.uniform(15.0, 29.99), 3)
        else:
            current_balance = round(monthly_payment * random.uniform(10, 30), 2)
            interest_rate = round(random.uniform(5.0, 18.0), 3)

        # For revolving accounts, original amount is often the credit limit
        original_amount = round(current_balance * random.uniform(1.2, 2.5), 2)

    # Generate dates
    today = datetime.date.today()

    # Origination date based on liability type and progress
    if term_length:
        # For installment loans, base on term length and progress
        months_passed = int(term_length * progress_through_loan)
        origination_date = today - datetime.timedelta(days=30 * months_passed)
    else:
        # For revolving accounts, 1-7 years ago
        years_ago = random.randint(1, 7)
        origination_date = today - datetime.timedelta(days=365 * years_ago + random.randint(0, 364))

    # Maturity date based on term length if applicable
    if term_length:
        maturity_date = origination_date + datetime.timedelta(days=30 * term_length)
    else:
        # For revolving accounts, typically no fixed maturity
        maturity_date = None

    # Generate verification status and date
    verification_status = VerificationStatus.get_random()

    verification_date = None
    if verification_status == VerificationStatus.VERIFIED:
        # Verification happened between 1 and 30 days ago
        days_ago = random.randint(1, 30)
        verification_date = today - datetime.timedelta(days=days_ago)

    # Decide if the liability will be paid off with mortgage proceeds
    # Higher chance for high-interest debt or debts that interfere with mortgage qualification
    pay_off_probabilities = {
        LiabilityType.CREDIT_CARD: 0.6,
        LiabilityType.AUTO_LOAN: 0.1,
        LiabilityType.STUDENT_LOAN: 0.05,
        LiabilityType.PERSONAL_LOAN: 0.5,
        LiabilityType.MORTGAGE: 0.9,  # Existing mortgage often paid off in refinance
        LiabilityType.HOME_EQUITY_LOAN: 0.7,
        LiabilityType.HOME_EQUITY_LINE_OF_CREDIT: 0.6,
        LiabilityType.MEDICAL_DEBT: 0.4,
        LiabilityType.BUSINESS_LOAN: 0.2,
        LiabilityType.RETAIL_CREDIT: 0.3,
        LiabilityType.INSTALLMENT_LOAN: 0.3,
        LiabilityType.PAYDAY_LOAN: 0.8,
        LiabilityType.TAX_DEBT: 0.4,
        LiabilityType.OTHER: 0.3
    }

    will_be_paid_off = random.random() < pay_off_probabilities.get(liability_type, 0.3)

    # Create the liability record
    liability = {
        "liability_type": liability_type.value,
        "creditor_name": creditor_name,
        "account_number": f"xxxx-xxxx-xxxx-{random.randint(1000, 9999)}",
        "monthly_payment": float(monthly_payment),
        "current_balance": float(current_balance),
        "original_amount": float(original_amount),
        "interest_rate": float(interest_rate),
        "origination_date": origination_date,
        "maturity_date": maturity_date,
        "verification_status": verification_status.value,
        "verification_date": verification_date,
        "will_be_paid_off": will_be_paid_off
    }

    return liability


def get_borrower_income(borrower_id: int, conn) -> float:
    """
    Get the borrower's monthly income to make liability data reasonable.
    Sums all income sources after converting to monthly values.

    Args:
        borrower_id: The ID of the borrower
        conn: PostgreSQL connection object

    Returns:
        Monthly income as a float
    """
    try:
        monthly_total = 0.0
        cursor = conn.cursor()

        # Get income from borrower_employments
        try:
            cursor.execute("""
                SELECT monthly_income 
                FROM mortgage_services.borrower_employments 
                WHERE mortgage_services_borrower_id = %s
            """, (borrower_id,))
        except psycopg2.ProgrammingError as e:
            logger.critical(f"Programming error detected in the SQL query: {e}")
            sys.exit(1)

        employment_results = cursor.fetchall()

        # Sum all employment income
        for result in employment_results:
            monthly_total += result.get("monthly_income", 0)

        # Get all income from borrower_incomes with appropriate frequency conversions
        try:
            cursor.execute("""
                SELECT amount, frequency
                FROM mortgage_services.borrower_incomes 
                WHERE mortgage_services_borrower_id = %s
            """, (borrower_id,))
        except psycopg2.ProgrammingError as e:
            logger.critical(f"Programming error detected in the SQL query: {e}")
            sys.exit(1)

        income_records = cursor.fetchall()

        # Process all additional income sources
        for record in income_records:
            amount = record.get('amount', 0)
            frequency = record.get('frequency', IncomeFrequency.MONTHLY.value)

            # Convert to monthly based on frequency
            if frequency == IncomeFrequency.WEEKLY.value:
                # Weekly × 52 ÷ 12
                monthly_amount = amount * 4.33
            elif frequency == IncomeFrequency.BI_WEEKLY.value:
                # Bi-weekly × 26 ÷ 12
                monthly_amount = amount * 2.17
            elif frequency == IncomeFrequency.SEMI_MONTHLY.value:
                # Semi-monthly × 2
                monthly_amount = amount * 2.0
            elif frequency == IncomeFrequency.MONTHLY.value:
                # Already monthly
                monthly_amount = amount
            elif frequency == IncomeFrequency.QUARTERLY.value:
                # Quarterly ÷ 3
                monthly_amount = amount / 3.0
            elif frequency == IncomeFrequency.SEMI_ANNUALLY.value:
                # Semi-annually ÷ 6
                monthly_amount = amount / 6.0
            elif frequency == IncomeFrequency.ANNUALLY.value:
                # Annually ÷ 12
                monthly_amount = amount / 12.0
            elif frequency == IncomeFrequency.IRREGULAR.value:
                # For irregular income, use a conservative approach
                # Assume it's spread over 6 months
                monthly_amount = amount / 6.0
            else:
                # Default to monthly if unknown
                monthly_amount = amount

            monthly_total += monthly_amount

        cursor.close()

        # If no income found, use a reasonable default
        if monthly_total <= 0:
            monthly_total = 5000.00  # Reasonable default monthly income

        return monthly_total

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching borrower income: {error}")
        # Return a reasonable default if there's an error
        return 5000.0
