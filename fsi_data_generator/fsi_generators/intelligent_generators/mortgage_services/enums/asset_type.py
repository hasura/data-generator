from enum import Enum

import random


class AssetType(str, Enum):
    CHECKING_ACCOUNT = "CHECKING_ACCOUNT"
    SAVINGS_ACCOUNT = "SAVINGS_ACCOUNT"
    MONEY_MARKET = "MONEY_MARKET"
    CERTIFICATE_OF_DEPOSIT = "CERTIFICATE_OF_DEPOSIT"
    BROKERAGE_ACCOUNT = "BROKERAGE_ACCOUNT"
    RETIREMENT_ACCOUNT = "RETIREMENT_ACCOUNT"
    INVESTMENT_PROPERTY = "INVESTMENT_PROPERTY"
    PRIMARY_RESIDENCE = "PRIMARY_RESIDENCE"
    SECONDARY_RESIDENCE = "SECONDARY_RESIDENCE"
    MUTUAL_FUND = "MUTUAL_FUND"
    STOCK_EQUITY = "STOCK_EQUITY"
    BONDS = "BONDS"
    LIFE_INSURANCE = "LIFE_INSURANCE"
    VEHICLE = "VEHICLE"
    BUSINESS_EQUITY = "BUSINESS_EQUITY"
    TRUST_ACCOUNT = "TRUST_ACCOUNT"
    CRYPTOCURRENCY = "CRYPTOCURRENCY"
    OTHER = "OTHER"
    OTHER_REAL_ESTATE = "OTHER_REAL_ESTATE"

    @classmethod
    def get_random(cls):
        """Return a random status value, weighted toward ACTIVE"""
        choices = [income_type for income_type in cls]
        weights = [
            0.15,  # CHECKING_ACCOUNT
            0.15,  # SAVINGS_ACCOUNT
            0.08,  # MONEY_MARKET
            0.05,  # CERTIFICATE_OF_DEPOSIT
            0.08,  # BROKERAGE_ACCOUNT
            0.10,  # RETIREMENT_ACCOUNT
            0.05,  # STOCK_EQUITY
            0.03,  # BONDS
            0.05,  # MUTUAL_FUND
            0.05,  # INVESTMENT_PROPERTY
            0.03,  # PRIMARY_RESIDENCE
            0.02,  # SECONDARY_RESIDENCE
            0.05,  # VEHICLE
            0.03,  # LIFE_INSURANCE
            0.02,  # TRUST_ACCOUNT
            0.02,  # CRYPTOCURRENCY
            0.02,  # BUSINESS_EQUITY
            0.01,  # OTHER
            0.01  # OTHER REAL ESTATE

        ]

        return random.choices(choices, weights=weights, k=1)[0]
