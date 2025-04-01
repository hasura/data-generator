from data_generator import DataGenerator
from typing import Any, Dict

import random


def generate_random_other_product_type(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking other product type with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated other product type data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_product_id' not in id_fields:
        raise ValueError("consumer_banking_product_id is required")

    # Fetch the product to verify it exists
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT product_name, product_type 
            FROM consumer_banking.products 
            WHERE consumer_banking_product_id = %s
        """, (id_fields['consumer_banking_product_id'],))

        product = cursor.fetchone()

        if not product:
            raise ValueError(f"No product found with ID {id_fields['consumer_banking_product_id']}")

        product_name = product.get('product_name')
        product_type = product.get('product_type')

        # Define a set of specialized product types based on the main product type
        specialized_types = {
            "CHECKING": [
                "Interest Checking", "Rewards Checking", "High-Yield Checking",
                "Eco-Friendly Checking", "Digital-Only Checking", "Lifestyle Checking",
                "Cashback Checking", "Zero-Fee Checking", "Round-Up Savings Checking"
            ],
            "SAVINGS": [
                "Goal-Based Savings", "Round-Up Savings", "Education Savings",
                "Emergency Fund Savings", "Holiday Club", "Vacation Savings",
                "Wedding Savings", "Home Down Payment Savings", "Tax Savings"
            ],
            "MONEY_MARKET": [
                "Tiered Money Market", "Premium Money Market", "Relationship Money Market",
                "Business Money Market Plus", "Investment Money Market", "Flex Money Market"
            ],
            "CERTIFICATE_OF_DEPOSIT": [
                "Step-Up CD", "Bump-Up CD", "Market-Linked CD", "Callable CD",
                "No-Penalty CD", "Jumbo CD", "Add-On CD", "Zero-Coupon CD"
            ],
            "IRA": [
                "Traditional IRA", "Roth IRA", "SEP IRA", "SIMPLE IRA",
                "Rollover IRA", "Inherited IRA", "Self-Directed IRA"
            ],
            "HSA": [
                "Standard HSA", "Investment HSA", "Family HSA", "Premium HSA"
            ],
            "STUDENT": [
                "College Student Checking", "Graduate Student Banking", "Study Abroad Banking",
                "First-Year Student Account", "Student Rewards Banking", "Campus Card Linked"
            ],
            "YOUTH": [
                "Kids Club Savings", "Teen Account", "Minor Trust Account",
                "Custodial Savings", "Junior Investor", "Education Savings"
            ],
            "SPECIALIZED": [
                "Medical Professional Banking", "Legal Professional Banking", "First Responder Banking",
                "Military Banking", "Non-Profit Banking", "Religious Organization Banking",
                "Real Estate Professional Banking", "Artist Banking", "Gig Economy Banking"
            ]
        }

        # Default specialized types (used if the product type doesn't match known categories)
        default_specialized_types = [
            "Flex Banking", "VIP Banking", "Premium Banking", "Select Banking",
            "Digital Banking", "Signature Banking", "Custom Banking", "Elite Banking"
        ]

        # Choose a specialized product type name
        if product_type in specialized_types:
            specialized_name = random.choice(specialized_types[product_type])
        else:
            specialized_name = random.choice(default_specialized_types)

        # Generate longer description based on the specialized name
        descriptions = {
            # Checking account specialized descriptions
            "Interest Checking": "A checking account that earns interest on balances, combining the convenience of a checking account with the earning potential of a savings account.",
            "Rewards Checking": "A checking account that offers rewards like cashback, points, or miles based on account activity and debit card usage.",
            "High-Yield Checking": "A premium checking account that offers higher interest rates for maintaining larger balances or meeting certain qualifying activities.",
            "Eco-Friendly Checking": "An environmentally conscious checking account with paperless statements, digital receipts, and contributions to environmental causes.",
            "Digital-Only Checking": "A fully digital checking experience with enhanced online and mobile banking features and no physical branch requirements.",
            "Lifestyle Checking": "A checking account with benefits and perks tailored to specific lifestyle preferences or interests.",
            "Cashback Checking": "A checking account that returns a percentage of debit card purchases as cash rewards to the customer.",
            "Zero-Fee Checking": "A checking account with no monthly maintenance fees, minimum balance requirements, or transaction fees.",
            "Round-Up Savings Checking": "A checking account that automatically rounds up transactions to the nearest dollar and deposits the difference into savings.",

            # Savings account specialized descriptions
            "Goal-Based Savings": "A savings account that helps customers track progress toward specific financial goals with visualization tools and milestone rewards.",
            "Round-Up Savings": "A savings program that automatically rounds up transactions from a linked checking account and transfers the difference to savings.",
            "Education Savings": "A specialized savings account designed for educational expenses with potential tax advantages and goal tracking features.",
            "Emergency Fund Savings": "A dedicated savings account designed to build and maintain an emergency fund with liquidity and separate tracking.",
            "Holiday Club": "A specialized savings program designed to help customers save for holiday expenses throughout the year.",
            "Vacation Savings": "A savings account specifically designed for vacation planning with travel-related benefits and spending tools.",
            "Wedding Savings": "A specialized savings account for wedding expenses with planning tools and potential vendor discounts.",
            "Home Down Payment Savings": "A savings account designed to help customers save for a home down payment with progress tracking and potential mortgage benefits.",
            "Tax Savings": "A specialized savings account for setting aside funds for future tax payments with automatic calculation assistance.",

            # Money Market specialized descriptions
            "Tiered Money Market": "A money market account with interest rates that increase at predetermined balance thresholds, encouraging higher deposits.",
            "Premium Money Market": "A high-balance money market account with enhanced interest rates and additional banking perks and privileges.",
            "Relationship Money Market": "A money market account with rate benefits based on the customer's overall relationship with the bank.",
            "Business Money Market Plus": "A business-focused money market account with enhanced cash management tools and competitive rates.",
            "Investment Money Market": "A money market account with integrated investment options and automatic sweep features.",
            "Flex Money Market": "A versatile money market account with adjustable terms and flexible access options based on customer needs.",

            # CD specialized descriptions
            "Step-Up CD": "A certificate of deposit that automatically increases the interest rate at predetermined intervals throughout the term.",
            "Bump-Up CD": "A CD that allows the customer to request a rate increase once during the term if market rates rise.",
            "Market-Linked CD": "A CD that ties returns to the performance of a market index while protecting the principal investment.",
            "Callable CD": "A higher-rate CD that the bank may redeem early after an initial locked period if interest rates fall significantly.",
            "No-Penalty CD": "A flexible CD that allows early withdrawal of funds without penalty after an initial grace period.",
            "Jumbo CD": "A high-balance certificate of deposit offering premium interest rates for substantial deposits.",
            "Add-On CD": "A flexible CD that allows additional deposits throughout the term while maintaining a guaranteed rate.",
            "Zero-Coupon CD": "A discounted CD purchased below face value that matures to full value at the end of the term.",

            # IRA specialized descriptions
            "Traditional IRA": "A tax-deferred individual retirement account with potential tax-deductible contributions and earnings taxed upon withdrawal.",
            "Roth IRA": "A retirement account funded with after-tax dollars offering tax-free growth and qualified tax-free withdrawals.",
            "SEP IRA": "A simplified employee pension plan allowing employers to contribute to traditional IRAs for employees and themselves.",
            "SIMPLE IRA": "A savings incentive match plan allowing employee and employer contributions for small businesses with fewer than 100 employees.",
            "Rollover IRA": "An account specifically designed to receive funds transferred from a previous employer's retirement plan.",
            "Inherited IRA": "A retirement account established when someone inherits IRA assets after the original owner's death.",
            "Self-Directed IRA": "An IRA allowing greater control over investment decisions with a wider range of alternative investment options.",

            # HSA specialized descriptions
            "Standard HSA": "A basic health savings account offering tax advantages for qualified medical expenses with a debit card for ease of use.",
            "Investment HSA": "A health savings account with investment options allowing account holders to invest funds above a specified threshold.",
            "Family HSA": "A health savings account optimized for family coverage with higher contribution limits and family-focused features.",
            "Premium HSA": "An enhanced health savings account with additional tools, resources, and potential preferential rates.",

            # Student specialized descriptions
            "College Student Checking": "A checking account specifically designed for college students with campus-related benefits and financial education tools.",
            "Graduate Student Banking": "A banking package tailored to graduate students with benefits like loan refinancing options and career resources.",
            "Study Abroad Banking": "A student account with international banking benefits like foreign ATM fee rebates and currency exchange services.",
            "First-Year Student Account": "A starter banking account for first-year college students with guided banking tools and educational resources.",
            "Student Rewards Banking": "A student-focused account that offers rewards for academic achievement and financial responsibility.",
            "Campus Card Linked": "A student account linked to campus ID card for seamless integration with university services and payments.",

            # Youth specialized descriptions
            "Kids Club Savings": "An educational savings account for children with age-appropriate financial literacy tools and incentives.",
            "Teen Account": "A transitional banking account for teenagers with parental oversight and progressive financial independence features.",
            "Minor Trust Account": "A custodial account held for a minor by a trustee until the minor reaches a specified age.",
            "Custodial Savings": "A savings account managed by an adult custodian for the benefit of a minor until age of majority.",
            "Junior Investor": "A youth account with basic investment education and monitored investment opportunities.",

            # Specialized descriptions
            "Medical Professional Banking": "A comprehensive banking package designed for healthcare professionals with benefits like loan discounts and practice financing options.",
            "Legal Professional Banking": "Banking services tailored to the needs of legal professionals with trust account management and firm-specific services.",
            "First Responder Banking": "Specialized banking benefits for first responders including emergency access features and service recognition benefits.",
            "Military Banking": "Banking services designed for active duty, reserve, and veteran military personnel with deployment support and relocation services.",
            "Non-Profit Banking": "Banking solutions for non-profit organizations with specialized fee structures and donation processing capabilities.",
            "Religious Organization Banking": "Banking services customized for religious organizations with donation management and community outreach support.",
            "Real Estate Professional Banking": "Banking solutions for real estate professionals with commission management and client escrow services.",
            "Artist Banking": "Banking services tailored to artists and creative professionals with irregular income management tools and career support resources.",
            "Gig Economy Banking": "Banking designed for independent contractors and gig workers with variable income management and tax assistance tools.",

            # Default specialized descriptions
            "Flex Banking": "A customizable banking experience allowing customers to select features and benefits that match their specific needs and preferences.",
            "VIP Banking": "An exclusive banking package for high-value customers offering personalized service and premium benefits across all banking products.",
            "Premium Banking": "An enhanced banking experience with preferential rates, reduced fees, and dedicated customer service for qualifying customers.",
            "Select Banking": "A relationship-based banking package with benefits that increase based on the customer's overall banking relationship.",
            "Digital Banking": "A technology-forward banking experience with advanced digital tools, biometric security, and integrated financial management features.",
            "Signature Banking": "A distinguished banking relationship with personalized service, exclusive benefits, and invitations to special bank events.",
            "Custom Banking": "A highly adaptable banking solution allowing for tailored terms, conditions, and features based on individual customer needs.",
            "Elite Banking": "A top-tier banking package with maximum benefits, minimum restrictions, and white-glove service for the bank's most valued customers."
        }

        # Use default description if the specialized name is not in the descriptions dictionary
        description = descriptions.get(specialized_name,
                                       f"A specialized version of the {product_name} with enhanced features and benefits tailored to specific customer needs.")

        # Create the other product type dictionary
        other_product_type = {
            "consumer_banking_product_id": id_fields['consumer_banking_product_id'],
            "name": specialized_name,
            "description": description
        }

        return other_product_type

    finally:
        cursor.close()
