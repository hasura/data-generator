import os
import sys

import psycopg2
from dotenv import load_dotenv

from fsi_data_generator.banking_generators import custom_generators

# Load environment variables from .env file
load_dotenv()

# Import the DataGenerator class
# Assuming the DataGenerator code is in a file named data_generator.py
try:
    from data_generator import DataGenerator
except ImportError:
    print("Error: Could not import DataGenerator. Make sure data_generator.py is in the same directory.")
    sys.exit(1)


def generate_banking_data():
    """Run a DataGenerator with the retail financial services database."""

    conn_params = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "database": "postgres",  # Connect to default postgres database first
        "user": os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASSWORD", "password"),
        "port": os.environ.get("DB_PORT", "5432")
    }

    # Get the SQL file path from the environment variable
    sql_file_path = os.environ.get("MODEL_FILE")
    if not sql_file_path or not os.path.isfile(sql_file_path):
        print(f"Error: SQL file not found at {sql_file_path}")
        return

    # Get the SQL file path from the environment variable
    drop_sql_file_path = os.environ.get("DROP_FILE")
    if not drop_sql_file_path or not os.path.isfile(drop_sql_file_path):
        print(f"Error: SQL file not found at {drop_sql_file_path}")
        return

    try:
        print("\nStarting DataGenerator test...")

        # Step 1: Execute the SQL file using conn_params
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:

                print(f"Executing SQL file: {drop_sql_file_path}")
                with open(drop_sql_file_path, "r") as file:
                    sql = file.read()
                    cursor.execute(sql)
                    conn.commit()
                    print(f"SQL execution completed successfully: {drop_sql_file_path}")

                print(f"Executing SQL file: {sql_file_path}")
                with open(sql_file_path, "r") as file:
                    sql = file.read()
                    cursor.execute(sql)
                    conn.commit()
                    print(f"SQL execution completed successfully: {sql_file_path}")

        # Step 2: Initialize the DataGenerator
        generator = DataGenerator(
            conn_params=conn_params,
            exclude_schemas=['public']
        )
        generator.custom_generators = custom_generators(generator)

        # Step 3: Generate data
        generator.generate_vectorized_data(scale=.1, row_counts={
            "consumer_banking.account_access_consents": 200,
            "enterprise.permissions": 50,
            "consumer_banking.account_access_consents_permissions": 300,
            "enterprise.account_identifiers": 1000,
            "consumer_banking.accounts": 500,
            "consumer_banking.balances": 5000,
            "consumer_banking.beneficiaries": 1000,
            "consumer_banking.beneficiary_creditor_agents": 500,
            "consumer_banking.beneficiary_creditor_accounts": 1000,
            "consumer_banking.direct_debits": 500,
            "consumer_banking.mandate_related_information": 500,
            "consumer_banking.offers": 200,
            "enterprise.parties": 2000,
            "enterprise.party_relationships": 1000,
            "enterprise.party_addresses": 2000,
            "consumer_banking.products": 1000,
            "consumer_banking.other_product_types": 200,
            "consumer_banking.scheduled_payments": 500,
            "consumer_banking.scheduled_payment_creditor_agents": 250,
            "consumer_banking.scheduled_payment_creditor_accounts": 500,
            "consumer_banking.standing_orders": 500,
            "consumer_banking.standing_order_creditor_agents": 250,
            "consumer_banking.standing_order_creditor_accounts": 500,
            "consumer_banking.statements": 5000,
            "consumer_banking.statement_descriptions": 5000,
            "consumer_banking.statement_benefits": 2000,
            "consumer_banking.statement_fees": 2000,
            "consumer_banking.statement_interests": 2000,
            "consumer_banking.statement_amounts": 10000,
            "consumer_banking.statement_date_times": 10000,
            "consumer_banking.statement_rates": 5000,
            "consumer_banking.statement_values": 5000,
            "consumer_banking.transactions": 10000,
            "consumer_banking.transaction_statement_references": 10000,
            "consumer_banking.transaction_currency_exchanges": 2000,
            "consumer_banking.transaction_bank_transaction_codes": 10000,
            "consumer_banking.transaction_proprietary_bank_transaction_codes": 10000,
            "consumer_banking.transaction_balances": 10000,
            "consumer_banking.transaction_merchant_details": 5000,
            "consumer_banking.transaction_creditor_agents": 5000,
            "consumer_banking.transaction_creditor_accounts": 5000,
            "consumer_banking.transaction_debtor_agents": 5000,
            "consumer_banking.transaction_debtor_accounts": 5000,
            "consumer_banking.transaction_card_instruments": 5000,
            "consumer_banking.transaction_ultimate_creditors": 5000,
            "consumer_banking.transaction_ultimate_debtors": 5000,
            "consumer_banking.statement_delivery_addresses": 1000,
            "enterprise.addresses": 2000,
            "enterprise.address_lines": 1000,
            "enterprise.entity_addresses": 2000,
            "enterprise.accounts": 1000,
            "enterprise.account_ownership": 1500,
            "consumer_banking.account_statement_preferences": 1000,
            "enterprise.associates": 100,
            "enterprise.departments": 20,
            "enterprise.buildings": 50,
            "mortgage_services.applications": 200,
            "mortgage_services.application_borrowers": 300,
            "mortgage_services.borrowers": 500,
            "mortgage_services.borrower_employments": 750,
            "mortgage_services.borrower_incomes": 1000,
            "mortgage_services.borrower_assets": 1500,
            "mortgage_services.borrower_liabilities": 1250,
            "mortgage_services.properties": 200,
            "mortgage_services.loans": 200,
            "mortgage_services.loan_products": 20,
            "mortgage_services.loan_rate_locks": 100,
            "mortgage_services.documents": 1000,
            "mortgage_services.conditions": 400,
            "mortgage_services.appraisals": 200,
            "mortgage_services.credit_reports": 500,
            "mortgage_services.closing_disclosures": 200,
            "mortgage_services.closing_appointments": 200,
            "mortgage_services.closed_loans": 200,
            "mortgage_services.servicing_accounts": 200,
            "mortgage_services.payments": 2000,
            "mortgage_services.escrow_disbursements": 1000,
            "mortgage_services.escrow_analyses": 200,
            "mortgage_services.insurance_policies": 200,
            "mortgage_services.loan_modifications": 50,
            "mortgage_services.customer_communications": 1000,
            "mortgage_services.hmda_records": 200,
            "mortgage_services.hmda_edits": 100,
            "mortgage_services.hmda_submissions": 50,
            "credit_cards.card_products": 50,
            "credit_cards.fraud_cases": 100,
            "credit_cards.fraud_transactions": 200,
            "credit_cards.security_blocks": 200,
            "credit_cards.credit_card_applications_hmda": 500,
            "credit_cards.reg_z_credit_card_disclosures": 1000,
            "credit_cards.ability_to_pay_assessments": 500,
            "credit_cards.consumer_complaints": 200,
            "credit_cards.card_product_features": 200,
            "credit_cards.card_product_reward_categories": 100,
            "credit_cards.applications": 500,
            "credit_cards.card_accounts": 500,
            "credit_cards.cards": 1000,
            "credit_cards.authorized_users": 200,
            "credit_cards.transactions": 10000,
            "credit_cards.statements": 5000,
            "credit_cards.fees": 2000,
            "credit_cards.interest_charges": 2000,
            "credit_cards.rewards": 5000,
            "credit_cards.reward_redemptions": 1000,
            "credit_cards.promotional_offers": 500,
            "credit_cards.balance_transfers": 500,
            "credit_cards.payment_methods": 1000,
            "credit_cards.autopay_settings": 500,
            "credit_cards.credit_limit_changes": 500,
            "credit_cards.card_alerts": 1000,
            "credit_cards.disputed_transactions": 200,
            # Row counts for small business banking tables

            # Core Business Tables
            "small_business_banking.businesses": 200,
            "small_business_banking.business_owners": 350,

            # Account and Product Tables
            "small_business_banking.accounts": 400,
            "small_business_banking.products": 30,
            "small_business_banking.account_signatories": 600,

            # Lending Products
            "small_business_banking.loans": 100,
            "small_business_banking.credit_lines": 80,
            "small_business_banking.collateral": 150,
            "small_business_banking.loan_collateral": 200,

            # Credit Card Integration
            "small_business_banking.business_card_accounts": 120,
            "small_business_banking.business_card_users": 300,
            "small_business_banking.business_expense_categories": 50,
            "small_business_banking.business_transaction_categories": 2000,

            # Transaction and Document Management
            "small_business_banking.transactions": 5000,
            "small_business_banking.payments": 1000,
            "small_business_banking.documents": 500,

            # Regulatory Tables
            "small_business_regulatory.regulatory_reports": 20,
            "small_business_regulatory.report_submissions": 50,
            "small_business_regulatory.regulatory_findings": 30,
            "small_business_regulatory.compliance_cases": 40,
            "small_business_regulatory.compliance_requirements": 25,
            "small_business_regulatory.business_risk_assessments": 150,
            "small_business_regulatory.loan_fair_lending": 100,
            "small_business_regulatory.credit_decisions": 200,
            "small_business_regulatory.adverse_action_notices": 40,
            "small_business_regulatory.business_due_diligence": 200,
            "small_business_regulatory.beneficial_owner_verification": 350,
            "small_business_regulatory.suspicious_activity_reports": 80,

            "consumer_lending.loan_applications": 1000,
            "consumer_lending.application_applicants": 1000,
            "consumer_lending.applicants": 2000,
            "consumer_lending.applicant_employments": 3000,  # Applicants may have multiple jobs
            "consumer_lending.applicant_incomes": 4000,  # Various income sources
            "consumer_lending.applicant_assets": 5000,
            "consumer_lending.applicant_liabilities": 4000,
            "consumer_lending.loan_products": 50,
            "consumer_lending.product_eligibility_criteria": 200,
            "consumer_lending.risk_based_pricing_tiers": 100,
            "consumer_lending.credit_reports": 2000,
            "consumer_lending.credit_report_tradelines": 10000,  # Multiple tradelines per report
            "consumer_lending.credit_inquiries": 5000,
            "consumer_lending.public_records": 1000,
            "consumer_lending.decision_models": 20,
            "consumer_lending.application_decisions": 1000,
            "consumer_lending.decision_reasons": 2000,  # Multiple reasons per decision
            "consumer_lending.adverse_action_notices": 200,  # For denied applications
            "consumer_lending.vehicles": 500,  # For auto loans
            "consumer_lending.loan_accounts": 800,  # Assuming some loans are not funded
            "consumer_lending.payment_schedules": 10000,  # Multiple payments per loan
            "consumer_lending.disbursements": 800,
            "consumer_lending.loan_payments": 8000,
            "consumer_lending.loan_fees": 2000,
            "consumer_lending.loan_collateral": 1000,
            "consumer_lending.loan_insurance": 1000,
            "consumer_lending.loan_documents": 2000,
            "consumer_lending.loan_communications": 5000,
            "consumer_lending.loan_statements": 4000,
            "consumer_lending.collection_accounts": 100,  # For delinquent loans
            "consumer_lending.collection_actions": 500,
            "consumer_lending.payment_arrangements": 200,
            "consumer_lending.loan_modifications": 100,
            "consumer_lending.reg_z_disclosures": 2000,
            "consumer_lending.adverse_action_details": 200,
            "consumer_lending.ecoa_monitoring": 1000,
            "consumer_lending.fairlending_analysis": 50,
            "consumer_lending.reg_b_notices": 500,
            "consumer_lending.appraisal_disclosures": 500,
            "consumer_lending.military_lending_checks": 500,
            "consumer_lending.high_cost_mortgage_tests": 200,
            "consumer_lending.compliance_exceptions": 200
        })
        print("\nDataGenerator completed successfully!")

    except Exception as e:
        print(f"Error during data generation: {e}")
