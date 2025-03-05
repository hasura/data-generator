from faker import Faker

from fsi_data_generator.fsi_generators.text_list import text_list

fake = Faker()


def credit_cards(_dg):
    return [
        ('credit_cards\\.card_product_reward_categories', '^category_name$', text_list([
            "Dining",
            "Travel",
            "Gas",
            "Groceries",
            "Entertainment",
            "Other"
        ])),
        ('credit_cards\\.card_product_reward_categories', '^cap_period$', text_list([
            "Monthly",
            "Quarterly",
            "Annually"
        ])),
        ('credit_cards\\.applications', '^application_channel$', text_list([
            "Online",
            "Branch",
            "Mail",
            "Phone"
        ])),
        ('credit_cards\\.applications', '^status$', text_list([
            "Pending",
            "Approved",
            "Denied",
            "Canceled"
        ])),
        ('credit_cards\\.applications', '^decision_method$', text_list([
            "Automated",
            "Manual"
        ])),
        ('credit_cards\\.applications', '^employment_status$', text_list([
            "Employed",
            "Self-employed",
            "Unemployed",
            "Retired",
            "Student"
        ])),
        ('credit_cards\\.card_accounts', '^status$', text_list([
            "Active",
            "Inactive",
            "Closed",
            "Suspended"
        ])),
        ('credit_cards\\.cards', '^user_type$', text_list([
            "Primary",
            "Authorized User"
        ])),
        ('credit_cards\\.cards', '^card_status$', text_list([
            "Active",
            "Inactive",
            "Lost",
            "Stolen",
            "Expired",
            "Replaced"
        ])),
        ('credit_cards\\.authorized_users', '^relationship$', text_list([
            "Spouse",
            "Parent",
            "Child",
            "Sibling",
            "Other"
        ])),
        ('credit_cards\\.authorized_users', '^status$', text_list([
            "Active",
            "Removed"
        ])),
        ('credit_cards\\.transactions', '^transaction_type$', text_list([
            "Purchase",
            "Cash Advance",
            "Balance Transfer",
            "Payment",
            "Fee",
            "Adjustment"
        ])),
        ('credit_cards\\.transactions', '^status$', text_list([
            "Approved",
            "Declined",
            "Reversed",
            "Disputed"
        ])),
        ('credit_cards\\.fees', '^fee_type$', text_list([
            "Annual",
            "Late Payment",
            "Cash Advance",
            "Foreign Transaction",
            "Balance Transfer",
            "Overlimit",
            "Returned Payment"
        ])),
        ('credit_cards\\.interest_charges', '^interest_type$', text_list([
            "Purchase",
            "Cash Advance",
            "Balance Transfer",
            "Penalty"
        ])),
        ('credit_cards\\.rewards', '^reward_type$', text_list([
            "Points",
            "Cashback",
            "Miles"
        ])),
        ('credit_cards\\.rewards', '^event_type$', text_list([
            "Earned",
            "Bonus",
            "Redeemed",
            "Expired",
            "Adjusted"
        ])),
        ('credit_cards\\.reward_redemptions', '^redemption_type$', text_list([
            "Cashback",
            "Travel",
            "Gift Card",
            "Merchandise",
            "Statement Credit"
        ])),
        ('credit_cards\\.reward_redemptions', '^status$', text_list([
            "Pending",
            "Completed",
            "Canceled"
        ])),
        ('credit_cards\\.promotional_offers', '^offer_type$', text_list([
            "Balance Transfer",
            "Cash Advance",
            "Credit Limit Increase",
            "Rewards Bonus",
            "Introductory Rate"
        ])),
        ('credit_cards\\.promotional_offers', '^status$', text_list([
            "Active",
            "Accepted",
            "Declined",
            "Expired"
        ])),
        ('credit_cards\\.balance_transfers', '^status$', text_list([
            "Pending",
            "Completed",
            "Rejected"
        ])),
        ('credit_cards\\.payment_methods', '^payment_type$', text_list([
            "Bank Account",
            "Debit Card",
            "Check"
        ])),
        ('credit_cards\\.payment_methods', '^status$', text_list([
            "Active",
            "Inactive",
            "Removed"
        ])),
        ('credit_cards\\.payment_methods', '^verification_status$', text_list([
            "Verified",
            "Pending",
            "Failed"
        ])),
        ('credit_cards\\.autopay_settings', '^status$', text_list([
            "Active",
            "Inactive"
        ])),
        ('credit_cards\\.autopay_settings', '^payment_option$', text_list([
            "Minimum",
            "Statement Balance",
            "Current Balance",
            "Fixed Amount"
        ])),
        ('credit_cards\\.autopay_settings', '^payment_day$', text_list([
            "Due Date",
            "Days Before Due Date",
            "Specific Day"
        ])),
        ('credit_cards\\.credit_limit_changes', '^change_reason$', text_list([
            "Credit Limit Increase",
            "Credit Limit Decrease",
            "Automatic Increase",
            "Customer Request",
            "Risk Management",
            "Other"
        ])),
        ('credit_cards\\.credit_limit_changes', '^requested_by$', text_list([
            "Customer",
            "Bank"
        ])),
        ('credit_cards\\.card_alerts', '^alert_type$', text_list([
            "Payment Due",
            "Payment Posted",
            "Purchase",
            "Credit Limit",
            "Fraud"
        ])),
        ('credit_cards\\.card_alerts', '^delivery_method$', text_list([
            "Email",
            "SMS",
            "Push"
        ])),
        ('credit_cards\\.disputed_transactions', '^dispute_reason$', text_list([
            "Fraud",
            "Product Issue",
            "Duplicate Charge",
            "Billing Error",
            "Other"
        ])),
        ('credit_cards\\.disputed_transactions', '^status$', text_list([
            "Filed",
            "Processing",
            "Resolved",
            "Declined"
        ])),
        ('credit_cards\\.disputed_transactions', '^resolution$', text_list([
            "Customer Favor",
            "Merchant Favor"
        ])),
        ('credit_cards\\.fraud_cases', '^case_type$', text_list([
            "Card Fraud",
            "Account Takeover",
            "Application Fraud"
        ])),
        ('credit_cards\\.fraud_cases', '^status$', text_list([
            "Open",
            "Investigation",
            "Closed"
        ])),
        ('credit_cards\\.fraud_cases', '^reported_by$', text_list([
            "Customer",
            "Bank",
            "Merchant"
        ])),
        ('credit_cards\\.security_blocks', '^block_type$', text_list([
            "Temporary",
            "Permanent",
            "Geographic"
        ])),
        ('credit_cards\\.security_blocks', '^requested_by$', text_list([
            "Customer",
            "Bank",
            "Fraud System"
        ])),
        ('credit_cards\\.security_blocks', '^status$', text_list([
            "Active",
            "Removed"
        ])),
        ('credit_cards\\.credit_card_applications_hmda', '^hoepa_status$', text_list([
            "Yes",
            "No"
        ])),
        ('credit_cards\\.credit_card_applications_hmda', '^action_taken$', text_list([
            "Approved",
            "Denied",
            "Withdrawn",
            "Incomplete"
        ])),
        ('credit_cards\\.credit_card_applications_hmda', '^submission_status$', text_list([
            "PENDING",
            "SUBMITTED",
            "ACCEPTED",
            "REJECTED"
        ])),
        ('credit_cards\\.reg_z_credit_card_disclosures', '^disclosure_type$', text_list([
            "Solicitation",
            "Application",
            "Account-Opening",
            "Periodic Statement"
        ])),
        ('credit_cards\\.reg_z_credit_card_disclosures', '^delivery_method$', text_list([
            "Mail",
            "Electronic"
        ])),
        ('credit_cards\\.ability_to_pay_assessments', '^income_source$', text_list([
            "Paystub",
            "Tax Return",
            "Bank Statement",
            "Employer Verification",
            "Other"
        ])),
        ('credit_cards\\.consumer_complaints', '^source$', text_list([
            "Direct",
            "CFPB",
            "BBB",
            "Social Media"
        ])),
        ('credit_cards\\.consumer_complaints', '^complaint_type$', text_list([
            "Billing",
            "Fees",
            "Interest",
            "Customer Service",
            "Fraud",
            "Rewards",
            "Other"
        ])),
        ('credit_cards\\.consumer_complaints', '^status$', text_list([
            "New",
            "In Progress",
            "Resolved"
        ])),
        ('credit_cards\\.security_blocks', '^block_type$', text_list(["Temporary", "Permanent", "Geographic"])),
        ('credit_cards\\.security_blocks', 'requested_by', text_list(["Customer", "Bank", "Fraud System"])),
        ('credit_cards\\.security_blocks', '^status$', text_list(["Active", "Removed"])),
    ]
