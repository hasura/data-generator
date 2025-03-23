import random

import numpy as np


def generate_fake_balance(product_type):
    """
    Generates a fake balance for the given product type.

    :param product_type: Type of banking product (e.g., "CHECKING", "SAVINGS").
    :return: A fake balance (float).
    """
    if product_type == "CHECKING":
        # Checking accounts typically have $100–$10,000 in balances
        return round(np.random.lognormal(mean=8, sigma=0.4), 2)
    elif product_type == "SAVINGS":
        # Savings accounts typically have $1,000–$50,000 in balances
        return round(np.random.lognormal(mean=9, sigma=0.5), 2)
    elif product_type == "MONEY_MARKET_ACCOUNT":
        # Money Market Accounts range from $5,000–$100,000+
        return round(np.random.lognormal(mean=10, sigma=0.6), 2)
    elif product_type == "INDIVIDUAL_RETIREMENT_ACCOUNT":
        # IRAs typically hold $10,000–$500,000+
        return round(np.random.lognormal(mean=11, sigma=0.7), 2)
    elif product_type == "HEALTH_SAVINGS_ACCOUNT":
        # HSAs have lower balances, typically $500–$10,000
        return round(random.uniform(500, 10000), 2)
    elif product_type == "CERTIFICATE_OF_DEPOSIT":
        # CDs typically fixed $1,000–$500,000+
        return round(np.random.lognormal(mean=10.5, sigma=0.5), 2)
    elif product_type == "DEBIT_CARD":
        # Debit cards tied to linked accounts typically have $50–$5,000
        return round(random.uniform(50, 5000), 2)
    elif product_type == "PREPAID_CARD":
        # Prepaid cards typically hold $10–$1,000
        return round(random.uniform(10, 1000), 2)
    elif product_type == "TRUST_SERVICE":
        # Trust services handle large sums, $50,000–$10,000,000
        return round(np.random.lognormal(mean=13, sigma=0.8), 2)
    else:
        raise ValueError(f"Unknown product type: {product_type}")


def generate_fake_transaction(product_type, balance=None):
    """
    Generates a fake transaction amount for the given product type.

    :param product_type: Type of banking product (e.g., "CHECKING", "SAVINGS").
    :param balance: Account balance (optional; if provided, scales transaction size).
    :return: A fake transaction amount (float, can be negative for withdrawals).
    """
    if product_type == "CHECKING":
        # Transactions: mostly small ($5–$500), frequent
        transaction = round(random.uniform(5, min(balance * 0.25 if balance else 500, 500)), 2)
    elif product_type == "SAVINGS":
        # Transactions: less frequent, larger ($50–$2,500)
        transaction = round(random.uniform(50, min(balance * 0.1 if balance else 2500, 2500)), 2)
    elif product_type == "MONEY_MARKET_ACCOUNT":
        # Transactions: high-value ($500–$10,000)
        transaction = round(random.uniform(500, min(balance * 0.2 if balance else 10000, 10000)), 2)
    elif product_type == "INDIVIDUAL_RETIREMENT_ACCOUNT":
        # Transactions: large, rare ($1,000–$25,000)
        transaction = round(random.uniform(1000, min(balance * 0.05 if balance else 25000, 25000)), 2)
    elif product_type == "HEALTH_SAVINGS_ACCOUNT":
        # Transactions: frequent small payments ($10–$1,000)
        transaction = round(random.uniform(10, min(balance * 0.2 if balance else 1000, 1000)), 2)
    elif product_type == "CERTIFICATE_OF_DEPOSIT":
        # CDs typically have no transactions, simulate interest or rare withdrawals ($0–$5,000)
        transaction = round(random.uniform(0, min(balance * 0.01 if balance else 5000, 5000)), 2)
    elif product_type == "DEBIT_CARD":
        # Transactions: frequent, small ($5–$300)
        transaction = round(random.uniform(5, min(balance * 0.5 if balance else 300, 300)), 2)
    elif product_type == "PREPAID_CARD":
        # Transactions: frequent, small ($1–$200)
        transaction = round(random.uniform(1, min(balance * 0.8 if balance else 200, 200)), 2)
    elif product_type == "TRUST_SERVICE":
        # Trust transactions: rare but large ($10,000–$500,000)
        transaction = round(random.uniform(10000, min(balance * 0.05 if balance else 500000, 500000)), 2)
    else:
        raise ValueError(f"Unknown product type: {product_type}")

    # Randomize transaction direction (negative for withdrawals, positive for deposits)
    if random.random() > 0.5:
        transaction = -transaction  # Withdrawals are negative

    return transaction
