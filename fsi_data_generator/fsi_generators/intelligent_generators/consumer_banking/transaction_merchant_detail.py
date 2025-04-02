from .enums import TransactionCategory, TransactionType
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict, Optional

import random


def generate_random_transaction_merchant_detail(id_fields: Dict[str, Any], dg: DataGenerator) -> Optional[
    Dict[str, Any]]:
    """
    Generate a random transaction merchant detail with plausible values.
    May return None if the transaction type doesn't typically have merchant details.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction merchant detail data, or None
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_transaction_id' not in id_fields:
        raise ValueError("consumer_banking_transaction_id is required")

    # Fetch the transaction to verify it exists and get transaction type
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT transaction_type, category, description, amount 
            FROM consumer_banking.transactions 
            WHERE consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        transaction = cursor.fetchone()

        if not transaction:
            raise ValueError(f"No transaction found with ID {id_fields['consumer_banking_transaction_id']}")

        transaction_type = transaction.get('transaction_type')
        transaction_category = transaction.get('category')
        transaction_description = transaction.get('description')
        transaction_amount = transaction.get('amount')

        # Determine if this transaction type typically has merchant details
        # These types usually don't have merchant details
        non_merchant_types = [
            TransactionType.INTERNAL_TRANSFER.value,
            TransactionType.EXTERNAL_TRANSFER.value,
            TransactionType.SALARY.value,
            TransactionType.DIVIDEND.value,
            TransactionType.TAX_REFUND.value,
            TransactionType.INVESTMENT.value
        ]

        # These categories usually don't have merchant details
        non_merchant_categories = [
            TransactionCategory.INTEREST.value,
            TransactionCategory.FEE.value,
            TransactionCategory.ADJUSTMENT.value,
            TransactionCategory.TRANSFER.value,
        ]

        selected_category = None

        # Decide if this transaction should have merchant details
        # If it's a type that typically doesn't have merchant details, 80% chance of no merchant details
        if transaction_type in non_merchant_types and random.random() < 0.8:
            raise SkipRowGenerationError

        # If it's a category that typically doesn't have merchant details, 80% chance of no merchant details
        if transaction_category in non_merchant_categories and random.random() < 0.8:
            raise SkipRowGenerationError

        # Even for other transactions, there's a small chance (5%) they don't have merchant details
        # This helps simulate incomplete or missing data in real-world scenarios
        if random.random() < 0.05:
            raise SkipRowGenerationError

        # Use existing description if available, otherwise generate merchant info
        if transaction_description and len(transaction_description.strip()) > 0:
            merchant_name = transaction_description
        else:
            # Generate merchant name based on transaction type and category
            merchant_prefixes = [
                "American", "National", "Global", "City", "Metro", "United", "Express",
                "Royal", "Premier", "Pacific", "Atlantic", "European", "Eastern", "Western",
                "Northern", "Southern", "Central", "Digital", "Modern", "Classic"
            ]

            merchant_suffixes = [
                "Store", "Market", "Eatery", "Station", "Airlines", "Lodging", "Service",
                "Center", "Care", "Institute", "Provider", "Agency", "Shop", "Outlet",
                "Emporium", "Depot", "Express", "Plus", "Direct", "Prime"
            ]

            # Select appropriate merchant category based on transaction type
            if transaction_type == TransactionType.PURCHASE.value:
                if transaction_amount < 20:
                    likely_categories = ["Retail", "Grocery", "Restaurant", "Cafe", "Gas", "Pharmacy"]
                elif transaction_amount < 100:
                    likely_categories = ["Retail", "Grocery", "Restaurant", "Gas", "Electronics", "Clothing"]
                else:
                    likely_categories = ["Electronics", "Department", "Financial", "Auto", "Travel", "Hotel"]

                selected_category = random.choice(likely_categories)
            elif transaction_type == TransactionType.CASH_WITHDRAWAL.value:
                selected_category = "Financial"
            elif transaction_type == TransactionType.BILL_PAYMENT.value:
                selected_category = "Financial"
            elif transaction_type == TransactionType.FOOD_DINING.value:
                selected_category = "Restaurant"
            elif transaction_type == TransactionType.RETAIL.value:
                selected_category = "Retail"
            elif transaction_type == TransactionType.TRAVEL.value:
                selected_category = random.choice(["Airline", "Hotel", "Travel"])
            elif transaction_type == TransactionType.ENTERTAINMENT.value:
                selected_category = "Entertainment"
            elif transaction_type == TransactionType.HEALTHCARE.value:
                selected_category = "Healthcare"
            elif transaction_type == TransactionType.SUBSCRIPTION.value:
                selected_category = "Subscription"
            else:
                selected_category = random.choice([
                    "Retail", "Grocery", "Restaurant", "Financial", "Service",
                    "Healthcare", "Travel", "Subscription"
                ])

            # Generate appropriate name based on selected category
            if selected_category == "Restaurant" or selected_category == "Cafe":
                # For restaurants, use more specific naming patterns
                restaurant_names = [
                    "Joe's", "Luigi's", "Golden Dragon", "Taj Mahal", "El Mariachi",
                    "Big River", "Sunset", "Olive Tree", "Sakura", "The Burger Joint",
                    "Corner Bistro", "Blue Plate", "Green Kitchen", "Red Lobster", "China Garden"
                ]
                restaurant_types = [
                    "Restaurant", "Grill", "Diner", "Cafe", "Bistro", "Kitchen", "Eatery",
                    "Bar & Grill", "Steakhouse", "Pizzeria", "Sushi", "Brasserie"
                ]
                merchant_name = f"{random.choice(restaurant_names)} {random.choice(restaurant_types)}"
            elif selected_category == "Financial":
                # For financial institutions, use more formal naming patterns
                financial_names = [
                    "First", "Citizens", "Community", "Capital", "Security", "Trust", "Heritage",
                    "Fidelity", "Liberty", "Prosperity", "Cornerstone", "Landmark", "Summit"
                ]
                financial_types = [
                    "Bank", "Credit Union", "Financial", "Trust", "Savings & Loan", "Investment",
                    "Mutual", "Bancorp", "Banking", "Funding"
                ]
                merchant_name = f"{random.choice(financial_names)} {random.choice(financial_types)}"
            elif selected_category == "Grocery":
                grocery_names = [
                    "Fresh", "Natural", "Organic", "Family", "Super", "Harvest", "Green",
                    "Value", "Quality", "Farmers", "Daily", "Village", "Market"
                ]
                grocery_types = [
                    "Grocery", "Market", "Foods", "Supermarket", "Marketplace", "Farmers Market",
                    "Food Co-op", "Produce", "Provisions"
                ]
                merchant_name = f"{random.choice(grocery_names)} {random.choice(grocery_types)}"
            elif selected_category == "Retail":
                retail_names = [
                    "City", "Metro", "Urban", "Downtown", "Plaza", "Mall", "Gallery",
                    "Outlet", "Center", "Main Street", "Square", "Avenue"
                ]
                retail_types = [
                    "Retail", "Store", "Shop", "Boutique", "Mart", "Emporium", "Department Store",
                    "Outlet", "Shopping Center"
                ]
                merchant_name = f"{random.choice(retail_names)} {random.choice(retail_types)}"
            else:
                # General merchant name pattern
                prefix = random.choice(merchant_prefixes)
                suffix = random.choice(merchant_suffixes)

                # Make sure the suffix is appropriate for the category
                merchant_name = f"{prefix} {selected_category} {suffix}".strip()

        # Define merchant category codes
        mcc_mapping = {
            "Retail": "5411",  # Retail stores
            "Grocery": "5411",  # Grocery stores
            "Restaurant": "5812",  # Restaurants
            "Gas": "5542",  # Gas stations
            "Airline": "4511",  # Airlines
            "Hotel": "7011",  # Hotels and lodging
            "Auto": "7538",  # Auto service and repair
            "Entertainment": "7832",  # Movie theaters
            "Healthcare": "8099",  # Health services
            "Education": "8299",  # Educational services
            "Utilities": "4900",  # Utilities
            "Telecom": "4814",  # Telecommunications
            "Financial": "6012",  # Financial institutions
            "Insurance": "6300",  # Insurance
            "Government": "9399",  # Government services
            "Travel": "4722",  # Travel agencies
            "Department": "5311",  # Department stores
            "Clothing": "5651",  # Clothing stores
            "Electronics": "5732",  # Electronics stores
            "Furniture": "5712",  # Furniture stores
            "Hardware": "5251",  # Hardware stores
            "Pharmacy": "5912",  # Drug stores and pharmacies
            "Online": "5999",  # Online retailers
            "Subscription": "5968"  # Subscription services
        }

        # Determine merchant category code
        # Try to match merchant name to an appropriate category
        merchant_name_lower = merchant_name.lower()
        merchant_category_code = None

        # First try to match based on transaction type
        if transaction_type == TransactionType.FOOD_DINING.value:
            merchant_category_code = mcc_mapping["Restaurant"]
        elif transaction_type == TransactionType.RETAIL.value:
            merchant_category_code = mcc_mapping["Retail"]
        elif transaction_type == TransactionType.HEALTHCARE.value:
            merchant_category_code = mcc_mapping["Healthcare"]
        elif transaction_type == TransactionType.EDUCATION.value:
            merchant_category_code = mcc_mapping["Education"]
        elif transaction_type == TransactionType.ENTERTAINMENT.value:
            merchant_category_code = mcc_mapping["Entertainment"]
        elif transaction_type == TransactionType.TRAVEL.value:
            merchant_category_code = mcc_mapping["Travel"]
        elif transaction_type == TransactionType.SUBSCRIPTION.value:
            merchant_category_code = mcc_mapping["Subscription"]
        elif transaction_type == TransactionType.UTILITY_PAYMENT.value:
            merchant_category_code = mcc_mapping["Utilities"]
        elif transaction_type == TransactionType.INSURANCE_PREMIUM.value:
            merchant_category_code = mcc_mapping["Insurance"]
        elif transaction_type == TransactionType.CASH_WITHDRAWAL.value:
            merchant_category_code = mcc_mapping["Financial"]
        elif transaction_type == TransactionType.BILL_PAYMENT.value:
            merchant_category_code = mcc_mapping["Financial"]

        # If no match based on transaction type, try merchant name
        if not merchant_category_code:
            if "restaurant" in merchant_name_lower or "cafe" in merchant_name_lower or "diner" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Restaurant"]
            elif "grocery" in merchant_name_lower or "market" in merchant_name_lower or "food" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Grocery"]
            elif "gas" in merchant_name_lower or "petrol" in merchant_name_lower or "fuel" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Gas"]
            elif "air" in merchant_name_lower or "airline" in merchant_name_lower or "flight" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Airline"]
            elif "hotel" in merchant_name_lower or "lodging" in merchant_name_lower or "inn" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Hotel"]
            elif "bank" in merchant_name_lower or "financial" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Financial"]
            elif "health" in merchant_name_lower or "medical" in merchant_name_lower or "doctor" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Healthcare"]
            elif "school" in merchant_name_lower or "college" in merchant_name_lower or "university" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Education"]
            elif "cloth" in merchant_name_lower or "apparel" in merchant_name_lower or "fashion" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Clothing"]
            elif "electronic" in merchant_name_lower or "tech" in merchant_name_lower or "digital" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Electronics"]
            elif "online" in merchant_name_lower or "web" in merchant_name_lower or "internet" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Online"]
            elif "subscription" in merchant_name_lower or "service" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Subscription"]
            elif "movie" in merchant_name_lower or "theater" in merchant_name_lower or "cinema" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Entertainment"]
            elif "utility" in merchant_name_lower or "power" in merchant_name_lower or "water" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Utilities"]
            elif "insurance" in merchant_name_lower:
                merchant_category_code = mcc_mapping["Insurance"]

        # If still no match, use one based on selected category or a default
        if not merchant_category_code:
            if selected_category in mcc_mapping:
                merchant_category_code = mcc_mapping[selected_category]
            else:
                # Default to retail if no other matches
                merchant_category_code = mcc_mapping["Retail"]

        # Create the transaction merchant detail dictionary
        merchant_detail = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "merchant_name": merchant_name,
            "merchant_category_code": merchant_category_code
        }

        return merchant_detail

    finally:
        cursor.close()
