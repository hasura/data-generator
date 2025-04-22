CREATE SCHEMA "enterprise";

CREATE SCHEMA "consumer_banking";

CREATE SCHEMA "mortgage_services";

CREATE SCHEMA "consumer_lending";

CREATE SCHEMA "security";

CREATE SCHEMA "app_mgmt";

CREATE SCHEMA "credit_cards";

CREATE SCHEMA "small_business_banking";

CREATE SCHEMA "data_quality";

CREATE TYPE "enterprise"."currency_code" AS ENUM (
  'USD',
  'EUR',
  'GBP',
  'JPY',
  'AUD',
  'CAD',
  'CHF',
  'CNY',
  'HKD',
  'NZD',
  'SEK',
  'NOK',
  'DKK',
  'SGD',
  'MXN',
  'BRL',
  'INR',
  'RUB',
  'ZAR',
  'TRY',
  'KRW',
  'PLN',
  'ILS',
  'AED',
  'SAR',
  'THB',
  'MYR',
  'IDR',
  'PHP',
  'ARS'
);

CREATE TYPE "enterprise"."identifier_scheme" AS ENUM (
  'IBAN',
  'BIC',
  'ACCOUNT_NUMBER',
  'ROUTING_NUMBER',
  'SORT_CODE',
  'CREDIT_CARD',
  'CLABE',
  'BSB',
  'IFSC',
  'CNAPS',
  'LEI',
  'TAX_ID',
  'CIF',
  'DDA',
  'PROPRIETARY',
  'PASSPORT',
  'DRIVERS_LICENSE',
  'NATIONAL_ID',
  'OTHER'
);

CREATE TYPE "enterprise"."citizenship_status" AS ENUM (
  'US_CITIZEN',
  'US_PERMANENT_RESIDENT',
  'US_TEMPORARY_RESIDENT',
  'NON_RESIDENT_ALIEN',
  'FOREIGN_NATIONAL',
  'DUAL_CITIZEN_US',
  'REFUGEE_ASYLEE',
  'TEMPORARY_PROTECTED_STATUS',
  'DACA_RECIPIENT',
  'UNDOCUMENTED',
  'NOT_SPECIFIED'
);

CREATE TYPE "enterprise"."legal_structure" AS ENUM (
  'SOLE_PROPRIETORSHIP',
  'GENERAL_PARTNERSHIP',
  'LIMITED_PARTNERSHIP',
  'LIMITED_LIABILITY_PARTNERSHIP',
  'LIMITED_LIABILITY_COMPANY',
  'C_CORPORATION',
  'S_CORPORATION',
  'PROFESSIONAL_CORPORATION',
  'NONPROFIT_CORPORATION',
  'BENEFIT_CORPORATION',
  'COOPERATIVE',
  'JOINT_VENTURE',
  'TRUST',
  'ESTATE',
  'ASSOCIATION',
  'GOVERNMENT_ENTITY',
  'FOREIGN_ENTITY',
  'NOT_APPLICABLE',
  'OTHER'
);

CREATE TYPE "enterprise"."marital_status" AS ENUM (
  'SINGLE',
  'MARRIED',
  'DOMESTIC_PARTNERSHIP',
  'SEPARATED',
  'DIVORCED',
  'WIDOWED',
  'NOT_SPECIFIED'
);

CREATE TYPE "enterprise"."party_type" AS ENUM (
  'INDIVIDUAL',
  'ORGANIZATION'
);

CREATE TYPE "enterprise"."party_status" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'PENDING',
  'SUSPENDED',
  'DECEASED',
  'DISSOLVED'
);

CREATE TYPE "enterprise"."frequency" AS ENUM (
  'DAILY',
  'WEEKLY',
  'BI_WEEKLY',
  'SEMI_MONTHLY',
  'MONTHLY',
  'QUARTERLY',
  'SEMI_ANNUALLY',
  'ANNUALLY',
  'CUSTOM',
  'IRREGULAR',
  'ONE_TIME',
  'OTHER'
);

CREATE TYPE "enterprise"."party_relationship_type" AS ENUM (
  'POWER_OF_ATTORNEY',
  'GUARDIAN',
  'TRUSTEE',
  'BENEFICIARY',
  'EXECUTOR',
  'CUSTODIAN',
  'AUTHORIZED_USER',
  'BUSINESS_PARTNER',
  'SPOUSE',
  'DEPENDENT',
  'CO_SIGNER',
  'EMPLOYER_EMPLOYEE',
  'AGENT',
  'PARENT_CHILD',
  'SIBLING',
  'CORPORATE_OFFICER',
  'MEMBER',
  'OWNER',
  'OTHER'
);

CREATE TYPE "enterprise"."education_level" AS ENUM (
  'NO_FORMAL_EDUCATION',
  'PRIMARY_EDUCATION',
  'SECONDARY_EDUCATION',
  'VOCATIONAL_TRAINING',
  'ASSOCIATE_DEGREE',
  'BACHELORS_DEGREE',
  'MASTERS_DEGREE',
  'DOCTORATE',
  'PROFESSIONAL_DEGREE',
  'OTHER',
  'UNKNOWN'
);

CREATE TYPE "enterprise"."income_bracket" AS ENUM (
  'UNDER_15K',
  'INCOME_15K_25K',
  'INCOME_25K_35K',
  'INCOME_35K_50K',
  'INCOME_50K_75K',
  'INCOME_75K_100K',
  'INCOME_100K_150K',
  'INCOME_150K_200K',
  'INCOME_200K_250K',
  'INCOME_250K_PLUS',
  'UNKNOWN'
);

CREATE TYPE "enterprise"."occupation_category" AS ENUM (
  'MANAGEMENT',
  'BUSINESS_FINANCIAL',
  'COMPUTER_MATHEMATICAL',
  'ARCHITECTURE_ENGINEERING',
  'SCIENCE',
  'COMMUNITY_SOCIAL_SERVICE',
  'LEGAL',
  'EDUCATION',
  'ARTS_ENTERTAINMENT',
  'HEALTHCARE_PRACTITIONERS',
  'HEALTHCARE_SUPPORT',
  'PROTECTIVE_SERVICE',
  'FOOD_SERVICE',
  'BUILDING_MAINTENANCE',
  'PERSONAL_CARE',
  'SALES',
  'OFFICE_ADMIN',
  'FARMING_FISHING_FORESTRY',
  'CONSTRUCTION',
  'INSTALLATION_MAINTENANCE_REPAIR',
  'PRODUCTION',
  'TRANSPORTATION',
  'MILITARY',
  'RETIRED',
  'STUDENT',
  'HOMEMAKER',
  'UNEMPLOYED',
  'OTHER',
  'UNKNOWN'
);

CREATE TYPE "enterprise"."homeownership_status" AS ENUM (
  'OWNER',
  'MORTGAGED',
  'RENTER',
  'LIVING_WITH_FAMILY',
  'OTHER',
  'UNKNOWN'
);

CREATE TYPE "enterprise"."political_affiliation" AS ENUM (
  'DEMOCRAT',
  'REPUBLICAN',
  'INDEPENDENT',
  'LIBERTARIAN',
  'GREEN',
  'OTHER',
  'NONE',
  'UNKNOWN'
);

CREATE TYPE "enterprise"."family_life_stage" AS ENUM (
  'SINGLE_NO_CHILDREN',
  'COUPLE_NO_CHILDREN',
  'FAMILY_YOUNG_CHILDREN',
  'FAMILY_SCHOOL_CHILDREN',
  'FAMILY_ADULT_CHILDREN',
  'EMPTY_NEST',
  'RETIRED',
  'OTHER',
  'UNKNOWN'
);

CREATE TYPE "enterprise"."lifestyle_segment" AS ENUM (
  'URBAN_PROFESSIONAL',
  'SUBURBAN_FAMILY',
  'RURAL_TRADITIONAL',
  'BUDGET_CONSCIOUS',
  'LUXURY_SEEKER',
  'ECO_CONSCIOUS',
  'TECH_SAVVY',
  'EXPERIENTIAL',
  'HEALTH_FOCUSED',
  'CONVENIENCE_SEEKER',
  'TRADITIONAL_BANKING',
  'DIGITAL_FIRST',
  'COMMUNITY_ORIENTED',
  'CREDIT_REBUILDER',
  'WEALTH_BUILDER',
  'RETIREMENT_FOCUSED',
  'OTHER',
  'UNKNOWN'
);

CREATE TYPE "enterprise"."credit_risk_tier" AS ENUM (
  'SUPER_PRIME',
  'PRIME',
  'NEAR_PRIME',
  'SUBPRIME',
  'DEEP_SUBPRIME',
  'NO_SCORE',
  'UNKNOWN'
);

CREATE TYPE "enterprise"."address_relationship_type" AS ENUM (
  'RESIDENTIAL',
  'MAILING',
  'BUSINESS',
  'BRANCH',
  'BILLING',
  'SHIPPING',
  'LEGAL',
  'SEASONAL',
  'VACATION',
  'PREVIOUS',
  'OTHER'
);

CREATE TYPE "enterprise"."address_type" AS ENUM (
  'HOME',
  'WORK',
  'MAIL',
  'BILL',
  'SHIP'
);

CREATE TYPE "enterprise"."account_status" AS ENUM (
  'ACTIVE',
  'PENDING',
  'INACTIVE',
  'SUSPENDED',
  'DORMANT',
  'FROZEN',
  'CLOSED',
  'ARCHIVED'
);

CREATE TYPE "enterprise"."associate_status" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'PENDING_START',
  'ON_LEAVE',
  'TERMINATED'
);

CREATE TYPE "enterprise"."relationship_status" AS ENUM (
  'EMPLOYEE',
  'CONTRACTOR',
  'CONSULTANT',
  'INTERN',
  'TEMPORARY'
);

CREATE TYPE "enterprise"."operating_unit" AS ENUM (
  'HR',
  'IT',
  'OPS',
  'RISK',
  'LEGAL',
  'CONSUMER_BANKING',
  'CONSUMER_LENDING',
  'SMALL_BUSINESS_BANKING',
  'CREDIT_CARDS',
  'MORTGAGE_SERVICES'
);

CREATE TYPE "enterprise"."building_type" AS ENUM (
  'BRANCH',
  'HEADQUARTERS',
  'OPERATIONS_CENTER',
  'DATA_CENTER',
  'ADMINISTRATIVE',
  'WAREHOUSE',
  'TRAINING_CENTER',
  'DISASTER_RECOVERY',
  'CALL_CENTER',
  'ATM_LOCATION',
  'OTHER'
);

CREATE TYPE "enterprise"."switch_status" AS ENUM (
  'NOT_SWITCHED',
  'SWITCH_COMPLETED'
);

CREATE TYPE "enterprise"."account_category" AS ENUM (
  'PERSONAL',
  'BUSINESS'
);

CREATE TYPE "enterprise"."credit_debit_indicator" AS ENUM (
  'CREDIT',
  'DEBIT'
);

CREATE TYPE "consumer_banking"."account_status" AS ENUM (
  'ACTIVE',
  'PENDING',
  'INACTIVE',
  'SUSPENDED',
  'DORMANT',
  'FROZEN',
  'CLOSED',
  'ARCHIVED'
);

CREATE TYPE "consumer_banking"."consent_status" AS ENUM (
  'PENDING',
  'AUTHORIZED',
  'ACTIVE',
  'SUSPENDED',
  'EXPIRED',
  'REVOKED',
  'TERMINATED',
  'SUPERSEDED',
  'REJECTED',
  'ERROR'
);

CREATE TYPE "consumer_banking"."balance_type" AS ENUM (
  'AVAILABLE',
  'CURRENT',
  'CLOSING',
  'PENDING',
  'BLOCKED',
  'RESERVED',
  'OVERDRAFT',
  'HOLD',
  'INTEREST_BEARING',
  'MINIMUM_REQUIRED',
  'PROJECTED',
  'LEDGER',
  'OTHER'
);

CREATE TYPE "consumer_banking"."balance_sub_type" AS ENUM (
  'INTRA_DAY',
  'OPENING',
  'INTERIM',
  'FORWARD',
  'EXPECTED',
  'AUTHORISED',
  'PREVIOUS_DAY',
  'THRESHOLD',
  'SWEEP',
  'LIMIT',
  'CREDIT_LINE',
  'CUSHION',
  'VALUE_DATED',
  'NET',
  'NONE'
);

CREATE TYPE "consumer_banking"."beneficiary_type" AS ENUM (
  'INDIVIDUAL',
  'ORGANIZATION',
  'GOVERNMENT',
  'TRUST',
  'ESTATE',
  'CHARITY',
  'FINANCIAL_INSTITUTION',
  'MERCHANT',
  'UTILITY',
  'EDUCATIONAL',
  'HEALTHCARE',
  'SELF',
  'OTHER'
);

CREATE TYPE "consumer_banking"."direct_debit_status_code" AS ENUM (
  'ACTIVE',
  'PENDING',
  'CANCELED',
  'SUSPENDED',
  'REJECTED',
  'EXPIRED',
  'COMPLETED',
  'FAILED',
  'ON_HOLD',
  'AMENDED',
  'OTHER'
);

CREATE TYPE "consumer_banking"."direct_debit_classification" AS ENUM (
  'PERSONAL',
  'BUSINESS',
  'CHARITY',
  'HOUSEHOLD',
  'SUBSCRIPTION',
  'UTILITY',
  'INSURANCE',
  'MORTGAGE',
  'LOAN',
  'TAX',
  'OTHER'
);

CREATE TYPE "consumer_banking"."direct_debit_category" AS ENUM (
  'ELECTRICITY',
  'GAS',
  'WATER',
  'INTERNET',
  'PHONE',
  'TV',
  'RENT',
  'MORTGAGE',
  'INSURANCE_HOME',
  'INSURANCE_HEALTH',
  'INSURANCE_LIFE',
  'INSURANCE_AUTO',
  'SUBSCRIPTION_MEDIA',
  'SUBSCRIPTION_SOFTWARE',
  'SUBSCRIPTION_MEMBERSHIP',
  'LOAN_PAYMENT',
  'CREDIT_CARD',
  'CHARITY',
  'TAX_PAYMENT',
  'PENSION',
  'INVESTMENT',
  'EDUCATION',
  'OTHER'
);

CREATE TYPE "consumer_banking"."offer_type" AS ENUM (
  'LOAN',
  'BALANCE_TRANSFER',
  'CREDIT_LIMIT_INCREASE',
  'INTEREST_RATE_REDUCTION',
  'OVERDRAFT',
  'INVESTMENT',
  'SAVINGS',
  'INSURANCE',
  'CASHBACK',
  'REWARDS',
  'PREMIUM_ACCOUNT',
  'FEE_WAIVER',
  'BUNDLE',
  'PREAPPROVAL',
  'PROMOTIONAL',
  'OTHER'
);

CREATE TYPE "consumer_banking"."product_type" AS ENUM (
  'CHECKING',
  'SAVINGS',
  'MONEY_MARKET',
  'CERTIFICATE_OF_DEPOSIT',
  'IRA',
  'HSA',
  'STUDENT',
  'YOUTH',
  'SENIOR',
  'BUSINESS_CHECKING',
  'BUSINESS_SAVINGS',
  'PREMIUM',
  'FOREIGN_CURRENCY',
  'SPECIALIZED'
);

CREATE TYPE "consumer_banking"."interest_calculation_method" AS ENUM (
  'DAILY_BALANCE',
  'AVERAGE_DAILY_BALANCE',
  'MINIMUM_BALANCE',
  'TIERED_RATE',
  'BLENDED_RATE',
  'STEPPED_RATE'
);

CREATE TYPE "consumer_banking"."account_fee_schedule" AS ENUM (
  'STANDARD',
  'REDUCED',
  'WAIVED_WITH_MINIMUM_BALANCE',
  'WAIVED_WITH_DIRECT_DEPOSIT',
  'WAIVED_WITH_RELATIONSHIP',
  'NO_FEE',
  'ACTIVITY_BASED',
  'TIERED'
);

CREATE TYPE "consumer_banking"."product_status" AS ENUM (
  'ACTIVE',
  'GRANDFATHERED',
  'PROMOTIONAL',
  'DISCONTINUED',
  'ARCHIVED',
  'PILOT',
  'SEASONAL'
);

CREATE TYPE "consumer_banking"."scheduled_payment_type" AS ENUM (
  'SINGLE',
  'RECURRING',
  'INSTALLMENT',
  'CONDITIONAL',
  'VARIABLE'
);

CREATE TYPE "consumer_banking"."scheduled_payment_status" AS ENUM (
  'PENDING',
  'PROCESSING',
  'COMPLETED',
  'FAILED',
  'CANCELED',
  'EXPIRED',
  'RECURRENCE_ENDED',
  'ON_HOLD'
);

CREATE TYPE "consumer_banking"."payment_method" AS ENUM (
  'ACH',
  'WIRE',
  'INTERNAL',
  'CHECK',
  'CARD',
  'DIGITAL_WALLET',
  'OTHER'
);

CREATE TYPE "consumer_banking"."standing_order_status_code" AS ENUM (
  'ACTIVE',
  'PENDING',
  'CANCELLED',
  'SUSPENDED',
  'COMPLETED',
  'FAILED',
  'ON_HOLD',
  'EXPIRED',
  'OTHER'
);

CREATE TYPE "consumer_banking"."standing_order_type" AS ENUM (
  'FIXED_AMOUNT',
  'VARIABLE_AMOUNT',
  'BALANCE_SWEEP',
  'FULL_BALANCE',
  'PERCENTAGE',
  'INTEREST_ONLY',
  'OTHER'
);

CREATE TYPE "consumer_banking"."standing_order_category" AS ENUM (
  'BILL_PAYMENT',
  'SAVINGS',
  'INVESTMENT',
  'LOAN_PAYMENT',
  'SUBSCRIPTION',
  'CHARITY',
  'FAMILY_SUPPORT',
  'RENT',
  'BUSINESS_EXPENSE',
  'OTHER'
);

CREATE TYPE "consumer_banking"."statement_type" AS ENUM (
  'REGULAR',
  'INTERIM',
  'FINAL',
  'ANNUAL',
  'SUPPLEMENTARY',
  'TAX',
  'CORRECTED',
  'RECONCILIATION',
  'CONSOLIDATED',
  'OTHER'
);

CREATE TYPE "consumer_banking"."benefit_type" AS ENUM (
  'CASHBACK',
  'POINTS',
  'MILES',
  'INTEREST',
  'DISCOUNT',
  'INSURANCE',
  'FEE_WAIVER',
  'PROMOTIONAL',
  'LOYALTY',
  'REFERRAL',
  'ANNIVERSARY',
  'OTHER'
);

CREATE TYPE "consumer_banking"."fee_type" AS ENUM (
  'SERVICE',
  'TRANSACTION',
  'OVERDRAFT',
  'ATM',
  'WIRE_TRANSFER',
  'FOREIGN_TRANSACTION',
  'PAPER_STATEMENT',
  'STOP_PAYMENT',
  'REPLACEMENT_CARD',
  'EARLY_WITHDRAWAL',
  'INSUFFICIENT_FUNDS',
  'DORMANT_ACCOUNT',
  'RESEARCH',
  'SPECIAL_STATEMENT',
  'LATE_PAYMENT',
  'OTHER'
);

CREATE TYPE "consumer_banking"."fee_frequency" AS ENUM (
  'ONE_TIME',
  'MONTHLY',
  'QUARTERLY',
  'ANNUALLY',
  'PER_TRANSACTION',
  'CONDITIONAL',
  'OTHER'
);

CREATE TYPE "consumer_banking"."rate_type" AS ENUM (
  'FIXED',
  'VARIABLE',
  'TIERED',
  'PROMOTIONAL',
  'PENALTY',
  'STANDARD',
  'DISCOUNTED',
  'OTHER'
);

CREATE TYPE "consumer_banking"."interest_type" AS ENUM (
  'DEPOSIT',
  'SAVINGS',
  'CERTIFICATE',
  'MONEY_MARKET',
  'CHECKING',
  'BONUS',
  'PROMOTIONAL',
  'PENALTY',
  'LOAN',
  'CREDIT_CARD',
  'OVERDRAFT',
  'LINE_OF_CREDIT',
  'ADJUSTMENT',
  'OTHER'
);

CREATE TYPE "consumer_banking"."amount_type" AS ENUM (
  'OPENING_BALANCE',
  'CLOSING_BALANCE',
  'PAYMENTS',
  'DEPOSITS',
  'WITHDRAWALS',
  'INTEREST_EARNED',
  'INTEREST_CHARGED',
  'FEES',
  'CREDITS',
  'DEBITS',
  'TRANSFERS_IN',
  'TRANSFERS_OUT',
  'MINIMUM_PAYMENT_DUE',
  'AVAILABLE_CREDIT',
  'AVAILABLE_BALANCE',
  'CURRENT_BALANCE',
  'PENDING_BALANCE',
  'OVERDRAFT_LIMIT',
  'OVERDRAFT_USED',
  'OTHER'
);

CREATE TYPE "consumer_banking"."amount_sub_type" AS ENUM (
  'PRINCIPAL',
  'INTEREST',
  'FEES',
  'PENALTIES',
  'REWARDS',
  'PROMOTIONAL',
  'TEMPORARY',
  'ESTIMATED',
  'ADJUSTED',
  'CORRECTED',
  'NONE'
);

CREATE TYPE "consumer_banking"."statement_date_type" AS ENUM (
  'STATEMENT_DATE',
  'DUE_DATE',
  'PAYMENT_CUTOFF_DATE',
  'CLOSE_DATE',
  'NEXT_STATEMENT_DATE',
  'MINIMUM_PAYMENT_DATE',
  'GRACE_PERIOD_END',
  'LATE_FEE_DATE',
  'CYCLE_START_DATE',
  'LAST_PAYMENT_DATE',
  'OTHER'
);

CREATE TYPE "consumer_banking"."statement_rate_type" AS ENUM (
  'APR',
  'CASH_ADVANCE_APR',
  'BALANCE_TRANSFER_APR',
  'PENALTY_APR',
  'PROMOTIONAL_APR',
  'SAVINGS_RATE',
  'CD_RATE',
  'EXCHANGE_RATE',
  'INTRODUCTORY_RATE',
  'VARIABLE_RATE_INDEX',
  'MARGIN',
  'DEFAULT_RATE',
  'REWARD_RATE',
  'EFFECTIVE_RATE',
  'OTHER'
);

CREATE TYPE "consumer_banking"."statement_value_type" AS ENUM (
  'LOYALTY_POINTS',
  'REWARD_BALANCE',
  'CASH_BACK_EARNED',
  'POINTS_EARNED',
  'POINTS_REDEEMED',
  'TIER_LEVEL',
  'CREDIT_SCORE',
  'CARBON_FOOTPRINT',
  'SPENDING_CATEGORY',
  'MILES_EARNED',
  'MILES_BALANCE',
  'MERCHANT_CATEGORY',
  'NEXT_TIER_PROGRESS',
  'ANNUAL_REWARDS_SUMMARY',
  'ANNUAL_SPENDING_SUMMARY',
  'OTHER'
);

CREATE TYPE "consumer_banking"."transaction_status" AS ENUM (
  'PENDING',
  'BOOKED',
  'CANCELLED',
  'REJECTED',
  'REVERSED',
  'HELD',
  'EXPIRED',
  'OTHER'
);

CREATE TYPE "consumer_banking"."transaction_mutability" AS ENUM (
  'MUTABLE',
  'IMMUTABLE',
  'CONDITIONAL'
);

CREATE TYPE "consumer_banking"."transaction_category" AS ENUM (
  'PAYMENT',
  'DEPOSIT',
  'WITHDRAWAL',
  'FEE',
  'INTEREST',
  'TRANSFER',
  'ATM',
  'POINT_OF_SALE',
  'CARD_PAYMENT',
  'DIRECT_DEBIT',
  'STANDING_ORDER',
  'CREDIT',
  'DEBIT',
  'REVERSAL',
  'ADJUSTMENT',
  'CHECK',
  'LOAN_DISBURSEMENT',
  'LOAN_PAYMENT',
  'OTHER'
);

CREATE TYPE "consumer_banking"."transaction_type" AS ENUM (
  'PURCHASE',
  'CASH_WITHDRAWAL',
  'REFUND',
  'BILL_PAYMENT',
  'SALARY',
  'SUBSCRIPTION',
  'DIVIDEND',
  'TAX_PAYMENT',
  'TAX_REFUND',
  'INTERNAL_TRANSFER',
  'EXTERNAL_TRANSFER',
  'MERCHANT_PAYMENT',
  'UTILITY_PAYMENT',
  'RENT_PAYMENT',
  'MORTGAGE_PAYMENT',
  'INVESTMENT',
  'INSURANCE_PREMIUM',
  'DONATION',
  'TRANSPORTATION',
  'FOOD_DINING',
  'HEALTHCARE',
  'EDUCATION',
  'ENTERTAINMENT',
  'TRAVEL',
  'RETAIL',
  'OTHER'
);

CREATE TYPE "consumer_banking"."transaction_bank_code" AS ENUM (
  'RETAIL__CLOTHING_STORE',
  'RETAIL__ELECTRONICS',
  'RETAIL__DEPARTMENT_STORE',
  'RETAIL__ONLINE_SHOPPING',
  'RETAIL__GROCERY',
  'RETAIL__CONVENIENCE_STORE',
  'RETAIL__OTHER',
  'SERVICES__RESTAURANT',
  'SERVICES__ENTERTAINMENT',
  'SERVICES__TRAVEL',
  'SERVICES__CAR_RENTAL',
  'SERVICES__HOTEL',
  'SERVICES__PROFESSIONAL',
  'SERVICES__UTILITIES',
  'SERVICES__TELECOMMUNICATIONS',
  'SERVICES__OTHER',
  'FINANCIAL__ATM_WITHDRAWAL',
  'FINANCIAL__BANK_TRANSFER',
  'FINANCIAL__LOAN_PAYMENT',
  'FINANCIAL__CREDIT_CARD_PAYMENT',
  'FINANCIAL__INVESTMENT',
  'FINANCIAL__INSURANCE_PAYMENT',
  'FINANCIAL__WIRE_TRANSFER',
  'FINANCIAL__OTHER',
  'REGULATORY__BSA_REPORTING',
  'REGULATORY__AML_THRESHOLD',
  'REGULATORY__OFAC_SCREENING',
  'REGULATORY__CTR_REPORT',
  'REGULATORY__SUSPICIOUS_ACTIVITY',
  'REGULATORY__KYC_VERIFICATION',
  'REGULATORY__PEP_TRANSACTION',
  'REGULATORY__SANCTIONS_CHECK',
  'REGULATORY__TAX_REPORTING',
  'REGULATORY__FATCA_REPORTING',
  'REGULATORY__OTHER',
  'RISK__HIGH_RISK_GEO',
  'RISK__UNUSUAL_PATTERN',
  'RISK__VELOCITY_CHECK',
  'RISK__LARGE_CASH_DEPOSIT',
  'RISK__CROSS_BORDER',
  'RISK__FIRST_TIME_MERCHANT',
  'RISK__DEVICE_ANOMALY',
  'RISK__REPEATED_DECLINED',
  'RISK__OTHER'
);

CREATE TYPE "consumer_banking"."card_scheme_name" AS ENUM (
  'VISA',
  'MASTERCARD',
  'AMEX',
  'DISCOVER',
  'DINERS',
  'JCB',
  'UNIONPAY',
  'MAESTRO',
  'INTERAC',
  'ELO',
  'MIR',
  'RUPAY',
  'OTHER'
);

CREATE TYPE "consumer_banking"."authorization_type" AS ENUM (
  'PIN',
  'SIGNATURE',
  'PIN_AND_SIGNATURE',
  'ONLINE',
  'CONTACTLESS',
  'CHIP',
  'MAGNETIC_STRIPE',
  'TOKENIZED',
  'BIOMETRIC',
  'RECURRING',
  'MANUAL_ENTRY',
  'OTHER'
);

CREATE TYPE "consumer_banking"."statement_format" AS ENUM (
  'PDF',
  'HTML',
  'TEXT',
  'CSV',
  'XML',
  'JSON'
);

CREATE TYPE "consumer_banking"."communication_method" AS ENUM (
  'EMAIL',
  'MAIL',
  'PORTAL',
  'MOBILE_APP',
  'SMS_NOTIFICATION',
  'BRANCH_PICKUP',
  'MULTIPLE'
);

CREATE TYPE "consumer_banking"."interaction_type" AS ENUM (
  'PHONE_CALL',
  'EMAIL',
  'CHAT',
  'IN_PERSON',
  'VIDEO_CALL',
  'ONLINE_FORM',
  'SOCIAL_MEDIA',
  'ATM_INTERACTION',
  'MOBILE_APP',
  'MAIL',
  'SMS',
  'FAX'
);

CREATE TYPE "consumer_banking"."interaction_channel" AS ENUM (
  'PHONE',
  'EMAIL',
  'WEB',
  'BRANCH',
  'MOBILE_APP',
  'ATM',
  'MAIL',
  'SOCIAL_MEDIA',
  'VIDEO',
  'SMS',
  'THIRD_PARTY'
);

CREATE TYPE "consumer_banking"."interaction_status" AS ENUM (
  'OPEN',
  'PENDING',
  'IN_PROGRESS',
  'RESOLVED',
  'ESCALATED',
  'TRANSFERRED',
  'CLOSED',
  'FOLLOW_UP',
  'REOPENED'
);

CREATE TYPE "consumer_banking"."interaction_priority" AS ENUM (
  'CRITICAL',
  'HIGH',
  'MEDIUM',
  'LOW',
  'ROUTINE'
);

CREATE TYPE "mortgage_services"."borrower_type" AS ENUM (
  'PRIMARY',
  'CO_BORROWER',
  'GUARANTOR',
  'COSIGNER'
);

CREATE TYPE "mortgage_services"."relationship_type" AS ENUM (
  'SPOUSE',
  'PARENT',
  'CHILD',
  'SIBLING',
  'FRIEND',
  'BUSINESS_PARTNER',
  'OTHER'
);

CREATE TYPE "mortgage_services"."employment_type" AS ENUM (
  'FULL_TIME',
  'PART_TIME',
  'SELF_EMPLOYED',
  'CONTRACTOR',
  'SEASONAL',
  'COMMISSION',
  'RETIRED',
  'UNEMPLOYED',
  'MILITARY',
  'OTHER'
);

CREATE TYPE "mortgage_services"."verification_status" AS ENUM (
  'VERIFIED',
  'PENDING',
  'UNVERIFIED',
  'FAILED',
  'WAIVED',
  'EXPIRED'
);

CREATE TYPE "mortgage_services"."income_type" AS ENUM (
  'SALARY',
  'BONUS',
  'COMMISSION',
  'OVERTIME',
  'SELF_EMPLOYMENT',
  'RENTAL',
  'INVESTMENT',
  'RETIREMENT',
  'PENSION',
  'SOCIAL_SECURITY',
  'DISABILITY',
  'ALIMONY',
  'CHILD_SUPPORT',
  'TRUST',
  'GOVERNMENT_ASSISTANCE',
  'ROYALTIES',
  'OTHER'
);

CREATE TYPE "mortgage_services"."income_frequency" AS ENUM (
  'WEEKLY',
  'BI_WEEKLY',
  'SEMI_MONTHLY',
  'MONTHLY',
  'QUARTERLY',
  'SEMI_ANNUALLY',
  'ANNUALLY',
  'IRREGULAR'
);

CREATE TYPE "mortgage_services"."asset_type" AS ENUM (
  'CHECKING_ACCOUNT',
  'SAVINGS_ACCOUNT',
  'MONEY_MARKET',
  'CERTIFICATE_OF_DEPOSIT',
  'BROKERAGE_ACCOUNT',
  'RETIREMENT_ACCOUNT',
  'INVESTMENT_PROPERTY',
  'PRIMARY_RESIDENCE',
  'SECONDARY_RESIDENCE',
  'OTHER_REAL_ESTATE',
  'MUTUAL_FUND',
  'STOCK_EQUITY',
  'BONDS',
  'LIFE_INSURANCE',
  'VEHICLE',
  'BUSINESS_EQUITY',
  'TRUST_ACCOUNT',
  'CRYPTOCURRENCY',
  'OTHER'
);

CREATE TYPE "mortgage_services"."liability_type" AS ENUM (
  'CREDIT_CARD',
  'AUTO_LOAN',
  'STUDENT_LOAN',
  'PERSONAL_LOAN',
  'MORTGAGE',
  'HOME_EQUITY_LOAN',
  'HOME_EQUITY_LINE_OF_CREDIT',
  'MEDICAL_DEBT',
  'BUSINESS_LOAN',
  'RETAIL_CREDIT',
  'INSTALLMENT_LOAN',
  'PAYDAY_LOAN',
  'TAX_DEBT',
  'OTHER'
);

CREATE TYPE "mortgage_services"."property_type" AS ENUM (
  'SINGLE_FAMILY',
  'CONDO',
  'TOWNHOUSE',
  'MULTI_FAMILY',
  'APARTMENT_BUILDING',
  'MANUFACTURED_HOME',
  'COOPERATIVE',
  'PUD',
  'VACANT_LAND',
  'COMMERCIAL',
  'MIXED_USE',
  'FARM',
  'OTHER'
);

CREATE TYPE "mortgage_services"."occupancy_type" AS ENUM (
  'PRIMARY_RESIDENCE',
  'SECONDARY_RESIDENCE',
  'INVESTMENT',
  'NOT_APPLICABLE'
);

CREATE TYPE "mortgage_services"."application_type" AS ENUM (
  'PURCHASE',
  'REFINANCE',
  'CASH_OUT',
  'CONSTRUCTION',
  'HOME_IMPROVEMENT',
  'RENOVATION',
  'REVERSE_MORTGAGE',
  'JUMBO',
  'FHA',
  'VA',
  'USDA',
  'LAND',
  'OTHER'
);

CREATE TYPE "mortgage_services"."application_status" AS ENUM (
  'DRAFT',
  'SUBMITTED',
  'IN_REVIEW',
  'ADDITIONAL_INFO_REQUIRED',
  'CONDITIONAL_APPROVAL',
  'APPROVED',
  'DENIED',
  'WITHDRAWN',
  'EXPIRED',
  'SUSPENDED'
);

CREATE TYPE "mortgage_services"."loan_purpose" AS ENUM (
  'PRIMARY_RESIDENCE',
  'SECOND_HOME',
  'INVESTMENT_PROPERTY',
  'RENTAL',
  'VACATION_HOME',
  'MULTI_FAMILY',
  'RELOCATION',
  'OTHER'
);

CREATE TYPE "mortgage_services"."submission_channel" AS ENUM (
  'ONLINE',
  'MOBILE_APP',
  'BRANCH',
  'PHONE',
  'MAIL',
  'REFERRAL',
  'BROKER',
  'EMAIL',
  'OTHER'
);

CREATE TYPE "mortgage_services"."loan_type" AS ENUM (
  'CONVENTIONAL',
  'FHA',
  'VA',
  'USDA',
  'JUMBO',
  'CONSTRUCTION',
  'HOME_EQUITY',
  'REFINANCE',
  'REVERSE_MORTGAGE',
  'OTHER'
);

CREATE TYPE "mortgage_services"."interest_rate_type" AS ENUM (
  'FIXED',
  'ADJUSTABLE',
  'HYBRID',
  'INTEREST_ONLY',
  'STEP_RATE',
  'BALLOON',
  'OTHER'
);

CREATE TYPE "mortgage_services"."loan_rate_lock_status" AS ENUM (
  'Active',
  'Locked',
  'Expired',
  'Closed'
);

CREATE TYPE "mortgage_services"."document_type" AS ENUM (
  'TAX_RETURN',
  'W2',
  'PAY_STUB',
  'BANK_STATEMENT',
  'CREDIT_REPORT',
  'ASSET_STATEMENT',
  'IDENTITY_VERIFICATION',
  'PROPERTY_APPRAISAL',
  'PURCHASE_AGREEMENT',
  'TITLE_INSURANCE',
  'CLOSING_DISCLOSURE',
  'LOAN_ESTIMATE',
  'MORTGAGE_NOTE',
  'DEED',
  'INSURANCE_PROOF',
  'LETTER_OF_EXPLANATION',
  'GIFT_LETTER',
  'SELF_EMPLOYMENT',
  'BANKRUPTCY_DISCHARGE',
  'DIVORCE_DECREE',
  'OTHER'
);

CREATE TYPE "mortgage_services"."document_status" AS ENUM (
  'PENDING',
  'REVIEWED',
  'ACCEPTED',
  'REJECTED',
  'REQUIRES_REVISION',
  'IN_REVIEW',
  'ARCHIVED',
  'EXPIRED',
  'OTHER'
);

CREATE TYPE "mortgage_services"."condition_type" AS ENUM (
  'PRIOR_TO_APPROVAL',
  'PRIOR_TO_CLOSING',
  'PRIOR_TO_FUNDING',
  'PRIOR_TO_DOCS',
  'AT_CLOSING',
  'POST_CLOSING',
  'UNDERWRITER_REQUIREMENT',
  'AGENCY_REQUIREMENT',
  'OTHER'
);

CREATE TYPE "mortgage_services"."condition_status" AS ENUM (
  'PENDING',
  'IN_PROCESS',
  'SUBMITTED',
  'ACCEPTED',
  'REJECTED',
  'WAIVED',
  'EXPIRED',
  'CLEARED',
  'OTHER'
);

CREATE TYPE "mortgage_services"."appraisal_type" AS ENUM (
  'FULL_APPRAISAL',
  'DRIVE_BY',
  'DESKTOP',
  'BPO',
  'AVM',
  'APPRAISAL_UPDATE',
  'FIELD_REVIEW',
  'DESK_REVIEW',
  'RECERTIFICATION',
  'FHA_APPRAISAL',
  'VA_APPRAISAL',
  'USDA_APPRAISAL',
  'OTHER'
);

CREATE TYPE "mortgage_services"."appraisal_status" AS ENUM (
  'ORDERED',
  'ASSIGNED',
  'SCHEDULED',
  'INSPECTION_COMPLETED',
  'IN_PROGRESS',
  'SUBMITTED',
  'UNDER_REVIEW',
  'REVISION_NEEDED',
  'COMPLETED',
  'REJECTED',
  'CANCELLED',
  'EXPIRED',
  'OTHER'
);

CREATE TYPE "mortgage_services"."credit_report_type" AS ENUM (
  'TRI_MERGE',
  'SINGLE_BUREAU',
  'MERGED_BUREAU',
  'EXPANDED',
  'CUSTOM',
  'OTHER'
);

CREATE TYPE "mortgage_services"."credit_bureau" AS ENUM (
  'EQUIFAX',
  'EXPERIAN',
  'TRANSUNION',
  'INNOVIS',
  'CLEAR_REPORT',
  'OTHER'
);

CREATE TYPE "mortgage_services"."disclosure_type" AS ENUM (
  'LOAN_ESTIMATE',
  'CLOSING_DISCLOSURE',
  'CHANGE_IN_TERMS',
  'REVISED_CLOSING_DISCLOSURE',
  'CORRECTED_CLOSING_DISCLOSURE',
  'FEE_ESTIMATE',
  'INITIAL_ESCROW_STATEMENT',
  'OTHER'
);

CREATE TYPE "mortgage_services"."delivery_method" AS ENUM (
  'EMAIL',
  'MAIL',
  'IN_PERSON',
  'ELECTRONIC_PORTAL',
  'COURIER',
  'FAX',
  'OTHER'
);

CREATE TYPE "mortgage_services"."appointment_status" AS ENUM (
  'SCHEDULED',
  'RESCHEDULED',
  'CONFIRMED',
  'IN_PROGRESS',
  'COMPLETED',
  'CANCELLED',
  'MISSED',
  'PENDING'
);

CREATE TYPE "mortgage_services"."closing_type" AS ENUM (
  'IN_PERSON',
  'HYBRID',
  'REMOTE',
  'MAIL_AWAY',
  'ESCROW',
  'POWER_OF_ATTORNEY',
  'DRY_CLOSING',
  'WET_CLOSING'
);

CREATE TYPE "mortgage_services"."servicing_account_status" AS ENUM (
  'ACTIVE',
  'DELINQUENT',
  'DEFAULT',
  'FORECLOSURE',
  'BANKRUPTCY',
  'PAID_OFF',
  'TRANSFERRED',
  'MODIFICATION_IN_PROCESS',
  'LOSS_MITIGATION',
  'FORBEARANCE',
  'REO',
  'SHORT_SALE',
  'CHARGE_OFF',
  'SATISFIED',
  'SUSPENDED'
);

CREATE TYPE "mortgage_services"."payment_type" AS ENUM (
  'PRINCIPAL_AND_INTEREST',
  'PRINCIPAL_ONLY',
  'INTEREST_ONLY',
  'ESCROW',
  'LATE_FEE',
  'PREPAYMENT_PENALTY',
  'FULL_PAYOFF',
  'PARTIAL_PAYMENT',
  'BIWEEKLY',
  'FORBEARANCE',
  'LOAN_MODIFICATION',
  'BALLOON',
  'SERVICING_FEE',
  'EXTENSION_FEE',
  'OTHER'
);

CREATE TYPE "mortgage_services"."disbursement_type" AS ENUM (
  'PROPERTY_TAX',
  'HOMEOWNERS_INSURANCE',
  'MORTGAGE_INSURANCE',
  'FLOOD_INSURANCE',
  'HOA_DUES',
  'HAZARD_INSURANCE',
  'CONDO_INSURANCE',
  'CITY_TAX',
  'COUNTY_TAX',
  'SCHOOL_TAX',
  'SPECIAL_ASSESSMENT',
  'GROUND_RENT',
  'ESCROW_REFUND',
  'ESCROW_SHORTAGE',
  'OTHER'
);

CREATE TYPE "mortgage_services"."disbursement_status" AS ENUM (
  'PENDING',
  'PROCESSING',
  'COMPLETED',
  'FAILED',
  'RETURNED',
  'CANCELED',
  'HOLD',
  'CLEARED',
  'VOID',
  'REISSUED',
  'PARTIAL',
  'SCHEDULED',
  'SENT',
  'OTHER'
);

CREATE TYPE "mortgage_services"."escrow_analysis_status" AS ENUM (
  'PENDING',
  'COMPLETED',
  'REVIEWED',
  'APPROVED',
  'REJECTED',
  'IN_PROGRESS',
  'CANCELLED',
  'CUSTOMER_NOTIFIED',
  'ADJUSTMENT_PENDING',
  'ADJUSTMENT_APPLIED',
  'EXCEPTION',
  'EXPIRED',
  'OTHER'
);

CREATE TYPE "mortgage_services"."insurance_policy_status" AS ENUM (
  'ACTIVE',
  'PENDING',
  'EXPIRED',
  'CANCELLED',
  'RENEWED',
  'LAPSED',
  'REINSTATED',
  'FORCE_PLACED',
  'UNDER_REVIEW',
  'CLAIM_IN_PROGRESS',
  'NON_RENEWAL',
  'OTHER'
);

CREATE TYPE "mortgage_services"."insurance_type" AS ENUM (
  'HAZARD',
  'FLOOD',
  'WIND',
  'EARTHQUAKE',
  'PMI',
  'LENDERS_PLACED',
  'OTHER'
);

CREATE TYPE "mortgage_services"."loan_modification_type" AS ENUM (
  'RATE_REDUCTION',
  'TERM_EXTENSION',
  'PRINCIPAL_REDUCTION',
  'INTEREST_ONLY_PERIOD',
  'CAPITALIZATION',
  'PAYMENT_DEFERRAL',
  'FORBEARANCE',
  'WORKOUT',
  'REFINANCE',
  'PRINCIPAL_FORGIVENESS',
  'BALLOON_MODIFICATION',
  'STEP_RATE',
  'OTHER'
);

CREATE TYPE "mortgage_services"."loan_modification_status" AS ENUM (
  'PENDING',
  'APPROVED',
  'DENIED',
  'COMPLETED',
  'IN_PROGRESS',
  'SUSPENDED',
  'PARTIAL',
  'CANCELED',
  'EXPIRED',
  'TRIAL_PERIOD',
  'BORROWER_ACCEPTED',
  'BORROWER_REJECTED',
  'OTHER'
);

CREATE TYPE "mortgage_services"."hardship_reason" AS ENUM (
  'FINANCIAL_HARDSHIP',
  'JOB_LOSS',
  'MEDICAL_ISSUES',
  'NATURAL_DISASTER',
  'DIVORCE',
  'INCOME_REDUCTION',
  'DEATH_IN_FAMILY',
  'MILITARY_SERVICE',
  'BUSINESS_FAILURE',
  'DISABILITY',
  'INCREASED_EXPENSES',
  'RELOCATION',
  'PROPERTY_ISSUES',
  'OTHER'
);

CREATE TYPE "mortgage_services"."communication_type" AS ENUM (
  'EMAIL',
  'LETTER',
  'PHONE_CALL',
  'SMS',
  'IN_PERSON',
  'PORTAL_MESSAGE',
  'VOICEMAIL',
  'FAX',
  'VIDEO_CALL',
  'CHAT',
  'OTHER'
);

CREATE TYPE "mortgage_services"."communication_direction" AS ENUM (
  'INBOUND',
  'OUTBOUND',
  'INTERNAL'
);

CREATE TYPE "mortgage_services"."communication_status" AS ENUM (
  'SENT',
  'DELIVERED',
  'FAILED',
  'RECEIVED',
  'READ',
  'PENDING',
  'DRAFT',
  'CANCELLED',
  'RETURNED',
  'OTHER'
);

CREATE TYPE "mortgage_services"."communication_purpose" AS ENUM (
  'PAYMENT_REMINDER',
  'PAYMENT_CONFIRMATION',
  'ESCROW_ANALYSIS',
  'FORBEARANCE',
  'MODIFICATION',
  'DOCUMENT_REQUEST',
  'DOCUMENT_RECEIPT',
  'STATEMENT',
  'INSURANCE',
  'TAXES',
  'DEFAULT_NOTICE',
  'FORECLOSURE',
  'LOSS_MITIGATION',
  'GENERAL_INQUIRY',
  'COMPLAINT',
  'WELCOME',
  'REGULATORY',
  'OTHER'
);

CREATE TYPE "mortgage_services"."hmda_loan_purpose" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '31',
  '32',
  'OTHER'
);

CREATE TYPE "mortgage_services"."hmda_preapproval" AS ENUM (
  '1',
  '2',
  '3'
);

CREATE TYPE "mortgage_services"."hmda_construction_method" AS ENUM (
  '1',
  '2'
);

CREATE TYPE "mortgage_services"."hmda_occupancy_type" AS ENUM (
  '1',
  '2',
  '3'
);

CREATE TYPE "mortgage_services"."hmda_action_taken" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8'
);

CREATE TYPE "mortgage_services"."hmda_denial_reason" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '10'
);

CREATE TYPE "mortgage_services"."hmda_hoepa_status" AS ENUM (
  '1',
  '2',
  '3'
);

CREATE TYPE "mortgage_services"."hmda_lien_status" AS ENUM (
  '1',
  '2',
  '3',
  '4'
);

CREATE TYPE "mortgage_services"."hmda_credit_score_model" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '1111'
);

CREATE TYPE "mortgage_services"."hmda_submission_status" AS ENUM (
  'PENDING',
  'SUBMITTED',
  'ACCEPTED',
  'REJECTED',
  'EXEMPTED'
);

CREATE TYPE "mortgage_services"."hmda_balloon_payment" AS ENUM (
  '1',
  '2'
);

CREATE TYPE "mortgage_services"."hmda_interest_only" AS ENUM (
  '1',
  '2'
);

CREATE TYPE "mortgage_services"."hmda_negative_amortization" AS ENUM (
  '1',
  '2'
);

CREATE TYPE "mortgage_services"."hmda_other_non_amortizing" AS ENUM (
  '1',
  '2'
);

CREATE TYPE "mortgage_services"."hmda_manufactured_home_type" AS ENUM (
  '1',
  '2',
  '3'
);

CREATE TYPE "mortgage_services"."hmda_manufactured_land_property_interest" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5'
);

CREATE TYPE "mortgage_services"."hmda_submission_method" AS ENUM (
  '1',
  '2',
  '3'
);

CREATE TYPE "mortgage_services"."hmda_aus" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '1111'
);

CREATE TYPE "mortgage_services"."hmda_reverse_mortgage" AS ENUM (
  '1',
  '2',
  '1111'
);

CREATE TYPE "mortgage_services"."hmda_open_end_line_of_credit" AS ENUM (
  '1',
  '2',
  '1111'
);

CREATE TYPE "mortgage_services"."hmda_business_or_commercial_purpose" AS ENUM (
  '1',
  '2',
  '1111'
);

CREATE TYPE "mortgage_services"."hmda_record_edit_status" AS ENUM (
  'NOT_STARTED',
  'IN_PROGRESS',
  'VALID',
  'INVALID',
  'QUALITY_ISSUES',
  'MACRO_ISSUES'
);

CREATE TYPE "mortgage_services"."hmda_ethnicity" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5'
);

CREATE TYPE "mortgage_services"."hmda_ethnicity_detail" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7'
);

CREATE TYPE "mortgage_services"."hmda_race" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8'
);

CREATE TYPE "mortgage_services"."hmda_race_asian_detail" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7'
);

CREATE TYPE "mortgage_services"."hmda_race_pacific_islander_detail" AS ENUM (
  '1',
  '2',
  '3',
  '4'
);

CREATE TYPE "mortgage_services"."hmda_sex" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6'
);

CREATE TYPE "mortgage_services"."hmda_collection_method" AS ENUM (
  '1',
  '2',
  '3'
);

CREATE TYPE "mortgage_services"."hmda_age_group" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9'
);

CREATE TYPE "mortgage_services"."hmda_applicant_present" AS ENUM (
  '1',
  '2',
  '3'
);

CREATE TYPE "mortgage_services"."hmda_applicant_type" AS ENUM (
  'PRIMARY',
  'CO_APPLICANT',
  'BORROWER',
  'CO_BORROWER',
  'GUARANTOR'
);

CREATE TYPE "mortgage_services"."hmda_edit_type" AS ENUM (
  'SYNTACTICAL',
  'VALIDITY',
  'QUALITY',
  'MACRO'
);

CREATE TYPE "mortgage_services"."hmda_edit_status" AS ENUM (
  'OPEN',
  'VERIFIED',
  'CORRECTED',
  'IN_PROGRESS',
  'WAIVED'
);

CREATE TYPE "mortgage_services"."reporting_period" AS ENUM (
  'ANNUAL',
  'QUARTERLY_Q1',
  'QUARTERLY_Q2',
  'QUARTERLY_Q3'
);

CREATE TYPE "mortgage_services"."submission_status" AS ENUM (
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '10',
  '11',
  '12',
  '13',
  '14',
  '15'
);

CREATE TYPE "consumer_lending"."housing_status" AS ENUM (
  'OWN',
  'RENT',
  'LIVE_WITH_PARENTS',
  'MILITARY_HOUSING',
  'EMPLOYER_PROVIDED',
  'STUDENT_HOUSING',
  'SHARED_HOUSING',
  'TEMPORARY',
  'HOMELESS',
  'OTHER'
);

CREATE TYPE "consumer_lending"."income_type" AS ENUM (
  'SALARY',
  'SELF_EMPLOYMENT',
  'RENTAL_INCOME',
  'ALIMONY',
  'CHILD_SUPPORT',
  'PENSION',
  'SOCIAL_SECURITY',
  'DISABILITY_INCOME',
  'INVESTMENT_INCOME',
  'COMMISSION',
  'BONUS',
  'ROYALTIES',
  'ANNUITY',
  'MILITARY_PAY',
  'TIPS',
  'OTHER'
);

CREATE TYPE "consumer_lending"."asset_type" AS ENUM (
  'CHECKING_ACCOUNT',
  'SAVINGS_ACCOUNT',
  'MONEY_MARKET_ACCOUNT',
  'CERTIFICATE_OF_DEPOSIT',
  'INVESTMENT_ACCOUNT',
  'RETIREMENT_ACCOUNT',
  'STOCKS',
  'BONDS',
  'MUTUAL_FUNDS',
  'REAL_ESTATE',
  'VACANT_LAND',
  'VEHICLE',
  'BUSINESS_OWNERSHIP',
  'CRYPTOCURRENCY',
  'PRECIOUS_METALS',
  'LIFE_INSURANCE_CASH_VALUE',
  'OTHER'
);

CREATE TYPE "consumer_lending"."liability_type" AS ENUM (
  'CREDIT_CARD',
  'AUTO_LOAN',
  'STUDENT_LOAN',
  'PERSONAL_LOAN',
  'MORTGAGE',
  'HOME_EQUITY_LOAN',
  'HOME_EQUITY_LINE_OF_CREDIT',
  'MEDICAL_DEBT',
  'BUSINESS_LOAN',
  'PERSONAL_LINE_OF_CREDIT',
  'INSTALLMENT_LOAN',
  'PAYDAY_LOAN',
  'RENT_TO_OWN',
  'ALIMONY',
  'CHILD_SUPPORT',
  'TAX_DEBT',
  'OTHER'
);

CREATE TYPE "consumer_lending"."verification_status" AS ENUM (
  'SELF_REPORTED',
  'VERIFIED',
  'FAILED',
  'PENDING',
  'PARTIALLY_VERIFIED',
  'UNABLE_TO_VERIFY'
);

CREATE TYPE "consumer_lending"."loan_type" AS ENUM (
  'PERSONAL',
  'AUTO',
  'STUDENT',
  'HOME_IMPROVEMENT',
  'DEBT_CONSOLIDATION',
  'MEDICAL',
  'BUSINESS',
  'RECREATIONAL_VEHICLE',
  'MOTORCYCLE',
  'BOAT',
  'WEDDING',
  'VACATION',
  'GREEN_ENERGY',
  'OTHER'
);

CREATE TYPE "consumer_lending"."interest_rate_type" AS ENUM (
  'FIXED',
  'VARIABLE',
  'ADJUSTABLE',
  'HYBRID'
);

CREATE TYPE "consumer_lending"."fee_type" AS ENUM (
  'FLAT',
  'PERCENTAGE',
  'TIERED'
);

CREATE TYPE "consumer_lending"."disbursement_option" AS ENUM (
  'DIRECT_DEPOSIT',
  'CHECK',
  'DEALER_DIRECT',
  'WIRE_TRANSFER',
  'CASH',
  'CREDIT_TO_ACCOUNT',
  'OTHER'
);

CREATE TYPE "consumer_lending"."eligibility_criteria_type" AS ENUM (
  'CREDIT_SCORE',
  'INCOME',
  'DEBT_TO_INCOME_RATIO',
  'EMPLOYMENT_STATUS',
  'TIME_IN_BUSINESS',
  'AGE',
  'CITIZENSHIP',
  'EXISTING_DEBT',
  'BANKRUPTCY_HISTORY',
  'COLLATERAL_VALUE',
  'INDUSTRY',
  'GEOGRAPHIC_LOCATION',
  'EDUCATION_LEVEL',
  'NET_WORTH',
  'OTHER'
);

CREATE TYPE "consumer_lending"."credit_report_type" AS ENUM (
  'TRI_MERGE',
  'SINGLE_BUREAU',
  'MERGED_BUREAU',
  'EXPANDED',
  'CUSTOM',
  'OTHER'
);

CREATE TYPE "consumer_lending"."credit_bureau" AS ENUM (
  'EQUIFAX',
  'EXPERIAN',
  'TRANSUNION',
  'INNOVIS',
  'CLEAR_REPORT',
  'OTHER'
);

CREATE TYPE "consumer_lending"."credit_report_status" AS ENUM (
  'COMPLETED',
  'FAILED',
  'PENDING',
  'PARTIALLY_RETRIEVED',
  'EXPIRED',
  'UNDER_REVIEW',
  'ERROR',
  'OTHER'
);

CREATE TYPE "consumer_lending"."account_type" AS ENUM (
  'MORTGAGE',
  'INSTALLMENT',
  'REVOLVING',
  'AUTO_LOAN',
  'STUDENT_LOAN',
  'PERSONAL_LOAN',
  'CREDIT_CARD',
  'HOME_EQUITY',
  'BUSINESS_LOAN',
  'LEASE',
  'MEDICAL_DEBT',
  'COLLECTION',
  'CHARGE_ACCOUNT',
  'OTHER'
);

CREATE TYPE "consumer_lending"."payment_status" AS ENUM (
  'CURRENT',
  'DAYS_30_LATE',
  'DAYS_60_LATE',
  'DAYS_90_LATE',
  'DAYS_120_LATE',
  'DAYS_150_LATE',
  'CHARGED_OFF',
  'IN_COLLECTIONS',
  'SETTLED',
  'REPOSSESSION',
  'FORECLOSURE',
  'BANKRUPTCY',
  'OTHER'
);

CREATE TYPE "consumer_lending"."delinquency_severity" AS ENUM (
  'NONE',
  'MINOR',
  'MODERATE',
  'SERIOUS',
  'SEVERE',
  'CRITICAL',
  'LEGAL_ACTION',
  'BANKRUPTCY',
  'OTHER'
);

CREATE TYPE "consumer_lending"."inquiry_type" AS ENUM (
  'HARD',
  'SOFT',
  'PRE_APPROVAL',
  'ACCOUNT_REVIEW',
  'EMPLOYMENT_VERIFICATION',
  'INSURANCE_QUOTE',
  'TENANT_SCREENING',
  'PROMOTIONAL',
  'COLLECTION',
  'FRAUD_PREVENTION',
  'OTHER'
);

CREATE TYPE "consumer_lending"."public_record_type" AS ENUM (
  'BANKRUPTCY',
  'TAX_LIEN',
  'JUDGMENT',
  'FORECLOSURE',
  'REPOSSESSION',
  'WAGE_GARNISHMENT',
  'CIVIL_LAWSUIT',
  'SMALL_CLAIMS',
  'CHILD_SUPPORT_LIEN',
  'FEDERAL_TAX_LIEN',
  'STATE_TAX_LIEN',
  'OTHER'
);

CREATE TYPE "consumer_lending"."public_record_status" AS ENUM (
  'ACTIVE',
  'SATISFIED',
  'DISCHARGED',
  'SETTLED',
  'VACATED',
  'PENDING',
  'RELEASED',
  'EXPIRED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."decision_model_type" AS ENUM (
  'CREDIT_SCORE',
  'INCOME_VERIFICATION',
  'FRAUD_DETECTION',
  'RISK_ASSESSMENT',
  'DEBT_TO_INCOME_ANALYSIS',
  'BEHAVIORAL_SCORING',
  'MACHINE_LEARNING_PREDICTIVE',
  'ALTERNATIVE_CREDIT_SCORING',
  'EMPLOYMENT_VERIFICATION',
  'COLLATERAL_VALUATION',
  'REGULATORY_COMPLIANCE',
  'PRICING_MODEL',
  'OTHER'
);

CREATE TYPE "consumer_lending"."decision_type" AS ENUM (
  'PREQUALIFICATION',
  'INITIAL',
  'FINAL',
  'RECONSIDERATION',
  'COUNTER_OFFER',
  'CONDITIONAL',
  'ADMINISTRATIVE_REVIEW',
  'OTHER'
);

CREATE TYPE "consumer_lending"."decision_result" AS ENUM (
  'APPROVED',
  'DENIED',
  'PENDING_REVIEW',
  'SUSPENDED',
  'INCOMPLETE',
  'REFERRED',
  'COUNTER_OFFER',
  'WITHDRAWN',
  'OTHER'
);

CREATE TYPE "consumer_lending"."decision_reason_code" AS ENUM (
  'INSUFFICIENT_INCOME',
  'HIGH_DEBT_TO_INCOME',
  'LOW_CREDIT_SCORE',
  'INSUFFICIENT_CREDIT_HISTORY',
  'RECENT_BANKRUPTCY',
  'OUTSTANDING_COLLECTIONS',
  'INCOMPLETE_APPLICATION',
  'NEGATIVE_PAYMENT_HISTORY',
  'INSUFFICIENT_COLLATERAL',
  'EMPLOYMENT_INSTABILITY',
  'FRAUD_RISK',
  'REGULATORY_RESTRICTIONS',
  'GEOGRAPHIC_RESTRICTION',
  'UNVERIFIABLE_INFORMATION',
  'INSUFFICIENT_ASSETS',
  'AGE_REQUIREMENTS',
  'EXISTING_RELATIONSHIP',
  'RISK_TIER_INELIGIBILITY',
  'OTHER'
);

CREATE TYPE "consumer_lending"."delivery_method" AS ENUM (
  'EMAIL',
  'MAIL',
  'PORTAL',
  'SMS',
  'PHONE',
  'FAX',
  'IN_PERSON',
  'OTHER'
);

CREATE TYPE "consumer_lending"."adverse_action_notice_status" AS ENUM (
  'GENERATED',
  'SENT',
  'DELIVERED',
  'FAILED',
  'PENDING',
  'READ',
  'RETURNED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."vehicle_condition" AS ENUM (
  'NEW',
  'USED',
  'CERTIFIED_PRE_OWNED',
  'DEMO',
  'SALVAGE',
  'RECONSTRUCTED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."valuation_source" AS ENUM (
  'KELLEY_BLUE_BOOK',
  'NADA_GUIDES',
  'EDMUNDS',
  'BLACK_BOOK',
  'CARFAX',
  'DEALER_APPRAISAL',
  'INDEPENDENT_APPRAISAL',
  'MANHEIM',
  'OTHER'
);

CREATE TYPE "consumer_lending"."payment_schedule_status" AS ENUM (
  'SCHEDULED',
  'PAID',
  'PAST_DUE',
  'PARTIALLY_PAID',
  'SKIPPED',
  'LATE_PROCESSED',
  'CANCELED',
  'PENDING',
  'FAILED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."payment_type" AS ENUM (
  'REGULAR',
  'EXTRA_PRINCIPAL',
  'LATE',
  'FULL_PAYOFF',
  'PARTIAL',
  'CATCH_UP',
  'PREPAYMENT',
  'REFINANCE',
  'OTHER'
);

CREATE TYPE "consumer_lending"."payment_method" AS ENUM (
  'ACH',
  'CHECK',
  'ONLINE',
  'CREDIT_CARD',
  'DEBIT_CARD',
  'WIRE_TRANSFER',
  'CASH',
  'MONEY_ORDER',
  'MOBILE_APP',
  'IN_PERSON',
  'AUTOMATIC',
  'OTHER'
);

CREATE TYPE "consumer_lending"."loan_payment_status" AS ENUM (
  'PENDING',
  'COMPLETED',
  'RETURNED',
  'CANCELED',
  'REVERSED',
  'FAILED',
  'PARTIAL',
  'SUSPENDED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."loan_fee_type" AS ENUM (
  'LATE_FEE',
  'NSF_FEE',
  'ORIGINATION_FEE',
  'PREPAYMENT_PENALTY',
  'UNDERWRITING_FEE',
  'DOCUMENTATION_FEE',
  'APPLICATION_FEE',
  'ANNUAL_FEE',
  'WIRE_TRANSFER_FEE',
  'RETURNED_CHECK_FEE',
  'MODIFICATION_FEE',
  'EXTENSION_FEE',
  'COLLECTION_FEE',
  'OTHER'
);

CREATE TYPE "consumer_lending"."loan_fee_status" AS ENUM (
  'PENDING',
  'CHARGED',
  'WAIVED',
  'PAID',
  'PARTIALLY_PAID',
  'REVERSED',
  'DISPUTED',
  'WRITTEN_OFF',
  'OTHER'
);

CREATE TYPE "consumer_lending"."collateral_type" AS ENUM (
  'VEHICLE',
  'REAL_ESTATE',
  'DEPOSIT_ACCOUNT',
  'INVESTMENT_SECURITIES',
  'EQUIPMENT',
  'BOAT',
  'RECREATIONAL_VEHICLE',
  'MACHINERY',
  'INVENTORY',
  'ACCOUNTS_RECEIVABLE',
  'LIFE_INSURANCE_POLICY',
  'JEWELRY',
  'FARM_ASSETS',
  'OTHER'
);

CREATE TYPE "consumer_lending"."insurance_type" AS ENUM (
  'AUTO',
  'HAZARD',
  'CREDIT_LIFE',
  'DISABILITY',
  'COMPREHENSIVE',
  'COLLISION',
  'PROPERTY',
  'TITLE',
  'LIFE',
  'UNEMPLOYMENT',
  'MARINE',
  'EQUIPMENT',
  'OTHER'
);

CREATE TYPE "consumer_lending"."premium_frequency" AS ENUM (
  'ANNUAL',
  'MONTHLY',
  'QUARTERLY',
  'SEMI_ANNUAL',
  'ONE_TIME',
  'OTHER'
);

CREATE TYPE "consumer_lending"."insurance_status" AS ENUM (
  'ACTIVE',
  'LAPSED',
  'CANCELED',
  'PENDING',
  'SUSPENDED',
  'EXPIRED',
  'IN_GRACE_PERIOD',
  'OTHER'
);

CREATE TYPE "consumer_lending"."document_type" AS ENUM (
  'APPLICATION',
  'CONTRACT',
  'STATEMENT',
  'INCOME_VERIFICATION',
  'TAX_RETURN',
  'BANK_STATEMENT',
  'IDENTIFICATION',
  'PROOF_OF_ADDRESS',
  'CREDIT_REPORT',
  'COLLATERAL_DOCUMENT',
  'INSURANCE_DOCUMENT',
  'PROMISSORY_NOTE',
  'CLOSING_DISCLOSURE',
  'RECEIPT',
  'COMMUNICATION',
  'OTHER'
);

CREATE TYPE "consumer_lending"."document_status" AS ENUM (
  'PENDING',
  'REVIEWED',
  'ACCEPTED',
  'REJECTED',
  'REQUIRES_REVISION',
  'IN_REVIEW',
  'ARCHIVED',
  'EXPIRED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."communication_type" AS ENUM (
  'EMAIL',
  'LETTER',
  'PHONE_CALL',
  'TEXT_MESSAGE',
  'VOICEMAIL',
  'CHAT',
  'VIDEO_CALL',
  'FAX',
  'IN_PERSON',
  'OTHER'
);

CREATE TYPE "consumer_lending"."communication_direction" AS ENUM (
  'INBOUND',
  'OUTBOUND',
  'INTERNAL',
  'OTHER'
);

CREATE TYPE "consumer_lending"."communication_status" AS ENUM (
  'SENT',
  'DELIVERED',
  'FAILED',
  'RECEIVED',
  'PENDING',
  'READ',
  'PARTIALLY_DELIVERED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."communication_context" AS ENUM (
  'PAYMENT_REMINDER',
  'STATEMENT',
  'NOTICE',
  'APPLICATION_STATUS',
  'DOCUMENT_REQUEST',
  'ACCOUNT_REVIEW',
  'COLLECTION',
  'VERIFICATION',
  'MARKETING',
  'CUSTOMER_SERVICE',
  'OTHER'
);

CREATE TYPE "consumer_lending"."statement_delivery_method" AS ENUM (
  'EMAIL',
  'MAIL',
  'PORTAL',
  'SMS',
  'MOBILE_APP',
  'FAX',
  'PRINT_AT_BRANCH',
  'OTHER'
);

CREATE TYPE "consumer_lending"."collection_status" AS ENUM (
  'ACTIVE',
  'RESOLVED',
  'CHARGED_OFF',
  'NEGOTIATING',
  'SUSPENDED',
  'LEGAL_PROCEEDINGS',
  'PAYMENT_PLAN',
  'OTHER'
);

CREATE TYPE "consumer_lending"."collection_priority" AS ENUM (
  'HIGH',
  'MEDIUM',
  'LOW',
  'CRITICAL',
  'MINIMAL',
  'OTHER'
);

CREATE TYPE "consumer_lending"."collection_resolution_type" AS ENUM (
  'PAID_IN_FULL',
  'SETTLEMENT',
  'MODIFICATION',
  'CHARGE_OFF',
  'BANKRUPTCY',
  'DEBT_CONSOLIDATION',
  'PAYMENT_PLAN',
  'LEGAL_JUDGMENT',
  'FORGIVEN',
  'OTHER'
);

CREATE TYPE "consumer_lending"."collection_action_type" AS ENUM (
  'CALL',
  'LETTER',
  'EMAIL',
  'FIELD_VISIT',
  'SMS',
  'VOICEMAIL',
  'LEGAL_NOTICE',
  'ONLINE_MESSAGE',
  'AUTOMATED_MESSAGE',
  'OTHER'
);

CREATE TYPE "consumer_lending"."collection_action_result" AS ENUM (
  'CONTACT_MADE',
  'LEFT_MESSAGE',
  'NO_ANSWER',
  'WRONG_NUMBER',
  'PROMISE_TO_PAY',
  'PARTIAL_PAYMENT',
  'DISPUTE_RAISED',
  'REFERRED_TO_LEGAL',
  'UNABLE_TO_LOCATE',
  'OTHER'
);

CREATE TYPE "consumer_lending"."next_collection_action_type" AS ENUM (
  'FOLLOW_UP_CALL',
  'SEND_DEMAND_LETTER',
  'ESCALATE_TO_LEGAL',
  'SKIP_TRACE',
  'NEGOTIATE_SETTLEMENT',
  'PAYMENT_PLAN_DISCUSSION',
  'CREDIT_REPORTING',
  'ASSET_INVESTIGATION',
  'SUSPEND_COLLECTION',
  'OTHER'
);

CREATE TYPE "consumer_lending"."payment_arrangement_status" AS ENUM (
  'ACTIVE',
  'COMPLETED',
  'BROKEN',
  'SUSPENDED',
  'PENDING',
  'NEGOTIATING',
  'CANCELED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."payment_frequency" AS ENUM (
  'WEEKLY',
  'BI_WEEKLY',
  'MONTHLY',
  'SEMI_MONTHLY',
  'QUARTERLY',
  'SEMI_ANNUALLY',
  'ANNUALLY',
  'CUSTOM',
  'OTHER'
);

CREATE TYPE "consumer_lending"."loan_modification_type" AS ENUM (
  'RATE_REDUCTION',
  'TERM_EXTENSION',
  'PRINCIPAL_REDUCTION',
  'INTEREST_ONLY_PERIOD',
  'CAPITALIZATION',
  'PAYMENT_DEFERRAL',
  'FORBEARANCE',
  'WORKOUT',
  'REFINANCE',
  'OTHER'
);

CREATE TYPE "consumer_lending"."loan_modification_status" AS ENUM (
  'PENDING',
  'APPROVED',
  'DENIED',
  'COMPLETED',
  'IN_PROGRESS',
  'SUSPENDED',
  'PARTIAL',
  'CANCELED',
  'OTHER'
);

CREATE TYPE "consumer_lending"."disclosure_type" AS ENUM (
  'INITIAL_TIL',
  'LOAN_ESTIMATE',
  'CLOSING_DISCLOSURE',
  'CHANGE_IN_TERMS',
  'PERIODIC_STATEMENT',
  'PAYMENT_NOTICE',
  'INTEREST_RATE_ADJUSTMENT',
  'PRE_QUALIFICATION',
  'ADVERSE_ACTION',
  'REFINANCE_NOTICE',
  'OTHER'
);

CREATE TYPE "consumer_lending"."disclosure_delivery_method" AS ENUM (
  'EMAIL',
  'MAIL',
  'IN_PERSON',
  'ELECTRONIC',
  'SMS',
  'FAX',
  'MOBILE_APP',
  'BRANCH_PICKUP',
  'OTHER'
);

CREATE TYPE "consumer_lending"."ecoa_reason_code" AS ENUM (
  '01',
  '02',
  '03',
  '04',
  '05',
  '10',
  '11',
  '12',
  '20',
  '21',
  '22',
  '23',
  '30',
  '31',
  '32',
  '40',
  '41',
  '50',
  '51',
  '52',
  '60',
  '61',
  '62',
  '63',
  '64',
  '65'
);

CREATE TYPE "consumer_lending"."fcra_reason_code" AS ENUM (
  'A1',
  'A2',
  'A3',
  'A4',
  'A5',
  'A6',
  'A7',
  'A8',
  'A9',
  'B1',
  'B2',
  'B3',
  'B4',
  'C1',
  'C2',
  'C3',
  'D1',
  'D2',
  'D3'
);

CREATE TYPE "consumer_lending"."information_method" AS ENUM (
  'SELF_REPORTED',
  'OBSERVED',
  'NOT_PROVIDED'
);

CREATE TYPE "consumer_lending"."action_taken" AS ENUM (
  'APPROVED',
  'DENIED',
  'WITHDRAWN',
  'INCOMPLETE'
);

CREATE TYPE "consumer_lending"."analysis_type" AS ENUM (
  'PRICING',
  'UNDERWRITING',
  'MARKETING',
  'PRODUCT_DESIGN',
  'PORTFOLIO_REVIEW',
  'GEOGRAPHIC'
);

CREATE TYPE "consumer_lending"."protected_class" AS ENUM (
  'RACE',
  'ETHNICITY',
  'SEX',
  'AGE',
  'NATIONAL_ORIGIN',
  'DISABILITY_STATUS',
  'MARITAL_STATUS',
  'RELIGION',
  'VETERAN_STATUS'
);

CREATE TYPE "consumer_lending"."outcome_variable" AS ENUM (
  'APPROVAL_RATE',
  'APR',
  'FEES',
  'LOAN_AMOUNT',
  'INTEREST_RATE',
  'LOAN_TERMS',
  'COLLATERAL_REQUIREMENTS'
);

CREATE TYPE "consumer_lending"."statistical_test" AS ENUM (
  'T_TEST',
  'CHI_SQUARE',
  'REGRESSION',
  'ANOVA',
  'LOGISTIC_REGRESSION',
  'WILCOXON'
);

CREATE TYPE "consumer_lending"."reg_b_notice_type" AS ENUM (
  'INCOMPLETENESS',
  'COUNTEROFFER',
  'ACTION_TAKEN',
  'PRE_ADVERSE_ACTION',
  'ADVERSE_ACTION',
  'REQUEST_FOR_INFORMATION',
  'CONDITIONAL_APPROVAL'
);

CREATE TYPE "security"."role_status" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'DEPRECATED',
  'RETIRED',
  'DRAFT'
);

CREATE TYPE "security"."entitlement_status" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'DEPRECATED',
  'DRAFT'
);

CREATE TYPE "security"."resource_type" AS ENUM (
  'DATA',
  'APPLICATION',
  'HOST',
  'NETWORK_DEVICE'
);

CREATE TYPE "security"."permission_type" AS ENUM (
  'READ',
  'MASKED',
  'WRITE',
  'DELETE',
  'EXECUTE',
  'ADMIN'
);

CREATE TYPE "security"."sync_status" AS ENUM (
  'PENDING',
  'IN_PROGRESS',
  'COMPLETED',
  'FAILED'
);

CREATE TYPE "security"."tcp_flag_type" AS ENUM (
  'SYN',
  'ACK',
  'FIN',
  'RST',
  'PSH',
  'URG',
  'ECE',
  'CWR'
);

CREATE TYPE "security"."environment" AS ENUM (
  'production',
  'preproduction',
  'qa',
  'development'
);

CREATE TYPE "security"."risk_level" AS ENUM (
  'LOW',
  'MEDIUM',
  'HIGH',
  'CRITICAL'
);

CREATE TYPE "security"."threat_level_type" AS ENUM (
  'HIGH',
  'MEDIUM',
  'LOW',
  'INFORMATIONAL',
  'UNKNOWN'
);

CREATE TYPE "security"."network_protocols" AS ENUM (
  'TCP',
  'UDP',
  'ICMP',
  'HTTP2',
  'TLS',
  'QUIC',
  'SIP'
);

CREATE TYPE "security"."system_type" AS ENUM (
  'SERVER',
  'WORKSTATION',
  'LAPTOP',
  'VIRTUAL_MACHINE',
  'CONTAINER',
  'APPLIANCE'
);

CREATE TYPE "security"."agent_status" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'PENDING',
  'ERROR',
  'DISCONNECTED'
);

CREATE TYPE "security"."patch_status" AS ENUM (
  'CURRENT',
  'UP_TO_DATE',
  'OUTDATED',
  'CRITICAL',
  'UNKNOWN'
);

CREATE TYPE "security"."compliance_status" AS ENUM (
  'COMPLIANT',
  'NON_COMPLIANT',
  'EXCEPTION',
  'UNKNOWN'
);

CREATE TYPE "app_mgmt"."application_lifecycle_status" AS ENUM (
  'DEVELOPMENT',
  'PILOT',
  'PRODUCTION',
  'DEPRECATED',
  'DATA_MAINTENANCE',
  'DECOMMISSIONED',
  'ARCHIVED'
);

CREATE TYPE "app_mgmt"."deployment_environments" AS ENUM (
  'ON_PREMISES',
  'CLOUD_PUBLIC',
  'CLOUD_PRIVATE',
  'CLOUD_HYBRID',
  'CONTAINERIZED',
  'SERVERLESS',
  'EDGE'
);

CREATE TYPE "app_mgmt"."application_types" AS ENUM (
  'WEB',
  'MOBILE',
  'DESKTOP',
  'API',
  'BATCH',
  'MICROSERVICE',
  'LEGACY',
  'SAAS',
  'DATABASE',
  'MIDDLEWARE',
  'EMBEDDED'
);

CREATE TYPE "app_mgmt"."component_types" AS ENUM (
  'JAVA_LIBRARY',
  'NPM_PACKAGE',
  'NUGET_PACKAGE',
  'PYTHON_MODULE',
  'RUBY_GEM',
  'FRAMEWORK',
  'API',
  'DOTNET_ASSEMBLY',
  'DOCKER_IMAGE',
  'GRADLE_PLUGIN',
  'MAVEN_PLUGIN'
);

CREATE TYPE "app_mgmt"."dependency_types" AS ENUM (
  'RUNTIME',
  'BUILD',
  'TEST',
  'DEVELOPMENT',
  'OPTIONAL',
  'PROVIDED',
  'SYSTEM',
  'IMPORT',
  'COMPILE',
  'ANNOTATION_PROCESSOR'
);

CREATE TYPE "app_mgmt"."criticality_levels" AS ENUM (
  'NONE',
  'MINIMAL',
  'MINOR',
  'MODERATE',
  'SIGNIFICANT',
  'CRITICAL'
);

CREATE TYPE "app_mgmt"."relationship_types" AS ENUM (
  'AUTHORIZATION',
  'AUTHENTICATION',
  'DATA_ACCESS',
  'SERVICE_DEPENDENCY',
  'API_INTEGRATION',
  'CONFIGURATION_PROVIDER',
  'LOGGING_SERVICE',
  'MONITORING_SERVICE',
  'CACHING_SERVICE',
  'MESSAGING_QUEUE',
  'REPORTING_SERVICE',
  'DATA_PROCESSING',
  'UI_EMBEDDING',
  'WORKFLOW_TRIGGER',
  'EVENT_SUBSCRIPTION',
  'NOTIFICATION_SERVICE',
  'IDENTITY_MANAGEMENT',
  'PAYMENT_PROCESSING',
  'STORAGE_SERVICE',
  'SEARCH_SERVICE',
  'SECURITY_SCANNING',
  'AUDIT_LOGGING',
  'RESOURCE_MANAGEMENT',
  'TASK_SCHEDULING',
  'CONTENT_DELIVERY'
);

CREATE TYPE "app_mgmt"."license_types" AS ENUM (
  'MIT',
  'APACHE_2_0',
  'BSD_2_CLAUSE',
  'BSD_3_CLAUSE',
  'ISC',
  'GPL_2_0',
  'GPL_3_0',
  'LGPL_2_1',
  'LGPL_3_0',
  'AGPL_3_0',
  'PROPRIETARY',
  'CC_BY_4_0',
  'CC_BY_SA_4_0',
  'CC_BY_NC_4_0',
  'CC_BY_NC_SA_4_0',
  'CC_BY_ND_4_0',
  'CC_BY_NC_ND_4_0',
  'MPL_2_0',
  'EPL_2_0',
  'CDDL_1_1',
  'CPL_1_0',
  'APPL_2_0'
);

CREATE TABLE "enterprise"."permissions" (
  "enterprise_permission_id" SERIAL PRIMARY KEY,
  "permission_name" VARCHAR(50) NOT NULL
);

CREATE TABLE "enterprise"."currency" (
  "code" enterprise.currency_code PRIMARY KEY,
  "name" varchar(100)
);

CREATE TABLE "enterprise"."identifiers" (
  "enterprise_identifier_id" SERIAL PRIMARY KEY,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(256) NOT NULL,
  "name" VARCHAR(100),
  "secondary_identification" VARCHAR(50),
  "lei" VARCHAR(20),
  "note" TEXT
);

CREATE TABLE "enterprise"."parties" (
  "enterprise_party_id" SERIAL PRIMARY KEY,
  "party_number" VARCHAR(35),
  "party_type" enterprise.party_type NOT NULL,
  "name" VARCHAR(350) NOT NULL,
  "full_business_legal_name" VARCHAR(350),
  "legal_structure" enterprise.legal_structure,
  "lei" VARCHAR(20),
  "beneficial_ownership" BOOLEAN,
  "email_address" VARCHAR(256),
  "phone" VARCHAR(30),
  "mobile" VARCHAR(30),
  "date_of_birth" DATE,
  "ssn" VARCHAR(11),
  "marital_status" enterprise.marital_status,
  "citizenship_status" enterprise.citizenship_status,
  "party_status" enterprise.party_status NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE "enterprise"."party_relationships" (
  "enterprise_party_relationship_id" SERIAL PRIMARY KEY,
  "enterprise_party_id" INTEGER NOT NULL,
  "related_party_id" INTEGER NOT NULL,
  "relationship_type" enterprise.party_relationship_type,
  "priority" INT
);

CREATE TABLE "enterprise"."customer_demographics" (
  "enterprise_customer_demographics_id" SERIAL PRIMARY KEY,
  "enterprise_party_id" INTEGER NOT NULL,
  "consumer_banking_account_id" BIGINT,
  "credit_cards_card_accounts_id" INTEGER,
  "data_source" VARCHAR(100) NOT NULL,
  "last_updated" DATE NOT NULL,
  "education_level" enterprise.education_level,
  "income_bracket" enterprise.income_bracket,
  "occupation_category" enterprise.occupation_category,
  "employer" VARCHAR(255),
  "employment_length_years" INTEGER,
  "total_household_income" NUMERIC(15,2),
  "household_size" INTEGER,
  "homeownership_status" enterprise.homeownership_status,
  "estimated_home_value" NUMERIC(15,2),
  "years_at_residence" INTEGER,
  "net_worth_estimate" NUMERIC(15,2),
  "political_affiliation" enterprise.political_affiliation,
  "number_of_children" INTEGER,
  "family_life_stage" enterprise.family_life_stage,
  "lifestyle_segment" enterprise.lifestyle_segment,
  "credit_risk_tier" enterprise.credit_risk_tier,
  "discretionary_spending_estimate" NUMERIC(15,2),
  "primary_investment_goals" VARCHAR(255),
  "risk_tolerance" VARCHAR(50),
  "digital_engagement_score" INTEGER,
  "customer_lifetime_value" NUMERIC(15,2),
  "churn_risk_score" INTEGER,
  "cross_sell_propensity" INTEGER,
  "channel_preference" VARCHAR(50),
  "data_consent_level" VARCHAR(50),
  "data_usage_restriction" TEXT
);

CREATE TABLE "enterprise"."party_entity_addresses" (
  "enterprise_party_entity_address_id" SERIAL PRIMARY KEY,
  "enterprise_party_id" INTEGER NOT NULL,
  "enterprise_address_id" INTEGER NOT NULL,
  "relationship_type" enterprise.address_relationship_type
);

CREATE TABLE "enterprise"."addresses" (
  "enterprise_address_id" SERIAL PRIMARY KEY,
  "address_type" enterprise.address_type,
  "department" VARCHAR(70),
  "sub_department" VARCHAR(70),
  "street_name" VARCHAR(140),
  "building_number" VARCHAR(16),
  "building_name" VARCHAR(140),
  "floor" VARCHAR(70),
  "room" VARCHAR(70),
  "unit_number" VARCHAR(16),
  "post_box" VARCHAR(16),
  "town_location_name" VARCHAR(140),
  "district_name" VARCHAR(140),
  "care_of" VARCHAR(140),
  "post_code" VARCHAR(16),
  "town_name" VARCHAR(140),
  "country_sub_division" VARCHAR(35),
  "country" VARCHAR(2)
);

CREATE TABLE "enterprise"."accounts" (
  "enterprise_account_id" SERIAL PRIMARY KEY,
  "opened_date" TIMESTAMPTZ,
  "status" enterprise.account_status NOT NULL,
  "status_update_date_time" TIMESTAMPTZ NOT NULL,
  "account_category" VARCHAR(40),
  "description" VARCHAR(35)
);

CREATE TABLE "enterprise"."account_ownership" (
  "enterprise_account_ownership_id" SERIAL PRIMARY KEY,
  "enterprise_account_id" INTEGER NOT NULL,
  "enterprise_party_id" INTEGER NOT NULL
);

CREATE TABLE "enterprise"."associates" (
  "enterprise_associate_id" SERIAL PRIMARY KEY,
  "first_name" VARCHAR(255),
  "last_name" VARCHAR(255),
  "email" VARCHAR(255) UNIQUE,
  "phone_number" VARCHAR(30),
  "hire_date" DATE,
  "status" enterprise.associate_status,
  "release_date" DATE,
  "job_title" VARCHAR(255),
  "officer_title" VARCHAR(50),
  "enterprise_department_id" INTEGER,
  "manager_id" INTEGER,
  "salary" decimal(10,2),
  "relationship_type" enterprise.relationship_status,
  "street_address" VARCHAR(255),
  "city" VARCHAR(255),
  "state" VARCHAR(2),
  "post_code" VARCHAR(10),
  "country" VARCHAR(255),
  "enterprise_building_id" INTEGER
);

CREATE TABLE "enterprise"."departments" (
  "enterprise_department_id" SERIAL PRIMARY KEY,
  "department_name" VARCHAR(255) UNIQUE,
  "location" VARCHAR(255),
  "operating_unit" enterprise.operating_unit
);

CREATE TABLE "enterprise"."buildings" (
  "enterprise_building_id" SERIAL PRIMARY KEY,
  "enterprise_address_id" INTEGER,
  "building_name" VARCHAR(255),
  "building_type" enterprise.building_type NOT NULL,
  "phone_number" VARCHAR(30),
  "open_date" DATE,
  "close_date" DATE
);

CREATE TABLE "consumer_banking"."accounts" (
  "consumer_banking_account_id" BIGSERIAL PRIMARY KEY,
  "enterprise_account_id" INT NOT NULL,
  "account_number" VARCHAR(20),
  "consumer_banking_product_id" INTEGER,
  "opened_date" TIMESTAMPTZ NOT NULL,
  "maturity_date" TIMESTAMPTZ,
  "nickname" VARCHAR(255),
  "displayName" VARCHAR(255),
  "account_category" enterprise.account_category DEFAULT 'PERSONAL',
  "currency_code" enterprise.currency_code,
  "status" consumer_banking.account_status NOT NULL,
  "switch_status" enterprise.switch_status DEFAULT 'NOT_SWITCHED',
  "status_update_date_time" TIMESTAMPTZ NOT NULL,
  "servicer_identifier_id" INT NOT NULL,
  "annualPercentageYield" NUMERIC(8,5),
  "interestYtd" NUMERIC(18,5),
  "term" NUMERIC(10,5),
  "available_balance" numeric(20,4) NOT NULL DEFAULT 0,
  "current_balance" numeric(20,4) NOT NULL DEFAULT 0,
  "opening_day_balance" numeric(20,4) NOT NULL DEFAULT 0
);

CREATE TABLE "consumer_banking"."account_access_consents" (
  "consumer_banking_consent_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "creation_date_time" TIMESTAMPTZ NOT NULL,
  "status" consumer_banking.consent_status NOT NULL,
  "status_update_date_time" TIMESTAMPTZ NOT NULL,
  "expiration_date_time" TIMESTAMPTZ
);

CREATE TABLE "consumer_banking"."account_access_consents_permissions" (
  "consumer_banking_consent_id" INTEGER,
  "enterprise_permission_id" INTEGER
);

CREATE TABLE "consumer_banking"."balances" (
  "consumer_banking_balance_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "credit_debit_indicator" enterprise.credit_debit_indicator NOT NULL,
  "type" consumer_banking.balance_type NOT NULL,
  "date_time" TIMESTAMPTZ NOT NULL,
  "amount" NUMERIC(18,5) NOT NULL,
  "currency" enterprise.currency_code NOT NULL,
  "sub_type" consumer_banking.balance_sub_type
);

CREATE TABLE "consumer_banking"."beneficiaries" (
  "consumer_banking_beneficiary_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "beneficiary_type" consumer_banking.beneficiary_type NOT NULL,
  "reference" VARCHAR(35),
  "supplementary_data" TEXT
);

CREATE TABLE "consumer_banking"."beneficiary_creditor_agents" (
  "consumer_banking_beneficiary_creditor_agent_id" SERIAL PRIMARY KEY,
  "consumer_banking_beneficiary_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(35) NOT NULL,
  "name" VARCHAR(140),
  "lei" VARCHAR(20)
);

CREATE TABLE "consumer_banking"."beneficiary_creditor_accounts" (
  "consumer_banking_beneficiary_creditor_account_id" SERIAL PRIMARY KEY,
  "consumer_banking_beneficiary_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(256) NOT NULL,
  "name" VARCHAR(350),
  "secondary_identification" VARCHAR(34)
);

CREATE TABLE "consumer_banking"."direct_debits" (
  "consumer_banking_direct_debit_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "direct_debit_status_code" consumer_banking.direct_debit_status_code NOT NULL,
  "name" VARCHAR(70) NOT NULL,
  "previous_payment_date_time" TIMESTAMPTZ,
  "previous_payment_amount" NUMERIC(18,5),
  "previous_payment_currency" VARCHAR(3)
);

CREATE TABLE "consumer_banking"."mandate_related_information" (
  "consumer_banking_mandate_related_information_id" SERIAL PRIMARY KEY,
  "consumer_banking_direct_debit_id" INTEGER NOT NULL,
  "mandate_id" INTEGER NOT NULL,
  "classification" consumer_banking.direct_debit_classification,
  "category" consumer_banking.direct_debit_category,
  "first_payment_date_time" TIMESTAMPTZ,
  "recurring_payment_date_time" TIMESTAMPTZ,
  "final_payment_date_time" TIMESTAMPTZ,
  "frequency_type" enterprise.frequency NOT NULL,
  "frequency_count_per_period" INT,
  "frequency_point_in_time" VARCHAR(2),
  "reason" VARCHAR(256)
);

CREATE TABLE "consumer_banking"."offers" (
  "consumer_banking_offer_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "offer_type" consumer_banking.offer_type NOT NULL,
  "description" VARCHAR(500),
  "start_date_time" TIMESTAMPTZ,
  "end_date_time" TIMESTAMPTZ,
  "rate" NUMERIC(10,4),
  "value" INT,
  "term" VARCHAR(500),
  "url" VARCHAR(256),
  "amount" NUMERIC(18,5),
  "amount_currency" enterprise.currency_code,
  "fee" NUMERIC(18,5),
  "fee_currency" enterprise.currency_code
);

CREATE TABLE "consumer_banking"."products" (
  "consumer_banking_product_id" SERIAL PRIMARY KEY,
  "product_code" VARCHAR(20) NOT NULL,
  "product_name" VARCHAR(100) NOT NULL,
  "product_type" consumer_banking.product_type NOT NULL,
  "description" TEXT,
  "min_opening_deposit" DECIMAL(18,2),
  "monthly_fee" DECIMAL(10,2),
  "fee_schedule" consumer_banking.account_fee_schedule NOT NULL DEFAULT 'STANDARD',
  "transaction_limit" INTEGER,
  "transaction_fee" DECIMAL(10,2),
  "min_balance" DECIMAL(18,2),
  "is_interest_bearing" BOOLEAN NOT NULL DEFAULT false,
  "base_interest_rate" DECIMAL(6,4),
  "interest_calculation_method" consumer_banking.interest_calculation_method,
  "term_length" INTEGER,
  "status" consumer_banking.product_status NOT NULL DEFAULT 'ACTIVE',
  "launch_date" DATE,
  "discontinue_date" DATE
);

CREATE TABLE "consumer_banking"."other_product_types" (
  "consumer_banking_other_product_type_id" SERIAL PRIMARY KEY,
  "consumer_banking_product_id" INTEGER NOT NULL,
  "name" VARCHAR(350) NOT NULL,
  "description" VARCHAR(350) NOT NULL
);

CREATE TABLE "consumer_banking"."scheduled_payments" (
  "consumer_banking_scheduled_payment_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "scheduled_payment_date_time" TIMESTAMPTZ NOT NULL,
  "scheduled_type" consumer_banking.scheduled_payment_type NOT NULL,
  "payment_method" consumer_banking.payment_method NOT NULL,
  "payment_status" consumer_banking.scheduled_payment_status NOT NULL DEFAULT 'PENDING',
  "frequency" enterprise.frequency,
  "reference" VARCHAR(35),
  "debtor_reference" VARCHAR(35),
  "instructed_amount" NUMERIC(18,5) NOT NULL,
  "instructed_amount_currency" enterprise.currency_code NOT NULL,
  "end_date" DATE,
  "execution_count" INTEGER,
  "max_executions" INTEGER
);

CREATE TABLE "consumer_banking"."scheduled_payment_creditor_agents" (
  "consumer_banking_scheduled_payment_creditor_agent_id" SERIAL PRIMARY KEY,
  "consumer_banking_scheduled_payment_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(256) NOT NULL,
  "name" VARCHAR(140),
  "lei" VARCHAR(20)
);

CREATE TABLE "consumer_banking"."scheduled_payment_creditor_accounts" (
  "consumer_banking_scheduled_payment_creditor_account_id" SERIAL PRIMARY KEY,
  "consumer_banking_scheduled_payment_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(256) NOT NULL,
  "name" VARCHAR(350),
  "secondary_identification" VARCHAR(34)
);

CREATE TABLE "consumer_banking"."standing_orders" (
  "consumer_banking_standing_order_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "next_payment_date_time" TIMESTAMPTZ,
  "last_payment_date_time" TIMESTAMPTZ,
  "standing_order_status_code" consumer_banking.standing_order_status_code NOT NULL DEFAULT 'ACTIVE',
  "first_payment_amount" NUMERIC(18,5),
  "first_payment_currency" enterprise.currency_code,
  "next_payment_amount" NUMERIC(18,5),
  "next_payment_currency" enterprise.currency_code,
  "last_payment_amount" NUMERIC(18,5),
  "last_payment_currency" enterprise.currency_code,
  "final_payment_amount" NUMERIC(18,5),
  "final_payment_currency" enterprise.currency_code,
  "frequency" enterprise.frequency NOT NULL,
  "start_date" DATE NOT NULL,
  "end_date" DATE,
  "day_of_month" INTEGER,
  "day_of_week" INTEGER,
  "payment_type" consumer_banking.standing_order_type NOT NULL DEFAULT 'FIXED_AMOUNT',
  "category" consumer_banking.standing_order_category,
  "reference" VARCHAR(100),
  "description" VARCHAR(255),
  "created_date" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  "created_by" VARCHAR(50),
  "modified_date" TIMESTAMPTZ,
  "supplementary_data" TEXT
);

CREATE TABLE "consumer_banking"."standing_order_creditor_agents" (
  "consumer_banking_standing_order_creditor_agent_id" SERIAL PRIMARY KEY,
  "consumer_banking_standing_order_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(35) NOT NULL,
  "name" VARCHAR(140),
  "lei" VARCHAR(20)
);

CREATE TABLE "consumer_banking"."standing_order_creditor_accounts" (
  "consumer_banking_standing_order_creditor_account_id" SERIAL PRIMARY KEY,
  "consumer_banking_standing_order_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(256) NOT NULL,
  "name" VARCHAR(350),
  "secondary_identification" VARCHAR(34)
);

CREATE TABLE "consumer_banking"."statements" (
  "consumer_banking_statement_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "statement_reference" VARCHAR(35),
  "type" consumer_banking.statement_type NOT NULL,
  "start_date_time" TIMESTAMPTZ NOT NULL,
  "end_date_time" TIMESTAMPTZ NOT NULL,
  "creation_date_time" TIMESTAMPTZ NOT NULL
);

CREATE TABLE "consumer_banking"."statement_descriptions" (
  "consumer_banking_statement_description_id" SERIAL PRIMARY KEY,
  "consumer_banking_statement_id" INTEGER NOT NULL,
  "description" VARCHAR(500) NOT NULL
);

CREATE TABLE "consumer_banking"."statement_benefits" (
  "consumer_banking_statement_benefit_id" SERIAL PRIMARY KEY,
  "consumer_banking_statement_id" INTEGER NOT NULL,
  "type" consumer_banking.benefit_type NOT NULL,
  "amount" NUMERIC(18,5) NOT NULL,
  "currency" VARCHAR(3) NOT NULL
);

CREATE TABLE "consumer_banking"."statement_fees" (
  "consumer_banking_statement_fee_id" SERIAL PRIMARY KEY,
  "consumer_banking_statement_id" INTEGER NOT NULL,
  "description" VARCHAR(128),
  "credit_debit_indicator" enterprise.credit_debit_indicator NOT NULL,
  "type" consumer_banking.fee_type NOT NULL,
  "rate" NUMERIC(10,4),
  "rate_type" consumer_banking.rate_type,
  "frequency" consumer_banking.fee_frequency,
  "amount" NUMERIC(18,5) NOT NULL,
  "currency" enterprise.currency_code NOT NULL
);

CREATE TABLE "consumer_banking"."statement_interests" (
  "consumer_banking_statement_interest_id" SERIAL PRIMARY KEY,
  "consumer_banking_statement_id" INTEGER NOT NULL,
  "description" VARCHAR(128),
  "credit_debit_indicator" enterprise.credit_debit_indicator NOT NULL,
  "type" consumer_banking.interest_type NOT NULL,
  "rate" NUMERIC(10,4),
  "rate_type" consumer_banking.rate_type,
  "frequency" enterprise.frequency,
  "amount" NUMERIC(18,5) NOT NULL,
  "currency" enterprise.currency_code NOT NULL
);

CREATE TABLE "consumer_banking"."statement_amounts" (
  "consumer_banking_statement_amount_id" SERIAL PRIMARY KEY,
  "consumer_banking_statement_id" INTEGER NOT NULL,
  "credit_debit_indicator" enterprise.credit_debit_indicator NOT NULL,
  "type" consumer_banking.amount_type NOT NULL,
  "amount" NUMERIC(18,5) NOT NULL,
  "currency" enterprise.currency_code NOT NULL,
  "sub_type" consumer_banking.amount_sub_type
);

CREATE TABLE "consumer_banking"."statement_date_times" (
  "consumer_banking_statement_date_time_id" SERIAL PRIMARY KEY,
  "consumer_banking_statement_id" INTEGER NOT NULL,
  "date_time" TIMESTAMPTZ NOT NULL,
  "type" consumer_banking.statement_date_type NOT NULL
);

CREATE TABLE "consumer_banking"."statement_rates" (
  "consumer_banking_statement_rate_id" SERIAL PRIMARY KEY,
  "consumer_banking_statement_id" INTEGER NOT NULL,
  "rate" NUMERIC(10,4) NOT NULL,
  "type" consumer_banking.statement_rate_type NOT NULL,
  "description" VARCHAR(255),
  "effective_date" DATE,
  "expiration_date" DATE,
  "is_variable" BOOLEAN NOT NULL DEFAULT false,
  "index_rate" NUMERIC(10,4),
  "margin" NUMERIC(10,4),
  "balance_subject_to_rate" NUMERIC(18,2),
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  "updated_at" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "consumer_banking"."statement_values" (
  "consumer_banking_statement_value_id" SERIAL PRIMARY KEY,
  "consumer_banking_statement_id" INTEGER NOT NULL,
  "value" VARCHAR(255) NOT NULL,
  "type" consumer_banking.statement_value_type NOT NULL,
  "description" VARCHAR(255),
  "previous_value" VARCHAR(255),
  "change_percentage" NUMERIC(10,2),
  "is_estimated" BOOLEAN NOT NULL DEFAULT false,
  "reference_period_start" DATE,
  "reference_period_end" DATE,
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  "updated_at" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "consumer_banking"."transactions" (
  "consumer_banking_transaction_id" SERIAL PRIMARY KEY,
  "consumer_banking_account_id" BIGINT NOT NULL,
  "consumer_banking_balance_id" INTEGER,
  "transaction_reference" VARCHAR(210),
  "credit_debit_indicator" enterprise.credit_debit_indicator NOT NULL,
  "status" consumer_banking.transaction_status NOT NULL,
  "transaction_mutability" consumer_banking.transaction_mutability,
  "transaction_date" TIMESTAMPTZ NOT NULL,
  "category" consumer_banking.transaction_category,
  "transaction_type" consumer_banking.transaction_type,
  "value_date" TIMESTAMPTZ,
  "description" VARCHAR(500),
  "merchant_address" VARCHAR(70),
  "amount" NUMERIC(18,5) NOT NULL,
  "currency" enterprise.currency_code NOT NULL,
  "charge_amount" NUMERIC(18,5),
  "charge_currency" enterprise.currency_code
);

CREATE TABLE "consumer_banking"."transaction_statement_references" (
  "consumer_banking_transaction_statement_reference_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "statement_reference" VARCHAR(35)
);

CREATE TABLE "consumer_banking"."transaction_currency_exchanges" (
  "consumer_banking_transaction_currency_exchange_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "source_currency" enterprise.currency_code NOT NULL,
  "target_currency" enterprise.currency_code,
  "unit_currency" enterprise.currency_code,
  "exchange_rate" NUMERIC(10,4) NOT NULL,
  "contract_identification" VARCHAR(39),
  "quotation_date" TIMESTAMPTZ,
  "instructed_amount" NUMERIC(18,5),
  "instructed_amount_currency" enterprise.currency_code
);

CREATE TABLE "consumer_banking"."transaction_bank_transaction_codes" (
  "consumer_banking_transaction_bank_transaction_code_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "code" consumer_banking.transaction_bank_code NOT NULL
);

CREATE TABLE "consumer_banking"."proprietary_transaction_codes" (
  "consumer_banking_proprietary_transaction_code_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "code" VARCHAR(35) NOT NULL,
  "issuer" VARCHAR(35)
);

CREATE TABLE "consumer_banking"."transaction_balances" (
  "consumer_banking_transaction_balance_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "credit_debit_indicator" enterprise.credit_debit_indicator NOT NULL,
  "type" consumer_banking.balance_type NOT NULL,
  "amount" NUMERIC(18,5) NOT NULL,
  "currency" enterprise.currency_code NOT NULL
);

CREATE TABLE "consumer_banking"."transaction_merchant_details" (
  "consumer_banking_transaction_merchant_detail_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "merchant_name" VARCHAR(350) NOT NULL,
  "merchant_category_code" VARCHAR(20) NOT NULL
);

CREATE TABLE "consumer_banking"."transaction_creditor_agents" (
  "consumer_banking_transaction_creditor_agent_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(35) NOT NULL,
  "name" VARCHAR(140),
  "lei" VARCHAR(20)
);

CREATE TABLE "consumer_banking"."transaction_creditor_accounts" (
  "consumer_banking_transaction_creditor_account_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(256) NOT NULL,
  "name" VARCHAR(350),
  "secondary_identification" VARCHAR(34)
);

CREATE TABLE "consumer_banking"."transaction_debtor_agents" (
  "consumer_banking_transaction_debtor_agent_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(35) NOT NULL,
  "name" VARCHAR(140),
  "lei" VARCHAR(20)
);

CREATE TABLE "consumer_banking"."transaction_debtor_accounts" (
  "consumer_banking_transaction_debtor_account_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "scheme_name" enterprise.identifier_scheme NOT NULL,
  "identification" VARCHAR(256) NOT NULL,
  "name" VARCHAR(350),
  "secondary_identification" VARCHAR(34)
);

CREATE TABLE "consumer_banking"."transaction_card_instruments" (
  "consumer_banking_transaction_card_instrument_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "card_scheme_name" consumer_banking.card_scheme_name NOT NULL,
  "authorisation_type" consumer_banking.authorization_type,
  "name" VARCHAR(70),
  "identification" VARCHAR(34)
);

CREATE TABLE "consumer_banking"."transaction_ultimate_creditors" (
  "consumer_banking_transaction_ultimate_creditor_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "name" VARCHAR(140) NOT NULL,
  "identification" VARCHAR(256),
  "lei" VARCHAR(20),
  "scheme_name" VARCHAR(100)
);

CREATE TABLE "consumer_banking"."transaction_ultimate_debtors" (
  "consumer_banking_transaction_ultimate_debtor_id" SERIAL PRIMARY KEY,
  "consumer_banking_transaction_id" INTEGER NOT NULL,
  "name" VARCHAR(140) NOT NULL,
  "identification" VARCHAR(256),
  "lei" VARCHAR(20),
  "scheme_name" VARCHAR(100)
);

CREATE TABLE "consumer_banking"."account_statement_preferences" (
  "consumer_banking_account_id" BIGINT NOT NULL,
  "consumer_banking_statement_id" INTEGER,
  "frequency" enterprise.frequency NOT NULL,
  "format" consumer_banking.statement_format NOT NULL,
  "communication_method" consumer_banking.communication_method NOT NULL DEFAULT 'EMAIL',
  "next_statement_date" DATE,
  "last_statement_date" DATE,
  "enterprise_address_id" INTEGER
);

CREATE TABLE "consumer_banking"."customer_interactions" (
  "consumer_banking_interaction_id" SERIAL PRIMARY KEY,
  "customer_id" INT,
  "account_id" BIGINT,
  "enterprise_associate_id" INT,
  "interaction_type" consumer_banking.interaction_type,
  "interaction_date_time" TIMESTAMPTZ,
  "channel" consumer_banking.interaction_channel,
  "subject" VARCHAR(255),
  "description" TEXT,
  "resolution" TEXT,
  "status" consumer_banking.interaction_status,
  "priority" consumer_banking.interaction_priority,
  "related_transaction_id" INT,
  "created_at" TIMESTAMPTZ DEFAULT (now()),
  "updated_at" TIMESTAMPTZ DEFAULT (now())
);

CREATE TABLE "mortgage_services"."application_borrowers" (
  "mortgage_services_application_borrower_id" SERIAL,
  "mortgage_services_application_id" INTEGER NOT NULL,
  "mortgage_services_borrower_id" INTEGER NOT NULL,
  "borrower_type" mortgage_services.borrower_type NOT NULL,
  "relationship_to_primary" mortgage_services.relationship_type,
  "contribution_percentage" NUMERIC(5,2),
  PRIMARY KEY ("mortgage_services_application_borrower_id", "mortgage_services_application_id")
);

CREATE TABLE "mortgage_services"."borrowers" (
  "mortgage_services_borrower_id" SERIAL PRIMARY KEY,
  "enterprise_party_id" INTEGER NOT NULL,
  "years_in_school" INTEGER,
  "dependent_count" INTEGER,
  "current_address_id" INTEGER,
  "mailing_address_id" INTEGER,
  "previous_address_id" INTEGER
);

CREATE TABLE "mortgage_services"."borrower_employments" (
  "mortgage_services_employment_id" SERIAL PRIMARY KEY,
  "mortgage_services_borrower_id" INTEGER NOT NULL,
  "employer_name" VARCHAR(150) NOT NULL,
  "position" VARCHAR(100) NOT NULL,
  "phone" VARCHAR(30),
  "employment_type" mortgage_services.employment_type NOT NULL,
  "start_date" DATE NOT NULL,
  "end_date" DATE,
  "is_current" BOOLEAN NOT NULL,
  "years_in_profession" INTEGER,
  "monthly_income" NUMERIC(18,2) NOT NULL,
  "verification_status" mortgage_services.verification_status NOT NULL,
  "verification_date" DATE
);

CREATE TABLE "mortgage_services"."borrower_incomes" (
  "mortgage_services_income_id" SERIAL PRIMARY KEY,
  "mortgage_services_borrower_id" INTEGER NOT NULL,
  "income_type" mortgage_services.income_type NOT NULL,
  "amount" NUMERIC(18,2) NOT NULL,
  "frequency" mortgage_services.income_frequency NOT NULL,
  "verification_status" mortgage_services.verification_status NOT NULL,
  "verification_date" DATE
);

CREATE TABLE "mortgage_services"."borrower_assets" (
  "mortgage_services_asset_id" SERIAL PRIMARY KEY,
  "mortgage_services_borrower_id" INTEGER NOT NULL,
  "asset_type" mortgage_services.asset_type NOT NULL,
  "institution_name" VARCHAR(100),
  "account_number" VARCHAR(50),
  "current_value" NUMERIC(18,2) NOT NULL,
  "verification_status" mortgage_services.verification_status NOT NULL,
  "verification_date" DATE,
  "property_address" VARCHAR(500)
);

CREATE TABLE "mortgage_services"."borrower_liabilities" (
  "mortgage_services_liability_id" SERIAL PRIMARY KEY,
  "mortgage_services_borrower_id" INTEGER NOT NULL,
  "liability_type" mortgage_services.liability_type NOT NULL,
  "creditor_name" VARCHAR(100) NOT NULL,
  "account_number" VARCHAR(50),
  "monthly_payment" NUMERIC(18,2) NOT NULL,
  "current_balance" NUMERIC(18,2) NOT NULL,
  "original_amount" NUMERIC(18,2),
  "interest_rate" NUMERIC(6,3),
  "origination_date" DATE,
  "maturity_date" DATE,
  "verification_status" mortgage_services.verification_status NOT NULL,
  "verification_date" DATE,
  "will_be_paid_off" BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE "mortgage_services"."properties" (
  "mortgage_services_property_id" SERIAL PRIMARY KEY,
  "mortgage_services_application_id" INTEGER NOT NULL,
  "address" VARCHAR(500) NOT NULL,
  "property_type" mortgage_services.property_type NOT NULL,
  "occupancy_type" mortgage_services.occupancy_type NOT NULL,
  "year_built" INTEGER,
  "bedrooms" INTEGER,
  "bathrooms" NUMERIC(3,1),
  "square_feet" INTEGER,
  "lot_size" NUMERIC(10,2),
  "hoa_dues" NUMERIC(10,2),
  "is_new_construction" BOOLEAN,
  "construction_completion_date" DATE
);

CREATE TABLE "mortgage_services"."applications" (
  "mortgage_services_application_id" SERIAL PRIMARY KEY,
  "mortgage_services_loan_product_id" INTEGER NOT NULL,
  "application_type" mortgage_services.application_type NOT NULL,
  "status" mortgage_services.application_status NOT NULL,
  "loan_purpose" mortgage_services.loan_purpose,
  "submission_channel" mortgage_services.submission_channel,
  "creation_date_time" TIMESTAMPTZ NOT NULL,
  "submission_date_time" TIMESTAMPTZ,
  "last_updated_date_time" TIMESTAMPTZ NOT NULL,
  "requested_loan_amount" NUMERIC(18,2) NOT NULL,
  "requested_loan_term_months" INTEGER NOT NULL,
  "estimated_property_value" NUMERIC(18,2),
  "estimated_credit_score" INTEGER,
  "referral_source" VARCHAR(100),
  "loan_officer_id" INTEGER,
  "branch_id" INTEGER
);

CREATE TABLE "mortgage_services"."loans" (
  "mortgage_services_loan_id" SERIAL PRIMARY KEY,
  "mortgage_services_application_id" INTEGER NOT NULL,
  "enterprise_account_id" INTEGER NOT NULL,
  "interest_rate" NUMERIC(6,3),
  "loan_term_months" INTEGER,
  "loan_amount" NUMERIC(18,2),
  "down_payment" NUMERIC(18,2),
  "down_payment_percentage" NUMERIC(5,2),
  "closing_costs" NUMERIC(18,2),
  "monthly_payment" NUMERIC(18,2),
  "private_mortgage_insurance" BOOLEAN,
  "pmi_rate" NUMERIC(5,3),
  "escrow_amount" NUMERIC(18,2),
  "origination_date" DATE,
  "first_payment_date" DATE,
  "maturity_date" DATE
);

CREATE TABLE "mortgage_services"."loan_products" (
  "mortgage_services_loan_product_id" SERIAL PRIMARY KEY,
  "product_name" VARCHAR(100) NOT NULL,
  "product_code" VARCHAR(20) NOT NULL,
  "loan_type" mortgage_services.loan_type NOT NULL,
  "interest_rate_type" mortgage_services.interest_rate_type NOT NULL,
  "description" TEXT,
  "base_interest_rate" NUMERIC(6,3) NOT NULL,
  "min_term_months" INTEGER NOT NULL,
  "max_term_months" INTEGER NOT NULL,
  "min_loan_amount" NUMERIC(18,2),
  "max_loan_amount" NUMERIC(18,2),
  "min_credit_score" INTEGER,
  "min_down_payment_percentage" NUMERIC(5,2),
  "requires_pmi" BOOLEAN,
  "is_active" BOOLEAN NOT NULL DEFAULT true,
  "launch_date" DATE,
  "discontinue_date" DATE
);

CREATE TABLE "mortgage_services"."loan_rate_locks" (
  "mortgage_services_rate_lock_id" SERIAL PRIMARY KEY,
  "mortgage_services_loan_id" INTEGER NOT NULL,
  "lock_date" TIMESTAMPTZ NOT NULL,
  "expiration_date" TIMESTAMPTZ NOT NULL,
  "locked_interest_rate" NUMERIC(6,3) NOT NULL,
  "lock_period_days" INTEGER NOT NULL,
  "status" mortgage_services.loan_rate_lock_status NOT NULL,
  "lock_fee" NUMERIC(10,2),
  "extension_date" TIMESTAMPTZ,
  "extension_fee" NUMERIC(10,2)
);

CREATE TABLE "mortgage_services"."documents" (
  "mortgage_services_document_id" SERIAL PRIMARY KEY,
  "mortgage_services_application_id" INTEGER NOT NULL,
  "document_type" mortgage_services.document_type NOT NULL,
  "document_name" VARCHAR(255) NOT NULL,
  "document_path" VARCHAR(500) NOT NULL,
  "upload_date" TIMESTAMPTZ NOT NULL,
  "status" mortgage_services.document_status NOT NULL,
  "review_date" TIMESTAMPTZ,
  "reviewer_id" INTEGER,
  "expiration_date" DATE,
  "notes" TEXT
);

CREATE TABLE "mortgage_services"."conditions" (
  "mortgage_services_condition_id" SERIAL PRIMARY KEY,
  "mortgage_services_application_id" INTEGER NOT NULL,
  "condition_type" mortgage_services.condition_type NOT NULL,
  "description" TEXT NOT NULL,
  "status" mortgage_services.condition_status NOT NULL,
  "created_date" TIMESTAMPTZ NOT NULL,
  "created_by_id" INTEGER NOT NULL,
  "due_date" DATE,
  "cleared_date" TIMESTAMPTZ,
  "cleared_by_id" INTEGER
);

CREATE TABLE "mortgage_services"."appraisals" (
  "mortgage_services_appraisal_id" SERIAL PRIMARY KEY,
  "mortgage_services_application_id" INTEGER NOT NULL,
  "mortgage_services_property_id" INTEGER NOT NULL,
  "appraisal_type" mortgage_services.appraisal_type NOT NULL,
  "ordered_date" TIMESTAMPTZ NOT NULL,
  "appraiser_name" VARCHAR(100),
  "appraisal_company" VARCHAR(100),
  "inspection_date" DATE,
  "completion_date" DATE,
  "appraised_value" NUMERIC(18,2),
  "status" mortgage_services.appraisal_status NOT NULL,
  "appraisal_fee" NUMERIC(10,2),
  "report_path" VARCHAR(500)
);

CREATE TABLE "mortgage_services"."credit_reports" (
  "mortgage_services_credit_report_id" SERIAL PRIMARY KEY,
  "mortgage_services_application_id" INTEGER NOT NULL,
  "mortgage_services_borrower_id" INTEGER NOT NULL,
  "report_date" TIMESTAMPTZ NOT NULL,
  "expiration_date" DATE NOT NULL,
  "credit_score" INTEGER,
  "report_type" mortgage_services.credit_report_type NOT NULL,
  "bureau_name" mortgage_services.credit_bureau,
  "report_path" VARCHAR(500),
  "status" mortgage_services.verification_status NOT NULL
);

CREATE TABLE "mortgage_services"."closing_disclosures" (
  "mortgage_services_disclosure_id" SERIAL PRIMARY KEY,
  "mortgage_services_loan_id" INTEGER NOT NULL,
  "disclosure_type" mortgage_services.disclosure_type NOT NULL,
  "created_date" TIMESTAMPTZ NOT NULL,
  "sent_date" TIMESTAMPTZ,
  "received_date" TIMESTAMPTZ,
  "delivery_method" mortgage_services.delivery_method NOT NULL,
  "document_path" VARCHAR(500),
  "loan_amount" NUMERIC(18,2) NOT NULL,
  "interest_rate" NUMERIC(6,3) NOT NULL,
  "monthly_payment" NUMERIC(18,2) NOT NULL,
  "total_closing_costs" NUMERIC(18,2) NOT NULL,
  "cash_to_close" NUMERIC(18,2) NOT NULL
);

CREATE TABLE "mortgage_services"."closing_appointments" (
  "mortgage_services_appointment_id" SERIAL PRIMARY KEY,
  "mortgage_services_loan_id" INTEGER NOT NULL,
  "scheduled_date" TIMESTAMPTZ NOT NULL,
  "location_address_id" INTEGER,
  "status" mortgage_services.appointment_status NOT NULL,
  "closing_type" mortgage_services.closing_type NOT NULL,
  "closing_agent" VARCHAR(100),
  "closing_company" VARCHAR(100),
  "closing_fee" NUMERIC(10,2),
  "actual_closing_date" TIMESTAMPTZ,
  "notes" TEXT
);

CREATE TABLE "mortgage_services"."closed_loans" (
  "mortgage_services_closed_loan_id" SERIAL PRIMARY KEY,
  "mortgage_services_loan_id" INTEGER NOT NULL,
  "closing_date" DATE NOT NULL,
  "funding_date" DATE NOT NULL,
  "final_loan_amount" NUMERIC(18,2) NOT NULL,
  "final_interest_rate" NUMERIC(6,3) NOT NULL,
  "final_monthly_payment" NUMERIC(18,2) NOT NULL,
  "final_cash_to_close" NUMERIC(18,2) NOT NULL,
  "disbursement_date" DATE,
  "first_payment_date" DATE NOT NULL,
  "maturity_date" DATE NOT NULL,
  "recording_date" DATE,
  "settlement_agent" VARCHAR(100),
  "settlement_company" VARCHAR(100)
);

CREATE TABLE "mortgage_services"."servicing_accounts" (
  "mortgage_services_servicing_account_id" SERIAL PRIMARY KEY,
  "mortgage_services_loan_id" INTEGER NOT NULL,
  "status" mortgage_services.servicing_account_status NOT NULL,
  "current_principal_balance" NUMERIC(18,2) NOT NULL,
  "original_principal_balance" NUMERIC(18,2) NOT NULL,
  "current_interest_rate" NUMERIC(6,3) NOT NULL,
  "escrow_balance" NUMERIC(18,2),
  "next_payment_due_date" DATE,
  "next_payment_amount" NUMERIC(18,2),
  "last_payment_date" DATE,
  "last_payment_amount" NUMERIC(18,2),
  "interest_paid_ytd" NUMERIC(18,2),
  "principal_paid_ytd" NUMERIC(18,2),
  "escrow_paid_ytd" NUMERIC(18,2),
  "property_tax_due_date" DATE,
  "homeowners_insurance_due_date" DATE,
  "servicing_transferred_date" DATE
);

CREATE TABLE "mortgage_services"."payments" (
  "mortgage_services_payment_id" SERIAL PRIMARY KEY,
  "mortgage_services_servicing_account_id" INTEGER NOT NULL,
  "payment_date" TIMESTAMPTZ NOT NULL,
  "payment_type" mortgage_services.payment_type NOT NULL,
  "payment_method" VARCHAR(30) NOT NULL,
  "payment_amount" NUMERIC(18,2) NOT NULL,
  "principal_amount" NUMERIC(18,2) NOT NULL,
  "interest_amount" NUMERIC(18,2) NOT NULL,
  "escrow_amount" NUMERIC(18,2),
  "late_fee_amount" NUMERIC(10,2),
  "other_fee_amount" NUMERIC(10,2),
  "transaction_id" VARCHAR(30),
  "confirmation_number" VARCHAR(50),
  "status" VARCHAR(20) NOT NULL
);

CREATE TABLE "mortgage_services"."escrow_disbursements" (
  "mortgage_services_disbursement_id" SERIAL PRIMARY KEY,
  "mortgage_services_servicing_account_id" INTEGER NOT NULL,
  "disbursement_date" DATE NOT NULL,
  "disbursement_type" mortgage_services.disbursement_type NOT NULL,
  "amount" NUMERIC(18,2) NOT NULL,
  "payee_name" VARCHAR(100) NOT NULL,
  "payee_account_number" VARCHAR(50),
  "check_number" VARCHAR(20),
  "status" mortgage_services.disbursement_status NOT NULL,
  "due_date" DATE,
  "coverage_start_date" DATE,
  "coverage_end_date" DATE
);

CREATE TABLE "mortgage_services"."escrow_analyses" (
  "mortgage_services_analysis_id" SERIAL PRIMARY KEY,
  "mortgage_services_servicing_account_id" INTEGER NOT NULL,
  "analysis_date" DATE NOT NULL,
  "effective_date" DATE NOT NULL,
  "previous_monthly_escrow" NUMERIC(18,2),
  "new_monthly_escrow" NUMERIC(18,2) NOT NULL,
  "escrow_shortage" NUMERIC(18,2),
  "escrow_surplus" NUMERIC(18,2),
  "shortage_spread_months" INTEGER,
  "surplus_refund_amount" NUMERIC(18,2),
  "status" mortgage_services.escrow_analysis_status NOT NULL,
  "customer_notification_date" DATE
);

CREATE TABLE "mortgage_services"."insurance_policies" (
  "mortgage_services_policy_id" SERIAL PRIMARY KEY,
  "mortgage_services_servicing_account_id" INTEGER NOT NULL,
  "insurance_type" mortgage_services.insurance_type NOT NULL,
  "carrier_name" VARCHAR(100) NOT NULL,
  "policy_number" VARCHAR(50) NOT NULL,
  "coverage_amount" NUMERIC(18,2) NOT NULL,
  "annual_premium" NUMERIC(18,2) NOT NULL,
  "effective_date" DATE NOT NULL,
  "expiration_date" DATE NOT NULL,
  "paid_through_escrow" BOOLEAN NOT NULL,
  "agent_name" VARCHAR(100),
  "agent_phone" VARCHAR(30),
  "status" mortgage_services.insurance_policy_status NOT NULL
);

CREATE TABLE "mortgage_services"."loan_modifications" (
  "mortgage_services_modification_id" SERIAL PRIMARY KEY,
  "loan_account_id" INTEGER NOT NULL,
  "modification_type" mortgage_services.loan_modification_type NOT NULL,
  "request_date" DATE NOT NULL,
  "approval_date" DATE,
  "effective_date" DATE,
  "original_rate" NUMERIC(6,3),
  "new_rate" NUMERIC(6,3),
  "original_term_months" INTEGER,
  "new_term_months" INTEGER,
  "original_principal_balance" NUMERIC(18,2),
  "new_principal_balance" NUMERIC(18,2),
  "capitalized_amount" NUMERIC(18,2),
  "status" mortgage_services.loan_modification_status NOT NULL,
  "hardship_reason" mortgage_services.hardship_reason NOT NULL,
  "approved_by_id" INTEGER,
  "document_path" VARCHAR(500)
);

CREATE TABLE "mortgage_services"."customer_communications" (
  "mortgage_services_communication_id" SERIAL PRIMARY KEY,
  "mortgage_services_servicing_account_id" INTEGER,
  "mortgage_services_application_id" INTEGER,
  "communication_date" TIMESTAMPTZ NOT NULL,
  "communication_type" mortgage_services.communication_type NOT NULL,
  "direction" mortgage_services.communication_direction NOT NULL,
  "subject" VARCHAR(255),
  "content" TEXT,
  "sender" VARCHAR(100),
  "recipient" VARCHAR(100),
  "template_id" VARCHAR(30),
  "status" mortgage_services.communication_status NOT NULL,
  "document_path" VARCHAR(500),
  "related_to" mortgage_services.communication_purpose
);

CREATE TABLE "mortgage_services"."hmda_records" (
  "mortgage_services_hmda_record_id" SERIAL PRIMARY KEY,
  "mortgage_services_application_id" INTEGER NOT NULL,
  "mortgage_services_loan_id" INTEGER,
  "reporting_year" INTEGER NOT NULL,
  "lei" VARCHAR(20) NOT NULL,
  "mortgage_services_loan_product_id" INTEGER NOT NULL,
  "loan_purpose" mortgage_services.hmda_loan_purpose NOT NULL,
  "preapproval" mortgage_services.hmda_preapproval NOT NULL,
  "construction_method" mortgage_services.hmda_construction_method NOT NULL,
  "occupancy_type" mortgage_services.hmda_occupancy_type NOT NULL,
  "loan_amount" NUMERIC(18,2) NOT NULL,
  "action_taken" mortgage_services.hmda_action_taken NOT NULL,
  "action_taken_date" DATE NOT NULL,
  "state" VARCHAR(2) NOT NULL,
  "county" VARCHAR(5) NOT NULL,
  "census_tract" VARCHAR(11) NOT NULL,
  "rate_spread" NUMERIC(6,3),
  "hoepa_status" mortgage_services.hmda_hoepa_status NOT NULL,
  "lien_status" mortgage_services.hmda_lien_status NOT NULL,
  "credit_score_applicant" INTEGER,
  "credit_score_co_applicant" INTEGER,
  "credit_score_model" mortgage_services.hmda_credit_score_model,
  "denial_reason1" mortgage_services.hmda_denial_reason,
  "denial_reason2" mortgage_services.hmda_denial_reason,
  "denial_reason3" mortgage_services.hmda_denial_reason,
  "denial_reason4" mortgage_services.hmda_denial_reason,
  "total_loan_costs" NUMERIC(18,2),
  "total_points_and_fees" NUMERIC(18,2),
  "origination_charges" NUMERIC(18,2),
  "discount_points" NUMERIC(18,2),
  "lender_credits" NUMERIC(18,2),
  "loan_term" INTEGER,
  "intro_rate_period" INTEGER,
  "balloon_payment" mortgage_services.hmda_balloon_payment,
  "interest_only_payment" mortgage_services.hmda_interest_only,
  "negative_amortization" mortgage_services.hmda_negative_amortization,
  "other_non_amortizing_features" mortgage_services.hmda_other_non_amortizing,
  "property_value" NUMERIC(18,2),
  "manufactured_home_secured_property_type" mortgage_services.hmda_manufactured_home_type,
  "manufactured_home_land_property_interest" mortgage_services.hmda_manufactured_land_property_interest,
  "total_units" INTEGER NOT NULL,
  "multifamily_affordable_units" INTEGER,
  "submission_of_application" mortgage_services.hmda_submission_method,
  "initially_payable_to_institution" BOOLEAN,
  "aus1" mortgage_services.hmda_aus,
  "aus2" mortgage_services.hmda_aus,
  "aus3" mortgage_services.hmda_aus,
  "aus4" mortgage_services.hmda_aus,
  "aus5" mortgage_services.hmda_aus,
  "reverse_mortgage" mortgage_services.hmda_reverse_mortgage,
  "open_end_line_of_credit" mortgage_services.hmda_open_end_line_of_credit,
  "business_or_commercial_purpose" mortgage_services.hmda_business_or_commercial_purpose,
  "submission_status" mortgage_services.hmda_submission_status NOT NULL DEFAULT 'PENDING',
  "last_submission_date" DATE,
  "last_modified_date" TIMESTAMPTZ NOT NULL,
  "edit_status" mortgage_services.hmda_record_edit_status NOT NULL DEFAULT 'NOT_STARTED'
);

CREATE TABLE "mortgage_services"."hmda_applicant_demographics" (
  "mortgage_services_applicant_demographics_id" SERIAL PRIMARY KEY,
  "mortgage_services_hmda_record_id" INTEGER NOT NULL,
  "applicant_type" mortgage_services.hmda_applicant_type NOT NULL,
  "ethnicity_1" mortgage_services.hmda_ethnicity,
  "ethnicity_2" mortgage_services.hmda_ethnicity_detail,
  "ethnicity_3" mortgage_services.hmda_ethnicity_detail,
  "ethnicity_4" mortgage_services.hmda_ethnicity_detail,
  "ethnicity_5" mortgage_services.hmda_ethnicity_detail,
  "ethnicity_free_form" VARCHAR(100),
  "ethnicity_observed" mortgage_services.hmda_collection_method,
  "race_1" mortgage_services.hmda_race,
  "race_2" mortgage_services.hmda_race,
  "race_3" mortgage_services.hmda_race,
  "race_4" mortgage_services.hmda_race,
  "race_5" mortgage_services.hmda_race,
  "race_detail_1" VARCHAR(100),
  "race_detail_2" VARCHAR(100),
  "race_detail_3" VARCHAR(100),
  "race_detail_4" VARCHAR(100),
  "race_detail_5" VARCHAR(100),
  "race_free_form" VARCHAR(100),
  "race_observed" mortgage_services.hmda_collection_method,
  "sex" mortgage_services.hmda_sex,
  "sex_observed" mortgage_services.hmda_collection_method,
  "age" INTEGER,
  "age_group" mortgage_services.hmda_age_group,
  "income" NUMERIC(18,2),
  "debt_to_income_ratio" NUMERIC(6,3),
  "applicant_present" mortgage_services.hmda_applicant_present,
  "created_date" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  "modified_date" TIMESTAMPTZ
);

CREATE TABLE "mortgage_services"."hmda_edits" (
  "mortgage_services_edit_id" SERIAL PRIMARY KEY,
  "mortgage_services_hmda_record_id" INTEGER NOT NULL,
  "edit_code" VARCHAR(20) NOT NULL,
  "edit_type" mortgage_services.hmda_edit_type NOT NULL,
  "edit_description" TEXT NOT NULL,
  "status" mortgage_services.hmda_edit_status NOT NULL,
  "created_date" TIMESTAMPTZ NOT NULL,
  "resolved_date" TIMESTAMPTZ,
  "resolved_by_id" INTEGER,
  "resolution_notes" TEXT
);

CREATE TABLE "mortgage_services"."hmda_submissions" (
  "mortgage_services_submission_id" SERIAL PRIMARY KEY,
  "reporting_year" INTEGER NOT NULL,
  "reporting_period" mortgage_services.reporting_period NOT NULL,
  "institution_lei" VARCHAR(20) NOT NULL,
  "submission_date" TIMESTAMPTZ NOT NULL,
  "submission_status" mortgage_services.submission_status NOT NULL,
  "file_name" VARCHAR(255),
  "file_size" INTEGER,
  "record_count" INTEGER,
  "error_count" INTEGER,
  "warning_count" INTEGER,
  "submitted_by_id" INTEGER,
  "submission_notes" TEXT,
  "confirmation_number" VARCHAR(50),
  "completion_date" TIMESTAMPTZ
);

CREATE TABLE "consumer_lending"."loan_applications" (
  "consumer_lending_application_id" SERIAL PRIMARY KEY,
  "customer_id" INTEGER NOT NULL,
  "application_type" VARCHAR(50) NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "creation_date_time" TIMESTAMPTZ NOT NULL,
  "submission_date_time" TIMESTAMPTZ,
  "last_updated_date_time" TIMESTAMPTZ NOT NULL,
  "requested_amount" NUMERIC(18,2) NOT NULL,
  "requested_term_months" INTEGER NOT NULL,
  "loan_purpose" VARCHAR(100) NOT NULL,
  "estimated_credit_score" INTEGER,
  "application_channel" VARCHAR(50),
  "referral_source" VARCHAR(100),
  "decision_date_time" TIMESTAMPTZ,
  "decision_reason" VARCHAR(100),
  "officer_id" INTEGER,
  "branch_id" INTEGER
);

CREATE TABLE "consumer_lending"."application_applicants" (
  "consumer_lending_application_applicant_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "consumer_lending_applicant_id" INTEGER NOT NULL,
  "applicant_type" VARCHAR(20) NOT NULL,
  "relationship_to_primary" VARCHAR(50),
  "contribution_percentage" NUMERIC(5,2)
);

CREATE TABLE "consumer_lending"."applicants" (
  "consumer_lending_applicant_id" SERIAL PRIMARY KEY,
  "first_name" VARCHAR(100) NOT NULL,
  "middle_name" VARCHAR(100),
  "last_name" VARCHAR(100) NOT NULL,
  "date_of_birth" DATE NOT NULL,
  "ssn" VARCHAR(11) NOT NULL,
  "marital_status" enterprise.marital_status,
  "email" VARCHAR(255) NOT NULL,
  "phone" VARCHAR(30) NOT NULL,
  "mobile_phone" VARCHAR(30),
  "citizenship_status" enterprise.citizenship_status NOT NULL,
  "years_at_current_address" INTEGER,
  "housing_status" consumer_lending.housing_status NOT NULL,
  "monthly_housing_expense" NUMERIC(10,2),
  "current_address_id" INTEGER,
  "mailing_address_id" INTEGER,
  "previous_address_id" INTEGER
);

CREATE TABLE "consumer_lending"."applicant_employments" (
  "consumer_lending_employment_id" SERIAL PRIMARY KEY,
  "consumer_lending_applicant_id" INTEGER NOT NULL,
  "employer_name" VARCHAR(150) NOT NULL,
  "position" VARCHAR(100) NOT NULL,
  "enterprise_address_id" INTEGER,
  "phone" VARCHAR(20),
  "employment_type" VARCHAR(30) NOT NULL,
  "start_date" DATE NOT NULL,
  "end_date" DATE,
  "is_current" BOOLEAN NOT NULL,
  "years_in_profession" INTEGER,
  "monthly_income" NUMERIC(18,2) NOT NULL
);

CREATE TABLE "consumer_lending"."applicant_incomes" (
  "consumer_lending_income_id" SERIAL PRIMARY KEY,
  "consumer_lending_applicant_id" INTEGER NOT NULL,
  "income_type" consumer_lending.income_type NOT NULL,
  "amount" NUMERIC(18,2) NOT NULL,
  "frequency" VARCHAR(20) NOT NULL,
  "verification_status" VARCHAR(20) NOT NULL,
  "verification_date" DATE
);

CREATE TABLE "consumer_lending"."applicant_assets" (
  "consumer_lending_asset_id" SERIAL PRIMARY KEY,
  "consumer_lending_applicant_id" INTEGER NOT NULL,
  "asset_type" consumer_lending.asset_type NOT NULL,
  "institution_name" VARCHAR(100),
  "account_number" VARCHAR(50),
  "current_value" NUMERIC(18,2) NOT NULL,
  "verification_status" consumer_lending.verification_status NOT NULL,
  "verification_date" DATE,
  "property_address_id" INTEGER
);

CREATE TABLE "consumer_lending"."applicant_liabilities" (
  "consumer_lending_liability_id" SERIAL PRIMARY KEY,
  "consumer_lending_applicant_id" INTEGER NOT NULL,
  "liability_type" consumer_lending.liability_type NOT NULL,
  "creditor_name" VARCHAR(100) NOT NULL,
  "account_number" VARCHAR(50),
  "monthly_payment" NUMERIC(18,2) NOT NULL,
  "current_balance" NUMERIC(18,2) NOT NULL,
  "original_amount" NUMERIC(18,2),
  "interest_rate" NUMERIC(6,3),
  "origination_date" DATE,
  "maturity_date" DATE,
  "verification_status" consumer_lending.verification_status NOT NULL,
  "verification_date" DATE,
  "will_be_paid_off" BOOLEAN DEFAULT false
);

CREATE TABLE "consumer_lending"."loan_products" (
  "consumer_lending_loan_product_id" SERIAL PRIMARY KEY,
  "product_name" VARCHAR(100) NOT NULL,
  "product_code" VARCHAR(20) NOT NULL,
  "loan_type" consumer_lending.loan_type NOT NULL,
  "description" TEXT,
  "interest_rate_type" consumer_lending.interest_rate_type NOT NULL,
  "base_interest_rate" NUMERIC(6,3) NOT NULL,
  "min_term_months" INTEGER NOT NULL,
  "max_term_months" INTEGER NOT NULL,
  "min_loan_amount" NUMERIC(18,2),
  "max_loan_amount" NUMERIC(18,2),
  "min_credit_score" INTEGER,
  "origination_fee_type" consumer_lending.fee_type,
  "origination_fee_amount" NUMERIC(10,2),
  "late_fee_type" consumer_lending.fee_type,
  "late_fee_amount" NUMERIC(10,2),
  "is_active" BOOLEAN NOT NULL DEFAULT true,
  "required_collateral" BOOLEAN NOT NULL DEFAULT false,
  "early_repayment_penalty" BOOLEAN NOT NULL DEFAULT false,
  "disbursement_options" consumer_lending.disbursement_option
);

CREATE TABLE "consumer_lending"."product_eligibility_criteria" (
  "consumer_lending_criteria_id" SERIAL PRIMARY KEY,
  "consumer_lending_loan_product_id" INTEGER NOT NULL,
  "criteria_type" consumer_lending.eligibility_criteria_type NOT NULL,
  "min_value" VARCHAR(50),
  "max_value" VARCHAR(50),
  "required" BOOLEAN NOT NULL,
  "description" TEXT
);

CREATE TABLE "consumer_lending"."risk_based_pricing_tiers" (
  "consumer_lending_pricing_tier_id" SERIAL PRIMARY KEY,
  "consumer_lending_loan_product_id" INTEGER NOT NULL,
  "tier_name" VARCHAR(50) NOT NULL,
  "min_credit_score" INTEGER,
  "max_credit_score" INTEGER,
  "interest_rate_adjustment" NUMERIC(4,2) NOT NULL,
  "min_loan_amount" NUMERIC(18,2),
  "max_loan_amount" NUMERIC(18,2),
  "max_dti_ratio" NUMERIC(5,2),
  "is_active" BOOLEAN NOT NULL
);

CREATE TABLE "consumer_lending"."credit_reports" (
  "consumer_lending_credit_report_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "consumer_lending_applicant_id" INTEGER NOT NULL,
  "report_date" TIMESTAMPTZ NOT NULL,
  "expiration_date" DATE NOT NULL,
  "credit_score" INTEGER,
  "report_type" consumer_lending.credit_report_type NOT NULL,
  "bureau_name" consumer_lending.credit_bureau,
  "report_reference" VARCHAR(100),
  "report_path" VARCHAR(500),
  "status" consumer_lending.credit_report_status NOT NULL
);

CREATE TABLE "consumer_lending"."credit_report_tradelines" (
  "consumer_lending_tradeline_id" SERIAL PRIMARY KEY,
  "consumer_lending_credit_report_id" INTEGER NOT NULL,
  "account_type" consumer_lending.account_type NOT NULL,
  "creditor_name" VARCHAR(100) NOT NULL,
  "account_number" VARCHAR(50),
  "open_date" DATE,
  "current_balance" NUMERIC(18,2),
  "high_credit" NUMERIC(18,2),
  "credit_limit" NUMERIC(18,2),
  "monthly_payment" NUMERIC(18,2),
  "payment_status" consumer_lending.payment_status,
  "days_past_due" INTEGER,
  "worst_delinquency" consumer_lending.delinquency_severity,
  "worst_delinquency_date" DATE
);

CREATE TABLE "consumer_lending"."credit_inquiries" (
  "consumer_lending_inquiry_id" SERIAL PRIMARY KEY,
  "consumer_lending_credit_report_id" INTEGER NOT NULL,
  "inquiry_date" DATE NOT NULL,
  "creditor_name" VARCHAR(100) NOT NULL,
  "inquiry_type" consumer_lending.inquiry_type
);

CREATE TABLE "consumer_lending"."public_records" (
  "consumer_lending_record_id" SERIAL PRIMARY KEY,
  "consumer_lending_credit_report_id" INTEGER NOT NULL,
  "record_type" consumer_lending.public_record_type NOT NULL,
  "status" consumer_lending.public_record_status NOT NULL,
  "filing_date" DATE NOT NULL,
  "amount" NUMERIC(18,2),
  "reference_number" VARCHAR(100)
);

CREATE TABLE "consumer_lending"."decision_models" (
  "consumer_lending_model_id" SERIAL PRIMARY KEY,
  "model_name" VARCHAR(100) NOT NULL,
  "model_version" VARCHAR(20) NOT NULL,
  "model_type" consumer_lending.decision_model_type NOT NULL,
  "is_active" BOOLEAN NOT NULL,
  "effective_date" DATE NOT NULL,
  "expiration_date" DATE,
  "description" TEXT
);

CREATE TABLE "consumer_lending"."application_decisions" (
  "consumer_lending_decision_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "decision_type" consumer_lending.decision_type NOT NULL,
  "decision_result" consumer_lending.decision_result NOT NULL,
  "decision_date_time" TIMESTAMPTZ NOT NULL,
  "decision_by_id" INTEGER,
  "consumer_lending_model_id" INTEGER,
  "decision_score" NUMERIC(10,2),
  "consumer_lending_pricing_tier_id" INTEGER,
  "approved_amount" NUMERIC(18,2),
  "approved_term_months" INTEGER,
  "approved_interest_rate" NUMERIC(6,3),
  "approved_monthly_payment" NUMERIC(18,2),
  "conditional_approval" BOOLEAN,
  "expires_date" DATE,
  "notes" TEXT
);

CREATE TABLE "consumer_lending"."decision_reasons" (
  "consumer_lending_decision_reason_id" SERIAL PRIMARY KEY,
  "consumer_lending_decision_id" INTEGER NOT NULL,
  "reason_code" consumer_lending.decision_reason_code NOT NULL,
  "reason_description" VARCHAR(255) NOT NULL,
  "sequence" INTEGER NOT NULL
);

CREATE TABLE "consumer_lending"."adverse_action_notices" (
  "consumer_lending_notice_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "generated_date" TIMESTAMPTZ NOT NULL,
  "sent_date" TIMESTAMPTZ,
  "delivery_method" consumer_lending.delivery_method NOT NULL,
  "notice_path" VARCHAR(500),
  "status" consumer_lending.adverse_action_notice_status NOT NULL
);

CREATE TABLE "consumer_lending"."vehicles" (
  "vehicle_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "year" INTEGER NOT NULL,
  "make" VARCHAR(50) NOT NULL,
  "model" VARCHAR(50) NOT NULL,
  "trim" VARCHAR(50),
  "vin" VARCHAR(17),
  "vehicle_type" consumer_lending.vehicle_condition NOT NULL,
  "mileage" INTEGER,
  "purchase_price" NUMERIC(18,2) NOT NULL,
  "down_payment" NUMERIC(18,2),
  "trade_in_value" NUMERIC(18,2),
  "trade_in_balance_owed" NUMERIC(18,2),
  "dealer_name" VARCHAR(100),
  "dealer_address_id" INTEGER,
  "is_private_sale" BOOLEAN NOT NULL DEFAULT false,
  "valuation_source" consumer_lending.valuation_source,
  "valuation_amount" NUMERIC(18,2),
  "valuation_date" DATE
);

CREATE TABLE "consumer_lending"."loan_accounts" (
  "consumer_lending_loan_account_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "consumer_lending_loan_product_id" INTEGER NOT NULL,
  "account_number" VARCHAR(30) UNIQUE NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "origination_date" DATE NOT NULL,
  "funding_date" DATE NOT NULL,
  "maturity_date" DATE NOT NULL,
  "first_payment_date" DATE NOT NULL,
  "original_principal_balance" NUMERIC(18,2) NOT NULL,
  "current_principal_balance" NUMERIC(18,2) NOT NULL,
  "original_interest_rate" NUMERIC(6,3) NOT NULL,
  "current_interest_rate" NUMERIC(6,3) NOT NULL,
  "original_term_months" INTEGER NOT NULL,
  "remaining_term_months" INTEGER NOT NULL,
  "payment_amount" NUMERIC(18,2) NOT NULL,
  "payment_frequency" VARCHAR(20) NOT NULL,
  "next_payment_date" DATE NOT NULL,
  "next_payment_amount" NUMERIC(18,2) NOT NULL,
  "past_due_amount" NUMERIC(18,2) NOT NULL DEFAULT 0,
  "days_past_due" INTEGER NOT NULL DEFAULT 0,
  "total_fees_charged" NUMERIC(18,2) NOT NULL DEFAULT 0,
  "total_fees_paid" NUMERIC(18,2) NOT NULL DEFAULT 0,
  "accrued_interest" NUMERIC(18,2) NOT NULL DEFAULT 0,
  "interest_paid_ytd" NUMERIC(18,2) NOT NULL DEFAULT 0,
  "principal_paid_ytd" NUMERIC(18,2) NOT NULL DEFAULT 0,
  "interest_paid_total" NUMERIC(18,2) NOT NULL DEFAULT 0,
  "principal_paid_total" NUMERIC(18,2) NOT NULL DEFAULT 0,
  "late_count_30" INTEGER NOT NULL DEFAULT 0,
  "late_count_60" INTEGER NOT NULL DEFAULT 0,
  "late_count_90" INTEGER NOT NULL DEFAULT 0,
  "auto_pay_enabled" BOOLEAN NOT NULL DEFAULT false,
  "servicing_transferred_date" DATE
);

CREATE TABLE "consumer_lending"."payment_schedules" (
  "payment_schedule_id" SERIAL PRIMARY KEY,
  "consumer_lending_loan_account_id" INTEGER NOT NULL,
  "payment_number" INTEGER NOT NULL,
  "scheduled_date" DATE NOT NULL,
  "payment_amount" NUMERIC(18,2) NOT NULL,
  "principal_amount" NUMERIC(18,2) NOT NULL,
  "interest_amount" NUMERIC(18,2) NOT NULL,
  "beginning_balance" NUMERIC(18,2) NOT NULL,
  "ending_balance" NUMERIC(18,2) NOT NULL,
  "status" consumer_lending.payment_schedule_status NOT NULL,
  "actual_payment_date" DATE,
  "actual_payment_id" INTEGER
);

CREATE TABLE "consumer_lending"."disbursements" (
  "disbursement_id" SERIAL PRIMARY KEY,
  "consumer_lending_loan_account_id" INTEGER NOT NULL,
  "disbursement_date" DATE NOT NULL,
  "disbursement_amount" NUMERIC(18,2) NOT NULL,
  "disbursement_method" VARCHAR(50) NOT NULL,
  "disbursement_status" VARCHAR(20) NOT NULL,
  "recipient_name" VARCHAR(100) NOT NULL,
  "recipient_account_type" VARCHAR(20),
  "recipient_account_number" VARCHAR(50),
  "recipient_routing_number" VARCHAR(9),
  "check_number" VARCHAR(20),
  "tracking_number" VARCHAR(50),
  "notes" TEXT
);

CREATE TABLE "consumer_lending"."loan_payments" (
  "consumer_lending_payment_id" SERIAL PRIMARY KEY,
  "consumer_lending_loan_account_id" INTEGER NOT NULL,
  "payment_date" TIMESTAMPTZ NOT NULL,
  "payment_effective_date" DATE NOT NULL,
  "payment_type" consumer_lending.payment_type NOT NULL,
  "payment_method" consumer_lending.payment_method NOT NULL,
  "payment_amount" NUMERIC(18,2) NOT NULL,
  "principal_amount" NUMERIC(18,2) NOT NULL,
  "interest_amount" NUMERIC(18,2) NOT NULL,
  "late_fee_amount" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "other_fee_amount" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "transaction_id" VARCHAR(50),
  "confirmation_number" VARCHAR(50),
  "payment_status" consumer_lending.loan_payment_status NOT NULL,
  "returned_reason" VARCHAR(100),
  "returned_date" DATE
);

CREATE TABLE "consumer_lending"."loan_fees" (
  "consumer_lending_fee_id" SERIAL PRIMARY KEY,
  "consumer_lending_loan_account_id" INTEGER NOT NULL,
  "fee_type" consumer_lending.loan_fee_type NOT NULL,
  "fee_date" DATE NOT NULL,
  "fee_amount" NUMERIC(10,2) NOT NULL,
  "fee_status" consumer_lending.loan_fee_status NOT NULL,
  "waived_date" DATE,
  "waived_by_id" INTEGER,
  "waiver_reason" VARCHAR(255),
  "paid_date" DATE,
  "consumer_lending_payment_id" INTEGER
);

CREATE TABLE "consumer_lending"."loan_collateral" (
  "consumer_lending_collateral_id" SERIAL PRIMARY KEY,
  "loan_account_id" INTEGER NOT NULL,
  "collateral_type" consumer_lending.collateral_type NOT NULL,
  "description" VARCHAR(255) NOT NULL,
  "value" NUMERIC(18,2) NOT NULL,
  "valuation_date" DATE NOT NULL,
  "vehicle_id" INTEGER,
  "property_address_id" INTEGER,
  "deposit_account_id" INTEGER,
  "lien_position" INTEGER,
  "lien_recording_date" DATE,
  "lien_recording_number" VARCHAR(50),
  "insurance_required" BOOLEAN NOT NULL,
  "insurance_expiration_date" DATE
);

CREATE TABLE "consumer_lending"."loan_insurance" (
  "consumer_lending_insurance_id" SERIAL PRIMARY KEY,
  "consumer_lending_loan_account_id" INTEGER NOT NULL,
  "consumer_lending_collateral_id" INTEGER,
  "insurance_type" consumer_lending.insurance_type NOT NULL,
  "carrier_name" VARCHAR(100) NOT NULL,
  "policy_number" VARCHAR(50) NOT NULL,
  "coverage_amount" NUMERIC(18,2) NOT NULL,
  "premium_amount" NUMERIC(18,2) NOT NULL,
  "premium_frequency" consumer_lending.premium_frequency NOT NULL,
  "effective_date" DATE NOT NULL,
  "expiration_date" DATE NOT NULL,
  "beneficiary" VARCHAR(100),
  "status" consumer_lending.insurance_status NOT NULL
);

CREATE TABLE "consumer_lending"."loan_documents" (
  "consumer_lending_document_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER,
  "loan_account_id" INTEGER,
  "document_type" consumer_lending.document_type NOT NULL,
  "document_name" VARCHAR(255) NOT NULL,
  "document_path" VARCHAR(500) NOT NULL,
  "upload_date" TIMESTAMPTZ NOT NULL,
  "status" consumer_lending.document_status NOT NULL,
  "review_date" TIMESTAMPTZ,
  "reviewer_id" INTEGER,
  "expiration_date" DATE,
  "notes" TEXT
);

CREATE TABLE "consumer_lending"."loan_communications" (
  "consumer_lending_communication_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER,
  "loan_account_id" INTEGER,
  "communication_date" TIMESTAMPTZ NOT NULL,
  "communication_type" consumer_lending.communication_type NOT NULL,
  "direction" consumer_lending.communication_direction NOT NULL,
  "subject" VARCHAR(255),
  "content" TEXT,
  "sender" VARCHAR(100),
  "recipient" VARCHAR(100),
  "template_id" VARCHAR(50),
  "status" consumer_lending.communication_status NOT NULL,
  "document_path" VARCHAR(500),
  "related_to" consumer_lending.communication_context
);

CREATE TABLE "consumer_lending"."loan_statements" (
  "consumer_lending_statement_id" SERIAL PRIMARY KEY,
  "loan_account_id" INTEGER NOT NULL,
  "statement_date" DATE NOT NULL,
  "statement_period_start" DATE NOT NULL,
  "statement_period_end" DATE NOT NULL,
  "opening_balance" NUMERIC(18,2) NOT NULL,
  "closing_balance" NUMERIC(18,2) NOT NULL,
  "total_payments" NUMERIC(18,2) NOT NULL,
  "principal_paid" NUMERIC(18,2) NOT NULL,
  "interest_paid" NUMERIC(18,2) NOT NULL,
  "fees_charged" NUMERIC(18,2) NOT NULL,
  "fees_paid" NUMERIC(18,2) NOT NULL,
  "amount_due" NUMERIC(18,2) NOT NULL,
  "due_date" DATE NOT NULL,
  "document_path" VARCHAR(500),
  "sent_date" DATE,
  "delivery_method" consumer_lending.statement_delivery_method
);

CREATE TABLE "consumer_lending"."collection_accounts" (
  "consumer_lending_collection_id" SERIAL PRIMARY KEY,
  "loan_account_id" INTEGER NOT NULL,
  "assigned_date" DATE NOT NULL,
  "status" consumer_lending.collection_status NOT NULL,
  "delinquency_reason" VARCHAR(100),
  "delinquency_date" DATE NOT NULL,
  "days_delinquent" INTEGER NOT NULL,
  "amount_past_due" NUMERIC(18,2) NOT NULL,
  "assigned_to" VARCHAR(50),
  "priority" consumer_lending.collection_priority,
  "next_action_date" DATE,
  "last_action_date" DATE,
  "resolution_date" DATE,
  "resolution_type" consumer_lending.collection_resolution_type
);

CREATE TABLE "consumer_lending"."collection_actions" (
  "consumer_lending_action_id" SERIAL PRIMARY KEY,
  "consumer_lending_collection_id" INTEGER NOT NULL,
  "action_date" TIMESTAMPTZ NOT NULL,
  "action_type" consumer_lending.collection_action_type NOT NULL,
  "action_result" consumer_lending.collection_action_result,
  "action_by_id" INTEGER NOT NULL,
  "notes" TEXT,
  "next_action_type" consumer_lending.next_collection_action_type,
  "next_action_date" DATE,
  "promise_to_pay_amount" NUMERIC(18,2),
  "promise_to_pay_date" DATE
);

CREATE TABLE "consumer_lending"."payment_arrangements" (
  "consumer_lending_arrangement_id" SERIAL PRIMARY KEY,
  "consumer_lending_collection_id" INTEGER NOT NULL,
  "arrangement_date" DATE NOT NULL,
  "status" consumer_lending.payment_arrangement_status NOT NULL,
  "total_amount" NUMERIC(18,2) NOT NULL,
  "number_of_payments" INTEGER NOT NULL,
  "first_payment_date" DATE NOT NULL,
  "payment_frequency" consumer_lending.payment_frequency NOT NULL,
  "payment_amount" NUMERIC(18,2) NOT NULL,
  "approved_by_id" INTEGER,
  "notes" TEXT
);

CREATE TABLE "consumer_lending"."loan_modifications" (
  "consumer_lending_modification_id" SERIAL PRIMARY KEY,
  "loan_account_id" INTEGER NOT NULL,
  "modification_type" consumer_lending.loan_modification_type NOT NULL,
  "request_date" DATE NOT NULL,
  "approval_date" DATE,
  "effective_date" DATE,
  "original_rate" NUMERIC(6,3),
  "new_rate" NUMERIC(6,3),
  "original_term_months" INTEGER,
  "new_term_months" INTEGER,
  "original_principal_balance" NUMERIC(18,2),
  "new_principal_balance" NUMERIC(18,2),
  "capitalized_amount" NUMERIC(18,2),
  "status" consumer_lending.loan_modification_status NOT NULL,
  "hardship_reason" VARCHAR(100),
  "approved_by_id" INTEGER,
  "document_path" VARCHAR(500)
);

CREATE TABLE "consumer_lending"."reg_z_disclosures" (
  "consumer_lending_disclosure_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "loan_account_id" INTEGER,
  "disclosure_type" consumer_lending.disclosure_type NOT NULL,
  "disclosure_date" TIMESTAMPTZ NOT NULL,
  "sent_date" TIMESTAMPTZ,
  "delivery_method" consumer_lending.disclosure_delivery_method NOT NULL,
  "annual_percentage_rate" NUMERIC(6,3) NOT NULL,
  "finance_charge" NUMERIC(18,2) NOT NULL,
  "amount_financed" NUMERIC(18,2) NOT NULL,
  "total_of_payments" NUMERIC(18,2) NOT NULL,
  "payment_schedule" TEXT,
  "security_interest" TEXT,
  "late_payment_fee" NUMERIC(10,2),
  "prepayment_penalty" TEXT,
  "document_path" VARCHAR(500),
  "received_by_customer" BOOLEAN,
  "receipt_date" TIMESTAMPTZ,
  "user_id" INTEGER,
  "version" INTEGER NOT NULL
);

CREATE TABLE "consumer_lending"."adverse_action_details" (
  "consumer_lending_adverse_action_id" SERIAL PRIMARY KEY,
  "consumer_lending_notice_id" INTEGER NOT NULL,
  "ecoa_reason_code" consumer_lending.ecoa_reason_code NOT NULL,
  "fcra_reason_code" consumer_lending.fcra_reason_code,
  "reason_description" VARCHAR(255) NOT NULL,
  "credit_score_disclosed" INTEGER,
  "credit_score_range_min" INTEGER,
  "credit_score_range_max" INTEGER,
  "credit_score_factors" TEXT,
  "credit_bureau_name" consumer_lending.credit_bureau,
  "generated_date" TIMESTAMPTZ NOT NULL,
  "user_id" INTEGER,
  "sequence" INTEGER NOT NULL
);

CREATE TABLE "consumer_lending"."ecoa_monitoring" (
  "consumer_lending_monitoring_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "consumer_lending_applicant_id" INTEGER NOT NULL,
  "ethnicity" VARCHAR(50),
  "race" VARCHAR(50),
  "sex" VARCHAR(10),
  "age" INTEGER,
  "marital_status" enterprise.marital_status,
  "information_method" consumer_lending.information_method NOT NULL,
  "income_monitored" NUMERIC(18,2),
  "action_taken" consumer_lending.action_taken NOT NULL,
  "action_date" DATE NOT NULL,
  "submission_date" DATE NOT NULL,
  "submitted_by_id" INTEGER
);

CREATE TABLE "consumer_lending"."fairlending_analysis" (
  "consumer_lending_analysis_id" SERIAL PRIMARY KEY,
  "analysis_date" DATE NOT NULL,
  "analysis_type" consumer_lending.analysis_type NOT NULL,
  "consumer_lending_loan_product_id" INTEGER NOT NULL,
  "time_period_start" DATE NOT NULL,
  "time_period_end" DATE NOT NULL,
  "protected_class" consumer_lending.protected_class NOT NULL,
  "control_group" VARCHAR(50) NOT NULL,
  "test_group" VARCHAR(50) NOT NULL,
  "sample_size_control" INTEGER NOT NULL,
  "sample_size_test" INTEGER NOT NULL,
  "outcome_variable" consumer_lending.outcome_variable NOT NULL,
  "statistical_test" consumer_lending.statistical_test,
  "disparity_ratio" NUMERIC(8,3),
  "p_value" NUMERIC(8,6),
  "statistically_significant" BOOLEAN,
  "controls_applied" TEXT,
  "findings" TEXT,
  "analyst" INTEGER,
  "reviewer" INTEGER,
  "action_recommended" TEXT,
  "report_path" VARCHAR(500)
);

CREATE TABLE "consumer_lending"."reg_b_notices" (
  "consumer_lending_notice_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "notice_type" consumer_lending.reg_b_notice_type NOT NULL,
  "generated_date" TIMESTAMPTZ NOT NULL,
  "sent_date" TIMESTAMPTZ NOT NULL,
  "delivery_method" consumer_lending.delivery_method NOT NULL,
  "incomplete_items" TEXT,
  "deadline_date" DATE,
  "counteroffer_terms" TEXT,
  "appraisal_notice_included" BOOLEAN NOT NULL DEFAULT false,
  "document_path" VARCHAR(500),
  "user_id" INTEGER
);

CREATE TABLE "consumer_lending"."appraisal_disclosures" (
  "consumer_lending_disclosure_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "property_address_id" INTEGER NOT NULL,
  "disclosure_type" VARCHAR(50) NOT NULL,
  "disclosure_date" TIMESTAMPTZ NOT NULL,
  "sent_date" TIMESTAMPTZ NOT NULL,
  "delivery_method" VARCHAR(30) NOT NULL,
  "appraisal_type" VARCHAR(50),
  "appraisal_ordered_date" DATE,
  "appraisal_received_date" DATE,
  "appraisal_provided_date" DATE,
  "appraisal_value" NUMERIC(18,2),
  "document_path" VARCHAR(500),
  "appraisal_waiver" BOOLEAN NOT NULL DEFAULT false,
  "waiver_reason" VARCHAR(100),
  "user_id" INTEGER
);

CREATE TABLE "consumer_lending"."military_lending_checks" (
  "consumer_lending_check_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "consumer_lending_applicant_id" INTEGER NOT NULL,
  "check_date" TIMESTAMPTZ NOT NULL,
  "covered_borrower" BOOLEAN NOT NULL,
  "verification_method" VARCHAR(50) NOT NULL,
  "military_status" VARCHAR(30),
  "certificate_date" DATE,
  "document_path" VARCHAR(500),
  "mapr_calculated" NUMERIC(6,3),
  "mapr_disclosure_provided" BOOLEAN,
  "user_id" INTEGER
);

CREATE TABLE "consumer_lending"."high_cost_mortgage_tests" (
  "consumer_lending_test_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER NOT NULL,
  "test_date" DATE NOT NULL,
  "test_type" VARCHAR(30) NOT NULL,
  "loan_amount" NUMERIC(18,2) NOT NULL,
  "apr" NUMERIC(6,3) NOT NULL,
  "points_and_fees" NUMERIC(18,2) NOT NULL,
  "points_and_fees_percentage" NUMERIC(6,3) NOT NULL,
  "points_and_fees_threshold" NUMERIC(18,2) NOT NULL,
  "apr_threshold" NUMERIC(6,3) NOT NULL,
  "apor" NUMERIC(6,3),
  "apor_date" DATE,
  "high_cost_mortgage" BOOLEAN NOT NULL,
  "additional_disclosures_required" BOOLEAN NOT NULL,
  "user_id" INTEGER,
  "notes" TEXT
);

CREATE TABLE "consumer_lending"."compliance_exceptions" (
  "consumer_lending_exception_id" SERIAL PRIMARY KEY,
  "consumer_lending_application_id" INTEGER,
  "loan_account_id" INTEGER,
  "exception_date" TIMESTAMPTZ NOT NULL,
  "exception_type" VARCHAR(50) NOT NULL,
  "regulation" VARCHAR(50) NOT NULL,
  "severity" VARCHAR(20) NOT NULL,
  "description" TEXT NOT NULL,
  "identified_by_id" INTEGER NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "remediation_plan" TEXT,
  "remediation_date" DATE,
  "remediated_by_id" INTEGER,
  "root_cause" TEXT,
  "preventive_action" TEXT,
  "notes" TEXT
);

CREATE TABLE "security"."identity_roles" (
  "security_identity_role_id" UUID PRIMARY KEY NOT NULL,
  "security_identity_id" UUID NOT NULL,
  "security_role_id" UUID NOT NULL,
  "start_date" TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP),
  "end_date" TIMESTAMPTZ,
  "assigned_by_id" INTEGER,
  "active" BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE "security"."roles" (
  "security_role_id" UUID PRIMARY KEY,
  "role_name" VARCHAR(255) NOT NULL,
  "display_name" VARCHAR(255),
  "description" TEXT,
  "status" security.role_status NOT NULL DEFAULT 'ACTIVE',
  "managing_application_id" UUID,
  "owner_id" INTEGER,
  "created_at" TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP),
  "created_by_id" INTEGER
);

CREATE TABLE "security"."security_account_roles" (
  "security_account_role_id" UUID PRIMARY KEY,
  "security_account_id" UUID NOT NULL,
  "security_role_id" UUID NOT NULL,
  "assigned_at" TIMESTAMPTZ,
  "assigned_by_id" INTEGER,
  "active" BOOLEAN DEFAULT true
);

CREATE TABLE "security"."security_account_enterprise_accounts" (
  "security_account_enterprise_account_id" UUID PRIMARY KEY,
  "security_account_id" UUID NOT NULL,
  "enterprise_account_id" INTEGER NOT NULL,
  "access_level" security.permission_type DEFAULT 'READ',
  "assigned_at" TIMESTAMPTZ,
  "assigned_by_id" INTEGER,
  "active" BOOLEAN DEFAULT true
);

CREATE TABLE "security"."role_entitlements" (
  "security_role_entitlement_id" UUID PRIMARY KEY NOT NULL,
  "security_role_id" UUID NOT NULL,
  "security_entitlement_id" UUID NOT NULL,
  "created_at" TIMESTAMPTZ NOT NULL,
  "created_by_id" INTEGER,
  "updated_by_id" INTEGER,
  "started_at" TIMESTAMPTZ NOT NULL,
  "ended_at" TIMESTAMPTZ,
  "active" BOOL
);

CREATE TABLE "security"."enhanced_entitlements" (
  "security_entitlement_id" UUID PRIMARY KEY,
  "entitlement_name" VARCHAR(255) NOT NULL,
  "display_name" VARCHAR(255),
  "description" TEXT,
  "status" security.entitlement_status NOT NULL DEFAULT 'ACTIVE',
  "managing_application_id" UUID,
  "created_at" TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP),
  "created_by_id" INTEGER
);

CREATE TABLE "security"."entitlement_resources" (
  "security_entitlement_resource_id" UUID PRIMARY KEY,
  "security_entitlement_id" UUID NOT NULL,
  "security_resource_id" UUID NOT NULL,
  "permission_type" security.permission_type NOT NULL,
  "context_conditions" VARCHAR(1000),
  "resource_details" VARCHAR(1000),
  "created_at" TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP),
  "created_by_id" INTEGER
);

CREATE TABLE "security"."resource_definitions" (
  "security_resource_id" UUID PRIMARY KEY,
  "resource_name" VARCHAR(255) NOT NULL,
  "resource_type" security.resource_type NOT NULL,
  "resource_identifier" VARCHAR(500) NOT NULL,
  "application_id" UUID,
  "host_id" UUID,
  "network_device_id" INET,
  "description" TEXT,
  "created_at" TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP),
  "created_by_id" INTEGER
);

CREATE TABLE "security"."devices" (
  "security_device_id" INET PRIMARY KEY NOT NULL,
  "device_type" VARCHAR(50) NOT NULL,
  "subnet" VARCHAR(50),
  "hostname" VARCHAR(100),
  "created_at" TIMESTAMP(6) DEFAULT (CURRENT_TIMESTAMP),
  "updated_at" TIMESTAMP(6) DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "security"."network_events" (
  "security_network_event_id" BIGSERIAL PRIMARY KEY NOT NULL,
  "timestamp" TIMESTAMP(6) NOT NULL,
  "source_ip" INET NOT NULL,
  "source_port" INTEGER NOT NULL,
  "dest_ip" INET NOT NULL,
  "dest_port" INTEGER NOT NULL,
  "protocol" security.network_protocols NOT NULL,
  "status" VARCHAR(50) NOT NULL,
  "tcp_flag" security.tcp_flag_type,
  "sequence" BIGINT,
  "ack" BIGINT,
  "window_size" INTEGER,
  "length" INTEGER NOT NULL DEFAULT 0,
  "bytes_sent" INTEGER NOT NULL DEFAULT 0,
  "bytes_received" INTEGER NOT NULL DEFAULT 0,
  "security_device_id" INET NOT NULL,
  "log_message" TEXT,
  "created_at" TIMESTAMP(6)
);

CREATE TABLE "security"."policies" (
  "security_policy_id" UUID PRIMARY KEY NOT NULL,
  "name" VARCHAR(200) UNIQUE NOT NULL,
  "description" TEXT NOT NULL,
  "created_by_id" INTEGER,
  "updated_by_id" INTEGER,
  "created_at" TIMESTAMP(6) DEFAULT (CURRENT_TIMESTAMP),
  "updated_at" TIMESTAMP(6) DEFAULT (CURRENT_TIMESTAMP),
  "started_at" TIMESTAMP(6) NOT NULL,
  "ended_at" TIMESTAMP(6),
  "active" BOOLEAN DEFAULT true
);

CREATE TABLE "security"."policy_attributes" (
  "security_policy_id" UUID NOT NULL,
  "attribute_name" VARCHAR(200) NOT NULL,
  "attribute_value" VARCHAR(200)
);

CREATE TABLE "security"."policy_rules" (
  "security_policy_rule_id" UUID PRIMARY KEY NOT NULL,
  "security_policy_id" UUID,
  "rule_name" VARCHAR(200) NOT NULL,
  "rule_description" TEXT NOT NULL
);

CREATE TABLE "security"."accounts" (
  "security_account_id" UUID PRIMARY KEY NOT NULL,
  "security_identity_id" UUID,
  "name" VARCHAR(200),
  "account_id_string" VARCHAR(200),
  "security_source_id" UUID,
  "disabled" BOOLEAN,
  "locked" BOOLEAN,
  "privileged" BOOLEAN,
  "manually_correlated" BOOLEAN,
  "password_last_set" TIMESTAMP(6),
  "created" TIMESTAMP(6),
  "status_update_date_time" TIMESTAMP(6)
);

CREATE TABLE "security"."governance_groups" (
  "security_governance_group_id" UUID PRIMARY KEY NOT NULL,
  "name" VARCHAR(200),
  "owner_id" integer
);

CREATE TABLE "security"."iam_logins" (
  "security_login_id" UUID PRIMARY KEY NOT NULL,
  "security_account_id" UUID NOT NULL,
  "user_name" VARCHAR(200),
  "login_time" TIMESTAMP(6) NOT NULL,
  "logout_time" TIMESTAMP(6),
  "login_method" VARCHAR(200) NOT NULL
);

CREATE TABLE "security"."identities" (
  "security_identity_id" UUID PRIMARY KEY NOT NULL,
  "name" VARCHAR(200),
  "display_name" VARCHAR(200),
  "owner_id" INTEGER,
  "service_account" BOOL DEFAULT false,
  "environment" security.environment,
  "created" TIMESTAMP(6),
  "inactive" BOOLEAN,
  "status" VARCHAR(200),
  "security_identity_profile_id" UUID,
  "modified" TIMESTAMP(6),
  "synced" TIMESTAMP(6),
  "is_fallback_approver" BOOLEAN
);

CREATE TABLE "security"."identity_profiles" (
  "security_identity_profile_id" UUID PRIMARY KEY NOT NULL,
  "name" VARCHAR(200),
  "description" TEXT,
  "access_review_frequency_days" INTEGER,
  "max_inactive_days" INTEGER,
  "requires_mfa" BOOLEAN DEFAULT false,
  "password_expiry_days" INTEGER,
  "default_session_timeout_minutes" INTEGER,
  "risk_level" security.risk_level NOT NULL DEFAULT 'MEDIUM',
  "created_at" TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP),
  "updated_at" TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "security"."file_accesses" (
  "security_file_access_id" UUID PRIMARY KEY NOT NULL,
  "security_system_id" UUID NOT NULL,
  "security_file_id" UUID NOT NULL,
  "access_type" VARCHAR(10),
  "access_time" TIMESTAMP(6),
  "security_process_execution_id" UUID NOT NULL
);

CREATE TABLE "security"."file_threats" (
  "security_file_threat_hash" VARCHAR(64) PRIMARY KEY NOT NULL,
  "threat_level" security.threat_level_type NOT NULL DEFAULT 'UNKNOWN',
  "threat_description" TEXT
);

CREATE TABLE "security"."files" (
  "security_file_id" UUID PRIMARY KEY NOT NULL,
  "security_host_id" UUID NOT NULL,
  "file_path" TEXT,
  "file_hash" VARCHAR(64),
  "file_size" BIGINT,
  "last_modified" TIMESTAMP(6)
);

CREATE TABLE "security"."installed_applications" (
  "security_host_id" UUID NOT NULL,
  "app_mgmt_application_id" UUID NOT NULL,
  "application_version" VARCHAR(50),
  "installation_date" TIMESTAMP(6),
  PRIMARY KEY ("security_host_id", "app_mgmt_application_id")
);

CREATE TABLE "security"."network_connections" (
  "security_network_connection_id" UUID PRIMARY KEY NOT NULL,
  "security_host_id" UUID NOT NULL,
  "security_process_execution_id" UUID NOT NULL,
  "connection_type" VARCHAR(10),
  "protocol" security.network_protocols,
  "local_ip" INET,
  "local_port" INTEGER,
  "remote_ip" INET,
  "remote_port" INTEGER,
  "start_time" TIMESTAMP(6),
  "end_time" TIMESTAMP(6)
);

CREATE TABLE "security"."open_ports" (
  "security_host_id" UUID NOT NULL,
  "port_number" INTEGER NOT NULL,
  "protocol" security.network_protocols NOT NULL,
  PRIMARY KEY ("security_host_id", "port_number", "protocol")
);

CREATE TABLE "security"."process_executions" (
  "security_process_execution_id" UUID PRIMARY KEY NOT NULL,
  "security_host_id" UUID NOT NULL,
  "process_name" VARCHAR(255),
  "process_id" INTEGER,
  "parent_process_id" INTEGER,
  "start_time" TIMESTAMP(6),
  "end_time" TIMESTAMP(6),
  "command_line" TEXT,
  "user_name" VARCHAR(50)
);

CREATE TABLE "security"."running_services" (
  "security_host_id" UUID NOT NULL,
  "running_service_name" VARCHAR(100) NOT NULL,
  "start_time" TIMESTAMP(6),
  "status" VARCHAR(20),
  PRIMARY KEY ("security_host_id", "running_service_name")
);

CREATE TABLE "security"."system_stats" (
  "security_system_stat_id" UUID PRIMARY KEY NOT NULL,
  "security_host_id" UUID NOT NULL,
  "cpu_usage_percent" INTEGER,
  "memory_usage_gb" NUMERIC(5,1),
  "memory_total_gb" INTEGER,
  "disk_free_gb" INTEGER,
  "disk_total_gb" INTEGER,
  "timestamp" TIMESTAMP(6)
);

CREATE TABLE "security"."hosts" (
  "security_host_id" UUID PRIMARY KEY NOT NULL,
  "hostname" VARCHAR(255),
  "agent_identifier" VARCHAR(36),
  "ip_address_internal" INET,
  "ip_address_external" INET,
  "mac_address" VARCHAR(17),
  "system_type" security.system_type,
  "os" VARCHAR(50),
  "os_version" VARCHAR(100),
  "last_seen" TIMESTAMP(6),
  "agent_version" VARCHAR(50),
  "agent_status" security.agent_status,
  "patch_status" security.patch_status,
  "last_patched" TIMESTAMP(6),
  "compliance" security.compliance_status,
  "checked_out_date" DATE,
  "asset_owner_name" VARCHAR(50),
  "asset_owner_email" VARCHAR(50),
  "patch_level" VARCHAR(50),
  "patch_update_available" BOOLEAN
);

CREATE TABLE "security"."usb_device_usage" (
  "security_usb_device_usage_id" UUID PRIMARY KEY NOT NULL,
  "security_system_id" UUID NOT NULL,
  "device_name" VARCHAR(100),
  "device_type" VARCHAR(50),
  "connection_time" TIMESTAMP(6),
  "disconnection_time" TIMESTAMP(6)
);

CREATE TABLE "security"."cvss" (
  "cve" VARCHAR(20) PRIMARY KEY,
  "attack_complexity_3" VARCHAR(5),
  "attack_vector_3" VARCHAR(20),
  "availability_impact_3" VARCHAR(5),
  "confidentiality_impact_3" VARCHAR(5),
  "integrity_impact_3" VARCHAR(5),
  "privileges_required_3" VARCHAR(5),
  "scope_3" VARCHAR(10),
  "user_interaction_3" VARCHAR(10),
  "vector_string_3" VARCHAR(50),
  "exploitability_score_3" REAL,
  "impact_score_3" REAL,
  "base_score_3" REAL,
  "base_severity_3" VARCHAR(10),
  "access_complexity" VARCHAR(10),
  "access_vector" VARCHAR(20),
  "authentication" VARCHAR(10),
  "availability_impact" VARCHAR(10),
  "confidentiality_impact" VARCHAR(10),
  "integrity_impact" VARCHAR(10),
  "obtain_all_privileges" BOOLEAN,
  "obtain_other_privileges" BOOLEAN,
  "obtain_user_privileges" BOOLEAN,
  "user_interaction_required" BOOLEAN,
  "vector_string" VARCHAR(50),
  "exploitability_score" REAL,
  "impact_score" REAL,
  "base_score" REAL,
  "severity" VARCHAR(10),
  "description" TEXT,
  "published_date" DATE,
  "last_modified_date" DATE
);

CREATE TABLE "security"."cpe" (
  "cve" VARCHAR(20),
  "cpe23uri" TEXT,
  "vulnerable" VARCHAR(5)
);

CREATE TABLE "security"."cve_problem" (
  "cve" VARCHAR(20),
  "problem" TEXT,
  "cwe_id" INTEGER
);

CREATE TABLE "security"."cwe" (
  "cwe_id" INTEGER PRIMARY KEY,
  "name" TEXT,
  "description" TEXT,
  "extended_description" TEXT,
  "modes_of_introduction" TEXT,
  "common_consequences" TEXT,
  "potential_mitigations" TEXT
);

CREATE TABLE "app_mgmt"."architectures" (
  "app_mgmt_architecture_id" UUID PRIMARY KEY,
  "architecture_name" VARCHAR(255),
  "description" TEXT,
  "approval_date" TIMESTAMPTZ,
  "approved_by_id" INTEGER,
  "documentation_url" VARCHAR(2048),
  "status" VARCHAR(50),
  "sdlc_process_id" UUID,
  "created_by_user_id" INTEGER,
  "modified_by_user_id" INTEGER
);

CREATE TABLE "app_mgmt"."sdlc_processes" (
  "app_mgmt_sdlc_process_id" UUID PRIMARY KEY,
  "process_name" VARCHAR(255),
  "description" TEXT,
  "process_owner" INTEGER,
  "version" VARCHAR(50),
  "documentation_url" VARCHAR(2048),
  "app_mgmt_team_id" UUID
);

CREATE TABLE "app_mgmt"."applications" (
  "app_mgmt_application_id" UUID PRIMARY KEY,
  "enterprise_department_id" INTEGER,
  "application_name" VARCHAR(255),
  "description" TEXT,
  "application_type" app_mgmt.application_types,
  "vendor" VARCHAR(255),
  "version" VARCHAR(50),
  "deployment_environment" app_mgmt.deployment_environments,
  "operated_by_team_id" UUID,
  "maintained_by_team_id" UUID,
  "created_by_team_id" UUID,
  "application_owner_id" INTEGER,
  "lifecycle_status" app_mgmt.application_lifecycle_status,
  "date_deployed" TIMESTAMPTZ,
  "date_retired" TIMESTAMPTZ,
  "architecture_id" UUID,
  "sdlc_process_id" UUID,
  "source_code_repository" VARCHAR(2048),
  "documentation_url" VARCHAR(2048),
  "created_by_user_id" INTEGER,
  "modified_by_user_id" INTEGER,
  "rto" INTERVAL,
  "rpo" INTERVAL
);

CREATE TABLE "app_mgmt"."components" (
  "app_mgmt_component_id" UUID PRIMARY KEY,
  "component_name" VARCHAR(255),
  "component_version" VARCHAR(50),
  "component_type" app_mgmt.component_types,
  "vendor" VARCHAR(255),
  "app_mgmt_license_id" UUID,
  "description" TEXT,
  "created_by_user_id" INTEGER,
  "modified_by_user_id" INTEGER,
  "package_info" TEXT,
  "repository_url" VARCHAR(2048),
  "namespace_or_module" VARCHAR(255)
);

CREATE TABLE "app_mgmt"."component_dependencies" (
  "parent_component_id" UUID,
  "child_component_id" UUID,
  "quantity" INTEGER,
  "dependency_type" app_mgmt.dependency_types,
  PRIMARY KEY ("parent_component_id", "child_component_id")
);

CREATE TABLE "app_mgmt"."application_components" (
  "app_mgmt_application_id" UUID,
  "app_mgmt_component_id" UUID,
  "dependency_type" app_mgmt.dependency_types,
  PRIMARY KEY ("app_mgmt_application_id", "app_mgmt_component_id", "dependency_type")
);

CREATE TABLE "app_mgmt"."application_relationships" (
  "app_mgmt_application_relationship_id" SERIAL PRIMARY KEY,
  "application_id_1" UUID,
  "application_id_2" UUID,
  "relationship_type" app_mgmt.relationship_types,
  "description" TEXT,
  "criticality" app_mgmt.criticality_levels
);

CREATE TABLE "app_mgmt"."licenses" (
  "app_mgmt_license_id" UUID PRIMARY KEY,
  "license_name" VARCHAR(255),
  "license_type" app_mgmt.license_types,
  "license_text" TEXT
);

CREATE TABLE "app_mgmt"."application_licenses" (
  "app_mgmt_application_id" UUID,
  "app_mgmt_license_id" UUID,
  PRIMARY KEY ("app_mgmt_application_id", "app_mgmt_license_id")
);

CREATE TABLE "app_mgmt"."teams" (
  "app_mgmt_team_id" UUID PRIMARY KEY,
  "team_name" VARCHAR(255),
  "description" TEXT,
  "team_lead_id" INTEGER
);

CREATE TABLE "app_mgmt"."team_members" (
  "app_mgmt_team_id" UUID,
  "enterprise_associate_id" INTEGER,
  "function" VARCHAR(255),
  PRIMARY KEY ("app_mgmt_team_id", "enterprise_associate_id")
);

CREATE TABLE "credit_cards"."card_products" (
  "credit_cards_product_id" SERIAL PRIMARY KEY,
  "product_name" VARCHAR(100) NOT NULL,
  "product_code" VARCHAR(20) NOT NULL,
  "card_network" VARCHAR(20) NOT NULL,
  "card_type" VARCHAR(20) NOT NULL,
  "card_tier" VARCHAR(20) NOT NULL,
  "is_secured" BOOLEAN NOT NULL DEFAULT false,
  "annual_fee" NUMERIC(10,2),
  "is_annual_fee_waived_first_year" BOOLEAN DEFAULT false,
  "base_interest_rate" NUMERIC(6,3),
  "cash_advance_rate" NUMERIC(6,3),
  "penalty_rate" NUMERIC(6,3),
  "balance_transfer_rate" NUMERIC(6,3),
  "intro_rate" NUMERIC(6,3),
  "intro_rate_period_months" INTEGER,
  "grace_period_days" INTEGER,
  "min_credit_score" INTEGER,
  "min_credit_limit" NUMERIC(10,2),
  "max_credit_limit" NUMERIC(10,2),
  "reward_program" VARCHAR(100),
  "base_reward_rate" NUMERIC(5,2),
  "foreign_transaction_fee" NUMERIC(5,2),
  "late_payment_fee" NUMERIC(10,2),
  "overlimit_fee" NUMERIC(10,2),
  "cash_advance_fee_percent" NUMERIC(5,2),
  "cash_advance_fee_min" NUMERIC(10,2),
  "balance_transfer_fee_percent" NUMERIC(5,2),
  "balance_transfer_fee_min" NUMERIC(10,2),
  "return_payment_fee" NUMERIC(10,2),
  "is_active" BOOLEAN NOT NULL DEFAULT true,
  "launch_date" DATE,
  "discontinue_date" DATE,
  "terms_and_conditions_url" VARCHAR(255),
  "image_url" VARCHAR(255)
);

CREATE TABLE "credit_cards"."fraud_cases" (
  "credit_cards_case_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "credit_cards_card_id" INTEGER,
  "report_date" TIMESTAMPTZ NOT NULL,
  "case_type" VARCHAR(30) NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "reported_by" VARCHAR(20) NOT NULL,
  "description" TEXT,
  "total_disputed_amount" NUMERIC(10,2),
  "provisional_credit_issued" BOOLEAN,
  "resolution" VARCHAR(30),
  "resolution_date" DATE,
  "new_card_issued" BOOLEAN NOT NULL DEFAULT false,
  "police_report_filed" BOOLEAN NOT NULL DEFAULT false,
  "investigator_id" INTEGER
);

CREATE TABLE "credit_cards"."fraud_transactions" (
  "credit_cards_fraud_transaction_id" SERIAL PRIMARY KEY,
  "credit_cards_case_id" INTEGER NOT NULL,
  "credit_cards_transaction_id" INTEGER NOT NULL,
  "is_confirmed_fraud" BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE "credit_cards"."security_blocks" (
  "credit_cards_block_id" SERIAL PRIMARY KEY,
  "credit_cards_card_id" INTEGER NOT NULL,
  "block_type" VARCHAR(30) NOT NULL,
  "reason" VARCHAR(100) NOT NULL,
  "start_date" TIMESTAMPTZ NOT NULL,
  "end_date" TIMESTAMPTZ,
  "geographic_restriction" VARCHAR(100),
  "transaction_type_restricted" VARCHAR(30),
  "requested_by" VARCHAR(20) NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "removed_by_id" INTEGER,
  "removed_date" TIMESTAMPTZ
);

CREATE TABLE "credit_cards"."credit_card_applications_hmda" (
  "credit_cards_record_id" SERIAL PRIMARY KEY,
  "credit_cards_application_id" INTEGER NOT NULL,
  "reporting_year" INTEGER NOT NULL,
  "ethnicity" VARCHAR(20),
  "race" VARCHAR(20),
  "sex" VARCHAR(10),
  "age" INTEGER,
  "income" NUMERIC(18,2),
  "rate_spread" NUMERIC(6,3),
  "hoepa_status" VARCHAR(10),
  "action_taken" VARCHAR(20) NOT NULL,
  "action_taken_date" DATE NOT NULL,
  "denial_reason1" VARCHAR(30),
  "denial_reason2" VARCHAR(30),
  "submission_status" VARCHAR(20) NOT NULL DEFAULT 'PENDING'
);

CREATE TABLE "credit_cards"."reg_z_credit_card_disclosures" (
  "credit_cards_disclosure_id" SERIAL PRIMARY KEY,
  "credit_cards_application_id" INTEGER,
  "credit_cards_card_account_id" INTEGER,
  "disclosure_type" VARCHAR(50) NOT NULL,
  "disclosure_date" TIMESTAMPTZ NOT NULL,
  "delivery_method" VARCHAR(30) NOT NULL,
  "annual_percentage_rate" NUMERIC(6,3),
  "variable_rate_indicator" BOOLEAN,
  "annual_fee" NUMERIC(10,2),
  "transaction_fee_purchases" NUMERIC(10,2),
  "transaction_fee_balance_transfers" NUMERIC(10,2),
  "transaction_fee_cash_advance" NUMERIC(10,2),
  "late_payment_fee" NUMERIC(10,2),
  "over_limit_fee" NUMERIC(10,2),
  "grace_period_disclosure" TEXT,
  "balance_computation_method" VARCHAR(50),
  "document_path" VARCHAR(500)
);

CREATE TABLE "credit_cards"."ability_to_pay_assessments" (
  "credit_cards_assessment_id" SERIAL PRIMARY KEY,
  "credit_cards_application_id" INTEGER NOT NULL,
  "assessment_date" DATE NOT NULL,
  "income_verified" BOOLEAN NOT NULL,
  "income_source" VARCHAR(50) NOT NULL,
  "income_amount" NUMERIC(18,2) NOT NULL,
  "debt_obligations" NUMERIC(18,2),
  "living_expenses" NUMERIC(18,2),
  "dti_ratio" NUMERIC(5,2),
  "max_supportable_payment" NUMERIC(10,2),
  "passed_assessment" BOOLEAN NOT NULL,
  "performed_by_id" INTEGER,
  "notes" TEXT
);

CREATE TABLE "credit_cards"."consumer_complaints" (
  "credit_cards_complaint_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "receipt_date" TIMESTAMPTZ NOT NULL,
  "source" VARCHAR(30) NOT NULL,
  "complaint_type" VARCHAR(50) NOT NULL,
  "issue" VARCHAR(100) NOT NULL,
  "description" TEXT,
  "status" VARCHAR(20) NOT NULL,
  "response_sent_date" DATE,
  "resolution" TEXT,
  "resolution_date" DATE,
  "cfpb_case_number" VARCHAR(30),
  "monetary_relief_amount" NUMERIC(10,2),
  "regulatory_violation_found" BOOLEAN,
  "regulation_violated" VARCHAR(50)
);

CREATE TABLE "credit_cards"."card_product_features" (
  "credit_cards_feature_id" SERIAL PRIMARY KEY,
  "credit_cards_product_id" INTEGER NOT NULL,
  "feature_name" VARCHAR(100) NOT NULL,
  "feature_description" TEXT NOT NULL,
  "is_premium" BOOLEAN NOT NULL DEFAULT false,
  "is_limited_time" BOOLEAN NOT NULL DEFAULT false,
  "start_date" DATE,
  "end_date" DATE
);

CREATE TABLE "credit_cards"."card_product_reward_categories" (
  "credit_cards_category_id" SERIAL PRIMARY KEY,
  "credit_cards_product_id" INTEGER NOT NULL,
  "category_name" VARCHAR(50) NOT NULL,
  "reward_rate" NUMERIC(5,2) NOT NULL,
  "is_quarterly" BOOLEAN NOT NULL DEFAULT false,
  "is_capped" BOOLEAN NOT NULL DEFAULT false,
  "cap_amount" NUMERIC(10,2),
  "cap_period" VARCHAR(20),
  "start_date" DATE,
  "end_date" DATE
);

CREATE TABLE "credit_cards"."applications" (
  "credit_cards_application_id" INTEGER PRIMARY KEY,
  "customer_id" INTEGER NOT NULL,
  "credit_cards_product_id" INTEGER NOT NULL,
  "application_date" TIMESTAMPTZ NOT NULL,
  "application_channel" VARCHAR(30) NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "requested_credit_limit" NUMERIC(10,2),
  "approved_credit_limit" NUMERIC(10,2),
  "approved_interest_rate" NUMERIC(6,3),
  "decision_date" TIMESTAMPTZ,
  "decision_method" VARCHAR(20),
  "decision_reason" VARCHAR(100),
  "offer_code" VARCHAR(30),
  "referring_source" VARCHAR(50),
  "is_preapproved" BOOLEAN NOT NULL DEFAULT false,
  "is_secured" BOOLEAN NOT NULL DEFAULT false,
  "security_deposit_amount" NUMERIC(10,2),
  "balance_transfer_requested" BOOLEAN NOT NULL DEFAULT false,
  "authorized_users_requested" INTEGER,
  "annual_income" NUMERIC(18,2),
  "housing_payment" NUMERIC(10,2),
  "employment_status" VARCHAR(30),
  "approval_expiration_date" DATE,
  "time_at_current_address_years" INTEGER
);

CREATE TABLE "credit_cards"."card_accounts" (
  "credit_cards_card_account_id" SERIAL PRIMARY KEY,
  "customer_id" INTEGER NOT NULL,
  "enterprise_account_id" INTEGER NOT NULL,
  "credit_cards_product_id" INTEGER NOT NULL,
  "credit_cards_application_id" INTEGER,
  "account_number" VARCHAR(30) UNIQUE NOT NULL,
  "opened_date" DATE NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "status_update_date_time" TIMESTAMPTZ NOT NULL,
  "credit_limit" NUMERIC(10,2) NOT NULL,
  "available_credit" NUMERIC(10,2) NOT NULL,
  "cash_advance_limit" NUMERIC(10,2),
  "current_balance" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "statement_balance" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "minimum_payment_due" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "payment_due_date" DATE,
  "last_payment_date" DATE,
  "last_payment_amount" NUMERIC(10,2),
  "purchase_interest_rate" NUMERIC(6,3) NOT NULL,
  "cash_advance_interest_rate" NUMERIC(6,3),
  "balance_transfer_interest_rate" NUMERIC(6,3),
  "penalty_interest_rate" NUMERIC(6,3),
  "intro_rate_expiration_date" DATE,
  "days_past_due" INTEGER NOT NULL DEFAULT 0,
  "times_past_due_30_days" INTEGER NOT NULL DEFAULT 0,
  "times_past_due_60_days" INTEGER NOT NULL DEFAULT 0,
  "times_past_due_90_days" INTEGER NOT NULL DEFAULT 0,
  "overlimit_status" BOOLEAN NOT NULL DEFAULT false,
  "reward_points_balance" INTEGER NOT NULL DEFAULT 0,
  "is_secured" BOOLEAN NOT NULL DEFAULT false,
  "security_deposit_amount" NUMERIC(10,2),
  "annual_fee_next_charge_date" DATE,
  "cycle_cut_day" INTEGER
);

CREATE TABLE "credit_cards"."cards" (
  "credit_cards_card_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "card_number" VARCHAR(19),
  "user_type" VARCHAR(20) NOT NULL,
  "user_id" INTEGER NOT NULL,
  "card_status" VARCHAR(20) NOT NULL,
  "issue_date" DATE NOT NULL,
  "activation_date" DATE,
  "expiration_date" DATE NOT NULL,
  "card_design" VARCHAR(50),
  "is_virtual" BOOLEAN NOT NULL DEFAULT false,
  "digital_wallet_enabled" BOOLEAN NOT NULL DEFAULT false,
  "pin_set" BOOLEAN NOT NULL DEFAULT false,
  "temporary_limits" TEXT,
  "temporary_limits_expiry" DATE
);

CREATE TABLE "credit_cards"."authorized_users" (
  "credit_cards_authorized_user_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "enterprise_party_id" INTEGER NOT NULL,
  "relationship" VARCHAR(30),
  "status" VARCHAR(20) NOT NULL,
  "add_date" DATE NOT NULL,
  "remove_date" DATE,
  "spending_limit" NUMERIC(10,2),
  "limit_period" VARCHAR(20)
);

CREATE TABLE "credit_cards"."transactions" (
  "credit_cards_transaction_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "credit_cards_card_id" INTEGER NOT NULL,
  "transaction_date" TIMESTAMPTZ NOT NULL,
  "post_date" DATE NOT NULL,
  "transaction_type" VARCHAR(20) NOT NULL,
  "amount" NUMERIC(10,2) NOT NULL,
  "description" VARCHAR(100) NOT NULL,
  "category" VARCHAR(50),
  "mcc_code" VARCHAR(20),
  "is_international" BOOLEAN NOT NULL DEFAULT false,
  "original_currency" enterprise.currency_code,
  "original_amount" NUMERIC(10,2),
  "exchange_rate" NUMERIC(10,6),
  "is_recurring" BOOLEAN,
  "auth_code" VARCHAR(10),
  "reference_number" VARCHAR(30),
  "is_pending" BOOLEAN NOT NULL DEFAULT false,
  "status" VARCHAR(20) NOT NULL,
  "decline_reason" VARCHAR(50),
  "rewards_earned" NUMERIC(10,2),
  "is_billable" BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE "credit_cards"."statements" (
  "credit_cards_statement_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "statement_date" DATE NOT NULL,
  "statement_period_start" DATE NOT NULL,
  "statement_period_end" DATE NOT NULL,
  "due_date" DATE NOT NULL,
  "previous_balance" NUMERIC(10,2) NOT NULL,
  "new_charges" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "cash_advances" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "balance_transfers" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "payments" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "credits" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "fees" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "interest" NUMERIC(10,2) NOT NULL DEFAULT 0,
  "ending_balance" NUMERIC(10,2) NOT NULL,
  "minimum_payment" NUMERIC(10,2) NOT NULL,
  "payment_received" BOOLEAN NOT NULL DEFAULT false,
  "payment_received_date" DATE,
  "payment_received_amount" NUMERIC(10,2),
  "days_in_billing_cycle" INTEGER NOT NULL,
  "document_path" VARCHAR(500)
);

CREATE TABLE "credit_cards"."fees" (
  "credit_cards_fee_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "credit_cards_transaction_id" INTEGER,
  "fee_type" VARCHAR(30) NOT NULL,
  "amount" NUMERIC(10,2) NOT NULL,
  "description" VARCHAR(100),
  "date_assessed" DATE NOT NULL,
  "waived" BOOLEAN NOT NULL DEFAULT false,
  "waiver_reason" VARCHAR(100),
  "credit_cards_statement_id" INTEGER
);

CREATE TABLE "credit_cards"."interest_charges" (
  "credit_cards_charge_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "interest_type" VARCHAR(30) NOT NULL,
  "balance_subject_to_interest" NUMERIC(10,2) NOT NULL,
  "interest_rate" NUMERIC(6,3) NOT NULL,
  "days_in_period" INTEGER NOT NULL,
  "amount" NUMERIC(10,2) NOT NULL,
  "date_assessed" DATE NOT NULL,
  "credit_cards_statement_id" INTEGER NOT NULL
);

CREATE TABLE "credit_cards"."rewards" (
  "credit_cards_reward_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "credit_cards_transaction_id" INTEGER,
  "reward_type" VARCHAR(30) NOT NULL,
  "amount" NUMERIC(10,2) NOT NULL,
  "event_type" VARCHAR(20) NOT NULL,
  "description" VARCHAR(100) NOT NULL,
  "category" VARCHAR(50),
  "date_earned" DATE NOT NULL,
  "expiration_date" DATE
);

CREATE TABLE "credit_cards"."reward_redemptions" (
  "credit_cards_redemption_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "redemption_date" TIMESTAMPTZ NOT NULL,
  "redemption_type" VARCHAR(30) NOT NULL,
  "points_redeemed" INTEGER NOT NULL,
  "cash_value" NUMERIC(10,2) NOT NULL,
  "description" VARCHAR(100) NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "confirmation_code" VARCHAR(30),
  "shipping_address_id" INTEGER,
  "recipient_email" VARCHAR(100)
);

CREATE TABLE "credit_cards"."promotional_offers" (
  "credit_cards_offer_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "offer_type" VARCHAR(30) NOT NULL,
  "description" VARCHAR(255) NOT NULL,
  "offer_date" DATE NOT NULL,
  "expiration_date" DATE NOT NULL,
  "interest_rate" NUMERIC(6,3),
  "fee_percentage" NUMERIC(5,2),
  "status" VARCHAR(20) NOT NULL,
  "response_date" DATE,
  "amount_offered" NUMERIC(10,2),
  "promo_code" VARCHAR(20),
  "terms_and_conditions" TEXT
);

CREATE TABLE "credit_cards"."balance_transfers" (
  "credit_cards_transfer_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "credit_cards_transaction_id" INTEGER,
  "credit_cards_offer_id" INTEGER,
  "creditor_name" VARCHAR(100) NOT NULL,
  "account_number" VARCHAR(30),
  "transfer_amount" NUMERIC(10,2) NOT NULL,
  "fee_amount" NUMERIC(10,2),
  "interest_rate" NUMERIC(6,3) NOT NULL,
  "promotional_rate" BOOLEAN NOT NULL DEFAULT false,
  "promotion_end_date" DATE,
  "request_date" DATE NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "completion_date" DATE,
  "current_balance" NUMERIC(10,2)
);

CREATE TABLE "credit_cards"."payment_methods" (
  "credit_cards_payment_method_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "payment_type" VARCHAR(30) NOT NULL,
  "nickname" VARCHAR(50),
  "status" VARCHAR(20) NOT NULL,
  "is_default" BOOLEAN NOT NULL DEFAULT false,
  "bank_name" VARCHAR(100),
  "account_type" VARCHAR(20),
  "account_number" VARCHAR(30),
  "routing_number" VARCHAR(9),
  "expiration_date" DATE,
  "verification_status" VARCHAR(20) NOT NULL
);

CREATE TABLE "credit_cards"."autopay_settings" (
  "credit_cards_autopay_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "credit_cards_payment_method_id" INTEGER NOT NULL,
  "status" VARCHAR(20) NOT NULL,
  "payment_option" VARCHAR(30) NOT NULL,
  "fixed_amount" NUMERIC(10,2),
  "payment_day" VARCHAR(30) NOT NULL,
  "days_before_due" INTEGER,
  "specific_day" INTEGER,
  "start_date" DATE NOT NULL,
  "end_date" DATE,
  "last_payment_date" DATE,
  "next_payment_date" DATE
);

CREATE TABLE "credit_cards"."credit_limit_changes" (
  "credit_cards_change_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "change_date" DATE NOT NULL,
  "previous_limit" NUMERIC(10,2) NOT NULL,
  "new_limit" NUMERIC(10,2) NOT NULL,
  "change_reason" VARCHAR(50) NOT NULL,
  "requested_by" VARCHAR(20) NOT NULL,
  "approved_by_id" INTEGER
);

CREATE TABLE "credit_cards"."card_alerts" (
  "credit_cards_alert_id" SERIAL PRIMARY KEY,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "credit_cards_card_id" INTEGER,
  "alert_type" VARCHAR(30) NOT NULL,
  "delivery_method" VARCHAR(20) NOT NULL,
  "contact_info" VARCHAR(100) NOT NULL,
  "threshold_amount" NUMERIC(10,2),
  "is_active" BOOLEAN NOT NULL DEFAULT true,
  "created_date" DATE NOT NULL,
  "modified_date" DATE
);

CREATE TABLE "credit_cards"."disputed_transactions" (
  "credit_cards_dispute_id" SERIAL PRIMARY KEY,
  "credit_cards_transaction_id" INTEGER NOT NULL,
  "credit_cards_card_account_id" INTEGER NOT NULL,
  "dispute_date" TIMESTAMPTZ NOT NULL,
  "dispute_reason" VARCHAR(50) NOT NULL,
  "disputed_amount" NUMERIC(10,2) NOT NULL,
  "description" TEXT,
  "status" VARCHAR(20) NOT NULL,
  "resolution" VARCHAR(20),
  "resolution_date" DATE,
  "provisional_credit_date" DATE,
  "provisional_credit_amount" NUMERIC(10,2),
  "documentation_received" BOOLEAN NOT NULL DEFAULT false,
  "case_number" VARCHAR(30) NOT NULL
);

CREATE TABLE "small_business_banking"."businesses" (
  "small_business_banking_business_id" SERIAL PRIMARY KEY,
  "enterprise_party_id" INTEGER NOT NULL,
  "business_name" VARCHAR(350) NOT NULL,
  "tax_id" VARCHAR(50) NOT NULL,
  "business_type" VARCHAR(50) NOT NULL,
  "industry_code" VARCHAR(10) NOT NULL,
  "establishment_date" DATE,
  "annual_revenue" DECIMAL(18,2),
  "employee_count" INTEGER,
  "website" VARCHAR(255),
  "status" VARCHAR(20) NOT NULL DEFAULT 'active'
);

CREATE TABLE "small_business_banking"."business_owners" (
  "small_business_banking_business_owner_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "enterprise_party_id" INTEGER NOT NULL,
  "ownership_percentage" DECIMAL(5,2) NOT NULL,
  "role" VARCHAR(100) NOT NULL,
  "is_guarantor" BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE "small_business_banking"."accounts" (
  "small_business_banking_account_id" SERIAL PRIMARY KEY,
  "enterprise_account_id" INTEGER NOT NULL,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "account_number" VARCHAR(50) NOT NULL,
  "account_type" VARCHAR(50) NOT NULL,
  "small_business_banking_product_id" INTEGER NOT NULL,
  "status" VARCHAR(40) NOT NULL DEFAULT 'active',
  "status_update_date_time" TIMESTAMPTZ NOT NULL,
  "balance" DECIMAL(18,2) NOT NULL DEFAULT 0,
  "available_balance" DECIMAL(18,2) NOT NULL DEFAULT 0,
  "currency" enterprise.currency_code NOT NULL DEFAULT 'USD',
  "overdraft_limit" DECIMAL(18,2) NOT NULL DEFAULT 0,
  "interest_rate" DECIMAL(6,4),
  "statement_frequency" VARCHAR(20) NOT NULL DEFAULT 'monthly',
  "statement_day" INTEGER,
  "last_statement_date" DATE,
  "opened_date" DATE NOT NULL
);

CREATE TABLE "small_business_banking"."products" (
  "small_business_banking_product_id" SERIAL PRIMARY KEY,
  "product_code" VARCHAR(20) NOT NULL,
  "product_name" VARCHAR(100) NOT NULL,
  "product_type" VARCHAR(50) NOT NULL,
  "description" TEXT,
  "min_opening_deposit" DECIMAL(18,2),
  "monthly_fee" DECIMAL(10,2),
  "transaction_limit" INTEGER,
  "transaction_fee" DECIMAL(10,2),
  "min_balance" DECIMAL(18,2),
  "is_interest_bearing" BOOLEAN NOT NULL DEFAULT false,
  "base_interest_rate" DECIMAL(6,4),
  "term_length" INTEGER,
  "is_active" BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE "small_business_banking"."account_signatories" (
  "small_business_banking_account_signatory_id" SERIAL PRIMARY KEY,
  "small_business_banking_account_id" INTEGER NOT NULL,
  "enterprise_party_id" INTEGER NOT NULL,
  "signatory_level" VARCHAR(20) NOT NULL,
  "daily_limit" DECIMAL(18,2),
  "is_active" BOOLEAN NOT NULL DEFAULT true,
  "start_date" DATE NOT NULL,
  "end_date" DATE
);

CREATE TABLE "small_business_banking"."loans" (
  "small_business_banking_loan_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "small_business_banking_account_id" INTEGER NOT NULL,
  "small_business_banking_product_id" INTEGER NOT NULL,
  "loan_number" VARCHAR(50) NOT NULL,
  "loan_amount" DECIMAL(18,2) NOT NULL,
  "outstanding_balance" DECIMAL(18,2) NOT NULL,
  "interest_rate" DECIMAL(6,4) NOT NULL,
  "interest_type" VARCHAR(20) NOT NULL,
  "reference_rate" VARCHAR(50),
  "rate_spread" DECIMAL(6,4),
  "term_months" INTEGER NOT NULL,
  "payment_frequency" VARCHAR(20) NOT NULL,
  "payment_amount" DECIMAL(18,2) NOT NULL,
  "balloon_payment" DECIMAL(18,2),
  "disbursal_date" DATE,
  "first_payment_date" DATE,
  "maturity_date" DATE,
  "purpose" VARCHAR(255),
  "status" VARCHAR(20) NOT NULL DEFAULT 'pending'
);

CREATE TABLE "small_business_banking"."credit_lines" (
  "small_business_banking_credit_line_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "small_business_banking_account_id" INTEGER NOT NULL,
  "small_business_banking_product_id" INTEGER NOT NULL,
  "credit_line_number" VARCHAR(50) NOT NULL,
  "credit_limit" DECIMAL(18,2) NOT NULL,
  "available_credit" DECIMAL(18,2) NOT NULL,
  "outstanding_balance" DECIMAL(18,2) NOT NULL DEFAULT 0,
  "interest_rate" DECIMAL(6,4) NOT NULL,
  "interest_type" VARCHAR(20) NOT NULL,
  "reference_rate" VARCHAR(50),
  "rate_spread" DECIMAL(6,4),
  "annual_fee" DECIMAL(10,2),
  "draw_period_months" INTEGER,
  "repayment_period_months" INTEGER,
  "minimum_payment_percentage" DECIMAL(5,2) NOT NULL,
  "minimum_payment_amount" DECIMAL(10,2) NOT NULL,
  "start_date" DATE NOT NULL,
  "renewal_date" DATE,
  "status" VARCHAR(20) NOT NULL DEFAULT 'active'
);

CREATE TABLE "small_business_banking"."collateral" (
  "small_business_banking_collateral_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "collateral_type" VARCHAR(50) NOT NULL,
  "description" TEXT NOT NULL,
  "value" DECIMAL(18,2) NOT NULL,
  "valuation_date" DATE NOT NULL,
  "valuation_type" VARCHAR(50) NOT NULL,
  "location" TEXT,
  "identification_number" VARCHAR(100),
  "lien_position" INTEGER,
  "lien_filing_number" VARCHAR(100),
  "insurance_provider" VARCHAR(100),
  "insurance_policy_number" VARCHAR(100),
  "insurance_expiry_date" DATE,
  "status" VARCHAR(20) NOT NULL DEFAULT 'active'
);

CREATE TABLE "small_business_banking"."loan_collateral" (
  "small_business_banking_loan_collateral_id" SERIAL PRIMARY KEY,
  "small_business_banking_loan_id" INTEGER NOT NULL,
  "small_business_banking_collateral_id" INTEGER NOT NULL,
  "collateral_percentage" DECIMAL(5,2) NOT NULL
);

CREATE TABLE "small_business_banking"."business_card_accounts" (
  "small_business_banking_business_card_account_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "card_account_id" INTEGER NOT NULL,
  "credit_cards_product_id" INTEGER NOT NULL,
  "account_type" VARCHAR(20) NOT NULL DEFAULT 'business',
  "tax_id_reporting" VARCHAR(50) NOT NULL,
  "business_structure" VARCHAR(50) NOT NULL,
  "ownership_type" VARCHAR(50) NOT NULL,
  "liability_type" VARCHAR(20) NOT NULL,
  "linked_deposit_account_id" INTEGER,
  "relationship_manager_id" INTEGER,
  "annual_review_date" DATE,
  "expense_category_setup" VARCHAR(20) NOT NULL DEFAULT 'standard'
);

CREATE TABLE "small_business_banking"."business_card_users" (
  "small_business_banking_business_card_user_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "small_business_banking_business_card_account_id" INTEGER NOT NULL,
  "enterprise_party_id" INTEGER NOT NULL,
  "credit_cards_card_id" INTEGER NOT NULL,
  "role" VARCHAR(50) NOT NULL,
  "department" VARCHAR(100),
  "employee_id" VARCHAR(50),
  "spending_limit" DECIMAL(18,2) NOT NULL,
  "transaction_approval_required" BOOLEAN NOT NULL DEFAULT false,
  "merchant_category_restrictions" TEXT,
  "can_view_all_transactions" BOOLEAN NOT NULL DEFAULT false,
  "can_manage_all_cards" BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE "small_business_banking"."business_expense_categories" (
  "small_business_banking_category_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "category_name" VARCHAR(100) NOT NULL,
  "category_description" TEXT,
  "parent_category_id" INTEGER,
  "budget_amount" DECIMAL(18,2),
  "is_tax_deductible" BOOLEAN,
  "gl_account_code" VARCHAR(50)
);

CREATE TABLE "small_business_banking"."business_transaction_categories" (
  "small_business_banking_transaction_category_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "transaction_id" INTEGER NOT NULL,
  "small_business_banking_category_id" INTEGER NOT NULL,
  "notes" TEXT,
  "receipt_image_path" VARCHAR(500),
  "tax_relevant" BOOLEAN NOT NULL DEFAULT false,
  "created_by_id" INTEGER
);

CREATE TABLE "small_business_banking"."transactions" (
  "small_business_banking_transaction_id" SERIAL PRIMARY KEY,
  "small_business_banking_account_id" INTEGER NOT NULL,
  "transaction_type" VARCHAR(50) NOT NULL,
  "amount" DECIMAL(18,2) NOT NULL,
  "running_balance" DECIMAL(18,2),
  "currency" enterprise.currency_code NOT NULL DEFAULT 'USD',
  "description" VARCHAR(255),
  "reference_number" VARCHAR(100),
  "status" VARCHAR(20) NOT NULL DEFAULT 'completed',
  "transaction_date" DATE NOT NULL,
  "post_date" DATE,
  "created_by_id" INTEGER
);

CREATE TABLE "small_business_banking"."payments" (
  "small_business_banking_payment_id" SERIAL PRIMARY KEY,
  "source_account_id" INTEGER,
  "destination_account_id" INTEGER,
  "small_business_banking_loan_id" INTEGER,
  "small_business_banking_credit_line_id" INTEGER,
  "credit_card_id" INTEGER,
  "payment_method" VARCHAR(50) NOT NULL,
  "payment_type" VARCHAR(50) NOT NULL,
  "amount" DECIMAL(18,2) NOT NULL,
  "principal_portion" DECIMAL(18,2),
  "interest_portion" DECIMAL(18,2),
  "fees_portion" DECIMAL(18,2),
  "payment_date" DATE NOT NULL,
  "effective_date" DATE,
  "status" VARCHAR(20) NOT NULL DEFAULT 'pending',
  "external_reference" VARCHAR(100),
  "memo" VARCHAR(255)
);

CREATE TABLE "small_business_banking"."documents" (
  "small_business_banking_document_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "document_type" VARCHAR(50) NOT NULL,
  "description" VARCHAR(255) NOT NULL,
  "file_name" VARCHAR(255) NOT NULL,
  "file_path" VARCHAR(1000) NOT NULL,
  "file_type" VARCHAR(50) NOT NULL,
  "file_size" INTEGER NOT NULL,
  "document_date" DATE NOT NULL,
  "upload_date" DATE NOT NULL,
  "expiration_date" DATE,
  "status" VARCHAR(20) NOT NULL DEFAULT 'active',
  "created_by_id" INTEGER
);

CREATE TABLE "small_business_banking"."regulatory_reports" (
  "small_business_banking_report_id" SERIAL PRIMARY KEY,
  "report_type" VARCHAR(50) NOT NULL,
  "period_start_date" DATE NOT NULL,
  "period_end_date" DATE NOT NULL,
  "due_date" DATE NOT NULL,
  "status" VARCHAR(20) NOT NULL DEFAULT 'pending',
  "regulatory_agency" VARCHAR(50) NOT NULL,
  "report_owner" INTEGER NOT NULL,
  "file_specification_version" VARCHAR(20),
  "notes" TEXT
);

CREATE TABLE "small_business_banking"."report_submissions" (
  "small_business_banking_submission_id" SERIAL PRIMARY KEY,
  "small_business_banking_report_id" INTEGER NOT NULL,
  "submission_date" TIMESTAMPTZ NOT NULL,
  "submission_method" VARCHAR(50) NOT NULL,
  "confirmation_number" VARCHAR(100),
  "submitted_by_id" INTEGER NOT NULL,
  "submission_file_path" VARCHAR(500),
  "response_date" TIMESTAMPTZ,
  "response_status" VARCHAR(20),
  "response_details" TEXT
);

CREATE TABLE "small_business_banking"."regulatory_findings" (
  "small_business_banking_finding_id" SERIAL PRIMARY KEY,
  "small_business_banking_report_id" INTEGER,
  "small_business_banking_business_id" INTEGER,
  "finding_date" DATE NOT NULL,
  "source" VARCHAR(50) NOT NULL,
  "finding_type" VARCHAR(50) NOT NULL,
  "severity" VARCHAR(20) NOT NULL,
  "description" TEXT NOT NULL,
  "regulation_reference" VARCHAR(100),
  "corrective_action_required" BOOLEAN NOT NULL DEFAULT true,
  "corrective_action_description" TEXT,
  "due_date" DATE,
  "responsible_party" INTEGER,
  "status" VARCHAR(20) NOT NULL DEFAULT 'open',
  "resolution_date" DATE,
  "resolution_description" TEXT
);

CREATE TABLE "small_business_banking"."compliance_cases" (
  "small_business_banking_case_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "case_type" VARCHAR(50) NOT NULL,
  "opened_date" DATE NOT NULL,
  "priority" VARCHAR(20) NOT NULL DEFAULT 'medium',
  "status" VARCHAR(20) NOT NULL DEFAULT 'open',
  "description" TEXT NOT NULL,
  "assigned_to" INTEGER,
  "source" VARCHAR(50) NOT NULL,
  "resolution" TEXT,
  "closed_date" DATE,
  "escalated" BOOLEAN NOT NULL DEFAULT false,
  "escalation_date" DATE,
  "escalation_reason" TEXT
);

CREATE TABLE "small_business_banking"."compliance_requirements" (
  "small_business_banking_requirement_id" SERIAL PRIMARY KEY,
  "requirement_name" VARCHAR(100) NOT NULL,
  "regulation" VARCHAR(100) NOT NULL,
  "regulatory_authority" VARCHAR(50) NOT NULL,
  "description" TEXT NOT NULL,
  "business_impact" TEXT NOT NULL,
  "effective_date" DATE NOT NULL,
  "end_date" DATE,
  "requirement_owner" INTEGER NOT NULL,
  "verification_frequency" VARCHAR(20) NOT NULL,
  "verification_procedure" TEXT,
  "control_measures" TEXT,
  "is_active" BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE "small_business_banking"."business_risk_assessments" (
  "small_business_banking_assessment_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "assessment_date" DATE NOT NULL,
  "assessment_type" VARCHAR(50) NOT NULL,
  "conducted_by_id" INTEGER NOT NULL,
  "methodology" TEXT NOT NULL,
  "industry_risk_score" INTEGER NOT NULL,
  "geographic_risk_score" INTEGER NOT NULL,
  "customer_risk_score" INTEGER NOT NULL,
  "transaction_risk_score" INTEGER NOT NULL,
  "product_risk_score" INTEGER NOT NULL,
  "overall_risk_score" INTEGER NOT NULL,
  "risk_rating" VARCHAR(20) NOT NULL,
  "rationale" TEXT NOT NULL,
  "mitigating_factors" TEXT,
  "recommended_actions" TEXT,
  "next_review_date" DATE NOT NULL
);

CREATE TABLE "small_business_banking"."loan_fair_lending" (
  "small_business_banking_lending_record_id" SERIAL PRIMARY KEY,
  "small_business_banking_loan_id" INTEGER NOT NULL,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "application_date" DATE NOT NULL,
  "decision_date" DATE NOT NULL,
  "census_tract" VARCHAR(11),
  "msa_md" VARCHAR(5),
  "reported_revenue" DECIMAL(18,2) NOT NULL,
  "loan_type" VARCHAR(50) NOT NULL,
  "loan_purpose" VARCHAR(100) NOT NULL,
  "loan_amount" DECIMAL(18,2) NOT NULL,
  "amount_approved" DECIMAL(18,2),
  "action_taken" VARCHAR(20) NOT NULL,
  "denial_reason_1" VARCHAR(50),
  "denial_reason_2" VARCHAR(50),
  "denial_reason_3" VARCHAR(50),
  "denial_reason_4" VARCHAR(50),
  "rate_spread" DECIMAL(6,4),
  "naics_code" VARCHAR(6),
  "number_of_employees" INTEGER,
  "minority_owned" BOOLEAN,
  "women_owned" BOOLEAN,
  "lgbtq_owned" BOOLEAN,
  "veteran_owned" BOOLEAN,
  "exemption_claimed" BOOLEAN NOT NULL DEFAULT false,
  "exemption_reason" VARCHAR(100)
);

CREATE TABLE "small_business_banking"."credit_decisions" (
  "small_business_banking_decision_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "product_type" VARCHAR(50) NOT NULL,
  "application_id" VARCHAR(50) NOT NULL,
  "decision_date" TIMESTAMPTZ NOT NULL,
  "decision_type" VARCHAR(20) NOT NULL,
  "decision_outcome" VARCHAR(20) NOT NULL,
  "decision_factors" TEXT,
  "credit_score" INTEGER,
  "credit_score_model" VARCHAR(50),
  "annual_revenue" DECIMAL(18,2),
  "time_in_business" INTEGER,
  "collateral_value" DECIMAL(18,2),
  "debt_service_coverage_ratio" DECIMAL(6,4),
  "loan_to_value_ratio" DECIMAL(6,4),
  "exception_made" BOOLEAN NOT NULL DEFAULT false,
  "exception_reason" TEXT,
  "exception_approver" INTEGER,
  "decision_notes" TEXT,
  "decision_made_by_id" INTEGER NOT NULL
);

CREATE TABLE "small_business_banking"."adverse_action_notices" (
  "small_business_banking_notice_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "small_business_banking_decision_id" INTEGER NOT NULL,
  "notice_date" DATE NOT NULL,
  "delivery_method" VARCHAR(20) NOT NULL,
  "delivery_address" VARCHAR(200) NOT NULL,
  "delivery_date" DATE NOT NULL,
  "primary_reason" VARCHAR(100) NOT NULL,
  "secondary_reasons" TEXT,
  "credit_score_disclosed" BOOLEAN NOT NULL DEFAULT false,
  "credit_score" INTEGER,
  "score_factors" TEXT,
  "score_range_low" INTEGER,
  "score_range_high" INTEGER,
  "ecoa_notice_included" BOOLEAN NOT NULL DEFAULT true,
  "fcra_notice_included" BOOLEAN NOT NULL DEFAULT true,
  "right_to_appraisal_notice" BOOLEAN NOT NULL DEFAULT false,
  "template_version" VARCHAR(20) NOT NULL,
  "generated_by_id" INTEGER NOT NULL,
  "notice_file_path" VARCHAR(500)
);

CREATE TABLE "small_business_banking"."business_due_diligence" (
  "small_business_banking_due_diligence_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "diligence_type" VARCHAR(20) NOT NULL,
  "diligence_date" DATE NOT NULL,
  "performed_by_id" INTEGER NOT NULL,
  "business_verified" BOOLEAN NOT NULL,
  "verification_method" VARCHAR(100) NOT NULL,
  "legal_structure_verified" BOOLEAN NOT NULL,
  "business_documents_reviewed" TEXT,
  "address_verified" BOOLEAN NOT NULL,
  "tin_verified" BOOLEAN NOT NULL,
  "high_risk_factors" TEXT,
  "expected_activity" TEXT,
  "actual_activity_consistent" BOOLEAN,
  "screening_results" TEXT,
  "site_visit_conducted" BOOLEAN NOT NULL DEFAULT false,
  "site_visit_date" DATE,
  "site_visit_notes" TEXT,
  "risk_rating" VARCHAR(20) NOT NULL,
  "review_frequency" VARCHAR(20) NOT NULL,
  "next_review_date" DATE NOT NULL,
  "approval_status" VARCHAR(20) NOT NULL,
  "approved_by_id" INTEGER,
  "approval_date" DATE,
  "notes" TEXT
);

CREATE TABLE "small_business_banking"."beneficial_owner_verification" (
  "small_business_banking_verification_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER NOT NULL,
  "small_business_banking_business_owner_id" INTEGER NOT NULL,
  "verification_date" DATE NOT NULL,
  "performed_by_id" INTEGER NOT NULL,
  "ownership_percentage_verified" BOOLEAN NOT NULL,
  "verification_method" VARCHAR(50) NOT NULL,
  "id_type" VARCHAR(50),
  "id_number" VARCHAR(100),
  "id_issuing_country" VARCHAR(2),
  "id_expiration_date" DATE,
  "address_verified" BOOLEAN NOT NULL,
  "ssn_verified" BOOLEAN,
  "tin_verified" BOOLEAN,
  "screening_conducted" BOOLEAN NOT NULL DEFAULT true,
  "screening_date" DATE,
  "screening_system" VARCHAR(50),
  "screening_results" TEXT,
  "pep_status" BOOLEAN NOT NULL DEFAULT false,
  "sanctions_hit" BOOLEAN NOT NULL DEFAULT false,
  "adverse_media_found" BOOLEAN NOT NULL DEFAULT false,
  "certification_received" BOOLEAN NOT NULL,
  "certification_date" DATE,
  "recertification_due_date" DATE,
  "verification_status" VARCHAR(20) NOT NULL DEFAULT 'pending',
  "exception_reason" TEXT,
  "notes" TEXT
);

CREATE TABLE "small_business_banking"."suspicious_activity_reports" (
  "small_business_banking_sar_id" SERIAL PRIMARY KEY,
  "small_business_banking_business_id" INTEGER,
  "filing_date" DATE NOT NULL,
  "activity_start_date" DATE NOT NULL,
  "activity_end_date" DATE NOT NULL,
  "filing_institution" VARCHAR(100) NOT NULL,
  "suspicious_activity_type" VARCHAR(100) NOT NULL,
  "suspicious_activity_description" TEXT NOT NULL,
  "amount_involved" DECIMAL(18,2) NOT NULL,
  "structuring_involved" BOOLEAN NOT NULL DEFAULT false,
  "terrorist_financing_involved" BOOLEAN NOT NULL DEFAULT false,
  "fraud_involved" BOOLEAN NOT NULL DEFAULT false,
  "money_laundering_involved" BOOLEAN NOT NULL DEFAULT false,
  "insider_abuse_involved" BOOLEAN NOT NULL DEFAULT false,
  "other_involved" BOOLEAN NOT NULL DEFAULT false,
  "other_description" TEXT,
  "law_enforcement_contacted" BOOLEAN NOT NULL DEFAULT false,
  "law_enforcement_agency" VARCHAR(100),
  "law_enforcement_contact_date" DATE,
  "law_enforcement_contact_name" VARCHAR(100),
  "account_closed" BOOLEAN NOT NULL DEFAULT false,
  "account_closing_date" DATE,
  "prepared_by_id" INTEGER NOT NULL,
  "approved_by_id" INTEGER NOT NULL,
  "bsa_officer_signature" INTEGER NOT NULL,
  "fincen_acknowledgment" VARCHAR(50),
  "sar_file_path" VARCHAR(500),
  "supporting_documentation" TEXT
);

CREATE TABLE "data_quality"."validation_run" (
  "validation_run_id" SERIAL PRIMARY KEY,
  "run_timestamp" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  "source_identifier" VARCHAR(255),
  "run_user" VARCHAR(100),
  "run_role" VARCHAR(100),
  "operation_name" VARCHAR(255),
  "variables" TEXT,
  "validation_config_data" BOOLEAN,
  "validation_config_verbose" BOOLEAN,
  "validation_config_all_errors" BOOLEAN,
  "validation_config_strict" BOOLEAN,
  "query" TEXT NOT NULL,
  "validation_schema" TEXT NOT NULL,
  "total_errors" INTEGER
);

CREATE TABLE "data_quality"."validation_error" (
  "validation_error_id" SERIAL PRIMARY KEY,
  "validation_run_id" INTEGER NOT NULL,
  "instance_path" TEXT NOT NULL,
  "schema_path" TEXT NOT NULL,
  "error_keyword" VARCHAR(100) NOT NULL,
  "error_message" TEXT NOT NULL,
  "failed_data" TEXT,
  "error_params" TEXT,
  "error_schema_detail" TEXT,
  "error_parent_schema_detail" TEXT
);

CREATE TABLE "data_quality"."api_calls" (
  "api_call_id" UUID PRIMARY KEY NOT NULL,
  "method" VARCHAR NOT NULL,
  "path" VARCHAR NOT NULL,
  "query_params" TEXT,
  "request_headers" TEXT,
  "server_name" VARCHAR,
  "major_version" INTEGER,
  "minor_version" INTEGER,
  "related_institution" VARCHAR,
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "data_quality"."record_transformations" (
  "record_transformation_id" UUID PRIMARY KEY NOT NULL,
  "input_type" VARCHAR NOT NULL,
  "output_type" VARCHAR NOT NULL,
  "description" VARCHAR NOT NULL,
  "primary_key_names" VARCHAR NOT NULL,
  "primary_key_values" VARCHAR NOT NULL,
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  "api_call_id" UUID
);

CREATE TABLE "data_quality"."field_transformation_details" (
  "field_transformation_detail_id" UUID PRIMARY KEY NOT NULL,
  "transform_description" VARCHAR NOT NULL,
  "input_field_name" VARCHAR NOT NULL,
  "input_field_value" TEXT,
  "output_field_name" VARCHAR NOT NULL,
  "output_field_value" TEXT,
  "record_transformation_id" UUID
);

CREATE TABLE "data_quality"."api_lineage" (
  "api_lineage_id" UUID PRIMARY KEY NOT NULL,
  "app_mgmt_application_id" UUID,
  "host_app_mgmt_application_id" UUID,
  "security_host_id" UUID,
  "server_name" VARCHAR NOT NULL,
  "major_version" INTEGER,
  "minor_version" INTEGER,
  "api_call" VARCHAR NOT NULL,
  "query" TEXT NOT NULL,
  "description" TEXT,
  "start_date" TIMESTAMPTZ NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  "end_date" TIMESTAMPTZ,
  "updated_at" TIMESTAMPTZ
);

CREATE TABLE "data_quality"."record_lineage" (
  "record_lineage_id" VARCHAR PRIMARY KEY NOT NULL,
  "input_type" VARCHAR NOT NULL,
  "output_type" VARCHAR NOT NULL,
  "description" TEXT,
  "input_description" TEXT,
  "output_description" TEXT,
  "pk_names" VARCHAR,
  "api_lineage_id" UUID
);

CREATE TABLE "data_quality"."field_lineage" (
  "field_lineage_id" VARCHAR PRIMARY KEY NOT NULL,
  "field_name" VARCHAR NOT NULL,
  "description" TEXT,
  "input_fields" VARCHAR,
  "record_lineage_id" VARCHAR
);

CREATE INDEX ON "consumer_banking"."account_access_consents_permissions" ("consumer_banking_consent_id", "enterprise_permission_id");

CREATE UNIQUE INDEX ON "consumer_banking"."products" ("product_code");

CREATE UNIQUE INDEX ON "consumer_banking"."transaction_bank_transaction_codes" ("consumer_banking_transaction_id", "code");

CREATE UNIQUE INDEX ON "mortgage_services"."hmda_submissions" ("reporting_year", "reporting_period", "institution_lei");

CREATE UNIQUE INDEX ON "consumer_lending"."application_applicants" ("consumer_lending_application_id", "consumer_lending_applicant_id");

CREATE UNIQUE INDEX ON "consumer_lending"."payment_schedules" ("consumer_lending_loan_account_id", "payment_number");

CREATE INDEX ON "security"."identity_roles" ("security_role_id");

CREATE INDEX ON "security"."roles" ("role_name");

CREATE INDEX ON "security"."roles" ("managing_application_id");

CREATE INDEX ON "security"."roles" ("status");

CREATE INDEX ON "security"."security_account_roles" ("security_account_id");

CREATE INDEX ON "security"."security_account_roles" ("security_role_id");

CREATE INDEX ON "security"."role_entitlements" ("security_entitlement_id");

CREATE INDEX ON "security"."enhanced_entitlements" ("entitlement_name");

CREATE INDEX ON "security"."enhanced_entitlements" ("managing_application_id");

CREATE INDEX ON "security"."enhanced_entitlements" ("status");

CREATE UNIQUE INDEX ON "security"."entitlement_resources" ("security_entitlement_id", "security_resource_id", "permission_type");

CREATE INDEX ON "security"."entitlement_resources" ("security_resource_id");

CREATE INDEX ON "security"."resource_definitions" ("resource_identifier");

CREATE UNIQUE INDEX ON "security"."policies" ("name");

CREATE UNIQUE INDEX ON "small_business_banking"."businesses" ("tax_id");

CREATE UNIQUE INDEX ON "small_business_banking"."business_owners" ("small_business_banking_business_id", "enterprise_party_id");

CREATE UNIQUE INDEX ON "small_business_banking"."accounts" ("account_number");

CREATE UNIQUE INDEX ON "small_business_banking"."products" ("product_code");

CREATE UNIQUE INDEX ON "small_business_banking"."account_signatories" ("small_business_banking_account_id", "enterprise_party_id");

CREATE UNIQUE INDEX ON "small_business_banking"."loans" ("loan_number");

CREATE UNIQUE INDEX ON "small_business_banking"."credit_lines" ("credit_line_number");

CREATE UNIQUE INDEX ON "small_business_banking"."loan_collateral" ("small_business_banking_loan_id", "small_business_banking_loan_collateral_id");

CREATE UNIQUE INDEX ON "small_business_banking"."business_card_accounts" ("small_business_banking_business_id", "card_account_id");

CREATE UNIQUE INDEX ON "small_business_banking"."business_card_users" ("small_business_banking_business_card_user_id", "enterprise_party_id");

CREATE UNIQUE INDEX ON "small_business_banking"."business_expense_categories" ("small_business_banking_business_id", "category_name");

COMMENT ON TABLE "enterprise"."permissions" IS 'Defines all possible permission types that can be granted in the system';

COMMENT ON COLUMN "enterprise"."permissions"."enterprise_permission_id" IS 'Auto-incrementing identifier for each permission';

COMMENT ON COLUMN "enterprise"."permissions"."permission_name" IS 'Unique name describing the permission (e.g., read_balances)';

COMMENT ON TABLE "enterprise"."identifiers" IS 'Registry of identifiers applicable to accounts, individuals, or institutions — referenced by business-line accounts';

COMMENT ON COLUMN "enterprise"."identifiers"."enterprise_identifier_id" IS 'Unique identifier for each identifier entry in the registry';

COMMENT ON COLUMN "enterprise"."identifiers"."scheme_name" IS 'Type of identifier (e.g., BIC, IBAN, SSN, LEI, etc.)';

COMMENT ON COLUMN "enterprise"."identifiers"."identification" IS 'Actual identifier value such as a BIC code or national ID';

COMMENT ON COLUMN "enterprise"."identifiers"."name" IS 'Optional display name for this identifier (e.g., institution name)';

COMMENT ON COLUMN "enterprise"."identifiers"."secondary_identification" IS 'Additional identifier component if applicable (e.g., sub-ID)';

COMMENT ON COLUMN "enterprise"."identifiers"."lei" IS 'Optional Legal Entity Identifier if known';

COMMENT ON COLUMN "enterprise"."identifiers"."note" IS 'Free-form notes or metadata about this identifier';

COMMENT ON TABLE "enterprise"."parties" IS 'Stores information about individuals and organizations that interact with accounts, now with additional common personal attributes for individuals';

COMMENT ON COLUMN "enterprise"."parties"."enterprise_party_id" IS 'Unique identifier for each party';

COMMENT ON COLUMN "enterprise"."parties"."party_number" IS 'Alternative reference number for the party';

COMMENT ON COLUMN "enterprise"."parties"."party_type" IS 'Type of party (individual or organization)';

COMMENT ON COLUMN "enterprise"."parties"."name" IS 'Name of the party';

COMMENT ON COLUMN "enterprise"."parties"."full_business_legal_name" IS 'Complete legal name for business entities';

COMMENT ON COLUMN "enterprise"."parties"."legal_structure" IS 'Legal structure of the organization';

COMMENT ON COLUMN "enterprise"."parties"."lei" IS 'Legal Entity Identifier for organizations';

COMMENT ON COLUMN "enterprise"."parties"."beneficial_ownership" IS 'Indicates if this party has beneficial ownership';

COMMENT ON COLUMN "enterprise"."parties"."email_address" IS 'Primary email contact';

COMMENT ON COLUMN "enterprise"."parties"."phone" IS 'Primary phone contact';

COMMENT ON COLUMN "enterprise"."parties"."mobile" IS 'Mobile phone contact';

COMMENT ON COLUMN "enterprise"."parties"."date_of_birth" IS 'Party''s date of birth (for individuals)';

COMMENT ON COLUMN "enterprise"."parties"."ssn" IS 'Social Security Number (for US individuals)';

COMMENT ON COLUMN "enterprise"."parties"."marital_status" IS 'Marital status (for individuals)';

COMMENT ON COLUMN "enterprise"."parties"."citizenship_status" IS 'Citizenship or residency status (for individuals)';

COMMENT ON COLUMN "enterprise"."parties"."party_status" IS 'Current status of the party';

COMMENT ON TABLE "enterprise"."party_relationships" IS 'Defines the role of related party acts to the the enterprise party, such as power of attorney, beneficiary designations, etc.';

COMMENT ON COLUMN "enterprise"."party_relationships"."enterprise_party_relationship_id" IS 'Auto-incrementing identifier for each relationship record';

COMMENT ON COLUMN "enterprise"."party_relationships"."enterprise_party_id" IS 'References the to the party being represented or acted upon';

COMMENT ON COLUMN "enterprise"."party_relationships"."related_party_id" IS 'References the party taking the role e.g. power of attorney, guardian, etc.';

COMMENT ON COLUMN "enterprise"."party_relationships"."relationship_type" IS 'Describes the role of the related party relative to the enterprise party';

COMMENT ON COLUMN "enterprise"."party_relationships"."priority" IS 'Order of precedence for the relationship type (lower number = higher priority)';

COMMENT ON TABLE "enterprise"."customer_demographics" IS 'Stores third-party demographic and marketing data about customers';

COMMENT ON COLUMN "enterprise"."customer_demographics"."enterprise_customer_demographics_id" IS 'Auto-incrementing identifier for each demographic record';

COMMENT ON COLUMN "enterprise"."customer_demographics"."enterprise_party_id" IS 'Reference to the party this demographic data belongs to';

COMMENT ON COLUMN "enterprise"."customer_demographics"."consumer_banking_account_id" IS 'Reference is here to make sure that customer demographics are only created afeter consumer_banking.accounts. Will always be NULL.';

COMMENT ON COLUMN "enterprise"."customer_demographics"."credit_cards_card_accounts_id" IS 'Reference is here to make sure that customer demographics are only created afeter credit_cards.card_accounts. Will always be NULL';

COMMENT ON COLUMN "enterprise"."customer_demographics"."data_source" IS 'Source of the demographic data (e.g., Experian, Acxiom, TransUnion)';

COMMENT ON COLUMN "enterprise"."customer_demographics"."last_updated" IS 'Date when the demographic data was last updated';

COMMENT ON COLUMN "enterprise"."customer_demographics"."education_level" IS 'Highest level of education completed';

COMMENT ON COLUMN "enterprise"."customer_demographics"."income_bracket" IS 'Estimated annual income range';

COMMENT ON COLUMN "enterprise"."customer_demographics"."occupation_category" IS 'General occupational category';

COMMENT ON COLUMN "enterprise"."customer_demographics"."employer" IS 'Current employer name if available';

COMMENT ON COLUMN "enterprise"."customer_demographics"."employment_length_years" IS 'Years with current employer';

COMMENT ON COLUMN "enterprise"."customer_demographics"."total_household_income" IS 'Estimated total household income';

COMMENT ON COLUMN "enterprise"."customer_demographics"."household_size" IS 'Number of individuals in household';

COMMENT ON COLUMN "enterprise"."customer_demographics"."homeownership_status" IS 'Housing status';

COMMENT ON COLUMN "enterprise"."customer_demographics"."estimated_home_value" IS 'Estimated value of primary residence if owned';

COMMENT ON COLUMN "enterprise"."customer_demographics"."years_at_residence" IS 'Number of years at current residence';

COMMENT ON COLUMN "enterprise"."customer_demographics"."net_worth_estimate" IS 'Estimated net worth';

COMMENT ON COLUMN "enterprise"."customer_demographics"."political_affiliation" IS 'Inferred political leaning';

COMMENT ON COLUMN "enterprise"."customer_demographics"."number_of_children" IS 'Number of children';

COMMENT ON COLUMN "enterprise"."customer_demographics"."family_life_stage" IS 'Current family/life stage';

COMMENT ON COLUMN "enterprise"."customer_demographics"."lifestyle_segment" IS 'Marketing lifestyle segmentation';

COMMENT ON COLUMN "enterprise"."customer_demographics"."credit_risk_tier" IS 'Credit risk category';

COMMENT ON COLUMN "enterprise"."customer_demographics"."discretionary_spending_estimate" IS 'Estimated monthly discretionary spending';

COMMENT ON COLUMN "enterprise"."customer_demographics"."primary_investment_goals" IS 'Main investment objectives';

COMMENT ON COLUMN "enterprise"."customer_demographics"."risk_tolerance" IS 'Investment risk tolerance level (conservative, moderate, aggressive)';

COMMENT ON COLUMN "enterprise"."customer_demographics"."digital_engagement_score" IS 'Score indicating level of digital channel usage (1-100)';

COMMENT ON COLUMN "enterprise"."customer_demographics"."customer_lifetime_value" IS 'Calculated lifetime value to the organization';

COMMENT ON COLUMN "enterprise"."customer_demographics"."churn_risk_score" IS 'Score indicating risk of account closure (1-100)';

COMMENT ON COLUMN "enterprise"."customer_demographics"."cross_sell_propensity" IS 'Score indicating likelihood to purchase additional products (1-100)';

COMMENT ON COLUMN "enterprise"."customer_demographics"."channel_preference" IS 'Preferred communication channel (mobile, online, branch, phone)';

COMMENT ON COLUMN "enterprise"."customer_demographics"."data_consent_level" IS 'Level of consent provided for data usage';

COMMENT ON COLUMN "enterprise"."customer_demographics"."data_usage_restriction" IS 'Any specific restrictions on data usage';

COMMENT ON TABLE "enterprise"."party_entity_addresses" IS 'Links parties to entity addresses with a defined relationship';

COMMENT ON COLUMN "enterprise"."party_entity_addresses"."enterprise_party_entity_address_id" IS 'Unique identifier for party-entity address association';

COMMENT ON COLUMN "enterprise"."party_entity_addresses"."enterprise_party_id" IS 'Reference to the party';

COMMENT ON COLUMN "enterprise"."party_entity_addresses"."enterprise_address_id" IS 'Reference to the entity address';

COMMENT ON COLUMN "enterprise"."party_entity_addresses"."relationship_type" IS 'Type of relationship between the party and the address';

COMMENT ON TABLE "enterprise"."addresses" IS 'Central repository for address information used across the system';

COMMENT ON COLUMN "enterprise"."addresses"."enterprise_address_id" IS 'Auto-incrementing identifier for each address record';

COMMENT ON COLUMN "enterprise"."addresses"."address_type" IS 'Type of address (e.g., home, work, mailing)';

COMMENT ON COLUMN "enterprise"."addresses"."department" IS 'Department name for organizational addresses';

COMMENT ON COLUMN "enterprise"."addresses"."sub_department" IS 'Sub-department name for organizational addresses';

COMMENT ON COLUMN "enterprise"."addresses"."street_name" IS 'Street name component of the address';

COMMENT ON COLUMN "enterprise"."addresses"."building_number" IS 'Building or house number';

COMMENT ON COLUMN "enterprise"."addresses"."building_name" IS 'Name of building if applicable';

COMMENT ON COLUMN "enterprise"."addresses"."floor" IS 'Floor number or description';

COMMENT ON COLUMN "enterprise"."addresses"."room" IS 'Room identifier if applicable';

COMMENT ON COLUMN "enterprise"."addresses"."unit_number" IS 'Apartment or unit number';

COMMENT ON COLUMN "enterprise"."addresses"."post_box" IS 'Post office box number';

COMMENT ON COLUMN "enterprise"."addresses"."town_location_name" IS 'Name of area within town';

COMMENT ON COLUMN "enterprise"."addresses"."district_name" IS 'District or county';

COMMENT ON COLUMN "enterprise"."addresses"."care_of" IS 'Person to whose attention mail should be sent';

COMMENT ON COLUMN "enterprise"."addresses"."post_code" IS 'Postal or zip code';

COMMENT ON COLUMN "enterprise"."addresses"."town_name" IS 'City or town name';

COMMENT ON COLUMN "enterprise"."addresses"."country_sub_division" IS 'State, province, or region';

COMMENT ON COLUMN "enterprise"."addresses"."country" IS 'Two-letter country code';

COMMENT ON TABLE "enterprise"."accounts" IS 'Root account record in the account hierarchy. All other account types (consumer, mortgage, credit) are children of an enterprise account and cannot exist without it. The single source of truth for account ownership and access control.';

COMMENT ON COLUMN "enterprise"."accounts"."enterprise_account_id" IS 'Unique identifier for each enterprise account';

COMMENT ON COLUMN "enterprise"."accounts"."opened_date" IS 'When the enterprise account was created, typically coincides with first LOB account.';

COMMENT ON COLUMN "enterprise"."accounts"."status" IS 'Current status of the account. When set to ''CLOSED'', all linked LOB accounts must be closed or in a terminal state.';

COMMENT ON COLUMN "enterprise"."accounts"."status_update_date_time" IS 'When the status was last updated. Updates here may trigger required status changes in linked LOB accounts.';

COMMENT ON COLUMN "enterprise"."accounts"."account_category" IS 'Customer defined category of account (e.g., personal, business, retirement)';

COMMENT ON COLUMN "enterprise"."accounts"."description" IS 'Customer defined description of the account';

COMMENT ON TABLE "enterprise"."account_ownership" IS 'The only table that controls account access rights. Creates the mandatory link between parties and accounts. Any query checking account access or ownership must start with this table. No direct relationships exist between parties and other account tables.';

COMMENT ON COLUMN "enterprise"."account_ownership"."enterprise_account_ownership_id" IS 'Auto-incrementing, unique identifier for each account ownership record';

COMMENT ON COLUMN "enterprise"."account_ownership"."enterprise_account_id" IS 'References the enterprise account being owned. When ownership ends, access to all linked LOB accounts is terminated.';

COMMENT ON COLUMN "enterprise"."account_ownership"."enterprise_party_id" IS 'References the party who owns the account. Party must exist before ownership can be established.';

COMMENT ON TABLE "enterprise"."associates" IS 'Stores information about employees, contractors, or other individuals associated with the enterprise.';

COMMENT ON COLUMN "enterprise"."associates"."enterprise_associate_id" IS 'Unique identifier for each associate.';

COMMENT ON COLUMN "enterprise"."associates"."first_name" IS 'Associate''s first name.';

COMMENT ON COLUMN "enterprise"."associates"."last_name" IS 'Associate''s last name.';

COMMENT ON COLUMN "enterprise"."associates"."email" IS 'Associate''s unique email address.';

COMMENT ON COLUMN "enterprise"."associates"."phone_number" IS 'Associate''s phone number.';

COMMENT ON COLUMN "enterprise"."associates"."hire_date" IS 'Date the associate was hired.';

COMMENT ON COLUMN "enterprise"."associates"."status" IS 'Current status of the associate.';

COMMENT ON COLUMN "enterprise"."associates"."release_date" IS 'Date the associate was released from employment, if applicable.';

COMMENT ON COLUMN "enterprise"."associates"."job_title" IS 'Associate''s functional job title (e.g., Teller, Loan Officer).';

COMMENT ON COLUMN "enterprise"."associates"."officer_title" IS 'Associate''s formal officer title (e.g., VP, MD), if applicable.';

COMMENT ON COLUMN "enterprise"."associates"."enterprise_department_id" IS 'Foreign key referencing the department the associate belongs to.';

COMMENT ON COLUMN "enterprise"."associates"."manager_id" IS 'Foreign key referencing the associate''s manager.';

COMMENT ON COLUMN "enterprise"."associates"."salary" IS 'Associate''s annual salary.';

COMMENT ON COLUMN "enterprise"."associates"."relationship_type" IS 'Type of relationship with the company.';

COMMENT ON COLUMN "enterprise"."associates"."street_address" IS 'Associate''s street address.';

COMMENT ON COLUMN "enterprise"."associates"."city" IS 'Associate''s city of residence.';

COMMENT ON COLUMN "enterprise"."associates"."state" IS 'Associate''s state of residence.';

COMMENT ON COLUMN "enterprise"."associates"."post_code" IS 'Associate''s postal code.';

COMMENT ON COLUMN "enterprise"."associates"."country" IS 'Associate''s country of residence.';

COMMENT ON COLUMN "enterprise"."associates"."enterprise_building_id" IS 'Foreign key referencing the building where the associate is primarily located.';

COMMENT ON TABLE "enterprise"."departments" IS 'Stores information about the various departments within the enterprise.';

COMMENT ON COLUMN "enterprise"."departments"."enterprise_department_id" IS 'Unique identifier for each department.';

COMMENT ON COLUMN "enterprise"."departments"."department_name" IS 'Name of the department.';

COMMENT ON COLUMN "enterprise"."departments"."location" IS 'Physical location of the department.';

COMMENT ON COLUMN "enterprise"."departments"."operating_unit" IS 'This department is managed under this operating unit.';

COMMENT ON TABLE "enterprise"."buildings" IS 'Stores information about the physical buildings used by the enterprise, including branches and other facilities.';

COMMENT ON COLUMN "enterprise"."buildings"."enterprise_building_id" IS 'Unique identifier for each building.';

COMMENT ON COLUMN "enterprise"."buildings"."enterprise_address_id" IS 'Address of the building';

COMMENT ON COLUMN "enterprise"."buildings"."building_name" IS 'Name of the building.';

COMMENT ON COLUMN "enterprise"."buildings"."building_type" IS 'Type of building classified by primary function.';

COMMENT ON COLUMN "enterprise"."buildings"."phone_number" IS 'Phone number of the building.';

COMMENT ON COLUMN "enterprise"."buildings"."open_date" IS 'Date the building was opened.';

COMMENT ON COLUMN "enterprise"."buildings"."close_date" IS 'Date the building was closed, if applicable.';

COMMENT ON TABLE "consumer_banking"."accounts" IS 'Deposit account linked to enterprise account; always serviced by a this institution';

COMMENT ON COLUMN "consumer_banking"."accounts"."consumer_banking_account_id" IS 'Unique ID for the consumer banking account';

COMMENT ON COLUMN "consumer_banking"."accounts"."enterprise_account_id" IS 'Link to the enterprise-level account bucket';

COMMENT ON COLUMN "consumer_banking"."accounts"."account_number" IS 'Customer facing account number';

COMMENT ON COLUMN "consumer_banking"."accounts"."consumer_banking_product_id" IS 'References the enterprise account this consumer account belongs to. Required for all consumer accounts';

COMMENT ON COLUMN "consumer_banking"."accounts"."opened_date" IS 'Date the account was opened';

COMMENT ON COLUMN "consumer_banking"."accounts"."maturity_date" IS 'Used for products such as certificates of deposits that have a maturity date';

COMMENT ON COLUMN "consumer_banking"."accounts"."nickname" IS 'A short name added by customer.';

COMMENT ON COLUMN "consumer_banking"."accounts"."displayName" IS 'A friendly account description provided by the institution.';

COMMENT ON COLUMN "consumer_banking"."accounts"."status" IS 'Operational status of the account';

COMMENT ON COLUMN "consumer_banking"."accounts"."switch_status" IS 'Specific to the UK account account switching service.';

COMMENT ON COLUMN "consumer_banking"."accounts"."status_update_date_time" IS 'Last time the status was updated';

COMMENT ON COLUMN "consumer_banking"."accounts"."servicer_identifier_id" IS 'Required reference to this institutions BIC scheme';

COMMENT ON COLUMN "consumer_banking"."accounts"."annualPercentageYield" IS 'APR on interest earned in this account, null if it is not interest earning.';

COMMENT ON COLUMN "consumer_banking"."accounts"."interestYtd" IS 'Interest earned year to date in this account. null if it is not interest earning.';

COMMENT ON COLUMN "consumer_banking"."accounts"."term" IS 'The total number of periods a time bound account is active (like a CD). null if it is not a time bound product.';

COMMENT ON TABLE "consumer_banking"."account_access_consents" IS 'Stores consent records for account access, tracking when and how third parties are permitted to access consumer banking account information';

COMMENT ON COLUMN "consumer_banking"."account_access_consents"."consumer_banking_consent_id" IS 'Unique identifier for each consent record';

COMMENT ON COLUMN "consumer_banking"."account_access_consents"."consumer_banking_account_id" IS 'References the account that the consent is related to.';

COMMENT ON COLUMN "consumer_banking"."account_access_consents"."creation_date_time" IS 'When the consent was initially created';

COMMENT ON COLUMN "consumer_banking"."account_access_consents"."status" IS 'Current status of the consent (e.g., Active, Revoked)';

COMMENT ON COLUMN "consumer_banking"."account_access_consents"."status_update_date_time" IS 'When the status was last changed';

COMMENT ON COLUMN "consumer_banking"."account_access_consents"."expiration_date_time" IS 'When the consent will expire (if applicable)';

COMMENT ON TABLE "consumer_banking"."account_access_consents_permissions" IS 'Junction table linking consents to specific permissions granted, implements a many-to-many relationship';

COMMENT ON COLUMN "consumer_banking"."account_access_consents_permissions"."consumer_banking_consent_id" IS 'References a consent record';

COMMENT ON COLUMN "consumer_banking"."account_access_consents_permissions"."enterprise_permission_id" IS 'References a permission record';

COMMENT ON TABLE "consumer_banking"."balances" IS 'Tracks account balance information with history, stores different types of balances';

COMMENT ON COLUMN "consumer_banking"."balances"."consumer_banking_balance_id" IS 'Auto-incrementing identifier for each balance record';

COMMENT ON COLUMN "consumer_banking"."balances"."consumer_banking_account_id" IS 'References the account this balance belongs to';

COMMENT ON COLUMN "consumer_banking"."balances"."credit_debit_indicator" IS 'Indicates if balance is credit or debit';

COMMENT ON COLUMN "consumer_banking"."balances"."type" IS 'Primary balance type (e.g., available, closing, etc.)';

COMMENT ON COLUMN "consumer_banking"."balances"."date_time" IS 'When this balance was recorded';

COMMENT ON COLUMN "consumer_banking"."balances"."amount" IS 'Monetary amount with precision to 5 decimal places';

COMMENT ON COLUMN "consumer_banking"."balances"."currency" IS 'Currency code (e.g., USD, EUR)';

COMMENT ON COLUMN "consumer_banking"."balances"."sub_type" IS 'Optional further classification of balance type';

COMMENT ON TABLE "consumer_banking"."beneficiaries" IS 'Stores beneficiary details for account payments, records entities that can receive payments';

COMMENT ON COLUMN "consumer_banking"."beneficiaries"."consumer_banking_beneficiary_id" IS 'Unique identifier for each beneficiary';

COMMENT ON COLUMN "consumer_banking"."beneficiaries"."consumer_banking_account_id" IS 'References the account this balance belongs to';

COMMENT ON COLUMN "consumer_banking"."beneficiaries"."beneficiary_type" IS 'Type of beneficiary (individual, organization, etc.)';

COMMENT ON COLUMN "consumer_banking"."beneficiaries"."reference" IS 'Optional reference identifier for the beneficiary';

COMMENT ON COLUMN "consumer_banking"."beneficiaries"."supplementary_data" IS 'Additional information in free-text format';

COMMENT ON TABLE "consumer_banking"."beneficiary_creditor_agents" IS 'Stores financial institution details for beneficiaries, records information about banks/agents';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_agents"."consumer_banking_beneficiary_creditor_agent_id" IS 'Auto-incrementing identifier for each agent record';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_agents"."consumer_banking_beneficiary_id" IS 'References the beneficiary this agent is associated with';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_agents"."scheme_name" IS 'Identifier scheme (e.g., BIC, SORT)';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_agents"."identification" IS 'The actual identifier of the institution';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_agents"."name" IS 'Display name of the financial institution';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_agents"."lei" IS 'Legal Entity Identifier of the institution';

COMMENT ON TABLE "consumer_banking"."beneficiary_creditor_accounts" IS 'Stores account details of beneficiaries for payment routing';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_accounts"."consumer_banking_beneficiary_creditor_account_id" IS 'Auto-incrementing identifier for each creditor account record';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_accounts"."consumer_banking_beneficiary_id" IS 'References the beneficiary this account belongs to';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_accounts"."scheme_name" IS 'Account identifier scheme (e.g., IBAN, BBAN)';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_accounts"."identification" IS 'The actual account identifier value';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_accounts"."name" IS 'Optional display name for this account';

COMMENT ON COLUMN "consumer_banking"."beneficiary_creditor_accounts"."secondary_identification" IS 'Additional account identification information';

COMMENT ON TABLE "consumer_banking"."direct_debits" IS 'Stores information about direct debit arrangements set up on accounts';

COMMENT ON COLUMN "consumer_banking"."direct_debits"."consumer_banking_direct_debit_id" IS 'Unique identifier for each direct debit mandate';

COMMENT ON COLUMN "consumer_banking"."direct_debits"."consumer_banking_account_id" IS 'References the account this direct debit belongs to';

COMMENT ON COLUMN "consumer_banking"."direct_debits"."direct_debit_status_code" IS 'Status code of the direct debit (e.g., active, canceled)';

COMMENT ON COLUMN "consumer_banking"."direct_debits"."name" IS 'Name of the merchant/organization collecting the direct debit';

COMMENT ON COLUMN "consumer_banking"."direct_debits"."previous_payment_date_time" IS 'When the last payment was made';

COMMENT ON COLUMN "consumer_banking"."direct_debits"."previous_payment_amount" IS 'Amount of the last payment';

COMMENT ON COLUMN "consumer_banking"."direct_debits"."previous_payment_currency" IS 'Currency of the last payment';

COMMENT ON TABLE "consumer_banking"."mandate_related_information" IS 'Stores detailed information about direct debit mandates including payment schedules';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."consumer_banking_mandate_related_information_id" IS 'Auto-incrementing identifier for mandate information';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."consumer_banking_direct_debit_id" IS 'References the direct debit this mandate belongs to';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."mandate_id" IS 'Unique reference for the direct debit mandate';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."classification" IS 'Classification of the mandate (e.g., personal, business)';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."category" IS 'Purpose code for categorizing the payment type';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."first_payment_date_time" IS 'When the first payment is scheduled';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."recurring_payment_date_time" IS 'When recurring payments are scheduled';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."final_payment_date_time" IS 'When the final payment is scheduled (if applicable)';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."frequency_type" IS 'How often payments occur (e.g., monthly, weekly)';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."frequency_count_per_period" IS 'Number of payments in each period';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."frequency_point_in_time" IS 'Specific day or time point for payments';

COMMENT ON COLUMN "consumer_banking"."mandate_related_information"."reason" IS 'Reason or purpose for the mandate';

COMMENT ON TABLE "consumer_banking"."offers" IS 'Stores promotional offers made to account holders';

COMMENT ON COLUMN "consumer_banking"."offers"."consumer_banking_offer_id" IS 'Unique identifier for each offer';

COMMENT ON COLUMN "consumer_banking"."offers"."consumer_banking_account_id" IS 'References the account this offer belongs to';

COMMENT ON COLUMN "consumer_banking"."offers"."offer_type" IS 'Type of offer (e.g., loan, investment, balance transfer)';

COMMENT ON COLUMN "consumer_banking"."offers"."description" IS 'Detailed description of the offer';

COMMENT ON COLUMN "consumer_banking"."offers"."start_date_time" IS 'When the offer becomes available';

COMMENT ON COLUMN "consumer_banking"."offers"."end_date_time" IS 'When the offer expires';

COMMENT ON COLUMN "consumer_banking"."offers"."rate" IS 'Interest rate associated with the offer';

COMMENT ON COLUMN "consumer_banking"."offers"."value" IS 'Numerical value related to the offer (e.g., reward points)';

COMMENT ON COLUMN "consumer_banking"."offers"."term" IS 'Terms and conditions of the offer';

COMMENT ON COLUMN "consumer_banking"."offers"."url" IS 'Web link for more information about the offer';

COMMENT ON COLUMN "consumer_banking"."offers"."amount" IS 'Monetary amount of the offer';

COMMENT ON COLUMN "consumer_banking"."offers"."amount_currency" IS 'Currency of the offer amount';

COMMENT ON COLUMN "consumer_banking"."offers"."fee" IS 'Any fee associated with accepting the offer';

COMMENT ON COLUMN "consumer_banking"."offers"."fee_currency" IS 'Currency of the fee';

COMMENT ON TABLE "consumer_banking"."products" IS 'Defines the financial products offered to customers';

COMMENT ON COLUMN "consumer_banking"."products"."consumer_banking_product_id" IS 'Unique identifier for each product';

COMMENT ON COLUMN "consumer_banking"."products"."product_code" IS 'Internal code for the product';

COMMENT ON COLUMN "consumer_banking"."products"."product_name" IS 'Display name for the product';

COMMENT ON COLUMN "consumer_banking"."products"."product_type" IS 'Type of product (checking, savings, money market, etc.)';

COMMENT ON COLUMN "consumer_banking"."products"."description" IS 'Detailed product description';

COMMENT ON COLUMN "consumer_banking"."products"."min_opening_deposit" IS 'Minimum amount required to open an account of this product type';

COMMENT ON COLUMN "consumer_banking"."products"."monthly_fee" IS 'Standard monthly maintenance fee';

COMMENT ON COLUMN "consumer_banking"."products"."fee_schedule" IS 'Type of fee structure applicable to this product';

COMMENT ON COLUMN "consumer_banking"."products"."transaction_limit" IS 'Number of free transactions per statement period';

COMMENT ON COLUMN "consumer_banking"."products"."transaction_fee" IS 'Fee charged per transaction beyond the limit';

COMMENT ON COLUMN "consumer_banking"."products"."min_balance" IS 'Minimum balance to avoid fees';

COMMENT ON COLUMN "consumer_banking"."products"."is_interest_bearing" IS 'Indicates if the product earns interest';

COMMENT ON COLUMN "consumer_banking"."products"."base_interest_rate" IS 'Standard interest rate for the product (if applicable)';

COMMENT ON COLUMN "consumer_banking"."products"."interest_calculation_method" IS 'Method used to calculate interest on the account';

COMMENT ON COLUMN "consumer_banking"."products"."term_length" IS 'Term in months (for term products)';

COMMENT ON COLUMN "consumer_banking"."products"."status" IS 'Current availability status of the product';

COMMENT ON COLUMN "consumer_banking"."products"."launch_date" IS 'Date when product was first offered';

COMMENT ON COLUMN "consumer_banking"."products"."discontinue_date" IS 'Date when product was discontinued if applicable';

COMMENT ON TABLE "consumer_banking"."other_product_types" IS 'Stores information about non-standard product types not covered in main categories';

COMMENT ON COLUMN "consumer_banking"."other_product_types"."consumer_banking_other_product_type_id" IS 'Auto-incrementing identifier for each custom product type';

COMMENT ON COLUMN "consumer_banking"."other_product_types"."consumer_banking_product_id" IS 'References the related product record';

COMMENT ON COLUMN "consumer_banking"."other_product_types"."name" IS 'Name of the custom product type';

COMMENT ON COLUMN "consumer_banking"."other_product_types"."description" IS 'Detailed description of the custom product type';

COMMENT ON TABLE "consumer_banking"."scheduled_payments" IS 'Stores information about one-time and recurring scheduled payments';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."consumer_banking_scheduled_payment_id" IS 'Unique identifier for each scheduled payment';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."consumer_banking_account_id" IS 'References the account this balance belongs to';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."scheduled_payment_date_time" IS 'When the payment is scheduled to occur';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."scheduled_type" IS 'Type of scheduled payment';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."payment_method" IS 'Method of payment execution';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."payment_status" IS 'Current status of the scheduled payment';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."frequency" IS 'Frequency of recurring payments if applicable';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."reference" IS 'Reference identifier for the payment';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."debtor_reference" IS 'Reference identifier for the payer';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."instructed_amount" IS 'Amount to be paid';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."instructed_amount_currency" IS 'Currency of the payment amount';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."end_date" IS 'End date for recurring payments';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."execution_count" IS 'Number of times recurring payment has executed';

COMMENT ON COLUMN "consumer_banking"."scheduled_payments"."max_executions" IS 'Maximum number of executions for recurring payment';

COMMENT ON TABLE "consumer_banking"."scheduled_payment_creditor_agents" IS 'Stores information about financial institutions receiving scheduled payments';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_agents"."consumer_banking_scheduled_payment_creditor_agent_id" IS 'Auto-incrementing identifier for each agent record';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_agents"."consumer_banking_scheduled_payment_id" IS 'References the scheduled payment';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_agents"."scheme_name" IS 'Identifier scheme for the receiving institution (e.g., BIC)';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_agents"."identification" IS 'Identifier of the receiving financial institution';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_agents"."name" IS 'Name of the receiving financial institution';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_agents"."lei" IS 'Legal Entity Identifier of the receiving institution';

COMMENT ON TABLE "consumer_banking"."scheduled_payment_creditor_accounts" IS 'Stores information about accounts receiving scheduled payments';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_accounts"."consumer_banking_scheduled_payment_creditor_account_id" IS 'Auto-incrementing identifier for each creditor account';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_accounts"."consumer_banking_scheduled_payment_id" IS 'References the scheduled payment';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_accounts"."scheme_name" IS 'Account identifier scheme (e.g., IBAN)';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_accounts"."identification" IS 'Account identifier for receiving the payment';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_accounts"."name" IS 'Name associated with the receiving account';

COMMENT ON COLUMN "consumer_banking"."scheduled_payment_creditor_accounts"."secondary_identification" IS 'Additional identification for the receiving account';

COMMENT ON TABLE "consumer_banking"."standing_orders" IS 'Stores information about recurring payment instructions (standing orders)';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."consumer_banking_standing_order_id" IS 'Unique identifier for each standing order';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."consumer_banking_account_id" IS 'References the account this standing order belongs to';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."next_payment_date_time" IS 'When the next payment is scheduled';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."last_payment_date_time" IS 'When the most recent payment was made';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."standing_order_status_code" IS 'Status code of the standing order (e.g., active, canceled)';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."first_payment_amount" IS 'Amount of the first payment (if different)';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."first_payment_currency" IS 'Currency of the first payment';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."next_payment_amount" IS 'Amount of the next scheduled payment';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."next_payment_currency" IS 'Currency of the next payment';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."last_payment_amount" IS 'Amount of the most recent payment';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."last_payment_currency" IS 'Currency of the most recent payment';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."final_payment_amount" IS 'Amount of the final payment (if different)';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."final_payment_currency" IS 'Currency of the final payment';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."frequency" IS 'Frequency of standing order payments';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."start_date" IS 'Date when the first payment should be made';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."end_date" IS 'Date when the standing order expires (if specified)';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."day_of_month" IS 'Day of month for payments (for monthly/quarterly frequencies)';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."day_of_week" IS 'Day of week for payments (for weekly frequencies)';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."payment_type" IS 'Type of payment (fixed, variable, etc.)';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."category" IS 'Category or purpose of the standing order';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."reference" IS 'Payment reference shown to the recipient';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."description" IS 'Description of the standing order purpose';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."created_date" IS 'When the standing order was created';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."created_by" IS 'Who or what created the standing order';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."modified_date" IS 'When the standing order was last modified';

COMMENT ON COLUMN "consumer_banking"."standing_orders"."supplementary_data" IS 'Additional information about the standing order in JSON format';

COMMENT ON TABLE "consumer_banking"."standing_order_creditor_agents" IS 'Stores information about financial institutions receiving standing order payments';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_agents"."consumer_banking_standing_order_creditor_agent_id" IS 'Auto-incrementing identifier for each agent record';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_agents"."consumer_banking_standing_order_id" IS 'References the standing order';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_agents"."scheme_name" IS 'Identifier scheme for the receiving institution';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_agents"."identification" IS 'Identifier of the receiving financial institution';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_agents"."name" IS 'Name of the receiving financial institution';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_agents"."lei" IS 'Legal Entity Identifier of the receiving institution';

COMMENT ON TABLE "consumer_banking"."standing_order_creditor_accounts" IS 'Stores information about accounts receiving standing order payments';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_accounts"."consumer_banking_standing_order_creditor_account_id" IS 'Auto-incrementing identifier for each creditor account';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_accounts"."consumer_banking_standing_order_id" IS 'References the standing order';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_accounts"."scheme_name" IS 'Account identifier scheme (e.g., IBAN)';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_accounts"."identification" IS 'Account identifier for receiving the payments';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_accounts"."name" IS 'Name associated with the receiving account';

COMMENT ON COLUMN "consumer_banking"."standing_order_creditor_accounts"."secondary_identification" IS 'Additional identification for the receiving account';

COMMENT ON TABLE "consumer_banking"."statements" IS 'Stores information about account statements';

COMMENT ON COLUMN "consumer_banking"."statements"."consumer_banking_statement_id" IS 'Unique identifier for each statement';

COMMENT ON COLUMN "consumer_banking"."statements"."consumer_banking_account_id" IS 'References the account this balance belongs to';

COMMENT ON COLUMN "consumer_banking"."statements"."statement_reference" IS 'Reference number for the statement';

COMMENT ON COLUMN "consumer_banking"."statements"."type" IS 'Type of statement (e.g., regular, interim, final)';

COMMENT ON COLUMN "consumer_banking"."statements"."start_date_time" IS 'Start of the period covered by the statement';

COMMENT ON COLUMN "consumer_banking"."statements"."end_date_time" IS 'End of the period covered by the statement';

COMMENT ON COLUMN "consumer_banking"."statements"."creation_date_time" IS 'When the statement was generated';

COMMENT ON TABLE "consumer_banking"."statement_descriptions" IS 'Stores additional descriptive information for statements';

COMMENT ON COLUMN "consumer_banking"."statement_descriptions"."consumer_banking_statement_description_id" IS 'Auto-incrementing identifier for each description entry';

COMMENT ON COLUMN "consumer_banking"."statement_descriptions"."consumer_banking_statement_id" IS 'References the statement this description belongs to';

COMMENT ON COLUMN "consumer_banking"."statement_descriptions"."description" IS 'Descriptive text about the statement';

COMMENT ON TABLE "consumer_banking"."statement_benefits" IS 'Stores information about benefits received during a statement period';

COMMENT ON COLUMN "consumer_banking"."statement_benefits"."consumer_banking_statement_benefit_id" IS 'Auto-incrementing identifier for each benefit record';

COMMENT ON COLUMN "consumer_banking"."statement_benefits"."consumer_banking_statement_id" IS 'References the statement this benefit belongs to';

COMMENT ON COLUMN "consumer_banking"."statement_benefits"."type" IS 'Type of benefit (e.g., cashback, rewards, insurance)';

COMMENT ON COLUMN "consumer_banking"."statement_benefits"."amount" IS 'Monetary value of the benefit';

COMMENT ON COLUMN "consumer_banking"."statement_benefits"."currency" IS 'Currency code for the benefit amount';

COMMENT ON TABLE "consumer_banking"."statement_fees" IS 'Stores information about fees charged during a statement period';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."consumer_banking_statement_fee_id" IS 'Auto-incrementing identifier for each fee record';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."consumer_banking_statement_id" IS 'References the statement this fee belongs to';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."description" IS 'Description of the fee';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."credit_debit_indicator" IS 'Indicates if fee is a credit or debit';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."type" IS 'Type of fee (e.g., service, transaction, late payment)';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."rate" IS 'Rate applied if fee is percentage-based';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."rate_type" IS 'Type of rate (e.g., fixed, variable)';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."frequency" IS 'How often the fee is applied (e.g., monthly, per transaction)';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."amount" IS 'Monetary amount of the fee';

COMMENT ON COLUMN "consumer_banking"."statement_fees"."currency" IS 'Currency code for the fee amount';

COMMENT ON TABLE "consumer_banking"."statement_interests" IS 'Stores information about interest earned or charged during a statement period';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."consumer_banking_statement_interest_id" IS 'Auto-incrementing identifier for each interest record';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."consumer_banking_statement_id" IS 'References the statement this interest belongs to';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."description" IS 'Description of the interest';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."credit_debit_indicator" IS 'Indicates if interest is earned (credit) or charged (debit)';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."type" IS 'Type of interest (e.g., deposit, loan, credit card)';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."rate" IS 'Interest rate applied';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."rate_type" IS 'Type of rate (e.g., fixed, variable, promotional)';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."frequency" IS 'How often interest is calculated (e.g., daily, monthly)';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."amount" IS 'Monetary amount of interest earned or charged';

COMMENT ON COLUMN "consumer_banking"."statement_interests"."currency" IS 'Currency code for the interest amount';

COMMENT ON TABLE "consumer_banking"."statement_amounts" IS 'Stores various monetary amount totals associated with a statement';

COMMENT ON COLUMN "consumer_banking"."statement_amounts"."consumer_banking_statement_amount_id" IS 'Auto-incrementing identifier for each amount record';

COMMENT ON COLUMN "consumer_banking"."statement_amounts"."consumer_banking_statement_id" IS 'References the statement this amount belongs to';

COMMENT ON COLUMN "consumer_banking"."statement_amounts"."credit_debit_indicator" IS 'Indicates if amount is a credit or debit';

COMMENT ON COLUMN "consumer_banking"."statement_amounts"."type" IS 'Type of amount (e.g., opening balance, closing balance, payments)';

COMMENT ON COLUMN "consumer_banking"."statement_amounts"."amount" IS 'Monetary value';

COMMENT ON COLUMN "consumer_banking"."statement_amounts"."currency" IS 'Currency code for the amount';

COMMENT ON COLUMN "consumer_banking"."statement_amounts"."sub_type" IS 'Further classification of the amount type';

COMMENT ON TABLE "consumer_banking"."statement_date_times" IS 'Stores important dates associated with a statement';

COMMENT ON COLUMN "consumer_banking"."statement_date_times"."consumer_banking_statement_date_time_id" IS 'Auto-incrementing identifier for each date record';

COMMENT ON COLUMN "consumer_banking"."statement_date_times"."consumer_banking_statement_id" IS 'References the statement this date belongs to';

COMMENT ON COLUMN "consumer_banking"."statement_date_times"."date_time" IS 'Date and time value';

COMMENT ON COLUMN "consumer_banking"."statement_date_times"."type" IS 'Type of date (e.g., payment due, minimum payment, cycle end)';

COMMENT ON TABLE "consumer_banking"."statement_rates" IS 'Stores various rate information associated with statements, including interest rates, promotional rates, and exchange rates';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."consumer_banking_statement_rate_id" IS 'Auto-incrementing identifier for each rate record';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."consumer_banking_statement_id" IS 'References the statement this rate belongs to';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."rate" IS 'Rate value (e.g., interest rate, exchange rate)';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."type" IS 'Type of rate (e.g., APR, promotional rate)';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."description" IS 'Additional description of the rate''s applicability';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."effective_date" IS 'Date when this rate became effective';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."expiration_date" IS 'Date when this rate expires (if applicable)';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."is_variable" IS 'Whether this is a variable rate';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."index_rate" IS 'Base index rate for variable rates';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."margin" IS 'Margin added to index for variable rates';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."balance_subject_to_rate" IS 'Balance amount subject to this rate';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."created_at" IS 'When this record was created';

COMMENT ON COLUMN "consumer_banking"."statement_rates"."updated_at" IS 'When this record was last updated';

COMMENT ON TABLE "consumer_banking"."statement_values" IS 'Stores miscellaneous values associated with a statement that aren''t monetary amounts, such as loyalty points, credit scores, or tier levels';

COMMENT ON COLUMN "consumer_banking"."statement_values"."consumer_banking_statement_value_id" IS 'Auto-incrementing identifier for each value record';

COMMENT ON COLUMN "consumer_banking"."statement_values"."consumer_banking_statement_id" IS 'References the statement this value belongs to';

COMMENT ON COLUMN "consumer_banking"."statement_values"."value" IS 'Value content (e.g., loyalty points, tier level, credit score)';

COMMENT ON COLUMN "consumer_banking"."statement_values"."type" IS 'Type of value stored';

COMMENT ON COLUMN "consumer_banking"."statement_values"."description" IS 'Additional description or context for the value';

COMMENT ON COLUMN "consumer_banking"."statement_values"."previous_value" IS 'Previous statement''s value of the same type, for comparison';

COMMENT ON COLUMN "consumer_banking"."statement_values"."change_percentage" IS 'Percentage change from previous statement';

COMMENT ON COLUMN "consumer_banking"."statement_values"."is_estimated" IS 'Whether this value is estimated rather than confirmed';

COMMENT ON COLUMN "consumer_banking"."statement_values"."reference_period_start" IS 'Start of the period this value refers to, if different from statement period';

COMMENT ON COLUMN "consumer_banking"."statement_values"."reference_period_end" IS 'End of the period this value refers to, if different from statement period';

COMMENT ON COLUMN "consumer_banking"."statement_values"."created_at" IS 'When this record was created';

COMMENT ON COLUMN "consumer_banking"."statement_values"."updated_at" IS 'When this record was last updated';

COMMENT ON TABLE "consumer_banking"."transactions" IS 'Stores detailed information about account transactions';

COMMENT ON COLUMN "consumer_banking"."transactions"."consumer_banking_transaction_id" IS 'Unique identifier for each transaction';

COMMENT ON COLUMN "consumer_banking"."transactions"."consumer_banking_account_id" IS 'References the account this transaction belongs to';

COMMENT ON COLUMN "consumer_banking"."transactions"."consumer_banking_balance_id" IS 'No meaningful relationship, just guarantees that balances must exist before a transaction can be created.';

COMMENT ON COLUMN "consumer_banking"."transactions"."transaction_reference" IS 'Reference code for the transaction';

COMMENT ON COLUMN "consumer_banking"."transactions"."credit_debit_indicator" IS 'Indicates if transaction is a credit or debit';

COMMENT ON COLUMN "consumer_banking"."transactions"."status" IS 'Status of the transaction (e.g., pending, booked, rejected)';

COMMENT ON COLUMN "consumer_banking"."transactions"."transaction_mutability" IS 'Whether the transaction can be changed (e.g., mutable, immutable)';

COMMENT ON COLUMN "consumer_banking"."transactions"."transaction_date" IS 'When the transaction was recorded in the books';

COMMENT ON COLUMN "consumer_banking"."transactions"."category" IS 'High-level categorization of the transaction';

COMMENT ON COLUMN "consumer_banking"."transactions"."transaction_type" IS 'Specific type of transaction with more detail';

COMMENT ON COLUMN "consumer_banking"."transactions"."value_date" IS 'When the transaction affects the account balance';

COMMENT ON COLUMN "consumer_banking"."transactions"."description" IS 'Additional information about the transaction';

COMMENT ON COLUMN "consumer_banking"."transactions"."merchant_address" IS 'Address associated with the transaction, if applicable';

COMMENT ON COLUMN "consumer_banking"."transactions"."amount" IS 'Monetary amount of the transaction';

COMMENT ON COLUMN "consumer_banking"."transactions"."currency" IS 'Currency code for the transaction amount';

COMMENT ON COLUMN "consumer_banking"."transactions"."charge_amount" IS 'Any fees associated with the transaction';

COMMENT ON COLUMN "consumer_banking"."transactions"."charge_currency" IS 'Currency code for the transaction fee';

COMMENT ON TABLE "consumer_banking"."transaction_statement_references" IS 'Links transactions to specific statements they appear on';

COMMENT ON COLUMN "consumer_banking"."transaction_statement_references"."consumer_banking_transaction_statement_reference_id" IS 'Auto-incrementing identifier for each transaction-statement reference record';

COMMENT ON COLUMN "consumer_banking"."transaction_statement_references"."consumer_banking_transaction_id" IS 'References the transaction this reference belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_statement_references"."statement_reference" IS 'Statement reference n';

COMMENT ON TABLE "consumer_banking"."transaction_currency_exchanges" IS 'Stores currency exchange details for cross-currency transactions';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."consumer_banking_transaction_currency_exchange_id" IS 'Auto-incrementing identifier for each currency exchange record';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."consumer_banking_transaction_id" IS 'References the transaction this currency exchange belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."source_currency" IS 'Original currency of the transaction';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."target_currency" IS 'Destination currency after conversion';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."unit_currency" IS 'Currency used as the unit for the exchange rate';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."exchange_rate" IS 'Rate used for the currency conversion';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."contract_identification" IS 'Identifier for any forex contract used';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."quotation_date" IS 'When the exchange rate was quoted';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."instructed_amount" IS 'Original amount before conversion';

COMMENT ON COLUMN "consumer_banking"."transaction_currency_exchanges"."instructed_amount_currency" IS 'Currency of the original instructed amount';

COMMENT ON TABLE "consumer_banking"."transaction_bank_transaction_codes" IS 'Stores standardized bank transaction codes that categorize transactions with detailed hierarchical classification';

COMMENT ON COLUMN "consumer_banking"."transaction_bank_transaction_codes"."consumer_banking_transaction_bank_transaction_code_id" IS 'Auto-incrementing identifier for each transaction code record';

COMMENT ON COLUMN "consumer_banking"."transaction_bank_transaction_codes"."consumer_banking_transaction_id" IS 'References the transaction this code belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_bank_transaction_codes"."code" IS 'Detailed bank-specific transaction classification code';

COMMENT ON TABLE "consumer_banking"."proprietary_transaction_codes" IS 'Stores non-standard proprietary codes for transaction categorization';

COMMENT ON COLUMN "consumer_banking"."proprietary_transaction_codes"."consumer_banking_proprietary_transaction_code_id" IS 'Auto-incrementing identifier for each proprietary code record';

COMMENT ON COLUMN "consumer_banking"."proprietary_transaction_codes"."consumer_banking_transaction_id" IS 'References the transaction this code belongs to';

COMMENT ON COLUMN "consumer_banking"."proprietary_transaction_codes"."code" IS 'Custom transaction code defined by the issuer';

COMMENT ON COLUMN "consumer_banking"."proprietary_transaction_codes"."issuer" IS 'Organization that defined the proprietary code';

COMMENT ON TABLE "consumer_banking"."transaction_balances" IS 'Stores account balance information at the time of each transaction';

COMMENT ON COLUMN "consumer_banking"."transaction_balances"."consumer_banking_transaction_balance_id" IS 'Auto-incrementing identifier for each transaction balance record';

COMMENT ON COLUMN "consumer_banking"."transaction_balances"."consumer_banking_transaction_id" IS 'References the transaction this balance belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_balances"."credit_debit_indicator" IS 'Indicates if balance is credit or debit';

COMMENT ON COLUMN "consumer_banking"."transaction_balances"."type" IS 'Type of balance (e.g., available, booked)';

COMMENT ON COLUMN "consumer_banking"."transaction_balances"."amount" IS 'Balance amount after the transaction';

COMMENT ON COLUMN "consumer_banking"."transaction_balances"."currency" IS 'Currency code for the balance amount';

COMMENT ON TABLE "consumer_banking"."transaction_merchant_details" IS 'Stores information about merchants involved in transactions';

COMMENT ON COLUMN "consumer_banking"."transaction_merchant_details"."consumer_banking_transaction_merchant_detail_id" IS 'Auto-incrementing identifier for each merchant detail record';

COMMENT ON COLUMN "consumer_banking"."transaction_merchant_details"."consumer_banking_transaction_id" IS 'References the transaction this merchant detail belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_merchant_details"."merchant_name" IS 'Name of the merchant involved in the transaction';

COMMENT ON COLUMN "consumer_banking"."transaction_merchant_details"."merchant_category_code" IS 'Standard code identifying the merchant''s business category';

COMMENT ON TABLE "consumer_banking"."transaction_creditor_agents" IS 'Stores information about financial institutions receiving funds in transactions';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_agents"."consumer_banking_transaction_creditor_agent_id" IS 'Auto-incrementing identifier for each creditor agent record';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_agents"."consumer_banking_transaction_id" IS 'References the transaction this creditor agent belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_agents"."scheme_name" IS 'Identifier scheme for the receiving institution (e.g., BIC)';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_agents"."identification" IS 'Identifier of the receiving financial institution';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_agents"."name" IS 'Name of the receiving financial institution';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_agents"."lei" IS 'Legal Entity Identifier of the receiving institution';

COMMENT ON TABLE "consumer_banking"."transaction_creditor_accounts" IS 'Stores information about accounts receiving funds in transactions';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_accounts"."consumer_banking_transaction_creditor_account_id" IS 'Auto-incrementing identifier for each creditor account record';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_accounts"."consumer_banking_transaction_id" IS 'References the transaction this creditor account belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_accounts"."scheme_name" IS 'Account identifier scheme (e.g., IBAN, BBAN)';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_accounts"."identification" IS 'Account identifier receiving the funds';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_accounts"."name" IS 'Name associated with the receiving account';

COMMENT ON COLUMN "consumer_banking"."transaction_creditor_accounts"."secondary_identification" IS 'Additional identification for the receiving account';

COMMENT ON TABLE "consumer_banking"."transaction_debtor_agents" IS 'Stores information about financial institutions sending funds in transactions';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_agents"."consumer_banking_transaction_debtor_agent_id" IS 'Auto-incrementing identifier for each debtor agent record';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_agents"."consumer_banking_transaction_id" IS 'References the transaction this debtor agent belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_agents"."scheme_name" IS 'Identifier scheme for the sending institution (e.g., BIC)';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_agents"."identification" IS 'Identifier of the sending financial institution';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_agents"."name" IS 'Name of the sending financial institution';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_agents"."lei" IS 'Legal Entity Identifier of the sending institution';

COMMENT ON TABLE "consumer_banking"."transaction_debtor_accounts" IS 'Stores information about accounts sending funds in transactions';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_accounts"."consumer_banking_transaction_debtor_account_id" IS 'Auto-incrementing identifier for each debtor account record';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_accounts"."consumer_banking_transaction_id" IS 'References the transaction this debtor account belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_accounts"."scheme_name" IS 'Account identifier scheme (e.g., IBAN, BBAN)';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_accounts"."identification" IS 'Account identifier sending the funds';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_accounts"."name" IS 'Name associated with the sending account';

COMMENT ON COLUMN "consumer_banking"."transaction_debtor_accounts"."secondary_identification" IS 'Additional identification for the sending account';

COMMENT ON TABLE "consumer_banking"."transaction_card_instruments" IS 'Stores information about payment cards used in transactions';

COMMENT ON COLUMN "consumer_banking"."transaction_card_instruments"."consumer_banking_transaction_card_instrument_id" IS 'Auto-incrementing identifier for each card instrument record';

COMMENT ON COLUMN "consumer_banking"."transaction_card_instruments"."consumer_banking_transaction_id" IS 'References the transaction this card instrument belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_card_instruments"."card_scheme_name" IS 'Card network (e.g., Visa, Mastercard, Amex)';

COMMENT ON COLUMN "consumer_banking"."transaction_card_instruments"."authorisation_type" IS 'Type of authorization (e.g., PIN, signature, contactless)';

COMMENT ON COLUMN "consumer_banking"."transaction_card_instruments"."name" IS 'Name of the cardholder as printed on the card';

COMMENT ON COLUMN "consumer_banking"."transaction_card_instruments"."identification" IS 'Masked card number or other identifier';

COMMENT ON TABLE "consumer_banking"."transaction_ultimate_creditors" IS 'Stores information about the final recipient of funds in a transaction chain';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_creditors"."consumer_banking_transaction_ultimate_creditor_id" IS 'Auto-incrementing identifier for each ultimate creditor record';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_creditors"."consumer_banking_transaction_id" IS 'References the transaction this ultimate creditor belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_creditors"."name" IS 'Name of the final beneficiary/recipient of the funds';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_creditors"."identification" IS 'Identification code for the ultimate creditor';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_creditors"."lei" IS 'Legal Entity Identifier if the ultimate creditor is an organization';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_creditors"."scheme_name" IS 'Identification scheme for the creditor''s identifier';

COMMENT ON TABLE "consumer_banking"."transaction_ultimate_debtors" IS 'Stores information about the original party that initiated the payment in a transaction chain';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_debtors"."consumer_banking_transaction_ultimate_debtor_id" IS 'Auto-incrementing identifier for each ultimate debtor record';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_debtors"."consumer_banking_transaction_id" IS 'References the transaction this ultimate debtor belongs to';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_debtors"."name" IS 'Name of the original party initiating the payment';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_debtors"."identification" IS 'Identification code for the ultimate debtor';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_debtors"."lei" IS 'Legal Entity Identifier if the ultimate debtor is an organization';

COMMENT ON COLUMN "consumer_banking"."transaction_ultimate_debtors"."scheme_name" IS 'Identification scheme for the debtor''s identifier';

COMMENT ON TABLE "consumer_banking"."account_statement_preferences" IS 'Stores customer preferences for account statements';

COMMENT ON COLUMN "consumer_banking"."account_statement_preferences"."consumer_banking_statement_id" IS 'Fake relationship, to influence data generator and make statements be created before this record.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."consumer_banking_interaction_id" IS 'A unique identifier for each interaction.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."customer_id" IS 'The ID of the customer involved in the interaction.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."account_id" IS 'The ID of the specific account related to the interaction. This can be NULL if the interaction isn''t tied to a specific account (e.g., a general inquiry).';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."enterprise_associate_id" IS 'The ID of the bank employee who handled the interaction. This can be NULL if it was an automated interaction.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."interaction_type" IS 'The type of interaction (e.g., "phone call," "email," "chat," "in-person," "online form," "ATM interaction").';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."interaction_date_time" IS 'The date and time of the interaction.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."channel" IS 'The channel through which the interaction occurred (e.g., "phone," "email," "web," "branch," "mobile app").';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."subject" IS 'A brief subject or title of the interaction.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."description" IS 'A detailed description of the interaction.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."resolution" IS 'Description of how the interaction was resolved.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."status" IS 'The status of the interaction (e.g., "open," "resolved," "pending").';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."priority" IS 'The priority of the interaction (e.g., "high," "medium," "low").';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."related_transaction_id" IS 'If the interaction relates to a specific transaction, this can hold that transaction ID.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."created_at" IS 'When the interaction record was created.';

COMMENT ON COLUMN "consumer_banking"."customer_interactions"."updated_at" IS 'When the interaction record was last updated.';

COMMENT ON TABLE "mortgage_services"."application_borrowers" IS 'Junction table linking mortgage applications to borrowers, supporting multiple borrowers per application and tracking their roles and relationships';

COMMENT ON COLUMN "mortgage_services"."application_borrowers"."mortgage_services_application_borrower_id" IS 'Auto-incrementing identifier for each application-borrower relationship';

COMMENT ON COLUMN "mortgage_services"."application_borrowers"."mortgage_services_application_id" IS 'References the mortgage application';

COMMENT ON COLUMN "mortgage_services"."application_borrowers"."mortgage_services_borrower_id" IS 'References the borrower associated with this application';

COMMENT ON COLUMN "mortgage_services"."application_borrowers"."borrower_type" IS 'Role of this borrower (Primary, Co-Borrower, etc.)';

COMMENT ON COLUMN "mortgage_services"."application_borrowers"."relationship_to_primary" IS 'Relationship of co-borrower to primary borrower';

COMMENT ON COLUMN "mortgage_services"."application_borrowers"."contribution_percentage" IS 'Percentage of financial contribution to the loan';

COMMENT ON TABLE "mortgage_services"."borrowers" IS 'Stores mortgage-specific information about borrowers, note additional personal information stored in the enterprise parties table';

COMMENT ON COLUMN "mortgage_services"."borrowers"."mortgage_services_borrower_id" IS 'Unique identifier for each borrower';

COMMENT ON COLUMN "mortgage_services"."borrowers"."enterprise_party_id" IS 'Reference to enterprise party record - the source of truth for personal information';

COMMENT ON COLUMN "mortgage_services"."borrowers"."years_in_school" IS 'Total years of education';

COMMENT ON COLUMN "mortgage_services"."borrowers"."dependent_count" IS 'Number of dependents claimed by borrower';

COMMENT ON COLUMN "mortgage_services"."borrowers"."current_address_id" IS 'References borrower''s current address';

COMMENT ON COLUMN "mortgage_services"."borrowers"."mailing_address_id" IS 'References borrower''s mailing address if different';

COMMENT ON COLUMN "mortgage_services"."borrowers"."previous_address_id" IS 'References borrower''s previous address if relevant';

COMMENT ON TABLE "mortgage_services"."borrower_employments" IS 'Tracks employment history and income sources for mortgage borrowers';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."mortgage_services_employment_id" IS 'Auto-incrementing identifier for each employment record';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."mortgage_services_borrower_id" IS 'References the borrower this employment belongs to';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."employer_name" IS 'Name of the employer';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."position" IS 'Job title or position';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."phone" IS 'Employer''s phone number';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."employment_type" IS 'Type of employment arrangement';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."start_date" IS 'When employment began';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."end_date" IS 'When employment ended, if applicable';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."is_current" IS 'Indicates if this is the borrower''s current job';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."years_in_profession" IS 'Total years in this profession, even at different employers';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."monthly_income" IS 'Gross monthly income from this employment';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."verification_status" IS 'Status of income verification process';

COMMENT ON COLUMN "mortgage_services"."borrower_employments"."verification_date" IS 'When the income was verified';

COMMENT ON TABLE "mortgage_services"."borrower_incomes" IS 'Tracks various income sources for mortgage borrowers beyond employment';

COMMENT ON COLUMN "mortgage_services"."borrower_incomes"."mortgage_services_income_id" IS 'Auto-incrementing identifier for each income record';

COMMENT ON COLUMN "mortgage_services"."borrower_incomes"."mortgage_services_borrower_id" IS 'References the borrower this income belongs to';

COMMENT ON COLUMN "mortgage_services"."borrower_incomes"."income_type" IS 'Source or type of income';

COMMENT ON COLUMN "mortgage_services"."borrower_incomes"."amount" IS 'Income amount';

COMMENT ON COLUMN "mortgage_services"."borrower_incomes"."frequency" IS 'How often income is received';

COMMENT ON COLUMN "mortgage_services"."borrower_incomes"."verification_status" IS 'Status of income verification process';

COMMENT ON COLUMN "mortgage_services"."borrower_incomes"."verification_date" IS 'When the income was verified';

COMMENT ON TABLE "mortgage_services"."borrower_assets" IS 'Tracks assets owned by borrowers that may be relevant to mortgage qualification';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."mortgage_services_asset_id" IS 'Auto-incrementing identifier for each asset record';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."mortgage_services_borrower_id" IS 'References the borrower this asset belongs to';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."asset_type" IS 'Type of asset (e.g., bank account, property)';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."institution_name" IS 'Financial institution holding the asset';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."account_number" IS 'Account number for financial assets';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."current_value" IS 'Current estimated value of the asset';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."verification_status" IS 'Status of asset verification process';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."verification_date" IS 'When the asset was verified';

COMMENT ON COLUMN "mortgage_services"."borrower_assets"."property_address" IS 'Full text address for real estate assets';

COMMENT ON TABLE "mortgage_services"."borrower_liabilities" IS 'Tracks debts and financial obligations of mortgage borrowers';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."mortgage_services_liability_id" IS 'Auto-incrementing identifier for each liability record';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."mortgage_services_borrower_id" IS 'References the borrower this liability belongs to';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."liability_type" IS 'Type of debt or obligation';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."creditor_name" IS 'Name of creditor';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."account_number" IS 'Account number for the liability';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."monthly_payment" IS 'Regular monthly payment amount';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."current_balance" IS 'Current outstanding balance';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."original_amount" IS 'Original amount of the liability';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."interest_rate" IS 'Current interest rate on the liability';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."origination_date" IS 'When the liability was originated';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."maturity_date" IS 'When the liability is scheduled to be fully paid';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."verification_status" IS 'Status of liability verification process';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."verification_date" IS 'When the liability was verified';

COMMENT ON COLUMN "mortgage_services"."borrower_liabilities"."will_be_paid_off" IS 'Whether this liability will be paid off with the mortgage proceeds';

COMMENT ON TABLE "mortgage_services"."properties" IS 'Stores information about properties being purchased or refinanced';

COMMENT ON COLUMN "mortgage_services"."properties"."mortgage_services_property_id" IS 'Auto-incrementing identifier for each property record';

COMMENT ON COLUMN "mortgage_services"."properties"."mortgage_services_application_id" IS 'References the mortgage application this property is associated with';

COMMENT ON COLUMN "mortgage_services"."properties"."address" IS 'References the complete property address';

COMMENT ON COLUMN "mortgage_services"."properties"."property_type" IS 'Type of property';

COMMENT ON COLUMN "mortgage_services"."properties"."occupancy_type" IS 'How the property will be used by the borrower';

COMMENT ON COLUMN "mortgage_services"."properties"."year_built" IS 'Year the property was constructed';

COMMENT ON COLUMN "mortgage_services"."properties"."bedrooms" IS 'Number of bedrooms';

COMMENT ON COLUMN "mortgage_services"."properties"."bathrooms" IS 'Number of bathrooms (allows for half baths)';

COMMENT ON COLUMN "mortgage_services"."properties"."square_feet" IS 'Total living area in square feet';

COMMENT ON COLUMN "mortgage_services"."properties"."lot_size" IS 'Size of the property lot';

COMMENT ON COLUMN "mortgage_services"."properties"."hoa_dues" IS 'Monthly homeowners association fees if applicable';

COMMENT ON COLUMN "mortgage_services"."properties"."is_new_construction" IS 'Indicates if the property is newly constructed';

COMMENT ON COLUMN "mortgage_services"."properties"."construction_completion_date" IS 'Expected completion date for new construction';

COMMENT ON TABLE "mortgage_services"."applications" IS 'Stores mortgage application details and tracks application status. Note that the primary borrower is accessible through the application_borrowers table, not directly from this table.';

COMMENT ON COLUMN "mortgage_services"."applications"."mortgage_services_application_id" IS 'Unique identifier for each mortgage application';

COMMENT ON COLUMN "mortgage_services"."applications"."mortgage_services_loan_product_id" IS 'References the loan product being applied for';

COMMENT ON COLUMN "mortgage_services"."applications"."application_type" IS 'Type of mortgage application';

COMMENT ON COLUMN "mortgage_services"."applications"."status" IS 'Current status in the application workflow';

COMMENT ON COLUMN "mortgage_services"."applications"."loan_purpose" IS 'Purpose of the loan';

COMMENT ON COLUMN "mortgage_services"."applications"."submission_channel" IS 'Channel through which application was submitted';

COMMENT ON COLUMN "mortgage_services"."applications"."creation_date_time" IS 'When the application was created';

COMMENT ON COLUMN "mortgage_services"."applications"."submission_date_time" IS 'When the application was formally submitted';

COMMENT ON COLUMN "mortgage_services"."applications"."last_updated_date_time" IS 'When the application was last modified';

COMMENT ON COLUMN "mortgage_services"."applications"."requested_loan_amount" IS 'Amount of financing requested';

COMMENT ON COLUMN "mortgage_services"."applications"."requested_loan_term_months" IS 'Requested duration of the loan in months';

COMMENT ON COLUMN "mortgage_services"."applications"."estimated_property_value" IS 'Estimated value of the property';

COMMENT ON COLUMN "mortgage_services"."applications"."estimated_credit_score" IS 'Estimated credit score of primary applicant';

COMMENT ON COLUMN "mortgage_services"."applications"."referral_source" IS 'How the applicant learned about the mortgage product';

COMMENT ON COLUMN "mortgage_services"."applications"."loan_officer_id" IS 'References the loan officer handling the application';

COMMENT ON COLUMN "mortgage_services"."applications"."branch_id" IS 'References the branch processing the application';

COMMENT ON TABLE "mortgage_services"."loans" IS 'Stores final, actual loan details after closing. Now includes reference to enterprise account.';

COMMENT ON COLUMN "mortgage_services"."loans"."mortgage_services_loan_id" IS 'Unique identifier for each loan';

COMMENT ON COLUMN "mortgage_services"."loans"."mortgage_services_application_id" IS 'References the mortgage application this loan is associated with';

COMMENT ON COLUMN "mortgage_services"."loans"."enterprise_account_id" IS 'References the enterprise account for this loan';

COMMENT ON COLUMN "mortgage_services"."loans"."interest_rate" IS 'Final annual percentage rate for the loan';

COMMENT ON COLUMN "mortgage_services"."loans"."loan_term_months" IS 'Final duration of the loan in months';

COMMENT ON COLUMN "mortgage_services"."loans"."loan_amount" IS 'Final principal amount of the loan';

COMMENT ON COLUMN "mortgage_services"."loans"."down_payment" IS 'Final amount paid upfront by the borrower';

COMMENT ON COLUMN "mortgage_services"."loans"."down_payment_percentage" IS 'Final down payment as a percentage of purchase price';

COMMENT ON COLUMN "mortgage_services"."loans"."closing_costs" IS 'Actual fees and costs paid at closing';

COMMENT ON COLUMN "mortgage_services"."loans"."monthly_payment" IS 'Actual monthly payment including principal and interest';

COMMENT ON COLUMN "mortgage_services"."loans"."private_mortgage_insurance" IS 'Whether PMI is required for this loan';

COMMENT ON COLUMN "mortgage_services"."loans"."pmi_rate" IS 'Actual PMI rate applied to this loan';

COMMENT ON COLUMN "mortgage_services"."loans"."escrow_amount" IS 'Actual monthly amount collected for taxes and insurance';

COMMENT ON COLUMN "mortgage_services"."loans"."origination_date" IS 'When the loan was originated';

COMMENT ON COLUMN "mortgage_services"."loans"."first_payment_date" IS 'Due date of the first loan payment';

COMMENT ON COLUMN "mortgage_services"."loans"."maturity_date" IS 'When the loan will be fully paid off';

COMMENT ON TABLE "mortgage_services"."loan_products" IS 'Defines mortgage loan products available to applicants';

COMMENT ON COLUMN "mortgage_services"."loan_products"."mortgage_services_loan_product_id" IS 'Unique identifier for each loan product';

COMMENT ON COLUMN "mortgage_services"."loan_products"."product_name" IS 'Marketing name of the loan product';

COMMENT ON COLUMN "mortgage_services"."loan_products"."product_code" IS 'Internal code identifying the loan product';

COMMENT ON COLUMN "mortgage_services"."loan_products"."loan_type" IS 'Type of loan product';

COMMENT ON COLUMN "mortgage_services"."loan_products"."interest_rate_type" IS 'Type of interest rate structure';

COMMENT ON COLUMN "mortgage_services"."loan_products"."description" IS 'Detailed description of the loan product and its features';

COMMENT ON COLUMN "mortgage_services"."loan_products"."base_interest_rate" IS 'Starting interest rate for this product';

COMMENT ON COLUMN "mortgage_services"."loan_products"."min_term_months" IS 'Minimum loan duration in months';

COMMENT ON COLUMN "mortgage_services"."loan_products"."max_term_months" IS 'Maximum loan duration in months';

COMMENT ON COLUMN "mortgage_services"."loan_products"."min_loan_amount" IS 'Minimum principal amount for this product';

COMMENT ON COLUMN "mortgage_services"."loan_products"."max_loan_amount" IS 'Maximum principal amount for this product';

COMMENT ON COLUMN "mortgage_services"."loan_products"."min_credit_score" IS 'Minimum credit score typically required';

COMMENT ON COLUMN "mortgage_services"."loan_products"."min_down_payment_percentage" IS 'Minimum down payment as percentage of purchase price';

COMMENT ON COLUMN "mortgage_services"."loan_products"."requires_pmi" IS 'Whether private mortgage insurance is required';

COMMENT ON COLUMN "mortgage_services"."loan_products"."is_active" IS 'Whether this product is currently offered';

COMMENT ON COLUMN "mortgage_services"."loan_products"."launch_date" IS 'Date when product was launched';

COMMENT ON COLUMN "mortgage_services"."loan_products"."discontinue_date" IS 'Date when product was discontinued if applicable';

COMMENT ON TABLE "mortgage_services"."loan_rate_locks" IS 'Tracks interest rate locks for mortgage loans';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."mortgage_services_rate_lock_id" IS 'Auto-incrementing identifier for each rate lock';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."mortgage_services_loan_id" IS 'References the loan this rate lock applies to';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."lock_date" IS 'When the interest rate was locked';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."expiration_date" IS 'When the rate lock expires';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."locked_interest_rate" IS 'The interest rate secured by this lock';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."lock_period_days" IS 'Duration of the lock in days';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."status" IS 'Current status of the rate lock';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."lock_fee" IS 'Fee charged for the rate lock, if any';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."extension_date" IS 'Date the lock was extended, if applicable';

COMMENT ON COLUMN "mortgage_services"."loan_rate_locks"."extension_fee" IS 'Fee charged for extending the lock, if any';

COMMENT ON TABLE "mortgage_services"."documents" IS 'Stores and tracks documents submitted for mortgage applications';

COMMENT ON COLUMN "mortgage_services"."documents"."mortgage_services_document_id" IS 'Auto-incrementing identifier for each document';

COMMENT ON COLUMN "mortgage_services"."documents"."mortgage_services_application_id" IS 'References the application this document belongs to';

COMMENT ON COLUMN "mortgage_services"."documents"."document_type" IS 'Category of document (e.g., W2, Tax Return)';

COMMENT ON COLUMN "mortgage_services"."documents"."document_name" IS 'Filename or display name of the document';

COMMENT ON COLUMN "mortgage_services"."documents"."document_path" IS 'Storage location or path to access the document';

COMMENT ON COLUMN "mortgage_services"."documents"."upload_date" IS 'When the document was uploaded';

COMMENT ON COLUMN "mortgage_services"."documents"."status" IS 'Current review status of the document';

COMMENT ON COLUMN "mortgage_services"."documents"."review_date" IS 'When the document was reviewed';

COMMENT ON COLUMN "mortgage_services"."documents"."reviewer_id" IS 'References the staff member who reviewed the document';

COMMENT ON COLUMN "mortgage_services"."documents"."expiration_date" IS 'When the document expires or needs to be updated';

COMMENT ON COLUMN "mortgage_services"."documents"."notes" IS 'Additional information about the document';

COMMENT ON TABLE "mortgage_services"."conditions" IS 'Tracks underwriting conditions that must be cleared for loan approval';

COMMENT ON COLUMN "mortgage_services"."conditions"."mortgage_services_condition_id" IS 'Auto-incrementing identifier for each condition';

COMMENT ON COLUMN "mortgage_services"."conditions"."mortgage_services_application_id" IS 'References the application this condition applies to';

COMMENT ON COLUMN "mortgage_services"."conditions"."condition_type" IS 'When the condition must be satisfied';

COMMENT ON COLUMN "mortgage_services"."conditions"."description" IS 'Detailed explanation of what must be provided or resolved';

COMMENT ON COLUMN "mortgage_services"."conditions"."status" IS 'Current status of the condition';

COMMENT ON COLUMN "mortgage_services"."conditions"."created_date" IS 'When the condition was created';

COMMENT ON COLUMN "mortgage_services"."conditions"."created_by_id" IS 'References the staff member who created the condition';

COMMENT ON COLUMN "mortgage_services"."conditions"."due_date" IS 'Deadline for satisfying the condition';

COMMENT ON COLUMN "mortgage_services"."conditions"."cleared_date" IS 'When the condition was satisfied or waived';

COMMENT ON COLUMN "mortgage_services"."conditions"."cleared_by_id" IS 'References the staff member who cleared the condition';

COMMENT ON TABLE "mortgage_services"."appraisals" IS 'Manages property appraisals for mortgage loans';

COMMENT ON COLUMN "mortgage_services"."appraisals"."mortgage_services_appraisal_id" IS 'Auto-incrementing identifier for each appraisal';

COMMENT ON COLUMN "mortgage_services"."appraisals"."mortgage_services_application_id" IS 'References the application this appraisal is for';

COMMENT ON COLUMN "mortgage_services"."appraisals"."mortgage_services_property_id" IS 'References the property being appraised';

COMMENT ON COLUMN "mortgage_services"."appraisals"."appraisal_type" IS 'Type of appraisal being performed';

COMMENT ON COLUMN "mortgage_services"."appraisals"."ordered_date" IS 'When the appraisal was ordered';

COMMENT ON COLUMN "mortgage_services"."appraisals"."appraiser_name" IS 'Name of the assigned appraiser';

COMMENT ON COLUMN "mortgage_services"."appraisals"."appraisal_company" IS 'Company performing the appraisal';

COMMENT ON COLUMN "mortgage_services"."appraisals"."inspection_date" IS 'When the property was inspected';

COMMENT ON COLUMN "mortgage_services"."appraisals"."completion_date" IS 'When the appraisal was completed';

COMMENT ON COLUMN "mortgage_services"."appraisals"."appraised_value" IS 'Value determined by the appraisal';

COMMENT ON COLUMN "mortgage_services"."appraisals"."status" IS 'Current status of the appraisal process';

COMMENT ON COLUMN "mortgage_services"."appraisals"."appraisal_fee" IS 'Fee charged for the appraisal';

COMMENT ON COLUMN "mortgage_services"."appraisals"."report_path" IS 'Storage location of the appraisal report';

COMMENT ON TABLE "mortgage_services"."credit_reports" IS 'Tracks credit reports pulled for mortgage applications';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."mortgage_services_credit_report_id" IS 'Auto-incrementing identifier for each credit report';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."mortgage_services_application_id" IS 'Reference to applications';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."mortgage_services_borrower_id" IS 'Reference to borrower this credit report is for';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."report_date" IS 'When credit report was pulled';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."expiration_date" IS 'When credit report expires';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."credit_score" IS 'Credit score from the report';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."report_type" IS 'Type of credit report pulled';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."bureau_name" IS 'Credit bureau providing the report';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."report_path" IS 'Path to stored credit report';

COMMENT ON COLUMN "mortgage_services"."credit_reports"."status" IS 'Status of credit report retrieval';

COMMENT ON TABLE "mortgage_services"."closing_disclosures" IS 'Manages closing disclosure documents required by regulations';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."mortgage_services_disclosure_id" IS 'Auto-incrementing identifier for each disclosure';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."mortgage_services_loan_id" IS 'Reference to the loan this disclosure is for';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."disclosure_type" IS 'Type of disclosure document';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."created_date" IS 'When the disclosure was created';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."sent_date" IS 'When the disclosure was sent to borrowers';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."received_date" IS 'When signed disclosure was received back';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."delivery_method" IS 'How disclosure was delivered';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."document_path" IS 'Storage location of the disclosure document';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."loan_amount" IS 'Loan amount shown on disclosure';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."interest_rate" IS 'Interest rate shown on disclosure';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."monthly_payment" IS 'Monthly payment shown on disclosure';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."total_closing_costs" IS 'Total closing costs shown on disclosure';

COMMENT ON COLUMN "mortgage_services"."closing_disclosures"."cash_to_close" IS 'Cash to close shown on disclosure';

COMMENT ON TABLE "mortgage_services"."closing_appointments" IS 'Schedules and tracks mortgage closing appointments';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."mortgage_services_appointment_id" IS 'Auto-incrementing identifier for each appointment';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."mortgage_services_loan_id" IS 'Reference to the loan this closing is for';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."scheduled_date" IS 'When the closing is scheduled';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."location_address_id" IS 'References the address where closing will occur';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."status" IS 'Current status of the closing appointment';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."closing_type" IS 'Type of closing process being used';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."closing_agent" IS 'Name of the closing agent';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."closing_company" IS 'Company handling the closing';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."closing_fee" IS 'Fee charged for closing services';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."actual_closing_date" IS 'When the closing actually occurred';

COMMENT ON COLUMN "mortgage_services"."closing_appointments"."notes" IS 'Additional information about the closing';

COMMENT ON TABLE "mortgage_services"."closed_loans" IS 'Records final details of closed mortgage loans';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."mortgage_services_closed_loan_id" IS 'Auto-incrementing identifier for each closed loan record';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."mortgage_services_loan_id" IS 'References the loan that was closed';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."closing_date" IS 'When loan documents were signed';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."funding_date" IS 'When loan funds were disbursed';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."final_loan_amount" IS 'Final principal amount of the loan';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."final_interest_rate" IS 'Final interest rate of the loan';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."final_monthly_payment" IS 'Final principal and interest payment';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."final_cash_to_close" IS 'Final amount borrower paid at closing';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."disbursement_date" IS 'When funds were disbursed to relevant parties';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."first_payment_date" IS 'When first loan payment is due';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."maturity_date" IS 'When loan is scheduled to be fully paid off';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."recording_date" IS 'When mortgage was recorded with government office';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."settlement_agent" IS 'Name of the settlement agent';

COMMENT ON COLUMN "mortgage_services"."closed_loans"."settlement_company" IS 'Company handling the settlement';

COMMENT ON TABLE "mortgage_services"."servicing_accounts" IS 'Manages ongoing servicing of closed mortgage loans';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."mortgage_services_servicing_account_id" IS 'Unique identifier for each servicing account';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."mortgage_services_loan_id" IS 'References the originated loan';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."status" IS 'Current status of the loan being serviced';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."current_principal_balance" IS 'Current remaining principal balance';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."original_principal_balance" IS 'Original loan amount at closing';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."current_interest_rate" IS 'Current applicable interest rate';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."escrow_balance" IS 'Current balance in escrow account';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."next_payment_due_date" IS 'When next payment is due';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."next_payment_amount" IS 'Amount due for next payment';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."last_payment_date" IS 'When last payment was received';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."last_payment_amount" IS 'Amount of last payment received';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."interest_paid_ytd" IS 'Interest paid year-to-date';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."principal_paid_ytd" IS 'Principal paid year-to-date';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."escrow_paid_ytd" IS 'Escrow paid year-to-date';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."property_tax_due_date" IS 'When next property tax payment is due';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."homeowners_insurance_due_date" IS 'When next insurance payment is due';

COMMENT ON COLUMN "mortgage_services"."servicing_accounts"."servicing_transferred_date" IS 'When servicing was transferred to current servicer';

COMMENT ON TABLE "mortgage_services"."payments" IS 'Tracks mortgage loan payments made by borrowers';

COMMENT ON COLUMN "mortgage_services"."payments"."mortgage_services_payment_id" IS 'Auto-incrementing identifier for each payment';

COMMENT ON COLUMN "mortgage_services"."payments"."mortgage_services_servicing_account_id" IS 'References the servicing account receiving the payment';

COMMENT ON COLUMN "mortgage_services"."payments"."payment_date" IS 'When the payment was made';

COMMENT ON COLUMN "mortgage_services"."payments"."payment_type" IS 'Type of payment (e.g., Regular, Extra Principal, Escrow Only)';

COMMENT ON COLUMN "mortgage_services"."payments"."payment_method" IS 'Method used to make payment (e.g., ACH, Check, Online)';

COMMENT ON COLUMN "mortgage_services"."payments"."payment_amount" IS 'Total amount of the payment';

COMMENT ON COLUMN "mortgage_services"."payments"."principal_amount" IS 'Portion of payment applied to principal';

COMMENT ON COLUMN "mortgage_services"."payments"."interest_amount" IS 'Portion of payment applied to interest';

COMMENT ON COLUMN "mortgage_services"."payments"."escrow_amount" IS 'Portion of payment applied to escrow';

COMMENT ON COLUMN "mortgage_services"."payments"."late_fee_amount" IS 'Portion of payment applied to late fees';

COMMENT ON COLUMN "mortgage_services"."payments"."other_fee_amount" IS 'Portion of payment applied to other fees';

COMMENT ON COLUMN "mortgage_services"."payments"."transaction_id" IS 'Financial transaction identifier';

COMMENT ON COLUMN "mortgage_services"."payments"."confirmation_number" IS 'Confirmation number provided to customer';

COMMENT ON COLUMN "mortgage_services"."payments"."status" IS 'Current status of the payment (e.g., Pending, Completed)';

COMMENT ON TABLE "mortgage_services"."escrow_disbursements" IS 'Tracks payments made from escrow accounts for taxes, insurance, etc.';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."mortgage_services_disbursement_id" IS 'Auto-incrementing identifier for each disbursement';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."mortgage_services_servicing_account_id" IS 'References the servicing account for this disbursement';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."disbursement_date" IS 'When the disbursement was made';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."disbursement_type" IS 'Type of disbursement (e.g., Property Tax, Insurance, PMI)';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."amount" IS 'Amount of the disbursement';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."payee_name" IS 'Entity receiving the disbursement';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."payee_account_number" IS 'Account number for electronic payments';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."check_number" IS 'Check number for paper disbursements';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."status" IS 'Current status of the disbursement';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."due_date" IS 'When the payment was due';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."coverage_start_date" IS 'Start of coverage period (for insurance payments)';

COMMENT ON COLUMN "mortgage_services"."escrow_disbursements"."coverage_end_date" IS 'End of coverage period (for insurance payments)';

COMMENT ON TABLE "mortgage_services"."escrow_analyses" IS 'Records periodic analyses of escrow accounts to determine payment adjustments';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."mortgage_services_analysis_id" IS 'Auto-incrementing identifier for each analysis';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."mortgage_services_servicing_account_id" IS 'References the servicing account being analyzed';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."analysis_date" IS 'When the analysis was performed';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."effective_date" IS 'When the analysis results take effect';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."previous_monthly_escrow" IS 'Previous monthly escrow payment amount';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."new_monthly_escrow" IS 'New monthly escrow payment amount';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."escrow_shortage" IS 'Amount by which the escrow account is short';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."escrow_surplus" IS 'Amount by which the escrow account exceeds requirements';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."shortage_spread_months" IS 'Number of months to spread shortage payment';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."surplus_refund_amount" IS 'Amount of surplus to be refunded';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."status" IS 'Current status of the analysis';

COMMENT ON COLUMN "mortgage_services"."escrow_analyses"."customer_notification_date" IS 'When the customer was notified of the analysis results';

COMMENT ON TABLE "mortgage_services"."insurance_policies" IS 'Tracks insurance policies protecting mortgaged properties';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."mortgage_services_policy_id" IS 'Auto-incrementing identifier for each policy';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."mortgage_services_servicing_account_id" IS 'References the servicing account this policy protects';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."insurance_type" IS 'Type of insurance coverage';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."carrier_name" IS 'Insurance company providing coverage';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."policy_number" IS 'Insurance policy identifier';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."coverage_amount" IS 'Amount of insurance coverage';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."annual_premium" IS 'Annual cost of the insurance policy';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."effective_date" IS 'Start date of policy coverage';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."expiration_date" IS 'End date of policy coverage';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."paid_through_escrow" IS 'Whether premium is paid from escrow account';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."agent_name" IS 'Insurance agent''s name';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."agent_phone" IS 'Insurance agent''s contact number';

COMMENT ON COLUMN "mortgage_services"."insurance_policies"."status" IS 'Current status of the policy';

COMMENT ON TABLE "mortgage_services"."loan_modifications" IS 'Tracks modifications made to existing loan accounts, such as changes to interest rates, terms, or principal balance.';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."mortgage_services_modification_id" IS 'Unique identifier for loan modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."modification_type" IS 'Type of loan modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."request_date" IS 'Date modification was requested';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."approval_date" IS 'Date modification was approved';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."effective_date" IS 'Date modification takes effect';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."original_rate" IS 'Interest rate before modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."new_rate" IS 'Interest rate after modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."original_term_months" IS 'Loan term before modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."new_term_months" IS 'Loan term after modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."original_principal_balance" IS 'Principal balance before modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."new_principal_balance" IS 'Principal balance after modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."capitalized_amount" IS 'Amount of interest or fees capitalized';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."status" IS 'Current status of the modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."hardship_reason" IS 'Customer''s reason for hardship';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."approved_by_id" IS 'User who approved modification';

COMMENT ON COLUMN "mortgage_services"."loan_modifications"."document_path" IS 'Path to modification agreement document';

COMMENT ON TABLE "mortgage_services"."customer_communications" IS 'Tracks all communications with customers throughout application and servicing';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."mortgage_services_communication_id" IS 'Unique identifier for each communication record';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."mortgage_services_servicing_account_id" IS 'References the servicing account if communication is about servicing';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."mortgage_services_application_id" IS 'References the application if communication is about application';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."communication_date" IS 'When the communication occurred';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."communication_type" IS 'Method of communication';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."direction" IS 'Whether communication was incoming or outgoing';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."subject" IS 'Subject or topic of communication';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."content" IS 'Content of the communication';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."sender" IS 'Person or system that sent the communication';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."recipient" IS 'Person or entity that received the communication';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."template_id" IS 'Template used for the communication if applicable';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."status" IS 'Delivery status of the communication';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."document_path" IS 'Storage location for communication document if applicable';

COMMENT ON COLUMN "mortgage_services"."customer_communications"."related_to" IS 'Purpose or context of the communication';

COMMENT ON TABLE "mortgage_services"."hmda_records" IS 'Stores data required for Home Mortgage Disclosure Act (HMDA) regulatory reporting';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."mortgage_services_hmda_record_id" IS 'Auto-incrementing identifier for each HMDA record';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."mortgage_services_application_id" IS 'References the associated mortgage application';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."mortgage_services_loan_id" IS 'References the associated loan if originated';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."reporting_year" IS 'Calendar year for HMDA reporting';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."lei" IS 'Legal Entity Identifier of the reporting institution';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."mortgage_services_loan_product_id" IS 'Type of mortgage loan product';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."loan_purpose" IS 'Code indicating loan purpose';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."preapproval" IS 'Code indicating if preapproval was requested';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."construction_method" IS 'Code indicating construction method';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."occupancy_type" IS 'Code indicating intended property use';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."loan_amount" IS 'Amount of the loan or application';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."action_taken" IS 'Code indicating final disposition';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."action_taken_date" IS 'Date of final action';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."state" IS 'Two-letter state code for property location';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."county" IS 'County code for property location';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."census_tract" IS 'Census tract for property location';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."rate_spread" IS 'Difference between APR and average prime offer rate';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."hoepa_status" IS 'Code indicating if loan is subject to HOEPA';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."lien_status" IS 'Code indicating lien position';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."credit_score_applicant" IS 'Credit score of primary applicant';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."credit_score_co_applicant" IS 'Credit score of co-applicant if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."credit_score_model" IS 'Code indicating credit scoring model used';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."denial_reason1" IS 'Primary reason for denial if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."denial_reason2" IS 'Secondary reason for denial if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."denial_reason3" IS 'Additional reason for denial if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."denial_reason4" IS 'Additional reason for denial if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."total_loan_costs" IS 'Total loan costs as disclosed';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."total_points_and_fees" IS 'Total points and fees charged';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."origination_charges" IS 'Total origination charges';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."discount_points" IS 'Discount points paid by borrower';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."lender_credits" IS 'Credits provided by lender';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."loan_term" IS 'Term of the loan in months';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."intro_rate_period" IS 'Months until first rate adjustment for ARMs';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."balloon_payment" IS 'Whether loan has balloon payment feature';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."interest_only_payment" IS 'Whether loan has interest-only payments';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."negative_amortization" IS 'Whether loan allows negative amortization';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."other_non_amortizing_features" IS 'Whether loan has other non-amortizing features';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."property_value" IS 'Value of the property securing the loan';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."manufactured_home_secured_property_type" IS 'Code for manufactured home property type';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."manufactured_home_land_property_interest" IS 'Code for land ownership with manufactured home';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."total_units" IS 'Number of dwelling units in the property';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."multifamily_affordable_units" IS 'Number of income-restricted units in multifamily property';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."submission_of_application" IS 'How application was submitted';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."initially_payable_to_institution" IS 'Whether loan was initially payable to reporting institution';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."aus1" IS 'Primary automated underwriting system used';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."aus2" IS 'Secondary automated underwriting system used if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."aus3" IS 'Additional automated underwriting system if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."aus4" IS 'Additional automated underwriting system if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."aus5" IS 'Additional automated underwriting system if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."reverse_mortgage" IS 'Whether loan is a reverse mortgage';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."open_end_line_of_credit" IS 'Whether loan is an open-end line of credit';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."business_or_commercial_purpose" IS 'Whether loan is for business purpose';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."submission_status" IS 'Status of HMDA submission for this record';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."last_submission_date" IS 'When record was last submitted to regulators';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."last_modified_date" IS 'When record was last modified';

COMMENT ON COLUMN "mortgage_services"."hmda_records"."edit_status" IS 'Status of edit checks for this record';

COMMENT ON TABLE "mortgage_services"."hmda_applicant_demographics" IS 'Stores demographic information about applicants for HMDA reporting';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."mortgage_services_applicant_demographics_id" IS 'Auto-incrementing identifier for each demographics record';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."mortgage_services_hmda_record_id" IS 'References the associated HMDA record';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."applicant_type" IS 'Indicates if record is for primary applicant or co-applicant';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."ethnicity_1" IS 'Primary ethnicity selection';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."ethnicity_2" IS 'Secondary ethnicity selection if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."ethnicity_3" IS 'Additional ethnicity selection if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."ethnicity_4" IS 'Additional ethnicity selection if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."ethnicity_5" IS 'Additional ethnicity selection if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."ethnicity_free_form" IS 'Free-form text description of ethnicity';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."ethnicity_observed" IS 'How ethnicity was determined if not provided by applicant';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_1" IS 'Primary race selection';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_2" IS 'Secondary race selection if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_3" IS 'Additional race selection if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_4" IS 'Additional race selection if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_5" IS 'Additional race selection if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_detail_1" IS 'Race detail for race_1 if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_detail_2" IS 'Race detail for race_2 if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_detail_3" IS 'Race detail for race_3 if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_detail_4" IS 'Race detail for race_4 if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_detail_5" IS 'Race detail for race_5 if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_free_form" IS 'Free-form text description of race';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."race_observed" IS 'How race was determined if not provided by applicant';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."sex" IS 'Applicant''s reported sex';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."sex_observed" IS 'How sex was determined if not provided by applicant';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."age" IS 'Applicant''s age in years';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."age_group" IS 'Applicant''s age group for reporting';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."income" IS 'Applicant''s annual income in thousands of dollars';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."debt_to_income_ratio" IS 'Applicant''s debt-to-income ratio percentage';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."applicant_present" IS 'Whether applicant was present during application';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."created_date" IS 'When the demographic record was created';

COMMENT ON COLUMN "mortgage_services"."hmda_applicant_demographics"."modified_date" IS 'When the demographic record was last modified';

COMMENT ON TABLE "mortgage_services"."hmda_edits" IS 'Tracks validation issues with HMDA data and their resolution';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."mortgage_services_edit_id" IS 'Auto-incrementing identifier for each edit finding';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."mortgage_services_hmda_record_id" IS 'References the HMDA record with the edit issue';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."edit_code" IS 'Standardized code identifying the specific edit rule';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."edit_type" IS 'Category of edit (SYNTACTICAL, VALIDITY, QUALITY, MACRO)';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."edit_description" IS 'Description of the edit issue';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."status" IS 'Current status of the edit (OPEN, VERIFIED, CORRECTED)';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."created_date" IS 'When the edit was first identified';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."resolved_date" IS 'When the edit was resolved if applicable';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."resolved_by_id" IS 'User who resolved the edit';

COMMENT ON COLUMN "mortgage_services"."hmda_edits"."resolution_notes" IS 'Notes explaining how the edit was resolved';

COMMENT ON TABLE "mortgage_services"."hmda_submissions" IS 'Tracks submissions of HMDA data to regulatory agencies';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."mortgage_services_submission_id" IS 'Auto-incrementing identifier for each submission';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."reporting_year" IS 'Calendar year for this submission';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."reporting_period" IS 'Reporting period (ANNUAL, QUARTERLY_Q1, etc.)';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."institution_lei" IS 'Legal Entity Identifier of the reporting institution';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."submission_date" IS 'When the submission was made';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."submission_status" IS 'Current status of the submission process';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."file_name" IS 'Name of the submitted file';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."file_size" IS 'Size of the submitted file in bytes';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."record_count" IS 'Number of records in the submission';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."error_count" IS 'Number of errors found in the submission';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."warning_count" IS 'Number of warnings found in the submission';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."submitted_by_id" IS 'User who made the submission';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."submission_notes" IS 'Additional notes about the submission';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."confirmation_number" IS 'Confirmation number provided by the regulatory agency';

COMMENT ON COLUMN "mortgage_services"."hmda_submissions"."completion_date" IS 'When the submission was accepted as complete';

COMMENT ON TABLE "consumer_lending"."loan_applications" IS 'Stores consumer lending applications for non-mortgage loans';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."consumer_lending_application_id" IS 'Unique identifier for the loan application';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."customer_id" IS 'Reference to enterprise.accounts';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."application_type" IS 'Personal, Auto, Student, Home Improvement, etc.';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."status" IS 'Draft, Submitted, In Review, Approved, Denied, Cancelled';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."creation_date_time" IS 'When application was initially created';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."submission_date_time" IS 'When application was submitted by customer';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."last_updated_date_time" IS 'Last modification timestamp';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."requested_amount" IS 'Amount requested by applicant';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."requested_term_months" IS 'Loan term in months requested by applicant';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."loan_purpose" IS 'Purpose for the loan';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."estimated_credit_score" IS 'Estimated or self-reported credit score';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."application_channel" IS 'Online, Mobile, Branch, Phone';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."referral_source" IS 'Marketing channel or referral source';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."decision_date_time" IS 'When final decision was made';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."decision_reason" IS 'Primary reason for approval/denial';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."officer_id" IS 'Loan officer assigned to application';

COMMENT ON COLUMN "consumer_lending"."loan_applications"."branch_id" IS 'Branch where application was processed';

COMMENT ON TABLE "consumer_lending"."application_applicants" IS 'Links loan applications to individual applicants, allowing for multiple applicants per application.';

COMMENT ON COLUMN "consumer_lending"."application_applicants"."consumer_lending_application_applicant_id" IS 'Unique identifier for application-applicant relationship';

COMMENT ON COLUMN "consumer_lending"."application_applicants"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."application_applicants"."consumer_lending_applicant_id" IS 'Reference to applicant';

COMMENT ON COLUMN "consumer_lending"."application_applicants"."applicant_type" IS 'Primary, Co-Applicant, Guarantor';

COMMENT ON COLUMN "consumer_lending"."application_applicants"."relationship_to_primary" IS 'Spouse, Relative, Friend, etc.';

COMMENT ON COLUMN "consumer_lending"."application_applicants"."contribution_percentage" IS 'Percentage of loan responsibility';

COMMENT ON TABLE "consumer_lending"."applicants" IS 'Stores personal and contact information for loan applicants.';

COMMENT ON COLUMN "consumer_lending"."applicants"."consumer_lending_applicant_id" IS 'Unique identifier for applicant, may link to parties table';

COMMENT ON COLUMN "consumer_lending"."applicants"."first_name" IS 'Applicant''s legal first name';

COMMENT ON COLUMN "consumer_lending"."applicants"."middle_name" IS 'Applicant''s middle name';

COMMENT ON COLUMN "consumer_lending"."applicants"."last_name" IS 'Applicant''s legal last name';

COMMENT ON COLUMN "consumer_lending"."applicants"."date_of_birth" IS 'Applicant''s date of birth';

COMMENT ON COLUMN "consumer_lending"."applicants"."ssn" IS 'Social Security Number, stored encrypted';

COMMENT ON COLUMN "consumer_lending"."applicants"."marital_status" IS 'Married, Single, Divorced, etc.';

COMMENT ON COLUMN "consumer_lending"."applicants"."email" IS 'Primary email address';

COMMENT ON COLUMN "consumer_lending"."applicants"."phone" IS 'Primary phone number';

COMMENT ON COLUMN "consumer_lending"."applicants"."mobile_phone" IS 'Mobile phone number if different from primary';

COMMENT ON COLUMN "consumer_lending"."applicants"."citizenship_status" IS 'US Citizen, Permanent Resident, etc.';

COMMENT ON COLUMN "consumer_lending"."applicants"."years_at_current_address" IS 'Years at current residence';

COMMENT ON COLUMN "consumer_lending"."applicants"."housing_status" IS 'Current housing situation';

COMMENT ON COLUMN "consumer_lending"."applicants"."monthly_housing_expense" IS 'Monthly housing payment amount';

COMMENT ON COLUMN "consumer_lending"."applicants"."current_address_id" IS 'Reference to enterprise.addresses';

COMMENT ON COLUMN "consumer_lending"."applicants"."mailing_address_id" IS 'Reference to enterprise.addresses if different from current';

COMMENT ON COLUMN "consumer_lending"."applicants"."previous_address_id" IS 'Reference to enterprise.addresses for previous residence';

COMMENT ON TABLE "consumer_lending"."applicant_employments" IS 'Stores employment history and income details for loan applicants.';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."consumer_lending_employment_id" IS 'Unique identifier for employment record';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."consumer_lending_applicant_id" IS 'Reference to applicant';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."employer_name" IS 'Name of employer';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."position" IS 'Job title or position';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."enterprise_address_id" IS 'Reference to enterprise.addresses for employer location';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."phone" IS 'Employer phone number';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."employment_type" IS 'Full-time, Part-time, Self-employed';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."start_date" IS 'Employment start date';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."end_date" IS 'Employment end date if applicable';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."is_current" IS 'Indicates if this is current employer';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."years_in_profession" IS 'Total years in this profession/industry';

COMMENT ON COLUMN "consumer_lending"."applicant_employments"."monthly_income" IS 'Gross monthly income';

COMMENT ON TABLE "consumer_lending"."applicant_incomes" IS 'Tracks various income sources for loan applicants, including employment and other income types.';

COMMENT ON COLUMN "consumer_lending"."applicant_incomes"."consumer_lending_income_id" IS 'Unique identifier for income record';

COMMENT ON COLUMN "consumer_lending"."applicant_incomes"."consumer_lending_applicant_id" IS 'Reference to applicant';

COMMENT ON COLUMN "consumer_lending"."applicant_incomes"."income_type" IS 'Type of income source';

COMMENT ON COLUMN "consumer_lending"."applicant_incomes"."amount" IS 'Income amount';

COMMENT ON COLUMN "consumer_lending"."applicant_incomes"."frequency" IS 'Monthly, Annual, etc.';

COMMENT ON COLUMN "consumer_lending"."applicant_incomes"."verification_status" IS 'Self-reported, Verified, Failed';

COMMENT ON COLUMN "consumer_lending"."applicant_incomes"."verification_date" IS 'Date income was verified';

COMMENT ON TABLE "consumer_lending"."applicant_assets" IS 'Records assets owned by loan applicants, including financial accounts and property.';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."consumer_lending_asset_id" IS 'Unique identifier for asset record';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."consumer_lending_applicant_id" IS 'Reference to applicant';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."asset_type" IS 'Type of asset';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."institution_name" IS 'Financial institution holding the asset';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."account_number" IS 'Account number, stored encrypted';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."current_value" IS 'Current market value of asset';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."verification_status" IS 'Self-reported, Verified, Failed';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."verification_date" IS 'Date asset was verified';

COMMENT ON COLUMN "consumer_lending"."applicant_assets"."property_address_id" IS 'Reference to enterprise.addresses if asset is property';

COMMENT ON TABLE "consumer_lending"."applicant_liabilities" IS 'Tracks liabilities and debt obligations of loan applicants.';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."consumer_lending_liability_id" IS 'Unique identifier for liability record';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."consumer_lending_applicant_id" IS 'Reference to applicant';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."liability_type" IS 'Type of liability';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."creditor_name" IS 'Name of creditor';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."account_number" IS 'Account number, stored encrypted';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."monthly_payment" IS 'Required monthly payment amount';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."current_balance" IS 'Current outstanding balance';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."original_amount" IS 'Original loan or credit amount';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."interest_rate" IS 'Current interest rate percentage';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."origination_date" IS 'When debt was originated';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."maturity_date" IS 'When debt will be paid off';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."verification_status" IS 'Status of liability verification';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."verification_date" IS 'Date liability was verified';

COMMENT ON COLUMN "consumer_lending"."applicant_liabilities"."will_be_paid_off" IS 'Indicates if debt will be paid off with loan';

COMMENT ON TABLE "consumer_lending"."loan_products" IS 'Defines the various loan products offered to consumers, including their terms, fees, and features.';

COMMENT ON COLUMN "consumer_lending"."loan_products"."consumer_lending_loan_product_id" IS 'Unique identifier for loan product';

COMMENT ON COLUMN "consumer_lending"."loan_products"."product_name" IS 'Marketing name of the product';

COMMENT ON COLUMN "consumer_lending"."loan_products"."product_code" IS 'Internal code for the product';

COMMENT ON COLUMN "consumer_lending"."loan_products"."loan_type" IS 'Type of loan product';

COMMENT ON COLUMN "consumer_lending"."loan_products"."description" IS 'Detailed product description';

COMMENT ON COLUMN "consumer_lending"."loan_products"."interest_rate_type" IS 'Type of interest rate';

COMMENT ON COLUMN "consumer_lending"."loan_products"."base_interest_rate" IS 'Starting interest rate before adjustments';

COMMENT ON COLUMN "consumer_lending"."loan_products"."min_term_months" IS 'Minimum allowed term in months';

COMMENT ON COLUMN "consumer_lending"."loan_products"."max_term_months" IS 'Maximum allowed term in months';

COMMENT ON COLUMN "consumer_lending"."loan_products"."min_loan_amount" IS 'Minimum allowed loan amount';

COMMENT ON COLUMN "consumer_lending"."loan_products"."max_loan_amount" IS 'Maximum allowed loan amount';

COMMENT ON COLUMN "consumer_lending"."loan_products"."min_credit_score" IS 'Minimum required credit score';

COMMENT ON COLUMN "consumer_lending"."loan_products"."origination_fee_type" IS 'Type of origination fee';

COMMENT ON COLUMN "consumer_lending"."loan_products"."origination_fee_amount" IS 'Amount or percentage of origination fee';

COMMENT ON COLUMN "consumer_lending"."loan_products"."late_fee_type" IS 'Type of late fee';

COMMENT ON COLUMN "consumer_lending"."loan_products"."late_fee_amount" IS 'Amount or percentage of late fee';

COMMENT ON COLUMN "consumer_lending"."loan_products"."is_active" IS 'Whether product is currently offered';

COMMENT ON COLUMN "consumer_lending"."loan_products"."required_collateral" IS 'Whether collateral is required';

COMMENT ON COLUMN "consumer_lending"."loan_products"."early_repayment_penalty" IS 'Whether penalty applies for early payoff';

COMMENT ON COLUMN "consumer_lending"."loan_products"."disbursement_options" IS 'Method of loan disbursement';

COMMENT ON TABLE "consumer_lending"."product_eligibility_criteria" IS 'Specifies the eligibility criteria for each loan product, such as credit score, income, and employment requirements.';

COMMENT ON COLUMN "consumer_lending"."product_eligibility_criteria"."consumer_lending_criteria_id" IS 'Unique identifier for eligibility criteria';

COMMENT ON COLUMN "consumer_lending"."product_eligibility_criteria"."consumer_lending_loan_product_id" IS 'Reference to loan product';

COMMENT ON COLUMN "consumer_lending"."product_eligibility_criteria"."criteria_type" IS 'Type of eligibility criteria';

COMMENT ON COLUMN "consumer_lending"."product_eligibility_criteria"."min_value" IS 'Minimum value for eligibility';

COMMENT ON COLUMN "consumer_lending"."product_eligibility_criteria"."max_value" IS 'Maximum value for eligibility';

COMMENT ON COLUMN "consumer_lending"."product_eligibility_criteria"."required" IS 'Whether this criteria is required';

COMMENT ON COLUMN "consumer_lending"."product_eligibility_criteria"."description" IS 'Description of the eligibility criteria';

COMMENT ON TABLE "consumer_lending"."risk_based_pricing_tiers" IS 'Defines pricing tiers based on risk factors, such as credit score and debt-to-income ratio, for loan products.';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."consumer_lending_pricing_tier_id" IS 'Unique identifier for pricing tier';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."consumer_lending_loan_product_id" IS 'Reference to loan product';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."tier_name" IS 'A, B, C, D, etc.';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."min_credit_score" IS 'Minimum credit score for this tier';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."max_credit_score" IS 'Maximum credit score for this tier';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."interest_rate_adjustment" IS 'Added to base rate';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."min_loan_amount" IS 'Minimum loan amount for this tier';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."max_loan_amount" IS 'Maximum loan amount for this tier';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."max_dti_ratio" IS 'Maximum debt-to-income ratio allowed';

COMMENT ON COLUMN "consumer_lending"."risk_based_pricing_tiers"."is_active" IS 'Whether tier is currently in use';

COMMENT ON TABLE "consumer_lending"."credit_reports" IS 'Stores credit reports obtained for loan applicants, including credit scores and other relevant information.';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."consumer_lending_credit_report_id" IS 'Unique identifier for credit report';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."consumer_lending_applicant_id" IS 'Reference to applicant';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."report_date" IS 'When report was pulled';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."expiration_date" IS 'When report expires';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."credit_score" IS 'Primary credit score from report';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."report_type" IS 'Type of credit report';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."bureau_name" IS 'Credit bureau providing the report';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."report_reference" IS 'External reference ID from bureau';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."report_path" IS 'Path to stored report file';

COMMENT ON COLUMN "consumer_lending"."credit_reports"."status" IS 'Status of credit report retrieval';

COMMENT ON TABLE "consumer_lending"."credit_report_tradelines" IS 'Contains details of individual tradelines (credit accounts) reported on a credit report.';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."consumer_lending_tradeline_id" IS 'Unique identifier for tradeline';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."consumer_lending_credit_report_id" IS 'Reference to credit report';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."account_type" IS 'Type of credit account';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."creditor_name" IS 'Name of creditor';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."account_number" IS 'Masked account number';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."open_date" IS 'When account was opened';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."current_balance" IS 'Current balance on account';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."high_credit" IS 'Highest balance or credit limit';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."credit_limit" IS 'Credit limit if applicable';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."monthly_payment" IS 'Monthly payment amount';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."payment_status" IS 'Current status of account payments';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."days_past_due" IS 'Current days past due';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."worst_delinquency" IS 'Worst historical delinquency';

COMMENT ON COLUMN "consumer_lending"."credit_report_tradelines"."worst_delinquency_date" IS 'Date of worst delinquency';

COMMENT ON TABLE "consumer_lending"."credit_inquiries" IS 'Records inquiries made on a credit report, indicating potential credit applications or checks.';

COMMENT ON COLUMN "consumer_lending"."credit_inquiries"."consumer_lending_inquiry_id" IS 'Unique identifier for inquiry record';

COMMENT ON COLUMN "consumer_lending"."credit_inquiries"."consumer_lending_credit_report_id" IS 'Reference to credit report';

COMMENT ON COLUMN "consumer_lending"."credit_inquiries"."inquiry_date" IS 'Date of credit inquiry';

COMMENT ON COLUMN "consumer_lending"."credit_inquiries"."creditor_name" IS 'Institution that made inquiry';

COMMENT ON COLUMN "consumer_lending"."credit_inquiries"."inquiry_type" IS 'Type of credit inquiry';

COMMENT ON TABLE "consumer_lending"."public_records" IS 'Stores public records, such as bankruptcies, liens, and judgments, associated with a credit report.';

COMMENT ON COLUMN "consumer_lending"."public_records"."consumer_lending_record_id" IS 'Unique identifier for public record';

COMMENT ON COLUMN "consumer_lending"."public_records"."consumer_lending_credit_report_id" IS 'Reference to credit report';

COMMENT ON COLUMN "consumer_lending"."public_records"."record_type" IS 'Type of public record';

COMMENT ON COLUMN "consumer_lending"."public_records"."status" IS 'Current status of the public record';

COMMENT ON COLUMN "consumer_lending"."public_records"."filing_date" IS 'Date record was filed';

COMMENT ON COLUMN "consumer_lending"."public_records"."amount" IS 'Amount of judgment or lien';

COMMENT ON COLUMN "consumer_lending"."public_records"."reference_number" IS 'Court or filing reference number';

COMMENT ON TABLE "consumer_lending"."decision_models" IS 'Contains information about the decision models used to evaluate loan applications, including credit scoring, income verification, and fraud detection models.';

COMMENT ON COLUMN "consumer_lending"."decision_models"."consumer_lending_model_id" IS 'Unique identifier for decision model';

COMMENT ON COLUMN "consumer_lending"."decision_models"."model_name" IS 'Name of the model';

COMMENT ON COLUMN "consumer_lending"."decision_models"."model_version" IS 'Version of the model';

COMMENT ON COLUMN "consumer_lending"."decision_models"."model_type" IS 'Type of decision model';

COMMENT ON COLUMN "consumer_lending"."decision_models"."is_active" IS 'Whether model is in active use';

COMMENT ON COLUMN "consumer_lending"."decision_models"."effective_date" IS 'When model became effective';

COMMENT ON COLUMN "consumer_lending"."decision_models"."expiration_date" IS 'When model expires';

COMMENT ON COLUMN "consumer_lending"."decision_models"."description" IS 'Description of the model and its purpose';

COMMENT ON TABLE "consumer_lending"."application_decisions" IS 'Records the decisions made on loan applications, including approvals, denials, and pre-qualifications.';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."consumer_lending_decision_id" IS 'Unique identifier for decision';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."decision_type" IS 'Type of decision';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."decision_result" IS 'Result of the decision';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."decision_date_time" IS 'When decision was made';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."decision_by_id" IS 'User that made decision';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."consumer_lending_model_id" IS 'Reference to decision model used';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."decision_score" IS 'Numeric score from decision model';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."consumer_lending_pricing_tier_id" IS 'Reference to pricing tier if approved';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."approved_amount" IS 'Approved loan amount';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."approved_term_months" IS 'Approved loan term in months';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."approved_interest_rate" IS 'Approved interest rate';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."approved_monthly_payment" IS 'Estimated monthly payment';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."conditional_approval" IS 'Whether approval has conditions';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."expires_date" IS 'When approval or prequalification expires';

COMMENT ON COLUMN "consumer_lending"."application_decisions"."notes" IS 'Additional decision notes';

COMMENT ON TABLE "consumer_lending"."decision_reasons" IS 'Provides specific reasons for the decisions made on loan applications, linked to the application_decisions table.';

COMMENT ON COLUMN "consumer_lending"."decision_reasons"."consumer_lending_decision_reason_id" IS 'Unique identifier for decision reason';

COMMENT ON COLUMN "consumer_lending"."decision_reasons"."consumer_lending_decision_id" IS 'Reference to application decision';

COMMENT ON COLUMN "consumer_lending"."decision_reasons"."reason_code" IS 'Standard reason code for decision';

COMMENT ON COLUMN "consumer_lending"."decision_reasons"."reason_description" IS 'Description of reason';

COMMENT ON COLUMN "consumer_lending"."decision_reasons"."sequence" IS 'Order of importance for reason';

COMMENT ON TABLE "consumer_lending"."adverse_action_notices" IS 'Tracks adverse action notices sent to applicants when their loan applications are denied.';

COMMENT ON COLUMN "consumer_lending"."adverse_action_notices"."consumer_lending_notice_id" IS 'Unique identifier for notice';

COMMENT ON COLUMN "consumer_lending"."adverse_action_notices"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."adverse_action_notices"."generated_date" IS 'When notice was generated';

COMMENT ON COLUMN "consumer_lending"."adverse_action_notices"."sent_date" IS 'When notice was sent to applicant';

COMMENT ON COLUMN "consumer_lending"."adverse_action_notices"."delivery_method" IS 'Method of delivering the notice';

COMMENT ON COLUMN "consumer_lending"."adverse_action_notices"."notice_path" IS 'Path to stored notice document';

COMMENT ON COLUMN "consumer_lending"."adverse_action_notices"."status" IS 'Current status of the notice';

COMMENT ON TABLE "consumer_lending"."vehicles" IS 'Stores information about vehicles involved in auto loan applications, including details like make, model, and purchase price.';

COMMENT ON COLUMN "consumer_lending"."vehicles"."vehicle_id" IS 'Unique identifier for vehicle';

COMMENT ON COLUMN "consumer_lending"."vehicles"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."vehicles"."year" IS 'Vehicle model year';

COMMENT ON COLUMN "consumer_lending"."vehicles"."make" IS 'Vehicle manufacturer';

COMMENT ON COLUMN "consumer_lending"."vehicles"."model" IS 'Vehicle model';

COMMENT ON COLUMN "consumer_lending"."vehicles"."trim" IS 'Vehicle trim level';

COMMENT ON COLUMN "consumer_lending"."vehicles"."vin" IS 'Vehicle Identification Number';

COMMENT ON COLUMN "consumer_lending"."vehicles"."vehicle_type" IS 'Condition of the vehicle';

COMMENT ON COLUMN "consumer_lending"."vehicles"."mileage" IS 'Current odometer reading';

COMMENT ON COLUMN "consumer_lending"."vehicles"."purchase_price" IS 'Agreed purchase price';

COMMENT ON COLUMN "consumer_lending"."vehicles"."down_payment" IS 'Down payment amount';

COMMENT ON COLUMN "consumer_lending"."vehicles"."trade_in_value" IS 'Value of trade-in vehicle';

COMMENT ON COLUMN "consumer_lending"."vehicles"."trade_in_balance_owed" IS 'Loan balance on trade-in';

COMMENT ON COLUMN "consumer_lending"."vehicles"."dealer_name" IS 'Name of dealership';

COMMENT ON COLUMN "consumer_lending"."vehicles"."dealer_address_id" IS 'Reference to enterprise.addresses';

COMMENT ON COLUMN "consumer_lending"."vehicles"."is_private_sale" IS 'Whether private sale or dealer';

COMMENT ON COLUMN "consumer_lending"."vehicles"."valuation_source" IS 'Source of vehicle valuation';

COMMENT ON COLUMN "consumer_lending"."vehicles"."valuation_amount" IS 'Third-party valuation amount';

COMMENT ON COLUMN "consumer_lending"."vehicles"."valuation_date" IS 'Date of valuation';

COMMENT ON TABLE "consumer_lending"."loan_accounts" IS 'Stores information about active loan accounts, including loan details, payment history, and current status.';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."consumer_lending_loan_account_id" IS 'Unique identifier for loan account';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."consumer_lending_loan_product_id" IS 'Reference to loan product';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."account_number" IS 'Customer-facing account number';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."status" IS 'Active, Paid Off, Charged Off, etc.';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."origination_date" IS 'Date loan was originated';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."funding_date" IS 'Date loan was funded';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."maturity_date" IS 'Scheduled loan payoff date';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."first_payment_date" IS 'Date first payment is due';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."original_principal_balance" IS 'Initial loan amount';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."current_principal_balance" IS 'Current principal balance';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."original_interest_rate" IS 'Interest rate at origination';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."current_interest_rate" IS 'Current interest rate';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."original_term_months" IS 'Original loan term in months';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."remaining_term_months" IS 'Remaining months on loan';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."payment_amount" IS 'Regular payment amount';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."payment_frequency" IS 'Monthly, Bi-weekly';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."next_payment_date" IS 'Next payment due date';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."next_payment_amount" IS 'Amount due for next payment';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."past_due_amount" IS 'Current past due amount';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."days_past_due" IS 'Current days past due';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."total_fees_charged" IS 'Sum of all fees charged';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."total_fees_paid" IS 'Sum of all fees paid';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."accrued_interest" IS 'Current accrued unpaid interest';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."interest_paid_ytd" IS 'Interest paid year to date';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."principal_paid_ytd" IS 'Principal paid year to date';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."interest_paid_total" IS 'Total interest paid life of loan';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."principal_paid_total" IS 'Total principal paid life of loan';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."late_count_30" IS 'Count of 30+ day late payments';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."late_count_60" IS 'Count of 60+ day late payments';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."late_count_90" IS 'Count of 90+ day late payments';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."auto_pay_enabled" IS 'Whether automatic payments are active';

COMMENT ON COLUMN "consumer_lending"."loan_accounts"."servicing_transferred_date" IS 'Date servicing was transferred if applicable';

COMMENT ON TABLE "consumer_lending"."payment_schedules" IS 'Contains the payment schedule for each loan account, including scheduled dates, amounts, and payment status.';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."payment_schedule_id" IS 'Unique identifier for schedule entry';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."consumer_lending_loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."payment_number" IS 'Sequential payment number';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."scheduled_date" IS 'Date payment is scheduled';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."payment_amount" IS 'Total payment amount due';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."principal_amount" IS 'Portion applied to principal';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."interest_amount" IS 'Portion applied to interest';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."beginning_balance" IS 'Principal balance before payment';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."ending_balance" IS 'Principal balance after payment';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."status" IS 'Current status of the payment schedule entry';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."actual_payment_date" IS 'Date payment was actually made';

COMMENT ON COLUMN "consumer_lending"."payment_schedules"."actual_payment_id" IS 'Reference to loan_payments if paid';

COMMENT ON TABLE "consumer_lending"."disbursements" IS 'Tracks the disbursement of funds for loan accounts, including the date, amount, method, and recipient information.';

COMMENT ON COLUMN "consumer_lending"."disbursements"."disbursement_id" IS 'Unique identifier for disbursement';

COMMENT ON COLUMN "consumer_lending"."disbursements"."consumer_lending_loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."disbursements"."disbursement_date" IS 'Date funds were disbursed';

COMMENT ON COLUMN "consumer_lending"."disbursements"."disbursement_amount" IS 'Amount disbursed';

COMMENT ON COLUMN "consumer_lending"."disbursements"."disbursement_method" IS 'ACH, Check, Wire';

COMMENT ON COLUMN "consumer_lending"."disbursements"."disbursement_status" IS 'Pending, Completed, Failed';

COMMENT ON COLUMN "consumer_lending"."disbursements"."recipient_name" IS 'Name of recipient';

COMMENT ON COLUMN "consumer_lending"."disbursements"."recipient_account_type" IS 'Checking, Savings';

COMMENT ON COLUMN "consumer_lending"."disbursements"."recipient_account_number" IS 'Recipient account number, encrypted';

COMMENT ON COLUMN "consumer_lending"."disbursements"."recipient_routing_number" IS 'Recipient routing number';

COMMENT ON COLUMN "consumer_lending"."disbursements"."check_number" IS 'Check number if applicable';

COMMENT ON COLUMN "consumer_lending"."disbursements"."tracking_number" IS 'Tracking or reference number';

COMMENT ON COLUMN "consumer_lending"."disbursements"."notes" IS 'Additional disbursement notes';

COMMENT ON TABLE "consumer_lending"."loan_payments" IS 'Records payments made on loan accounts, including payment date, amount, method, and status.';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."consumer_lending_payment_id" IS 'Unique identifier for payment';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."consumer_lending_loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."payment_date" IS 'Date/time payment was received';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."payment_effective_date" IS 'Date payment is effective';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."payment_type" IS 'Type of payment';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."payment_method" IS 'Method used to make payment';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."payment_amount" IS 'Total payment amount';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."principal_amount" IS 'Amount applied to principal';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."interest_amount" IS 'Amount applied to interest';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."late_fee_amount" IS 'Amount applied to late fees';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."other_fee_amount" IS 'Amount applied to other fees';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."transaction_id" IS 'External transaction identifier';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."confirmation_number" IS 'Payment confirmation number';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."payment_status" IS 'Current status of the payment';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."returned_reason" IS 'Reason for payment return if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_payments"."returned_date" IS 'Date payment was returned if applicable';

COMMENT ON TABLE "consumer_lending"."loan_fees" IS 'Tracks fees charged to loan accounts, including fee type, amount, status, and payment details.';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."consumer_lending_fee_id" IS 'Unique identifier for fee';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."consumer_lending_loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."fee_type" IS 'Type of fee charged';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."fee_date" IS 'Date fee was assessed';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."fee_amount" IS 'Fee amount';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."fee_status" IS 'Current status of the fee';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."waived_date" IS 'Date fee was waived if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."waived_by_id" IS 'User who waived the fee';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."waiver_reason" IS 'Reason fee was waived';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."paid_date" IS 'Date fee was paid';

COMMENT ON COLUMN "consumer_lending"."loan_fees"."consumer_lending_payment_id" IS 'Reference to loan_payments if paid';

COMMENT ON TABLE "consumer_lending"."loan_collateral" IS 'Stores information about collateral used to secure loans, including type, value, and insurance requirements.';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."consumer_lending_collateral_id" IS 'Unique identifier for collateral';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."collateral_type" IS 'Type of collateral';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."description" IS 'Description of collateral';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."value" IS 'Estimated value of collateral';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."valuation_date" IS 'Date of valuation';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."vehicle_id" IS 'Reference to vehicles table if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."property_address_id" IS 'Reference to enterprise.addresses if property';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."deposit_account_id" IS 'Reference to enterprise.accounts if deposit';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."lien_position" IS 'Priority of lien';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."lien_recording_date" IS 'Date lien was recorded';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."lien_recording_number" IS 'Lien recording reference number';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."insurance_required" IS 'Whether insurance is required';

COMMENT ON COLUMN "consumer_lending"."loan_collateral"."insurance_expiration_date" IS 'Expiration date of insurance policy';

COMMENT ON TABLE "consumer_lending"."loan_insurance" IS 'Stores information about insurance policies associated with loan accounts or collateral.';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."consumer_lending_insurance_id" IS 'Unique identifier for insurance record';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."consumer_lending_loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."consumer_lending_collateral_id" IS 'Reference to loan_collateral if associated with specific collateral';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."insurance_type" IS 'Type of insurance';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."carrier_name" IS 'Name of insurance company';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."policy_number" IS 'Insurance policy number';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."coverage_amount" IS 'Amount of coverage';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."premium_amount" IS 'Cost of insurance premium';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."premium_frequency" IS 'Frequency of premium payments';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."effective_date" IS 'Policy start date';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."expiration_date" IS 'Policy end date';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."beneficiary" IS 'Named beneficiary if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_insurance"."status" IS 'Current status of the insurance policy';

COMMENT ON TABLE "consumer_lending"."loan_documents" IS 'Tracks documents related to loan applications and accounts, including application forms, contracts, and statements.';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."consumer_lending_document_id" IS 'Unique identifier for document';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."consumer_lending_application_id" IS 'Reference to loan application if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."loan_account_id" IS 'Reference to loan account if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."document_type" IS 'Type of document';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."document_name" IS 'File name or title';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."document_path" IS 'Path to stored document';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."upload_date" IS 'When document was created/uploaded';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."status" IS 'Current status of the document';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."review_date" IS 'When document was reviewed';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."reviewer_id" IS 'User who reviewed document';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."expiration_date" IS 'Document expiration date if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_documents"."notes" IS 'Additional document notes';

COMMENT ON TABLE "consumer_lending"."loan_communications" IS 'Logs various communications related to loan applications and accounts, such as emails, letters, and phone calls.';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."consumer_lending_communication_id" IS 'Unique identifier for communication';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."consumer_lending_application_id" IS 'Reference to loan application if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."loan_account_id" IS 'Reference to loan account if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."communication_date" IS 'Date/time of communication';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."communication_type" IS 'Method of communication';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."direction" IS 'Direction of communication';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."subject" IS 'Communication subject';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."content" IS 'Communication content or transcript';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."sender" IS 'Person or system that sent communication';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."recipient" IS 'Person who received communication';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."template_id" IS 'Reference to template if applicable';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."status" IS 'Current status of communication';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."document_path" IS 'Path to stored communication document';

COMMENT ON COLUMN "consumer_lending"."loan_communications"."related_to" IS 'Context or purpose of communication';

COMMENT ON TABLE "consumer_lending"."loan_statements" IS 'Stores periodic loan statements, providing a summary of account activity, balances, and payments.';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."consumer_lending_statement_id" IS 'Unique identifier for statement';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."statement_date" IS 'Date statement was generated';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."statement_period_start" IS 'Start date of statement period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."statement_period_end" IS 'End date of statement period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."opening_balance" IS 'Balance at start of period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."closing_balance" IS 'Balance at end of period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."total_payments" IS 'Sum of payments in period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."principal_paid" IS 'Principal paid in period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."interest_paid" IS 'Interest paid in period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."fees_charged" IS 'Fees charged in period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."fees_paid" IS 'Fees paid in period';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."amount_due" IS 'Amount due for next payment';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."due_date" IS 'Next payment due date';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."document_path" IS 'Path to stored statement document';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."sent_date" IS 'Date statement was sent to customer';

COMMENT ON COLUMN "consumer_lending"."loan_statements"."delivery_method" IS 'Method of statement delivery';

COMMENT ON TABLE "consumer_lending"."collection_accounts" IS 'Tracks accounts that have been placed in collections, including delinquency details and collection actions.';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."consumer_lending_collection_id" IS 'Unique identifier for collection record';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."assigned_date" IS 'Date account was placed in collections';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."status" IS 'Current status of collection account';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."delinquency_reason" IS 'Customer-provided reason for delinquency';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."delinquency_date" IS 'First date of delinquency';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."days_delinquent" IS 'Current days delinquent';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."amount_past_due" IS 'Total amount past due';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."assigned_to" IS 'Collector assigned to account';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."priority" IS 'Priority level of the collection account';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."next_action_date" IS 'Date of next scheduled action';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."last_action_date" IS 'Date of most recent action taken';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."resolution_date" IS 'Date collection was resolved';

COMMENT ON COLUMN "consumer_lending"."collection_accounts"."resolution_type" IS 'Type of resolution for the collection account';

COMMENT ON TABLE "consumer_lending"."collection_actions" IS 'Logs specific actions taken to collect on delinquent loan accounts, such as calls, letters, and emails.';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."consumer_lending_action_id" IS 'Unique identifier for collection action';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."consumer_lending_collection_id" IS 'Reference to collection account';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."action_date" IS 'Date/time action was taken';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."action_type" IS 'Type of collection action';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."action_result" IS 'Result of the collection action';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."action_by_id" IS 'User who performed action';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."notes" IS 'Details of action and outcome';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."next_action_type" IS 'Type of next planned action';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."next_action_date" IS 'Date for next planned action';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."promise_to_pay_amount" IS 'Amount customer promised to pay';

COMMENT ON COLUMN "consumer_lending"."collection_actions"."promise_to_pay_date" IS 'Date customer promised to pay by';

COMMENT ON TABLE "consumer_lending"."payment_arrangements" IS 'Records payment arrangements made with borrowers to resolve delinquent accounts.';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."consumer_lending_arrangement_id" IS 'Unique identifier for payment arrangement';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."consumer_lending_collection_id" IS 'Reference to collection account';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."arrangement_date" IS 'Date arrangement was created';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."status" IS 'Current status of payment arrangement';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."total_amount" IS 'Total amount to be paid';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."number_of_payments" IS 'Number of payments in arrangement';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."first_payment_date" IS 'Date first payment is due';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."payment_frequency" IS 'Frequency of payments';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."payment_amount" IS 'Amount of each payment';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."approved_by_id" IS 'User who approved arrangement';

COMMENT ON COLUMN "consumer_lending"."payment_arrangements"."notes" IS 'Additional arrangement notes';

COMMENT ON TABLE "consumer_lending"."loan_modifications" IS 'Tracks modifications made to existing loan accounts, such as changes to interest rates, terms, or principal balance.';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."consumer_lending_modification_id" IS 'Unique identifier for loan modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."loan_account_id" IS 'Reference to loan account';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."modification_type" IS 'Type of loan modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."request_date" IS 'Date modification was requested';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."approval_date" IS 'Date modification was approved';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."effective_date" IS 'Date modification takes effect';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."original_rate" IS 'Interest rate before modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."new_rate" IS 'Interest rate after modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."original_term_months" IS 'Loan term before modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."new_term_months" IS 'Loan term after modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."original_principal_balance" IS 'Principal balance before modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."new_principal_balance" IS 'Principal balance after modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."capitalized_amount" IS 'Amount of interest or fees capitalized';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."status" IS 'Current status of the modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."hardship_reason" IS 'Customer''s reason for hardship';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."approved_by_id" IS 'User who approved modification';

COMMENT ON COLUMN "consumer_lending"."loan_modifications"."document_path" IS 'Path to modification agreement document';

COMMENT ON TABLE "consumer_lending"."reg_z_disclosures" IS 'Stores disclosures required by the Truth in Lending Act (Regulation Z), such as Loan Estimates and Closing Disclosures.';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."consumer_lending_disclosure_id" IS 'Unique identifier for disclosure';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."loan_account_id" IS 'Reference to loan account if originated';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."disclosure_type" IS 'Type of Regulation Z disclosure';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."disclosure_date" IS 'Date disclosure was generated';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."sent_date" IS 'Date disclosure was sent to applicant';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."delivery_method" IS 'Method of delivering the disclosure';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."annual_percentage_rate" IS 'APR disclosed';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."finance_charge" IS 'Total finance charge disclosed';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."amount_financed" IS 'Amount financed disclosed';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."total_of_payments" IS 'Total of payments disclosed';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."payment_schedule" IS 'Summary of payment schedule';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."security_interest" IS 'Description of security interest';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."late_payment_fee" IS 'Late payment fee disclosed';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."prepayment_penalty" IS 'Description of prepayment penalty if any';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."document_path" IS 'Path to stored disclosure document';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."received_by_customer" IS 'Whether receipt confirmed';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."receipt_date" IS 'Date receipt was confirmed';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."user_id" IS 'User who generated disclosure';

COMMENT ON COLUMN "consumer_lending"."reg_z_disclosures"."version" IS 'Version number if multiple disclosures of same type';

COMMENT ON TABLE "consumer_lending"."adverse_action_details" IS 'Provides detailed information about adverse action taken on loan applications, including reasons and credit information.';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."consumer_lending_adverse_action_id" IS 'Unique identifier for adverse action record';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."consumer_lending_notice_id" IS 'Reference to adverse_action_notices';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."ecoa_reason_code" IS 'Standard ECOA reason code';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."fcra_reason_code" IS 'Standard FCRA reason code if applicable';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."reason_description" IS 'Description of reason for adverse action';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."credit_score_disclosed" IS 'Credit score disclosed to applicant';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."credit_score_range_min" IS 'Minimum score in range';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."credit_score_range_max" IS 'Maximum score in range';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."credit_score_factors" IS 'Key factors affecting score';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."credit_bureau_name" IS 'Credit bureau providing the report';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."generated_date" IS 'Date details were generated';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."user_id" IS 'User who generated adverse action';

COMMENT ON COLUMN "consumer_lending"."adverse_action_details"."sequence" IS 'Order of importance for reason';

COMMENT ON TABLE "consumer_lending"."ecoa_monitoring" IS 'Tracks information related to the Equal Credit Opportunity Act (ECOA) for monitoring and compliance purposes.';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."consumer_lending_monitoring_id" IS 'Unique identifier for monitoring record';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."consumer_lending_applicant_id" IS 'Reference to applicant';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."ethnicity" IS 'Self-reported ethnicity';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."race" IS 'Self-reported race';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."sex" IS 'Self-reported sex';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."age" IS 'Applicant age';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."marital_status" IS 'Marital status';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."information_method" IS 'Method of obtaining information';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."income_monitored" IS 'Income used for decision';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."action_taken" IS 'Action taken on the loan application';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."action_date" IS 'Date of action';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."submission_date" IS 'Date monitoring info submitted';

COMMENT ON COLUMN "consumer_lending"."ecoa_monitoring"."submitted_by_id" IS 'User who submitted monitoring info';

COMMENT ON TABLE "consumer_lending"."fairlending_analysis" IS 'Records fair lending analysis conducted to identify and address potential disparities in lending practices.';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."consumer_lending_analysis_id" IS 'Unique identifier for analysis record';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."analysis_date" IS 'Date analysis was performed';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."analysis_type" IS 'Type of fair lending analysis';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."consumer_lending_loan_product_id" IS 'Loan product analyzed if specific product';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."time_period_start" IS 'Start of analysis period';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."time_period_end" IS 'End of analysis period';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."protected_class" IS 'Protected class being analyzed';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."control_group" IS 'Reference group for comparison';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."test_group" IS 'Group being tested for disparities';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."sample_size_control" IS 'Number in control group';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."sample_size_test" IS 'Number in test group';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."outcome_variable" IS 'Outcome being measured';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."statistical_test" IS 'Statistical method used';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."disparity_ratio" IS 'Ratio of outcomes between groups';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."p_value" IS 'Statistical significance level';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."statistically_significant" IS 'Whether result is statistically significant';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."controls_applied" IS 'Variables controlled for in analysis';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."findings" IS 'Summary of findings';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."analyst" IS 'Person who performed analysis';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."reviewer" IS 'Person who reviewed analysis';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."action_recommended" IS 'Recommended actions based on findings';

COMMENT ON COLUMN "consumer_lending"."fairlending_analysis"."report_path" IS 'Path to full analysis report';

COMMENT ON TABLE "consumer_lending"."reg_b_notices" IS 'Tracks notices and disclosures required by Regulation B (Equal Credit Opportunity Act), such as notices of incomplete applications or adverse action.';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."consumer_lending_notice_id" IS 'Unique identifier for Reg B notice';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."notice_type" IS 'Type of Regulation B notice';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."generated_date" IS 'Date notice was generated';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."sent_date" IS 'Date notice was sent';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."delivery_method" IS 'Method of delivering the notice';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."incomplete_items" IS 'Items needed if incompleteness notice';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."deadline_date" IS 'Deadline for response if applicable';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."counteroffer_terms" IS 'Terms of counteroffer if applicable';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."appraisal_notice_included" IS 'Whether appraisal notice included';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."document_path" IS 'Path to stored notice document';

COMMENT ON COLUMN "consumer_lending"."reg_b_notices"."user_id" IS 'User who generated notice';

COMMENT ON TABLE "consumer_lending"."appraisal_disclosures" IS 'Manages appraisal disclosures provided to loan applicants, including the type of appraisal and its value.';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."consumer_lending_disclosure_id" IS 'Unique identifier for appraisal disclosure';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."property_address_id" IS 'Reference to enterprise.addresses';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."disclosure_type" IS 'Initial Disclosure, Final Disclosure';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."disclosure_date" IS 'Date disclosure was generated';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."sent_date" IS 'Date disclosure was sent';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."delivery_method" IS 'Email, Mail, Electronic';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."appraisal_type" IS 'Full Appraisal, AVM, BPO, etc.';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."appraisal_ordered_date" IS 'Date appraisal was ordered';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."appraisal_received_date" IS 'Date appraisal was received';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."appraisal_provided_date" IS 'Date appraisal was provided to applicant';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."appraisal_value" IS 'Appraised value if known';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."document_path" IS 'Path to stored disclosure document';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."appraisal_waiver" IS 'Whether appraisal was waived';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."waiver_reason" IS 'Reason for waiver if applicable';

COMMENT ON COLUMN "consumer_lending"."appraisal_disclosures"."user_id" IS 'User who generated disclosure';

COMMENT ON TABLE "consumer_lending"."military_lending_checks" IS 'Tracks compliance with the Military Lending Act (MLA), including verification of military status and MAPR calculations.';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."consumer_lending_check_id" IS 'Unique identifier for MLA check';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."consumer_lending_applicant_id" IS 'Reference to applicant';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."check_date" IS 'Date MLA status was checked';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."covered_borrower" IS 'Whether applicant is a covered borrower';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."verification_method" IS 'MLA Database, Credit Report Flag';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."military_status" IS 'Active Duty, Dependent, Not Military';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."certificate_date" IS 'Date on covered borrower certificate';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."document_path" IS 'Path to stored verification document';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."mapr_calculated" IS 'Military Annual Percentage Rate if calculated';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."mapr_disclosure_provided" IS 'Whether MAPR disclosure was provided';

COMMENT ON COLUMN "consumer_lending"."military_lending_checks"."user_id" IS 'User who performed check';

COMMENT ON TABLE "consumer_lending"."high_cost_mortgage_tests" IS 'Records the results of high-cost mortgage tests performed under the Home Ownership and Equity Protection Act (HOEPA).';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."consumer_lending_test_id" IS 'Unique identifier for HOEPA test';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."consumer_lending_application_id" IS 'Reference to loan application';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."test_date" IS 'Date test was performed';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."test_type" IS 'APR Test, Points and Fees Test';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."loan_amount" IS 'Amount used for test';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."apr" IS 'APR used for test';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."points_and_fees" IS 'Total points and fees';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."points_and_fees_percentage" IS 'Points and fees as percentage of loan';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."points_and_fees_threshold" IS 'Threshold for points and fees test';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."apr_threshold" IS 'Threshold for APR test';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."apor" IS 'Average Prime Offer Rate used';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."apor_date" IS 'Date of APOR used';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."high_cost_mortgage" IS 'Whether loan is high-cost';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."additional_disclosures_required" IS 'Whether additional disclosures required';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."user_id" IS 'User who performed test';

COMMENT ON COLUMN "consumer_lending"."high_cost_mortgage_tests"."notes" IS 'Additional test notes';

COMMENT ON TABLE "consumer_lending"."compliance_exceptions" IS 'Tracks compliance exceptions and issues encountered during the lending process, including remediation efforts.';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."consumer_lending_exception_id" IS 'Unique identifier for exception';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."consumer_lending_application_id" IS 'Reference to loan application if applicable';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."loan_account_id" IS 'Reference to loan account if applicable';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."exception_date" IS 'Date exception was identified';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."exception_type" IS 'Documentation, Disclosure, Timing, etc.';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."regulation" IS 'Reg Z, Reg B, FCRA, etc.';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."severity" IS 'High, Medium, Low';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."description" IS 'Detailed description of exception';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."identified_by_id" IS 'Person that identified exception';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."status" IS 'Open, In Remediation, Closed';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."remediation_plan" IS 'Plan to address exception';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."remediation_date" IS 'Date remediation completed';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."remediated_by_id" IS 'Person who remediated exception';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."root_cause" IS 'Identified root cause';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."preventive_action" IS 'Action to prevent recurrence';

COMMENT ON COLUMN "consumer_lending"."compliance_exceptions"."notes" IS 'Additional exception notes';

COMMENT ON TABLE "security"."identity_roles" IS 'Associates identities with roles';

COMMENT ON COLUMN "security"."identity_roles"."security_identity_role_id" IS 'Reference to the identity role assignment';

COMMENT ON COLUMN "security"."identity_roles"."security_identity_id" IS 'Reference to the identity';

COMMENT ON COLUMN "security"."identity_roles"."security_role_id" IS 'Reference to the role';

COMMENT ON COLUMN "security"."identity_roles"."start_date" IS 'When the role became effective';

COMMENT ON COLUMN "security"."identity_roles"."end_date" IS 'When the role was no longer effective';

COMMENT ON COLUMN "security"."identity_roles"."assigned_by_id" IS 'Who assigned the role';

COMMENT ON COLUMN "security"."identity_roles"."active" IS 'Whether this assignment is currently active';

COMMENT ON TABLE "security"."roles" IS 'Defines roles that can be assigned to identities';

COMMENT ON COLUMN "security"."roles"."security_role_id" IS 'Unique identifier for the role';

COMMENT ON COLUMN "security"."roles"."role_name" IS 'Internal name for the role';

COMMENT ON COLUMN "security"."roles"."display_name" IS 'User-friendly name for the role';

COMMENT ON COLUMN "security"."roles"."description" IS 'Description of the role''s purpose and scope';

COMMENT ON COLUMN "security"."roles"."status" IS 'Current status of the role';

COMMENT ON COLUMN "security"."roles"."managing_application_id" IS 'Application that manages this role';

COMMENT ON COLUMN "security"."roles"."owner_id" IS 'Who owns/manages this role';

COMMENT ON COLUMN "security"."roles"."created_at" IS 'When the role was created';

COMMENT ON COLUMN "security"."roles"."created_by_id" IS 'Who created the role';

COMMENT ON TABLE "security"."security_account_roles" IS 'Explicitly assigns roles to security accounts';

COMMENT ON TABLE "security"."security_account_enterprise_accounts" IS 'Explicit, direct linkage primarily intended for customer access scenarios.  - Optimized for simplicity, performance, and clarity for common use-cases. - Clearly delineates straightforward customer access from more complex internal access controls managed via RBAC.';

COMMENT ON COLUMN "security"."security_account_enterprise_accounts"."access_level" IS 'READ, WRITE, ADMIN, etc.';

COMMENT ON TABLE "security"."role_entitlements" IS 'Maps roles to their constituent entitlements';

COMMENT ON COLUMN "security"."role_entitlements"."security_role_entitlement_id" IS 'Reference to the role entitlement pair';

COMMENT ON COLUMN "security"."role_entitlements"."security_role_id" IS 'Reference to the role';

COMMENT ON COLUMN "security"."role_entitlements"."security_entitlement_id" IS 'Reference to the entitlement';

COMMENT ON COLUMN "security"."role_entitlements"."created_at" IS 'When the entitlement was added to the role';

COMMENT ON COLUMN "security"."role_entitlements"."created_by_id" IS 'Who added the entitlement to the role';

COMMENT ON COLUMN "security"."role_entitlements"."updated_by_id" IS 'Who added the entitlement to the role';

COMMENT ON COLUMN "security"."role_entitlements"."started_at" IS 'When the entitlement became effective';

COMMENT ON COLUMN "security"."role_entitlements"."ended_at" IS 'When the entitlement was no longer effective';

COMMENT ON COLUMN "security"."role_entitlements"."active" IS 'Incicates that the entitlement is effective at this moment';

COMMENT ON TABLE "security"."enhanced_entitlements" IS 'Defines granular entitlements that can be granted to roles';

COMMENT ON COLUMN "security"."enhanced_entitlements"."security_entitlement_id" IS 'Unique identifier for the entitlement';

COMMENT ON COLUMN "security"."enhanced_entitlements"."entitlement_name" IS 'Internal name for the entitlement';

COMMENT ON COLUMN "security"."enhanced_entitlements"."display_name" IS 'User-friendly name for the entitlement';

COMMENT ON COLUMN "security"."enhanced_entitlements"."description" IS 'Description of what the entitlement grants access to';

COMMENT ON COLUMN "security"."enhanced_entitlements"."status" IS 'Current status of the entitlement';

COMMENT ON COLUMN "security"."enhanced_entitlements"."managing_application_id" IS 'Application that manages this entitlement';

COMMENT ON COLUMN "security"."enhanced_entitlements"."created_at" IS 'When the entitlement was created';

COMMENT ON COLUMN "security"."enhanced_entitlements"."created_by_id" IS 'Who created the entitlement';

COMMENT ON TABLE "security"."entitlement_resources" IS 'Maps entitlements to resources with specific permission types and contexts';

COMMENT ON COLUMN "security"."entitlement_resources"."security_entitlement_resource_id" IS 'Unique identifier for this entitlement-resource relationship';

COMMENT ON COLUMN "security"."entitlement_resources"."security_entitlement_id" IS 'Reference to the entitlement';

COMMENT ON COLUMN "security"."entitlement_resources"."security_resource_id" IS 'Reference to the resource';

COMMENT ON COLUMN "security"."entitlement_resources"."permission_type" IS 'Type of permission granted on the resource';

COMMENT ON COLUMN "security"."entitlement_resources"."context_conditions" IS 'Context conditions that restrict when this entitlement is applicable';

COMMENT ON COLUMN "security"."entitlement_resources"."resource_details" IS 'Resource-specific details like column filters, row filters, access parameters';

COMMENT ON COLUMN "security"."entitlement_resources"."created_at" IS 'When the relationship was created';

COMMENT ON COLUMN "security"."entitlement_resources"."created_by_id" IS 'Who created the relationship';

COMMENT ON TABLE "security"."resource_definitions" IS 'Defines resources that can be secured through entitlements';

COMMENT ON COLUMN "security"."resource_definitions"."security_resource_id" IS 'Unique identifier for the resource';

COMMENT ON COLUMN "security"."resource_definitions"."resource_name" IS 'Name of the resource';

COMMENT ON COLUMN "security"."resource_definitions"."resource_type" IS 'Type of resource (DATA, APPLICATION, HOST, NETWORK_DEVICE)';

COMMENT ON COLUMN "security"."resource_definitions"."resource_identifier" IS 'Unique identifier for the resource (table name, API endpoint, hostname, IP address, etc.)';

COMMENT ON COLUMN "security"."resource_definitions"."application_id" IS 'Owner application that manages this resource (for APPLICATION and DATA types)';

COMMENT ON COLUMN "security"."resource_definitions"."host_id" IS 'Host where the resource is located (for HOST types)';

COMMENT ON COLUMN "security"."resource_definitions"."network_device_id" IS 'Network device where the resource is located (for NETWORK_DEVICE types)';

COMMENT ON COLUMN "security"."resource_definitions"."description" IS 'Description of the resource';

COMMENT ON COLUMN "security"."resource_definitions"."created_at" IS 'When the resource definition was created';

COMMENT ON COLUMN "security"."resource_definitions"."created_by_id" IS 'Who created the resource definition';

COMMENT ON TABLE "security"."devices" IS 'Table storing information about network devices.';

COMMENT ON COLUMN "security"."devices"."security_device_id" IS 'The unique IP address of the device. Serves as the primary key.';

COMMENT ON COLUMN "security"."devices"."device_type" IS 'The type of the device (e.g., router, server, workstation).';

COMMENT ON COLUMN "security"."devices"."subnet" IS 'The subnet the device belongs to.';

COMMENT ON COLUMN "security"."devices"."hostname" IS 'The hostname of the device.';

COMMENT ON COLUMN "security"."devices"."created_at" IS 'The timestamp when the device record was created.';

COMMENT ON COLUMN "security"."devices"."updated_at" IS 'The timestamp when the device record was last updated.';

COMMENT ON TABLE "security"."network_events" IS 'Table storing detailed information about network events for security monitoring and analysis.';

COMMENT ON COLUMN "security"."network_events"."security_network_event_id" IS 'Unique identifier for the network event. Automatically incrementing.';

COMMENT ON COLUMN "security"."network_events"."timestamp" IS 'Timestamp when the network event occurred.';

COMMENT ON COLUMN "security"."network_events"."source_ip" IS 'Source IP address of the network event.';

COMMENT ON COLUMN "security"."network_events"."source_port" IS 'Source port of the network event.';

COMMENT ON COLUMN "security"."network_events"."dest_ip" IS 'Destination IP address of the network event.';

COMMENT ON COLUMN "security"."network_events"."dest_port" IS 'Destination port of the network event.';

COMMENT ON COLUMN "security"."network_events"."protocol" IS 'Network protocol used (e.g., TCP, UDP, ICMP).';

COMMENT ON COLUMN "security"."network_events"."status" IS 'Status of the network event (e.g., success, failure, blocked).';

COMMENT ON COLUMN "security"."network_events"."tcp_flag" IS 'TCP flags associated with the event, if applicable.';

COMMENT ON COLUMN "security"."network_events"."sequence" IS 'TCP sequence number, if applicable.';

COMMENT ON COLUMN "security"."network_events"."ack" IS 'TCP acknowledgment number, if applicable.';

COMMENT ON COLUMN "security"."network_events"."window_size" IS 'TCP window size, if applicable.';

COMMENT ON COLUMN "security"."network_events"."length" IS 'Length of the data packet in bytes.';

COMMENT ON COLUMN "security"."network_events"."bytes_sent" IS 'Number of bytes sent during the event.';

COMMENT ON COLUMN "security"."network_events"."bytes_received" IS 'Number of bytes received during the event.';

COMMENT ON COLUMN "security"."network_events"."security_device_id" IS 'IP address of the device involved in the event (likely the device that logged the event)';

COMMENT ON COLUMN "security"."network_events"."log_message" IS 'Detailed log message associated with the network event.';

COMMENT ON COLUMN "security"."network_events"."created_at" IS 'Timestamp when the event record was created.';

COMMENT ON TABLE "security"."policies" IS 'Table storing security policies and their details.';

COMMENT ON COLUMN "security"."policies"."security_policy_id" IS 'Unique identifier for the policy.';

COMMENT ON COLUMN "security"."policies"."name" IS 'Name of the policy. Must be unique.';

COMMENT ON COLUMN "security"."policies"."description" IS 'Detailed description of the policy.';

COMMENT ON COLUMN "security"."policies"."created_by_id" IS 'Who created the policy';

COMMENT ON COLUMN "security"."policies"."updated_by_id" IS 'Who updated the policy';

COMMENT ON COLUMN "security"."policies"."created_at" IS 'Timestamp when the policy was created.';

COMMENT ON COLUMN "security"."policies"."updated_at" IS 'Timestamp when the policy was last updated.';

COMMENT ON COLUMN "security"."policies"."started_at" IS 'Timestamp when the policy became effective.';

COMMENT ON COLUMN "security"."policies"."ended_at" IS 'Timestamp when the policy was no longer effective.';

COMMENT ON COLUMN "security"."policies"."active" IS 'Indicates whether the policy is currently active.';

COMMENT ON TABLE "security"."policy_attributes" IS 'Table storing attributes associated with security policies. Allows for flexible policy configuration.';

COMMENT ON COLUMN "security"."policy_attributes"."security_policy_id" IS 'Foreign key referencing the policy_id in the policies table.';

COMMENT ON COLUMN "security"."policy_attributes"."attribute_name" IS 'Name of the policy attribute.';

COMMENT ON COLUMN "security"."policy_attributes"."attribute_value" IS 'Value of the policy attribute.';

COMMENT ON TABLE "security"."policy_rules" IS 'Table storing specific rules associated with security policies.';

COMMENT ON COLUMN "security"."policy_rules"."security_policy_rule_id" IS 'Unique identifier for the policy rule.';

COMMENT ON COLUMN "security"."policy_rules"."security_policy_id" IS 'Foreign key referencing the policy_id in the policies table.';

COMMENT ON COLUMN "security"."policy_rules"."rule_name" IS 'Name of the policy rule.';

COMMENT ON COLUMN "security"."policy_rules"."rule_description" IS 'Detailed description of the policy rule.';

COMMENT ON TABLE "security"."accounts" IS 'Table storing information about user accounts across various systems.';

COMMENT ON COLUMN "security"."accounts"."security_account_id" IS 'Unique identifier for the account.';

COMMENT ON COLUMN "security"."accounts"."security_identity_id" IS 'Identifier of the associated identity.';

COMMENT ON COLUMN "security"."accounts"."name" IS 'Name of the account.';

COMMENT ON COLUMN "security"."accounts"."account_id_string" IS 'String representation of the account ID.';

COMMENT ON COLUMN "security"."accounts"."security_source_id" IS 'Identifier of the source system for the account.';

COMMENT ON COLUMN "security"."accounts"."disabled" IS 'Indicates if the account is disabled.';

COMMENT ON COLUMN "security"."accounts"."locked" IS 'Indicates if the account is locked.';

COMMENT ON COLUMN "security"."accounts"."privileged" IS 'Indicates if the account has privileged access.';

COMMENT ON COLUMN "security"."accounts"."manually_correlated" IS 'Indicates if the account was manually correlated.';

COMMENT ON COLUMN "security"."accounts"."password_last_set" IS 'Timestamp when the account password was last set.';

COMMENT ON COLUMN "security"."accounts"."created" IS 'Timestamp when the account was created.';

COMMENT ON COLUMN "security"."accounts"."status_update_date_time" IS 'Timestamp when the account status was last updated';

COMMENT ON TABLE "security"."governance_groups" IS 'Table storing information about governance groups, used for managing access and permissions.';

COMMENT ON COLUMN "security"."governance_groups"."security_governance_group_id" IS 'Unique identifier for the governance group.';

COMMENT ON COLUMN "security"."governance_groups"."name" IS 'Name of the governance group.';

COMMENT ON COLUMN "security"."governance_groups"."owner_id" IS 'Identifier of the owner of the governance group.';

COMMENT ON TABLE "security"."iam_logins" IS 'Table storing information about IAM logins, tracking user access via accounts.';

COMMENT ON COLUMN "security"."iam_logins"."security_login_id" IS 'Unique identifier for the IAM login.';

COMMENT ON COLUMN "security"."iam_logins"."security_account_id" IS 'Identifier of the account used for the login.';

COMMENT ON COLUMN "security"."iam_logins"."user_name" IS 'Username used for the login.';

COMMENT ON COLUMN "security"."iam_logins"."login_time" IS 'Timestamp when the login occurred.';

COMMENT ON COLUMN "security"."iam_logins"."logout_time" IS 'Timestamp when the logout occurred.';

COMMENT ON COLUMN "security"."iam_logins"."login_method" IS 'Method used for the login.';

COMMENT ON TABLE "security"."identities" IS 'Table storing information about user identities, representing individuals or entities.';

COMMENT ON COLUMN "security"."identities"."security_identity_id" IS 'Unique identifier for the identity.';

COMMENT ON COLUMN "security"."identities"."name" IS 'Internal name of the identity.';

COMMENT ON COLUMN "security"."identities"."display_name" IS 'User-friendly name of the identity.';

COMMENT ON COLUMN "security"."identities"."service_account" IS 'If false than access is considered to be on behalf of the owner, otherwise this is service account used for system to system automation';

COMMENT ON COLUMN "security"."identities"."environment" IS 'Identifies access to an environment e.g production, development, etc.';

COMMENT ON COLUMN "security"."identities"."created" IS 'Timestamp when the identity was created.';

COMMENT ON COLUMN "security"."identities"."inactive" IS 'Indicates if the identity is inactive.';

COMMENT ON COLUMN "security"."identities"."status" IS 'Status of the identity.';

COMMENT ON COLUMN "security"."identities"."security_identity_profile_id" IS 'Identifier of the identity profile associated with the identity.';

COMMENT ON COLUMN "security"."identities"."modified" IS 'Timestamp when the identity was last modified.';

COMMENT ON COLUMN "security"."identities"."synced" IS 'Timestamp when the identity was last synced.';

COMMENT ON COLUMN "security"."identities"."is_fallback_approver" IS 'Indicates if the identity is a fallback approver.';

COMMENT ON TABLE "security"."identity_profiles" IS 'Table storing information about identity profiles, defining sets of attributes and rules for identities.';

COMMENT ON COLUMN "security"."identity_profiles"."security_identity_profile_id" IS 'Unique identifier for the identity profile.';

COMMENT ON COLUMN "security"."identity_profiles"."name" IS 'Name of the identity profile.';

COMMENT ON COLUMN "security"."identity_profiles"."description" IS 'Detailed description of the profile and its purpose.';

COMMENT ON COLUMN "security"."identity_profiles"."access_review_frequency_days" IS 'How often accounts with this profile should be reviewed, in days.';

COMMENT ON COLUMN "security"."identity_profiles"."max_inactive_days" IS 'Maximum number of days an identity can be inactive before automatic disablement.';

COMMENT ON COLUMN "security"."identity_profiles"."requires_mfa" IS 'Whether multi-factor authentication is required for identities with this profile.';

COMMENT ON COLUMN "security"."identity_profiles"."password_expiry_days" IS 'Number of days before password expiration for this profile type.';

COMMENT ON COLUMN "security"."identity_profiles"."default_session_timeout_minutes" IS 'Default session timeout in minutes for identities with this profile.';

COMMENT ON COLUMN "security"."identity_profiles"."risk_level" IS 'Risk classification level for this profile type.';

COMMENT ON COLUMN "security"."identity_profiles"."created_at" IS 'When the profile was created.';

COMMENT ON COLUMN "security"."identity_profiles"."updated_at" IS 'When the profile was last updated.';

COMMENT ON TABLE "security"."file_accesses" IS 'Table storing information about file access events, tracking file usage and access patterns.';

COMMENT ON COLUMN "security"."file_accesses"."security_file_access_id" IS 'Unique identifier for the file access event.';

COMMENT ON COLUMN "security"."file_accesses"."security_system_id" IS 'Identifier of the system where the file access occurred.';

COMMENT ON COLUMN "security"."file_accesses"."security_file_id" IS 'Identifier of the accessed file.';

COMMENT ON COLUMN "security"."file_accesses"."access_type" IS 'Type of file access (e.g., read, write, execute).';

COMMENT ON COLUMN "security"."file_accesses"."access_time" IS 'Timestamp when the file access occurred.';

COMMENT ON COLUMN "security"."file_accesses"."security_process_execution_id" IS 'Identifier of the process execution that initiated the file access.';

COMMENT ON TABLE "security"."file_threats" IS 'Table storing information about file threats, linking file hashes to threat levels and descriptions.';

COMMENT ON COLUMN "security"."file_threats"."security_file_threat_hash" IS 'Hash of the file, used to identify threats.';

COMMENT ON COLUMN "security"."file_threats"."threat_level" IS 'Level of threat associated with the file.';

COMMENT ON COLUMN "security"."file_threats"."threat_description" IS 'Description of the threat associated with the file.';

COMMENT ON TABLE "security"."files" IS 'Table storing information about files on systems, including file paths, hashes, and sizes.';

COMMENT ON COLUMN "security"."files"."security_file_id" IS 'Unique identifier for the file.';

COMMENT ON COLUMN "security"."files"."security_host_id" IS 'Identifier of the system where the file is located.';

COMMENT ON COLUMN "security"."files"."file_path" IS 'Path to the file on the system.';

COMMENT ON COLUMN "security"."files"."file_hash" IS 'Hash of the file, used for integrity checks.';

COMMENT ON COLUMN "security"."files"."file_size" IS 'Size of the file in bytes.';

COMMENT ON COLUMN "security"."files"."last_modified" IS 'Timestamp when the file was last modified.';

COMMENT ON TABLE "security"."installed_applications" IS 'Table storing information about installed applications on servers, tracking software installations.';

COMMENT ON COLUMN "security"."installed_applications"."security_host_id" IS 'Identifier of the system where the application is installed.';

COMMENT ON COLUMN "security"."installed_applications"."app_mgmt_application_id" IS 'Reference to the application definition.';

COMMENT ON COLUMN "security"."installed_applications"."application_version" IS 'Version of the installed application.';

COMMENT ON COLUMN "security"."installed_applications"."installation_date" IS 'Timestamp when the application was installed.';

COMMENT ON TABLE "security"."network_connections" IS 'Table storing information about network connections, tracking network traffic and activity.';

COMMENT ON COLUMN "security"."network_connections"."security_network_connection_id" IS 'Unique identifier for the network connection.';

COMMENT ON COLUMN "security"."network_connections"."security_host_id" IS 'Identifier of the system where the connection originated.';

COMMENT ON COLUMN "security"."network_connections"."security_process_execution_id" IS 'Identifier of the process execution that initiated the connection.';

COMMENT ON COLUMN "security"."network_connections"."connection_type" IS 'Type of network connection (e.g., TCP, UDP).';

COMMENT ON COLUMN "security"."network_connections"."protocol" IS 'Network protocol used for the connection.';

COMMENT ON COLUMN "security"."network_connections"."local_ip" IS 'Local IP address of the connection.';

COMMENT ON COLUMN "security"."network_connections"."local_port" IS 'Local port number of the connection.';

COMMENT ON COLUMN "security"."network_connections"."remote_ip" IS 'Remote IP address of the connection.';

COMMENT ON COLUMN "security"."network_connections"."remote_port" IS 'Remote port number of the connection.';

COMMENT ON COLUMN "security"."network_connections"."start_time" IS 'Timestamp when the connection started.';

COMMENT ON COLUMN "security"."network_connections"."end_time" IS 'Timestamp when the connection ended.';

COMMENT ON TABLE "security"."open_ports" IS 'Table storing information about open ports on systems, tracking network services and potential vulnerabilities.';

COMMENT ON COLUMN "security"."open_ports"."security_host_id" IS 'Identifier of the system with the open port.';

COMMENT ON COLUMN "security"."open_ports"."port_number" IS 'Port number that is open.';

COMMENT ON COLUMN "security"."open_ports"."protocol" IS 'Network protocol associated with the open port.';

COMMENT ON TABLE "security"."process_executions" IS 'Table storing information about process executions, tracking application activity and system behavior.';

COMMENT ON COLUMN "security"."process_executions"."security_process_execution_id" IS 'Unique identifier for the process execution.';

COMMENT ON COLUMN "security"."process_executions"."security_host_id" IS 'Identifier of the system where the process was executed.';

COMMENT ON COLUMN "security"."process_executions"."process_name" IS 'Name of the executed process.';

COMMENT ON COLUMN "security"."process_executions"."process_id" IS 'Process ID of the executed process.';

COMMENT ON COLUMN "security"."process_executions"."parent_process_id" IS 'Process ID of the parent process.';

COMMENT ON COLUMN "security"."process_executions"."start_time" IS 'Timestamp when the process execution started.';

COMMENT ON COLUMN "security"."process_executions"."end_time" IS 'Timestamp when the process execution ended.';

COMMENT ON COLUMN "security"."process_executions"."command_line" IS 'Command line used to execute the process.';

COMMENT ON COLUMN "security"."process_executions"."user_name" IS 'Username of the user who executed the process.';

COMMENT ON TABLE "security"."running_services" IS 'Table storing information about running services on systems, tracking system services and their states.';

COMMENT ON COLUMN "security"."running_services"."security_host_id" IS 'Identifier of the system with the running service.';

COMMENT ON COLUMN "security"."running_services"."running_service_name" IS 'Name of the running service.';

COMMENT ON COLUMN "security"."running_services"."start_time" IS 'Timestamp when the service started running.';

COMMENT ON COLUMN "security"."running_services"."status" IS 'Status of the running service (e.g., running, stopped).';

COMMENT ON TABLE "security"."system_stats" IS 'Table storing system statistics, tracking resource usage and performance metrics.';

COMMENT ON COLUMN "security"."system_stats"."security_system_stat_id" IS 'Unique identifier for the system statistics record.';

COMMENT ON COLUMN "security"."system_stats"."security_host_id" IS 'Identifier of the system for which statistics are recorded.';

COMMENT ON COLUMN "security"."system_stats"."cpu_usage_percent" IS 'CPU usage percentage.';

COMMENT ON COLUMN "security"."system_stats"."memory_usage_gb" IS 'Memory usage in gigabytes.';

COMMENT ON COLUMN "security"."system_stats"."memory_total_gb" IS 'Total memory in gigabytes.';

COMMENT ON COLUMN "security"."system_stats"."disk_free_gb" IS 'Free disk space in gigabytes.';

COMMENT ON COLUMN "security"."system_stats"."disk_total_gb" IS 'Total disk space in gigabytes.';

COMMENT ON COLUMN "security"."system_stats"."timestamp" IS 'Timestamp when the statistics were recorded.';

COMMENT ON TABLE "security"."hosts" IS 'Table storing information about systems, including hardware, software, and status details.';

COMMENT ON COLUMN "security"."hosts"."security_host_id" IS 'Unique identifier for the system.';

COMMENT ON COLUMN "security"."hosts"."hostname" IS 'Hostname of the system.';

COMMENT ON COLUMN "security"."hosts"."agent_identifier" IS 'Identifier of the agent installed on the system.';

COMMENT ON COLUMN "security"."hosts"."ip_address_internal" IS 'Internal IP address of the system.';

COMMENT ON COLUMN "security"."hosts"."ip_address_external" IS 'External IP address of the system.';

COMMENT ON COLUMN "security"."hosts"."mac_address" IS 'MAC address of the system.';

COMMENT ON COLUMN "security"."hosts"."system_type" IS 'Type of the system (e.g., server, workstation).';

COMMENT ON COLUMN "security"."hosts"."os" IS 'Operating system of the system.';

COMMENT ON COLUMN "security"."hosts"."os_version" IS 'Operating system version.';

COMMENT ON COLUMN "security"."hosts"."last_seen" IS 'Timestamp when the system was last seen.';

COMMENT ON COLUMN "security"."hosts"."agent_version" IS 'Version of the agent installed on the system.';

COMMENT ON COLUMN "security"."hosts"."agent_status" IS 'Status of the agent installed on the system.';

COMMENT ON COLUMN "security"."hosts"."patch_status" IS 'Status of system patches.';

COMMENT ON COLUMN "security"."hosts"."last_patched" IS 'Timestamp when the system was last patched.';

COMMENT ON COLUMN "security"."hosts"."compliance" IS 'Compliance status of the system.';

COMMENT ON COLUMN "security"."hosts"."checked_out_date" IS 'Date when the system was checked out.';

COMMENT ON COLUMN "security"."hosts"."asset_owner_name" IS 'Name of the asset owner.';

COMMENT ON COLUMN "security"."hosts"."asset_owner_email" IS 'Email of the asset owner.';

COMMENT ON COLUMN "security"."hosts"."patch_level" IS 'Patch level of the system.';

COMMENT ON COLUMN "security"."hosts"."patch_update_available" IS 'Indicates if patch updates are available.';

COMMENT ON TABLE "security"."usb_device_usage" IS 'Table storing information about USB device usage, tracking connection and disconnection times.';

COMMENT ON COLUMN "security"."usb_device_usage"."security_usb_device_usage_id" IS 'Unique identifier for the USB device usage record.';

COMMENT ON COLUMN "security"."usb_device_usage"."security_system_id" IS 'Identifier of the system where the USB device was used.';

COMMENT ON COLUMN "security"."usb_device_usage"."device_name" IS 'Name of the USB device.';

COMMENT ON COLUMN "security"."usb_device_usage"."device_type" IS 'Type of the USB device.';

COMMENT ON COLUMN "security"."usb_device_usage"."connection_time" IS 'Timestamp when the USB device was connected.';

COMMENT ON COLUMN "security"."usb_device_usage"."disconnection_time" IS 'Timestamp when the USB device was disconnected.';

COMMENT ON TABLE "security"."cvss" IS 'Stores Common Vulnerability Scoring System (CVSS) metrics for CVEs, including both CVSS v2 and v3.';

COMMENT ON COLUMN "security"."cvss"."cve" IS 'Common Vulnerabilities and Exposures identifier. Primary key.';

COMMENT ON COLUMN "security"."cvss"."attack_complexity_3" IS 'CVSS v3 Attack Complexity metric.';

COMMENT ON COLUMN "security"."cvss"."attack_vector_3" IS 'CVSS v3 Attack Vector metric.';

COMMENT ON COLUMN "security"."cvss"."availability_impact_3" IS 'CVSS v3 Availability Impact metric.';

COMMENT ON COLUMN "security"."cvss"."confidentiality_impact_3" IS 'CVSS v3 Confidentiality Impact metric.';

COMMENT ON COLUMN "security"."cvss"."integrity_impact_3" IS 'CVSS v3 Integrity Impact metric.';

COMMENT ON COLUMN "security"."cvss"."privileges_required_3" IS 'CVSS v3 Privileges Required metric.';

COMMENT ON COLUMN "security"."cvss"."scope_3" IS 'CVSS v3 Scope metric.';

COMMENT ON COLUMN "security"."cvss"."user_interaction_3" IS 'CVSS v3 User Interaction metric.';

COMMENT ON COLUMN "security"."cvss"."vector_string_3" IS 'CVSS v3 Vector String.';

COMMENT ON COLUMN "security"."cvss"."exploitability_score_3" IS 'CVSS v3 Exploitability Score.';

COMMENT ON COLUMN "security"."cvss"."impact_score_3" IS 'CVSS v3 Impact Score.';

COMMENT ON COLUMN "security"."cvss"."base_score_3" IS 'CVSS v3 Base Score.';

COMMENT ON COLUMN "security"."cvss"."base_severity_3" IS 'CVSS v3 Base Severity.';

COMMENT ON COLUMN "security"."cvss"."access_complexity" IS 'CVSS v2 Access Complexity metric.';

COMMENT ON COLUMN "security"."cvss"."access_vector" IS 'CVSS v2 Access Vector metric.';

COMMENT ON COLUMN "security"."cvss"."authentication" IS 'CVSS v2 Authentication metric.';

COMMENT ON COLUMN "security"."cvss"."availability_impact" IS 'CVSS v2 Availability Impact metric.';

COMMENT ON COLUMN "security"."cvss"."confidentiality_impact" IS 'CVSS v2 Confidentiality Impact metric.';

COMMENT ON COLUMN "security"."cvss"."integrity_impact" IS 'CVSS v2 Integrity Impact metric.';

COMMENT ON COLUMN "security"."cvss"."obtain_all_privileges" IS 'CVSS v2 Obtain All Privileges metric.';

COMMENT ON COLUMN "security"."cvss"."obtain_other_privileges" IS 'CVSS v2 Obtain Other Privileges metric.';

COMMENT ON COLUMN "security"."cvss"."obtain_user_privileges" IS 'CVSS v2 Obtain User Privileges metric.';

COMMENT ON COLUMN "security"."cvss"."user_interaction_required" IS 'CVSS v2 User Interaction Required metric.';

COMMENT ON COLUMN "security"."cvss"."vector_string" IS 'CVSS v2 Vector String.';

COMMENT ON COLUMN "security"."cvss"."exploitability_score" IS 'CVSS v2 Exploitability Score.';

COMMENT ON COLUMN "security"."cvss"."impact_score" IS 'CVSS v2 Impact Score.';

COMMENT ON COLUMN "security"."cvss"."base_score" IS 'CVSS v2 Base Score.';

COMMENT ON COLUMN "security"."cvss"."severity" IS 'CVSS v2 Severity.';

COMMENT ON COLUMN "security"."cvss"."description" IS 'CVE description.';

COMMENT ON COLUMN "security"."cvss"."published_date" IS 'CVE publication date.';

COMMENT ON COLUMN "security"."cvss"."last_modified_date" IS 'CVE last modified date.';

COMMENT ON TABLE "security"."cpe" IS 'Stores Common Platform Enumeration (CPE) information associated with CVEs.';

COMMENT ON COLUMN "security"."cpe"."cve" IS 'Common Vulnerabilities and Exposures identifier. Foreign key referencing cvss.cve.';

COMMENT ON COLUMN "security"."cpe"."cpe23uri" IS 'CPE 2.3 URI string.';

COMMENT ON COLUMN "security"."cpe"."vulnerable" IS 'Indicates if the CPE is vulnerable to the CVE.';

COMMENT ON TABLE "security"."cve_problem" IS 'Stores problem descriptions associated with CVEs.';

COMMENT ON COLUMN "security"."cve_problem"."cve" IS 'Common Vulnerabilities and Exposures identifier. Foreign key referencing cvss.cve.';

COMMENT ON COLUMN "security"."cve_problem"."problem" IS 'Problem description related to the CVE.';

COMMENT ON COLUMN "security"."cve_problem"."cwe_id" IS 'A reference to the related Common Weakness Enumeration, if it exists';

COMMENT ON TABLE "security"."cwe" IS 'Stores Common Weakness Enumeration (CWE) information.';

COMMENT ON COLUMN "security"."cwe"."cwe_id" IS 'Common Weakness Enumeration identifier. Primary key.';

COMMENT ON COLUMN "security"."cwe"."name" IS 'CWE name.';

COMMENT ON COLUMN "security"."cwe"."description" IS 'CWE description.';

COMMENT ON COLUMN "security"."cwe"."extended_description" IS 'Extended CWE description.';

COMMENT ON COLUMN "security"."cwe"."modes_of_introduction" IS 'Modes of introduction for the CWE.';

COMMENT ON COLUMN "security"."cwe"."common_consequences" IS 'Common consequences of the CWE.';

COMMENT ON COLUMN "security"."cwe"."potential_mitigations" IS 'Potential mitigations for the CWE.';

COMMENT ON TABLE "app_mgmt"."architectures" IS 'Table to store approved architectural designs and their key details.';

COMMENT ON COLUMN "app_mgmt"."architectures"."app_mgmt_architecture_id" IS 'Unique identifier for an approved architectural design.';

COMMENT ON COLUMN "app_mgmt"."architectures"."architecture_name" IS 'Name given to the architectural design.';

COMMENT ON COLUMN "app_mgmt"."architectures"."description" IS 'Detailed explanation of the architectural design.';

COMMENT ON COLUMN "app_mgmt"."architectures"."approval_date" IS 'Date when the architectural design was officially approved.';

COMMENT ON COLUMN "app_mgmt"."architectures"."approved_by_id" IS 'Identifier of the employee who approved the design.';

COMMENT ON COLUMN "app_mgmt"."architectures"."documentation_url" IS 'Link to the full documentation for the architectural design.';

COMMENT ON COLUMN "app_mgmt"."architectures"."status" IS 'Current state of the architecture (e.g., approved, deprecated, proposed).';

COMMENT ON COLUMN "app_mgmt"."architectures"."sdlc_process_id" IS 'Identifier for the software development lifecycle process this architecture aligns with.';

COMMENT ON COLUMN "app_mgmt"."architectures"."created_by_user_id" IS 'Identifier of the employee who created the architectural design.';

COMMENT ON COLUMN "app_mgmt"."architectures"."modified_by_user_id" IS 'Identifier of the employee who last modified the architectural design.';

COMMENT ON TABLE "app_mgmt"."sdlc_processes" IS 'Table to store software development lifecycle processes and their attributes.';

COMMENT ON COLUMN "app_mgmt"."sdlc_processes"."app_mgmt_sdlc_process_id" IS 'Unique identifier for a defined software development lifecycle process.';

COMMENT ON COLUMN "app_mgmt"."sdlc_processes"."process_name" IS 'Name of the software development lifecycle process.';

COMMENT ON COLUMN "app_mgmt"."sdlc_processes"."description" IS 'Description of the steps and activities within the SDLC process.';

COMMENT ON COLUMN "app_mgmt"."sdlc_processes"."process_owner" IS 'The individual responsible for the SDLC process.';

COMMENT ON COLUMN "app_mgmt"."sdlc_processes"."version" IS 'Version number or identifier for the SDLC process.';

COMMENT ON COLUMN "app_mgmt"."sdlc_processes"."documentation_url" IS 'Link to the full documentation for the SDLC process.';

COMMENT ON COLUMN "app_mgmt"."sdlc_processes"."app_mgmt_team_id" IS 'Identifier for the team that manages this SDLC process.';

COMMENT ON TABLE "app_mgmt"."applications" IS 'Table to store comprehensive information about software applications within the organization.';

COMMENT ON COLUMN "app_mgmt"."applications"."app_mgmt_application_id" IS 'Unique identifier for an application.';

COMMENT ON COLUMN "app_mgmt"."applications"."enterprise_department_id" IS 'Has financial responsibility for resource. This is the department that pays for maintenance, upgrades and operation of the application.';

COMMENT ON COLUMN "app_mgmt"."applications"."application_name" IS 'Name of the application.';

COMMENT ON COLUMN "app_mgmt"."applications"."description" IS 'General description of the application''s purpose.';

COMMENT ON COLUMN "app_mgmt"."applications"."application_type" IS 'Type of application (e.g., web, mobile, desktop).';

COMMENT ON COLUMN "app_mgmt"."applications"."vendor" IS 'Name of the vendor if the application is purchased.';

COMMENT ON COLUMN "app_mgmt"."applications"."version" IS 'Current version of the application.';

COMMENT ON COLUMN "app_mgmt"."applications"."deployment_environment" IS 'Environment where the application is deployed (e.g., on-premises, cloud).';

COMMENT ON COLUMN "app_mgmt"."applications"."operated_by_team_id" IS 'Identifier for the team responsible for the day-to-day operation of the application.';

COMMENT ON COLUMN "app_mgmt"."applications"."maintained_by_team_id" IS 'Identifier for the team responsible for maintaining the application, including updates and fixes.';

COMMENT ON COLUMN "app_mgmt"."applications"."created_by_team_id" IS 'Identifier for the team that initially created the application.';

COMMENT ON COLUMN "app_mgmt"."applications"."application_owner_id" IS 'Identifier for the individual responsible for communication with stakeholders, funding, budget, and strategy for the application.';

COMMENT ON COLUMN "app_mgmt"."applications"."lifecycle_status" IS 'Current stage in the application''s lifecycle (e.g., development, production).';

COMMENT ON COLUMN "app_mgmt"."applications"."date_deployed" IS 'Date the application was deployed to its environment.';

COMMENT ON COLUMN "app_mgmt"."applications"."date_retired" IS 'Date the application was retired or decommissioned.';

COMMENT ON COLUMN "app_mgmt"."applications"."architecture_id" IS 'Identifier for the approved architecture the application adheres to.';

COMMENT ON COLUMN "app_mgmt"."applications"."sdlc_process_id" IS 'Identifier for the SDLC process used to develop or manage the application.';

COMMENT ON COLUMN "app_mgmt"."applications"."source_code_repository" IS 'Link to the repository where the application''s source code is stored.';

COMMENT ON COLUMN "app_mgmt"."applications"."documentation_url" IS 'Link to the application''s documentation.';

COMMENT ON COLUMN "app_mgmt"."applications"."created_by_user_id" IS 'Identifier of the employee who initially created the application record.';

COMMENT ON COLUMN "app_mgmt"."applications"."modified_by_user_id" IS 'Identifier of the employee who last modified the application record.';

COMMENT ON COLUMN "app_mgmt"."applications"."rto" IS 'Recovery Time Objective (RTO): The maximum acceptable downtime for the application.';

COMMENT ON COLUMN "app_mgmt"."applications"."rpo" IS 'Recovery Point Objective (RPO): The maximum acceptable data loss for the application.';

COMMENT ON TABLE "app_mgmt"."components" IS 'Table to store detailed information about software components (BOM).';

COMMENT ON COLUMN "app_mgmt"."components"."app_mgmt_component_id" IS 'Unique identifier for a software component (e.g., library, module).';

COMMENT ON COLUMN "app_mgmt"."components"."component_name" IS 'Name of the software component.';

COMMENT ON COLUMN "app_mgmt"."components"."component_version" IS 'Version identifier for the software component.';

COMMENT ON COLUMN "app_mgmt"."components"."component_type" IS 'Type of component (e.g., library, framework, API, module). Also used for language-specific categorization (e.g., java-library, npm-package).';

COMMENT ON COLUMN "app_mgmt"."components"."vendor" IS 'Vendor or provider of the software component.';

COMMENT ON COLUMN "app_mgmt"."components"."app_mgmt_license_id" IS 'Identifier for the license associated with the component.';

COMMENT ON COLUMN "app_mgmt"."components"."description" IS 'Description of the component''s functionality.';

COMMENT ON COLUMN "app_mgmt"."components"."created_by_user_id" IS 'Identifier of the employee who initially created the component record.';

COMMENT ON COLUMN "app_mgmt"."components"."modified_by_user_id" IS 'Identifier of the employee who last modified the component record.';

COMMENT ON COLUMN "app_mgmt"."components"."package_info" IS 'Language-specific package information (e.g., Maven coordinates, npm package name, NuGet package ID).';

COMMENT ON COLUMN "app_mgmt"."components"."repository_url" IS 'Link to the component''s repository (e.g., Maven repository, npm registry, NuGet feed).';

COMMENT ON COLUMN "app_mgmt"."components"."namespace_or_module" IS 'Namespace or module name within the component (if applicable).';

COMMENT ON TABLE "app_mgmt"."component_dependencies" IS 'Table to store component dependencies (BOM relationships).';

COMMENT ON COLUMN "app_mgmt"."component_dependencies"."parent_component_id" IS 'Identifier for the component that depends on another component.';

COMMENT ON COLUMN "app_mgmt"."component_dependencies"."child_component_id" IS 'Identifier for the component being depended upon.';

COMMENT ON COLUMN "app_mgmt"."component_dependencies"."quantity" IS 'Number of times the child component is used by the parent.';

COMMENT ON COLUMN "app_mgmt"."component_dependencies"."dependency_type" IS 'Type of dependency (e.g., runtime, build, test).';

COMMENT ON TABLE "app_mgmt"."application_components" IS 'Table to store dependencies between applications and their software components.';

COMMENT ON COLUMN "app_mgmt"."application_components"."app_mgmt_application_id" IS 'Identifier for the application that uses the component.';

COMMENT ON COLUMN "app_mgmt"."application_components"."app_mgmt_component_id" IS 'Identifier for the software component used by the application.';

COMMENT ON COLUMN "app_mgmt"."application_components"."dependency_type" IS 'Type of dependency (e.g., runtime, build, test).';

COMMENT ON TABLE "app_mgmt"."application_relationships" IS 'Table to store relationships between applications and their criticality levels. Applications may have many relationships, even of the same type. They are only differentiated through the description.';

COMMENT ON COLUMN "app_mgmt"."application_relationships"."app_mgmt_application_relationship_id" IS 'Primary key for application relationships';

COMMENT ON COLUMN "app_mgmt"."application_relationships"."application_id_1" IS 'Identifier for the first application involved in the relationship.';

COMMENT ON COLUMN "app_mgmt"."application_relationships"."application_id_2" IS 'Identifier for the second application involved in the relationship.';

COMMENT ON COLUMN "app_mgmt"."application_relationships"."relationship_type" IS 'Type of relationship between the applications (e.g., depends on, uses data from).';

COMMENT ON COLUMN "app_mgmt"."application_relationships"."description" IS 'Additional explanation about nature of relationship.';

COMMENT ON COLUMN "app_mgmt"."application_relationships"."criticality" IS 'Criticality score of the relationship, indicating the impact of its failure.';

COMMENT ON TABLE "app_mgmt"."licenses" IS 'Table to store information about software licenses.';

COMMENT ON COLUMN "app_mgmt"."licenses"."app_mgmt_license_id" IS 'Unique identifier for a software license.';

COMMENT ON COLUMN "app_mgmt"."licenses"."license_name" IS 'Name of the software license.';

COMMENT ON COLUMN "app_mgmt"."licenses"."license_type" IS 'Type of software license (e.g., MIT, GPL).';

COMMENT ON COLUMN "app_mgmt"."licenses"."license_text" IS 'Full text or a summary of the software license terms.';

COMMENT ON TABLE "app_mgmt"."application_licenses" IS 'Table to store associations between applications and the licenses they use.';

COMMENT ON COLUMN "app_mgmt"."application_licenses"."app_mgmt_application_id" IS 'Identifier for the application that uses the license.';

COMMENT ON COLUMN "app_mgmt"."application_licenses"."app_mgmt_license_id" IS 'Identifier for the software license used by the application.';

COMMENT ON TABLE "app_mgmt"."teams" IS 'Table to store information about development and management teams, including team lead association.';

COMMENT ON COLUMN "app_mgmt"."teams"."app_mgmt_team_id" IS 'Unique identifier for a development or management team.';

COMMENT ON COLUMN "app_mgmt"."teams"."team_name" IS 'Name of the team.';

COMMENT ON COLUMN "app_mgmt"."teams"."description" IS 'Description of the team''s responsibilities.';

COMMENT ON COLUMN "app_mgmt"."teams"."team_lead_id" IS 'Identifier of the team lead from the enterprise associates table.';

COMMENT ON TABLE "app_mgmt"."team_members" IS 'Table to store the associations between teams and their members, including member functions.';

COMMENT ON COLUMN "app_mgmt"."team_members"."app_mgmt_team_id" IS 'Identifier of the team.';

COMMENT ON COLUMN "app_mgmt"."team_members"."enterprise_associate_id" IS 'Identifier of the team member from the enterprise associates table.';

COMMENT ON COLUMN "app_mgmt"."team_members"."function" IS 'Function or role of the team member within the team.';

COMMENT ON TABLE "credit_cards"."card_products" IS 'Defines credit card products offered by the institution';

COMMENT ON COLUMN "credit_cards"."card_products"."credit_cards_product_id" IS 'Auto-incrementing identifier for each card product';

COMMENT ON COLUMN "credit_cards"."card_products"."product_name" IS 'Marketing name of the card product';

COMMENT ON COLUMN "credit_cards"."card_products"."product_code" IS 'Internal code identifying the card product';

COMMENT ON COLUMN "credit_cards"."card_products"."card_network" IS 'Card network (Visa, Mastercard, Amex, Discover)';

COMMENT ON COLUMN "credit_cards"."card_products"."card_type" IS 'Type of card (Debit, Credit, Prepaid, Charge)';

COMMENT ON COLUMN "credit_cards"."card_products"."card_tier" IS 'Card tier (Standard, Gold, Platinum, etc.)';

COMMENT ON COLUMN "credit_cards"."card_products"."is_secured" IS 'Whether card requires a security deposit';

COMMENT ON COLUMN "credit_cards"."card_products"."annual_fee" IS 'Annual fee for the card';

COMMENT ON COLUMN "credit_cards"."card_products"."is_annual_fee_waived_first_year" IS 'Whether annual fee is waived first year';

COMMENT ON COLUMN "credit_cards"."card_products"."base_interest_rate" IS 'Standard purchase APR (annual percentage rate)';

COMMENT ON COLUMN "credit_cards"."card_products"."cash_advance_rate" IS 'APR for cash advances';

COMMENT ON COLUMN "credit_cards"."card_products"."penalty_rate" IS 'Penalty APR applied after late payments';

COMMENT ON COLUMN "credit_cards"."card_products"."balance_transfer_rate" IS 'APR for balance transfers';

COMMENT ON COLUMN "credit_cards"."card_products"."intro_rate" IS 'Introductory APR if offered';

COMMENT ON COLUMN "credit_cards"."card_products"."intro_rate_period_months" IS 'Duration of introductory rate';

COMMENT ON COLUMN "credit_cards"."card_products"."grace_period_days" IS 'Interest-free grace period in days';

COMMENT ON COLUMN "credit_cards"."card_products"."min_credit_score" IS 'Minimum credit score typically required';

COMMENT ON COLUMN "credit_cards"."card_products"."min_credit_limit" IS 'Minimum credit limit offered';

COMMENT ON COLUMN "credit_cards"."card_products"."max_credit_limit" IS 'Maximum credit limit offered';

COMMENT ON COLUMN "credit_cards"."card_products"."reward_program" IS 'Description of reward program if any';

COMMENT ON COLUMN "credit_cards"."card_products"."base_reward_rate" IS 'Base reward earning rate (e.g., 1.5% cashback)';

COMMENT ON COLUMN "credit_cards"."card_products"."foreign_transaction_fee" IS 'Fee percentage for foreign transactions';

COMMENT ON COLUMN "credit_cards"."card_products"."late_payment_fee" IS 'Fee charged for late payments';

COMMENT ON COLUMN "credit_cards"."card_products"."overlimit_fee" IS 'Fee charged for exceeding credit limit';

COMMENT ON COLUMN "credit_cards"."card_products"."cash_advance_fee_percent" IS 'Percentage fee for cash advances';

COMMENT ON COLUMN "credit_cards"."card_products"."cash_advance_fee_min" IS 'Minimum fee amount for cash advances';

COMMENT ON COLUMN "credit_cards"."card_products"."balance_transfer_fee_percent" IS 'Percentage fee for balance transfers';

COMMENT ON COLUMN "credit_cards"."card_products"."balance_transfer_fee_min" IS 'Minimum fee amount for balance transfers';

COMMENT ON COLUMN "credit_cards"."card_products"."return_payment_fee" IS 'Fee charged for returned payments';

COMMENT ON COLUMN "credit_cards"."card_products"."is_active" IS 'Whether product is currently offered';

COMMENT ON COLUMN "credit_cards"."card_products"."launch_date" IS 'Date when product was launched';

COMMENT ON COLUMN "credit_cards"."card_products"."discontinue_date" IS 'Date when product was discontinued if applicable';

COMMENT ON COLUMN "credit_cards"."card_products"."terms_and_conditions_url" IS 'URL to terms and conditions document';

COMMENT ON COLUMN "credit_cards"."card_products"."image_url" IS 'URL to card image for marketing';

COMMENT ON TABLE "credit_cards"."fraud_cases" IS 'Tracks fraud cases related to card accounts';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."credit_cards_case_id" IS 'Auto-incrementing identifier for each fraud case';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."credit_cards_card_id" IS 'Reference to specific card if applicable';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."report_date" IS 'Date and time fraud was reported';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."case_type" IS 'Type of fraud (Card Fraud, Account Takeover, Application Fraud)';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."status" IS 'Status of case (Open, Investigation, Closed)';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."reported_by" IS 'Who reported fraud (Customer, Bank, Merchant)';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."description" IS 'Description of fraud incident';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."total_disputed_amount" IS 'Total amount of fraudulent transactions';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."provisional_credit_issued" IS 'Whether provisional credit was issued';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."resolution" IS 'Final resolution of case';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."resolution_date" IS 'Date case was resolved';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."new_card_issued" IS 'Whether replacement card was issued';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."police_report_filed" IS 'Whether police report was filed';

COMMENT ON COLUMN "credit_cards"."fraud_cases"."investigator_id" IS 'User ID of fraud investigator';

COMMENT ON TABLE "credit_cards"."fraud_transactions" IS 'Junction table linking fraud cases to specific transactions';

COMMENT ON COLUMN "credit_cards"."fraud_transactions"."credit_cards_fraud_transaction_id" IS 'Auto-incrementing identifier for each linked transaction';

COMMENT ON COLUMN "credit_cards"."fraud_transactions"."credit_cards_case_id" IS 'Reference to fraud_cases';

COMMENT ON COLUMN "credit_cards"."fraud_transactions"."credit_cards_transaction_id" IS 'Reference to transactions';

COMMENT ON COLUMN "credit_cards"."fraud_transactions"."is_confirmed_fraud" IS 'Whether transaction is confirmed fraudulent';

COMMENT ON TABLE "credit_cards"."security_blocks" IS 'Tracks security blocks placed on cards';

COMMENT ON COLUMN "credit_cards"."security_blocks"."credit_cards_block_id" IS 'Auto-incrementing identifier for each security block';

COMMENT ON COLUMN "credit_cards"."security_blocks"."credit_cards_card_id" IS 'Reference to specific card';

COMMENT ON COLUMN "credit_cards"."security_blocks"."block_type" IS 'Type of block (Temporary, Permanent, Geographic)';

COMMENT ON COLUMN "credit_cards"."security_blocks"."reason" IS 'Reason for security block';

COMMENT ON COLUMN "credit_cards"."security_blocks"."start_date" IS 'When block began';

COMMENT ON COLUMN "credit_cards"."security_blocks"."end_date" IS 'When block ends if temporary';

COMMENT ON COLUMN "credit_cards"."security_blocks"."geographic_restriction" IS 'Geographic area blocked if applicable';

COMMENT ON COLUMN "credit_cards"."security_blocks"."transaction_type_restricted" IS 'Transaction types blocked if specific';

COMMENT ON COLUMN "credit_cards"."security_blocks"."requested_by" IS 'Who requested the block (Customer, Bank, Fraud System)';

COMMENT ON COLUMN "credit_cards"."security_blocks"."status" IS 'Status of block (Active, Removed)';

COMMENT ON COLUMN "credit_cards"."security_blocks"."removed_by_id" IS 'User who removed the block';

COMMENT ON COLUMN "credit_cards"."security_blocks"."removed_date" IS 'When block was removed';

COMMENT ON TABLE "credit_cards"."credit_card_applications_hmda" IS 'Regulatory reporting data for credit card applications under HMDA';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."credit_cards_record_id" IS 'Auto-incrementing identifier for each HMDA record';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."credit_cards_application_id" IS 'Reference to applications';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."reporting_year" IS 'Year for HMDA reporting';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."ethnicity" IS 'Applicant''s ethnicity per HMDA categories';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."race" IS 'Applicant''s race per HMDA categories';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."sex" IS 'Applicant''s sex per HMDA categories';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."age" IS 'Applicant''s age at time of application';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."income" IS 'Applicant''s annual income in thousands';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."rate_spread" IS 'Difference between APR and average prime offer rate';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."hoepa_status" IS 'Whether subject to HOEPA (Yes, No)';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."action_taken" IS 'Final disposition (Approved, Denied, etc.)';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."action_taken_date" IS 'Date of final action';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."denial_reason1" IS 'Primary reason for denial if applicable';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."denial_reason2" IS 'Secondary reason for denial if applicable';

COMMENT ON COLUMN "credit_cards"."credit_card_applications_hmda"."submission_status" IS 'Status of HMDA submission';

COMMENT ON TABLE "credit_cards"."reg_z_credit_card_disclosures" IS 'Tracks Truth in Lending Act disclosures required for credit cards';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."credit_cards_disclosure_id" IS 'Auto-incrementing identifier for each disclosure';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."credit_cards_application_id" IS 'Reference to applications if pre-account opening';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."credit_cards_card_account_id" IS 'Reference to card_accounts if post-account opening';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."disclosure_type" IS 'Type of Reg Z disclosure (Solicitation, Application, Account-Opening, Periodic Statement)';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."disclosure_date" IS 'Date disclosure was generated';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."delivery_method" IS 'How disclosure was delivered (Mail, Electronic)';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."annual_percentage_rate" IS 'APR disclosed';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."variable_rate_indicator" IS 'Whether rate is variable';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."annual_fee" IS 'Annual fee disclosed';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."transaction_fee_purchases" IS 'Fee for purchases if any';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."transaction_fee_balance_transfers" IS 'Fee for balance transfers';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."transaction_fee_cash_advance" IS 'Fee for cash advances';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."late_payment_fee" IS 'Late payment fee disclosed';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."over_limit_fee" IS 'Over-limit fee disclosed';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."grace_period_disclosure" IS 'Grace period disclosure text';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."balance_computation_method" IS 'Method used to calculate balance';

COMMENT ON COLUMN "credit_cards"."reg_z_credit_card_disclosures"."document_path" IS 'Path to stored disclosure document';

COMMENT ON TABLE "credit_cards"."ability_to_pay_assessments" IS 'Documents ability to pay assessments required by Reg Z';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."credit_cards_assessment_id" IS 'Auto-incrementing identifier for each assessment';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."credit_cards_application_id" IS 'Reference to applications';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."assessment_date" IS 'Date of ability to pay assessment';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."income_verified" IS 'Whether income was verified';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."income_source" IS 'Source of income verification';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."income_amount" IS 'Income amount used in assessment';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."debt_obligations" IS 'Existing debt obligations considered';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."living_expenses" IS 'Basic living expenses considered';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."dti_ratio" IS 'Debt-to-income ratio calculated';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."max_supportable_payment" IS 'Maximum monthly payment calculated as supportable';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."passed_assessment" IS 'Whether applicant passed ability to pay test';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."performed_by_id" IS 'User who performed assessment';

COMMENT ON COLUMN "credit_cards"."ability_to_pay_assessments"."notes" IS 'Additional assessment notes';

COMMENT ON TABLE "credit_cards"."consumer_complaints" IS 'Tracks customer complaints about credit card accounts';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."credit_cards_complaint_id" IS 'Auto-incrementing identifier for each complaint';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."receipt_date" IS 'Date complaint was received';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."source" IS 'Source of complaint (Direct, CFPB, BBB, Social Media)';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."complaint_type" IS 'Type of complaint (Billing, Fees, Interest, Customer Service)';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."issue" IS 'Specific issue raised';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."description" IS 'Detailed description of complaint';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."status" IS 'Status of complaint (New, In Progress, Resolved)';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."response_sent_date" IS 'Date response was sent to consumer';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."resolution" IS 'Description of how complaint was resolved';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."resolution_date" IS 'Date complaint was resolved';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."cfpb_case_number" IS 'CFPB case number if applicable';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."monetary_relief_amount" IS 'Amount of monetary relief provided';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."regulatory_violation_found" IS 'Whether regulatory violation was identified';

COMMENT ON COLUMN "credit_cards"."consumer_complaints"."regulation_violated" IS 'Specific regulation violated if applicable';

COMMENT ON TABLE "credit_cards"."card_product_features" IS 'Stores features and benefits associated with card products';

COMMENT ON COLUMN "credit_cards"."card_product_features"."credit_cards_feature_id" IS 'Auto-incrementing identifier for each feature';

COMMENT ON COLUMN "credit_cards"."card_product_features"."credit_cards_product_id" IS 'Reference to card_products';

COMMENT ON COLUMN "credit_cards"."card_product_features"."feature_name" IS 'Name of the feature';

COMMENT ON COLUMN "credit_cards"."card_product_features"."feature_description" IS 'Detailed description of the feature';

COMMENT ON COLUMN "credit_cards"."card_product_features"."is_premium" IS 'Whether this is a premium feature';

COMMENT ON COLUMN "credit_cards"."card_product_features"."is_limited_time" IS 'Whether feature is limited-time offer';

COMMENT ON COLUMN "credit_cards"."card_product_features"."start_date" IS 'When feature becomes available';

COMMENT ON COLUMN "credit_cards"."card_product_features"."end_date" IS 'When feature expires if limited time';

COMMENT ON TABLE "credit_cards"."card_product_reward_categories" IS 'Defines reward earning categories for card products';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."credit_cards_category_id" IS 'Auto-incrementing identifier for each reward category';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."credit_cards_product_id" IS 'Reference to card_products';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."category_name" IS 'Category name (e.g., Dining, Travel, Gas)';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."reward_rate" IS 'Reward rate for this category (e.g., 3% cashback)';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."is_quarterly" IS 'Whether category rotates quarterly';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."is_capped" IS 'Whether rewards are capped';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."cap_amount" IS 'Spending cap for elevated rewards if applicable';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."cap_period" IS 'Period for cap (e.g., Monthly, Quarterly, Annually)';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."start_date" IS 'Start date for category if temporary';

COMMENT ON COLUMN "credit_cards"."card_product_reward_categories"."end_date" IS 'End date for category if temporary';

COMMENT ON TABLE "credit_cards"."applications" IS 'Stores credit card applications and their status';

COMMENT ON COLUMN "credit_cards"."applications"."credit_cards_application_id" IS 'Unique identifier for card application';

COMMENT ON COLUMN "credit_cards"."applications"."customer_id" IS 'Reference to enterprise.accounts';

COMMENT ON COLUMN "credit_cards"."applications"."credit_cards_product_id" IS 'Reference to card_products';

COMMENT ON COLUMN "credit_cards"."applications"."application_date" IS 'When application was submitted';

COMMENT ON COLUMN "credit_cards"."applications"."application_channel" IS 'Channel used for application (Online, Branch, Mail, Phone)';

COMMENT ON COLUMN "credit_cards"."applications"."status" IS 'Current status (Pending, Approved, Denied, Canceled)';

COMMENT ON COLUMN "credit_cards"."applications"."requested_credit_limit" IS 'Credit limit requested by applicant';

COMMENT ON COLUMN "credit_cards"."applications"."approved_credit_limit" IS 'Credit limit approved by issuer';

COMMENT ON COLUMN "credit_cards"."applications"."approved_interest_rate" IS 'Interest rate approved for account';

COMMENT ON COLUMN "credit_cards"."applications"."decision_date" IS 'When decision was made';

COMMENT ON COLUMN "credit_cards"."applications"."decision_method" IS 'Automated or Manual decision';

COMMENT ON COLUMN "credit_cards"."applications"."decision_reason" IS 'Primary reason for decision';

COMMENT ON COLUMN "credit_cards"."applications"."offer_code" IS 'Promotional offer code if applicable';

COMMENT ON COLUMN "credit_cards"."applications"."referring_source" IS 'Marketing source or referral';

COMMENT ON COLUMN "credit_cards"."applications"."is_preapproved" IS 'Whether application was pre-approved';

COMMENT ON COLUMN "credit_cards"."applications"."is_secured" IS 'Whether card requires security deposit';

COMMENT ON COLUMN "credit_cards"."applications"."security_deposit_amount" IS 'Amount of security deposit if secured card';

COMMENT ON COLUMN "credit_cards"."applications"."balance_transfer_requested" IS 'Whether balance transfer was requested';

COMMENT ON COLUMN "credit_cards"."applications"."authorized_users_requested" IS 'Number of authorized users requested';

COMMENT ON COLUMN "credit_cards"."applications"."annual_income" IS 'Applicant''s reported annual income';

COMMENT ON COLUMN "credit_cards"."applications"."housing_payment" IS 'Applicant''s monthly housing payment';

COMMENT ON COLUMN "credit_cards"."applications"."employment_status" IS 'Applicant''s employment status';

COMMENT ON COLUMN "credit_cards"."applications"."approval_expiration_date" IS 'Date when approval expires if not accepted';

COMMENT ON COLUMN "credit_cards"."applications"."time_at_current_address_years" IS 'Years at current address';

COMMENT ON TABLE "credit_cards"."card_accounts" IS 'Stores credit card accounts and their current status';

COMMENT ON COLUMN "credit_cards"."card_accounts"."credit_cards_card_account_id" IS 'Unique identifier for card account';

COMMENT ON COLUMN "credit_cards"."card_accounts"."customer_id" IS 'Reference to enterprise.accounts';

COMMENT ON COLUMN "credit_cards"."card_accounts"."enterprise_account_id" IS 'Reference to enterprise.accounts - the main account record';

COMMENT ON COLUMN "credit_cards"."card_accounts"."credit_cards_product_id" IS 'Reference to card_products';

COMMENT ON COLUMN "credit_cards"."card_accounts"."credit_cards_application_id" IS 'Reference to original application if applicable';

COMMENT ON COLUMN "credit_cards"."card_accounts"."account_number" IS 'Masked account number';

COMMENT ON COLUMN "credit_cards"."card_accounts"."opened_date" IS 'When account was opened';

COMMENT ON COLUMN "credit_cards"."card_accounts"."status" IS 'Account status (Active, Inactive, Closed, Suspended)';

COMMENT ON COLUMN "credit_cards"."card_accounts"."status_update_date_time" IS 'When the status was last updated';

COMMENT ON COLUMN "credit_cards"."card_accounts"."credit_limit" IS 'Current approved credit limit';

COMMENT ON COLUMN "credit_cards"."card_accounts"."available_credit" IS 'Current available credit';

COMMENT ON COLUMN "credit_cards"."card_accounts"."cash_advance_limit" IS 'Limit for cash advances if different';

COMMENT ON COLUMN "credit_cards"."card_accounts"."current_balance" IS 'Current outstanding balance';

COMMENT ON COLUMN "credit_cards"."card_accounts"."statement_balance" IS 'Balance as of last statement';

COMMENT ON COLUMN "credit_cards"."card_accounts"."minimum_payment_due" IS 'Minimum payment due';

COMMENT ON COLUMN "credit_cards"."card_accounts"."payment_due_date" IS 'Date payment is due';

COMMENT ON COLUMN "credit_cards"."card_accounts"."last_payment_date" IS 'Date of last payment received';

COMMENT ON COLUMN "credit_cards"."card_accounts"."last_payment_amount" IS 'Amount of last payment received';

COMMENT ON COLUMN "credit_cards"."card_accounts"."purchase_interest_rate" IS 'Current purchase APR';

COMMENT ON COLUMN "credit_cards"."card_accounts"."cash_advance_interest_rate" IS 'Current cash advance APR';

COMMENT ON COLUMN "credit_cards"."card_accounts"."balance_transfer_interest_rate" IS 'Current balance transfer APR';

COMMENT ON COLUMN "credit_cards"."card_accounts"."penalty_interest_rate" IS 'Current penalty APR if applicable';

COMMENT ON COLUMN "credit_cards"."card_accounts"."intro_rate_expiration_date" IS 'When introductory rate expires';

COMMENT ON COLUMN "credit_cards"."card_accounts"."days_past_due" IS 'Current days past due';

COMMENT ON COLUMN "credit_cards"."card_accounts"."times_past_due_30_days" IS 'Count of 30+ day late payments';

COMMENT ON COLUMN "credit_cards"."card_accounts"."times_past_due_60_days" IS 'Count of 60+ day late payments';

COMMENT ON COLUMN "credit_cards"."card_accounts"."times_past_due_90_days" IS 'Count of 90+ day late payments';

COMMENT ON COLUMN "credit_cards"."card_accounts"."overlimit_status" IS 'Whether account is over limit';

COMMENT ON COLUMN "credit_cards"."card_accounts"."reward_points_balance" IS 'Current reward points/cashback balance';

COMMENT ON COLUMN "credit_cards"."card_accounts"."is_secured" IS 'Whether account is secured';

COMMENT ON COLUMN "credit_cards"."card_accounts"."security_deposit_amount" IS 'Amount of security deposit if secured';

COMMENT ON COLUMN "credit_cards"."card_accounts"."annual_fee_next_charge_date" IS 'Next date annual fee will be charged';

COMMENT ON COLUMN "credit_cards"."card_accounts"."cycle_cut_day" IS 'Day of month when billing cycle closes';

COMMENT ON TABLE "credit_cards"."cards" IS 'Stores information about physical and virtual cards issued for accounts';

COMMENT ON COLUMN "credit_cards"."cards"."credit_cards_card_id" IS 'Auto-incrementing identifier for each physical card';

COMMENT ON COLUMN "credit_cards"."cards"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."cards"."card_number" IS 'Masked card number (last 4 digits only)';

COMMENT ON COLUMN "credit_cards"."cards"."user_type" IS 'Primary or Authorized User';

COMMENT ON COLUMN "credit_cards"."cards"."user_id" IS 'Reference to parties.party_id of cardholder';

COMMENT ON COLUMN "credit_cards"."cards"."card_status" IS 'Active, Inactive, Lost, Stolen, Expired, Replaced';

COMMENT ON COLUMN "credit_cards"."cards"."issue_date" IS 'When card was issued';

COMMENT ON COLUMN "credit_cards"."cards"."activation_date" IS 'When card was activated';

COMMENT ON COLUMN "credit_cards"."cards"."expiration_date" IS 'When card expires';

COMMENT ON COLUMN "credit_cards"."cards"."card_design" IS 'Design/style of physical card';

COMMENT ON COLUMN "credit_cards"."cards"."is_virtual" IS 'Whether card is virtual only';

COMMENT ON COLUMN "credit_cards"."cards"."digital_wallet_enabled" IS 'Whether added to digital wallet';

COMMENT ON COLUMN "credit_cards"."cards"."pin_set" IS 'Whether PIN has been set';

COMMENT ON COLUMN "credit_cards"."cards"."temporary_limits" IS 'Temporary spending limits if any';

COMMENT ON COLUMN "credit_cards"."cards"."temporary_limits_expiry" IS 'When temporary limits expire';

COMMENT ON TABLE "credit_cards"."authorized_users" IS 'Tracks authorized users who can use the account';

COMMENT ON COLUMN "credit_cards"."authorized_users"."credit_cards_authorized_user_id" IS 'Auto-incrementing identifier for each authorized user';

COMMENT ON COLUMN "credit_cards"."authorized_users"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."authorized_users"."enterprise_party_id" IS 'Reference to parties.party_id';

COMMENT ON COLUMN "credit_cards"."authorized_users"."relationship" IS 'Relationship to primary cardholder';

COMMENT ON COLUMN "credit_cards"."authorized_users"."status" IS 'Status of authorized user (Active, Removed)';

COMMENT ON COLUMN "credit_cards"."authorized_users"."add_date" IS 'When user was added';

COMMENT ON COLUMN "credit_cards"."authorized_users"."remove_date" IS 'When user was removed if applicable';

COMMENT ON COLUMN "credit_cards"."authorized_users"."spending_limit" IS 'Custom spending limit if applicable';

COMMENT ON COLUMN "credit_cards"."authorized_users"."limit_period" IS 'Period for limit (Daily, Monthly, etc.)';

COMMENT ON TABLE "credit_cards"."transactions" IS 'Stores all transaction activity on card accounts';

COMMENT ON COLUMN "credit_cards"."transactions"."credit_cards_transaction_id" IS 'Unique identifier for transaction';

COMMENT ON COLUMN "credit_cards"."transactions"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."transactions"."credit_cards_card_id" IS 'Reference to specific card used';

COMMENT ON COLUMN "credit_cards"."transactions"."transaction_date" IS 'Date and time of transaction';

COMMENT ON COLUMN "credit_cards"."transactions"."post_date" IS 'Date transaction posted to account';

COMMENT ON COLUMN "credit_cards"."transactions"."transaction_type" IS 'Purchase, Cash Advance, Balance Transfer, Payment, Fee, Adjustment';

COMMENT ON COLUMN "credit_cards"."transactions"."amount" IS 'Transaction amount';

COMMENT ON COLUMN "credit_cards"."transactions"."description" IS 'Merchant name or transaction description';

COMMENT ON COLUMN "credit_cards"."transactions"."category" IS 'Spending category (e.g., Dining, Travel, Merchandise)';

COMMENT ON COLUMN "credit_cards"."transactions"."mcc_code" IS 'Merchant Category Code';

COMMENT ON COLUMN "credit_cards"."transactions"."is_international" IS 'Whether transaction is international';

COMMENT ON COLUMN "credit_cards"."transactions"."original_currency" IS 'Original currency if international';

COMMENT ON COLUMN "credit_cards"."transactions"."original_amount" IS 'Amount in original currency if international';

COMMENT ON COLUMN "credit_cards"."transactions"."exchange_rate" IS 'Exchange rate used if international';

COMMENT ON COLUMN "credit_cards"."transactions"."is_recurring" IS 'Whether transaction appears to be recurring';

COMMENT ON COLUMN "credit_cards"."transactions"."auth_code" IS 'Authorization code';

COMMENT ON COLUMN "credit_cards"."transactions"."reference_number" IS 'Transaction reference number';

COMMENT ON COLUMN "credit_cards"."transactions"."is_pending" IS 'Whether transaction is pending';

COMMENT ON COLUMN "credit_cards"."transactions"."status" IS 'Approved, Declined, Reversed, Disputed';

COMMENT ON COLUMN "credit_cards"."transactions"."decline_reason" IS 'Reason for decline if applicable';

COMMENT ON COLUMN "credit_cards"."transactions"."rewards_earned" IS 'Rewards points or cashback earned';

COMMENT ON COLUMN "credit_cards"."transactions"."is_billable" IS 'Whether transaction is included in statement billing';

COMMENT ON TABLE "credit_cards"."statements" IS 'Stores monthly billing statements for card accounts';

COMMENT ON COLUMN "credit_cards"."statements"."credit_cards_statement_id" IS 'Auto-incrementing identifier for each statement';

COMMENT ON COLUMN "credit_cards"."statements"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."statements"."statement_date" IS 'Date statement was generated';

COMMENT ON COLUMN "credit_cards"."statements"."statement_period_start" IS 'Start date for statement period';

COMMENT ON COLUMN "credit_cards"."statements"."statement_period_end" IS 'End date for statement period';

COMMENT ON COLUMN "credit_cards"."statements"."due_date" IS 'Payment due date';

COMMENT ON COLUMN "credit_cards"."statements"."previous_balance" IS 'Balance carried over from previous statement';

COMMENT ON COLUMN "credit_cards"."statements"."new_charges" IS 'New purchases and charges';

COMMENT ON COLUMN "credit_cards"."statements"."cash_advances" IS 'Cash advances in period';

COMMENT ON COLUMN "credit_cards"."statements"."balance_transfers" IS 'Balance transfers in period';

COMMENT ON COLUMN "credit_cards"."statements"."payments" IS 'Payments received in period';

COMMENT ON COLUMN "credit_cards"."statements"."credits" IS 'Credits/refunds in period';

COMMENT ON COLUMN "credit_cards"."statements"."fees" IS 'Fees charged in period';

COMMENT ON COLUMN "credit_cards"."statements"."interest" IS 'Interest charged in period';

COMMENT ON COLUMN "credit_cards"."statements"."ending_balance" IS 'Ending statement balance';

COMMENT ON COLUMN "credit_cards"."statements"."minimum_payment" IS 'Minimum payment due';

COMMENT ON COLUMN "credit_cards"."statements"."payment_received" IS 'Whether payment was received by due date';

COMMENT ON COLUMN "credit_cards"."statements"."payment_received_date" IS 'Date payment was received';

COMMENT ON COLUMN "credit_cards"."statements"."payment_received_amount" IS 'Amount of payment received';

COMMENT ON COLUMN "credit_cards"."statements"."days_in_billing_cycle" IS 'Number of days in billing cycle';

COMMENT ON COLUMN "credit_cards"."statements"."document_path" IS 'Path to stored statement document';

COMMENT ON TABLE "credit_cards"."fees" IS 'Tracks fees charged to card accounts';

COMMENT ON COLUMN "credit_cards"."fees"."credit_cards_fee_id" IS 'Auto-incrementing identifier for each fee';

COMMENT ON COLUMN "credit_cards"."fees"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."fees"."credit_cards_transaction_id" IS 'Reference to transactions if associated with specific transaction';

COMMENT ON COLUMN "credit_cards"."fees"."fee_type" IS 'Type of fee (Annual, Late Payment, Cash Advance, Foreign Transaction, etc.)';

COMMENT ON COLUMN "credit_cards"."fees"."amount" IS 'Fee amount';

COMMENT ON COLUMN "credit_cards"."fees"."description" IS 'Description of fee';

COMMENT ON COLUMN "credit_cards"."fees"."date_assessed" IS 'Date fee was charged';

COMMENT ON COLUMN "credit_cards"."fees"."waived" IS 'Whether fee was waived';

COMMENT ON COLUMN "credit_cards"."fees"."waiver_reason" IS 'Reason fee was waived if applicable';

COMMENT ON COLUMN "credit_cards"."fees"."credit_cards_statement_id" IS 'Reference to statements if included in statement';

COMMENT ON TABLE "credit_cards"."interest_charges" IS 'Tracks interest charges applied to card accounts';

COMMENT ON COLUMN "credit_cards"."interest_charges"."credit_cards_charge_id" IS 'Auto-incrementing identifier for each interest charge';

COMMENT ON COLUMN "credit_cards"."interest_charges"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."interest_charges"."interest_type" IS 'Type of interest (Purchase, Cash Advance, Balance Transfer, Penalty)';

COMMENT ON COLUMN "credit_cards"."interest_charges"."balance_subject_to_interest" IS 'Balance amount subject to interest';

COMMENT ON COLUMN "credit_cards"."interest_charges"."interest_rate" IS 'Interest rate applied';

COMMENT ON COLUMN "credit_cards"."interest_charges"."days_in_period" IS 'Number of days interest was calculated for';

COMMENT ON COLUMN "credit_cards"."interest_charges"."amount" IS 'Interest amount charged';

COMMENT ON COLUMN "credit_cards"."interest_charges"."date_assessed" IS 'Date interest was charged';

COMMENT ON COLUMN "credit_cards"."interest_charges"."credit_cards_statement_id" IS 'Reference to statements';

COMMENT ON TABLE "credit_cards"."rewards" IS 'Tracks reward earning and redemption activity';

COMMENT ON COLUMN "credit_cards"."rewards"."credit_cards_reward_id" IS 'Auto-incrementing identifier for each reward record';

COMMENT ON COLUMN "credit_cards"."rewards"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."rewards"."credit_cards_transaction_id" IS 'Reference to transactions if earned from transaction';

COMMENT ON COLUMN "credit_cards"."rewards"."reward_type" IS 'Type of reward (Points, Cashback, Miles)';

COMMENT ON COLUMN "credit_cards"."rewards"."amount" IS 'Amount of reward earned or redeemed';

COMMENT ON COLUMN "credit_cards"."rewards"."event_type" IS 'Earned, Bonus, Redeemed, Expired, Adjusted';

COMMENT ON COLUMN "credit_cards"."rewards"."description" IS 'Description of reward activity';

COMMENT ON COLUMN "credit_cards"."rewards"."category" IS 'Category associated with reward if applicable';

COMMENT ON COLUMN "credit_cards"."rewards"."date_earned" IS 'Date reward was earned or redeemed';

COMMENT ON COLUMN "credit_cards"."rewards"."expiration_date" IS 'Date reward will expire if applicable';

COMMENT ON TABLE "credit_cards"."reward_redemptions" IS 'Stores details of reward point redemptions';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."credit_cards_redemption_id" IS 'Auto-incrementing identifier for each redemption';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."redemption_date" IS 'Date and time of redemption';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."redemption_type" IS 'Type of redemption (Cashback, Travel, Gift Card, Merchandise, Statement Credit)';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."points_redeemed" IS 'Number of points redeemed';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."cash_value" IS 'Cash value of redemption';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."description" IS 'Description of redemption';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."status" IS 'Status of redemption (Pending, Completed, Canceled)';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."confirmation_code" IS 'Confirmation code for redemption';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."shipping_address_id" IS 'Reference to addresses if physical item';

COMMENT ON COLUMN "credit_cards"."reward_redemptions"."recipient_email" IS 'Email for digital items if applicable';

COMMENT ON TABLE "credit_cards"."promotional_offers" IS 'Tracks promotional offers made to cardholders';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."credit_cards_offer_id" IS 'Auto-incrementing identifier for each offer';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."offer_type" IS 'Type of offer (Balance Transfer, Cash Advance, Credit Limit Increase, etc.)';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."description" IS 'Description of offer';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."offer_date" IS 'Date offer was made';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."expiration_date" IS 'Date offer expires';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."interest_rate" IS 'Interest rate associated with offer';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."fee_percentage" IS 'Fee percentage associated with offer';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."status" IS 'Status of offer (Active, Accepted, Declined, Expired)';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."response_date" IS 'Date customer responded to offer';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."amount_offered" IS 'Amount of credit offered if applicable';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."promo_code" IS 'Promotional code associated with offer';

COMMENT ON COLUMN "credit_cards"."promotional_offers"."terms_and_conditions" IS 'Terms and conditions of offer';

COMMENT ON TABLE "credit_cards"."balance_transfers" IS 'Tracks balance transfers from other creditors';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."credit_cards_transfer_id" IS 'Auto-incrementing identifier for each balance transfer';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."credit_cards_transaction_id" IS 'Reference to transactions';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."credit_cards_offer_id" IS 'Reference to promotional_offers if applicable';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."creditor_name" IS 'Name of creditor being paid';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."account_number" IS 'Account number at other creditor, masked';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."transfer_amount" IS 'Amount transferred';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."fee_amount" IS 'Fee charged for transfer';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."interest_rate" IS 'Interest rate applied to transfer';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."promotional_rate" IS 'Whether rate is promotional';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."promotion_end_date" IS 'When promotional rate ends if applicable';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."request_date" IS 'When transfer was requested';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."status" IS 'Status of transfer (Pending, Completed, Rejected)';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."completion_date" IS 'When transfer was completed';

COMMENT ON COLUMN "credit_cards"."balance_transfers"."current_balance" IS 'Current balance remaining from transfer';

COMMENT ON TABLE "credit_cards"."payment_methods" IS 'Stores payment methods for card account payments';

COMMENT ON COLUMN "credit_cards"."payment_methods"."credit_cards_payment_method_id" IS 'Auto-incrementing identifier for each payment method';

COMMENT ON COLUMN "credit_cards"."payment_methods"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."payment_methods"."payment_type" IS 'Type of payment method (Bank Account, Debit Card, Check)';

COMMENT ON COLUMN "credit_cards"."payment_methods"."nickname" IS 'User-assigned nickname for payment method';

COMMENT ON COLUMN "credit_cards"."payment_methods"."status" IS 'Status of payment method (Active, Inactive, Removed)';

COMMENT ON COLUMN "credit_cards"."payment_methods"."is_default" IS 'Whether this is the default payment method';

COMMENT ON COLUMN "credit_cards"."payment_methods"."bank_name" IS 'Name of the bank if applicable';

COMMENT ON COLUMN "credit_cards"."payment_methods"."account_type" IS 'Checking or Savings if bank account';

COMMENT ON COLUMN "credit_cards"."payment_methods"."account_number" IS 'Masked account number';

COMMENT ON COLUMN "credit_cards"."payment_methods"."routing_number" IS 'Routing number if bank account';

COMMENT ON COLUMN "credit_cards"."payment_methods"."expiration_date" IS 'Expiration date if debit card';

COMMENT ON COLUMN "credit_cards"."payment_methods"."verification_status" IS 'Status of verification (Verified, Pending, Failed)';

COMMENT ON TABLE "credit_cards"."autopay_settings" IS 'Stores automatic payment settings';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."credit_cards_autopay_id" IS 'Auto-incrementing identifier for each autopay setup';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."credit_cards_payment_method_id" IS 'Reference to payment_methods';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."status" IS 'Status of autopay (Active, Inactive)';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."payment_option" IS 'What to pay (Minimum, Statement Balance, Current Balance, Fixed Amount)';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."fixed_amount" IS 'Fixed amount if applicable';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."payment_day" IS 'When to pay (Due Date, Days Before Due Date, Specific Day)';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."days_before_due" IS 'Days before due date if applicable';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."specific_day" IS 'Specific day of month if applicable';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."start_date" IS 'When autopay begins';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."end_date" IS 'When autopay ends if applicable';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."last_payment_date" IS 'Date of last autopay payment';

COMMENT ON COLUMN "credit_cards"."autopay_settings"."next_payment_date" IS 'Scheduled date of next payment';

COMMENT ON TABLE "credit_cards"."credit_limit_changes" IS 'Tracks history of credit limit changes';

COMMENT ON COLUMN "credit_cards"."credit_limit_changes"."credit_cards_change_id" IS 'Auto-incrementing identifier for each limit change';

COMMENT ON COLUMN "credit_cards"."credit_limit_changes"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."credit_limit_changes"."change_date" IS 'Date of credit limit change';

COMMENT ON COLUMN "credit_cards"."credit_limit_changes"."previous_limit" IS 'Credit limit before change';

COMMENT ON COLUMN "credit_cards"."credit_limit_changes"."new_limit" IS 'Credit limit after change';

COMMENT ON COLUMN "credit_cards"."credit_limit_changes"."change_reason" IS 'Reason for limit change';

COMMENT ON COLUMN "credit_cards"."credit_limit_changes"."requested_by" IS 'Who requested change (Customer, Bank)';

COMMENT ON COLUMN "credit_cards"."credit_limit_changes"."approved_by_id" IS 'User who approved change';

COMMENT ON TABLE "credit_cards"."card_alerts" IS 'Stores customer alert preferences';

COMMENT ON COLUMN "credit_cards"."card_alerts"."credit_cards_alert_id" IS 'Auto-incrementing identifier for each alert';

COMMENT ON COLUMN "credit_cards"."card_alerts"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."card_alerts"."credit_cards_card_id" IS 'Reference to specific card if applicable';

COMMENT ON COLUMN "credit_cards"."card_alerts"."alert_type" IS 'Type of alert (Payment Due, Payment Posted, Purchase, Credit Limit, Fraud)';

COMMENT ON COLUMN "credit_cards"."card_alerts"."delivery_method" IS 'How alert is delivered (Email, SMS, Push)';

COMMENT ON COLUMN "credit_cards"."card_alerts"."contact_info" IS 'Email or phone number for alert';

COMMENT ON COLUMN "credit_cards"."card_alerts"."threshold_amount" IS 'Amount threshold if applicable';

COMMENT ON COLUMN "credit_cards"."card_alerts"."is_active" IS 'Whether alert is currently active';

COMMENT ON COLUMN "credit_cards"."card_alerts"."created_date" IS 'When alert was set up';

COMMENT ON COLUMN "credit_cards"."card_alerts"."modified_date" IS 'When alert was last modified';

COMMENT ON TABLE "credit_cards"."disputed_transactions" IS 'Tracks disputed transactions and their resolution';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."credit_cards_dispute_id" IS 'Auto-incrementing identifier for each dispute';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."credit_cards_transaction_id" IS 'Reference to transactions';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."credit_cards_card_account_id" IS 'Reference to card_accounts';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."dispute_date" IS 'Date and time dispute was filed';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."dispute_reason" IS 'Reason for dispute (Fraud, Product Issue, Duplicate Charge, etc.)';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."disputed_amount" IS 'Amount being disputed';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."description" IS 'Customer description of dispute';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."status" IS 'Status of dispute (Filed, Processing, Resolved, Declined)';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."resolution" IS 'Final resolution (Customer Favor, Merchant Favor)';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."resolution_date" IS 'Date dispute was resolved';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."provisional_credit_date" IS 'Date provisional credit was issued if applicable';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."provisional_credit_amount" IS 'Amount of provisional credit';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."documentation_received" IS 'Whether documentation was received';

COMMENT ON COLUMN "credit_cards"."disputed_transactions"."case_number" IS 'Dispute case identifier';

COMMENT ON TABLE "small_business_banking"."businesses" IS 'Stores core information about small businesses that are customers of the bank';

COMMENT ON COLUMN "small_business_banking"."businesses"."small_business_banking_business_id" IS 'Unique identifier for each business entity';

COMMENT ON COLUMN "small_business_banking"."businesses"."enterprise_party_id" IS 'Reference to the enterprise party record representing this business';

COMMENT ON COLUMN "small_business_banking"."businesses"."business_name" IS 'Operating name of the business';

COMMENT ON COLUMN "small_business_banking"."businesses"."tax_id" IS 'Tax identification number for the business (e.g., EIN)';

COMMENT ON COLUMN "small_business_banking"."businesses"."business_type" IS 'Type of business entity (e.g., LLC, Corporation, Sole Proprietorship)';

COMMENT ON COLUMN "small_business_banking"."businesses"."industry_code" IS 'Standard industry classification code for the business';

COMMENT ON COLUMN "small_business_banking"."businesses"."establishment_date" IS 'Date the business was established';

COMMENT ON COLUMN "small_business_banking"."businesses"."annual_revenue" IS 'Annual revenue amount for the business';

COMMENT ON COLUMN "small_business_banking"."businesses"."employee_count" IS 'Number of employees in the business';

COMMENT ON COLUMN "small_business_banking"."businesses"."website" IS 'Business website URL';

COMMENT ON COLUMN "small_business_banking"."businesses"."status" IS 'Current status of the business (active, inactive, suspended, etc.)';

COMMENT ON TABLE "small_business_banking"."business_owners" IS 'Identifies individuals who own or have significant control over a business entity';

COMMENT ON COLUMN "small_business_banking"."business_owners"."small_business_banking_business_owner_id" IS 'Unique identifier for each business owner record';

COMMENT ON COLUMN "small_business_banking"."business_owners"."small_business_banking_business_id" IS 'Reference to the business the person owns or controls';

COMMENT ON COLUMN "small_business_banking"."business_owners"."enterprise_party_id" IS 'Reference to the enterprise party record representing this individual';

COMMENT ON COLUMN "small_business_banking"."business_owners"."ownership_percentage" IS 'Percentage of business ownership (0-100)';

COMMENT ON COLUMN "small_business_banking"."business_owners"."role" IS 'Role in the business (e.g., CEO, CFO, Managing Partner)';

COMMENT ON COLUMN "small_business_banking"."business_owners"."is_guarantor" IS 'Indicates if this owner serves as a loan guarantor';

COMMENT ON TABLE "small_business_banking"."accounts" IS 'Stores the business deposit and transaction accounts managed by the bank';

COMMENT ON COLUMN "small_business_banking"."accounts"."small_business_banking_account_id" IS 'Unique identifier for each business account';

COMMENT ON COLUMN "small_business_banking"."accounts"."enterprise_account_id" IS 'References the main account';

COMMENT ON COLUMN "small_business_banking"."accounts"."small_business_banking_business_id" IS 'Reference to the business that owns this account';

COMMENT ON COLUMN "small_business_banking"."accounts"."account_number" IS 'Unique account number visible to customers';

COMMENT ON COLUMN "small_business_banking"."accounts"."account_type" IS 'Type of account (checking, savings, money market, etc.)';

COMMENT ON COLUMN "small_business_banking"."accounts"."small_business_banking_product_id" IS 'Reference to the product this account is based on';

COMMENT ON COLUMN "small_business_banking"."accounts"."status" IS 'Current status of the account (active, inactive, frozen, closed)';

COMMENT ON COLUMN "small_business_banking"."accounts"."status_update_date_time" IS 'When the status was last updated';

COMMENT ON COLUMN "small_business_banking"."accounts"."balance" IS 'Current balance of the account';

COMMENT ON COLUMN "small_business_banking"."accounts"."available_balance" IS 'Available balance after holds and pending transactions';

COMMENT ON COLUMN "small_business_banking"."accounts"."currency" IS 'ISO currency code for the account';

COMMENT ON COLUMN "small_business_banking"."accounts"."overdraft_limit" IS 'Maximum allowed overdraft amount';

COMMENT ON COLUMN "small_business_banking"."accounts"."interest_rate" IS 'Current interest rate applied to the account (if applicable)';

COMMENT ON COLUMN "small_business_banking"."accounts"."statement_frequency" IS 'Frequency of account statements (daily, weekly, monthly)';

COMMENT ON COLUMN "small_business_banking"."accounts"."statement_day" IS 'Day of month/week when statements are generated';

COMMENT ON COLUMN "small_business_banking"."accounts"."last_statement_date" IS 'Date when the last statement was generated';

COMMENT ON COLUMN "small_business_banking"."accounts"."opened_date" IS 'Date when the account was opened';

COMMENT ON TABLE "small_business_banking"."products" IS 'Defines the financial products offered to small business customers';

COMMENT ON COLUMN "small_business_banking"."products"."small_business_banking_product_id" IS 'Unique identifier for each product';

COMMENT ON COLUMN "small_business_banking"."products"."product_code" IS 'Internal code for the product';

COMMENT ON COLUMN "small_business_banking"."products"."product_name" IS 'Display name for the product';

COMMENT ON COLUMN "small_business_banking"."products"."product_type" IS 'Type of product (checking, savings, loan, credit line, credit card)';

COMMENT ON COLUMN "small_business_banking"."products"."description" IS 'Detailed product description';

COMMENT ON COLUMN "small_business_banking"."products"."min_opening_deposit" IS 'Minimum amount required to open an account of this product type';

COMMENT ON COLUMN "small_business_banking"."products"."monthly_fee" IS 'Standard monthly maintenance fee';

COMMENT ON COLUMN "small_business_banking"."products"."transaction_limit" IS 'Number of free transactions per statement period';

COMMENT ON COLUMN "small_business_banking"."products"."transaction_fee" IS 'Fee charged per transaction beyond the limit';

COMMENT ON COLUMN "small_business_banking"."products"."min_balance" IS 'Minimum balance to avoid fees';

COMMENT ON COLUMN "small_business_banking"."products"."is_interest_bearing" IS 'Indicates if the product earns interest';

COMMENT ON COLUMN "small_business_banking"."products"."base_interest_rate" IS 'Standard interest rate for the product (if applicable)';

COMMENT ON COLUMN "small_business_banking"."products"."term_length" IS 'Term in months (for term products)';

COMMENT ON COLUMN "small_business_banking"."products"."is_active" IS 'Indicates if the product is currently offered';

COMMENT ON TABLE "small_business_banking"."account_signatories" IS 'Identifies individuals who have authority to sign on or manage a business account';

COMMENT ON COLUMN "small_business_banking"."account_signatories"."small_business_banking_account_signatory_id" IS 'Unique identifier for each account signatory record';

COMMENT ON COLUMN "small_business_banking"."account_signatories"."small_business_banking_account_id" IS 'Reference to the account';

COMMENT ON COLUMN "small_business_banking"."account_signatories"."enterprise_party_id" IS 'Reference to the enterprise party who has signing authority';

COMMENT ON COLUMN "small_business_banking"."account_signatories"."signatory_level" IS 'Level of signing authority (primary, secondary, view-only)';

COMMENT ON COLUMN "small_business_banking"."account_signatories"."daily_limit" IS 'Maximum daily transaction limit for this signatory';

COMMENT ON COLUMN "small_business_banking"."account_signatories"."is_active" IS 'Indicates if the signing authority is currently active';

COMMENT ON COLUMN "small_business_banking"."account_signatories"."start_date" IS 'Date when the signing authority begins';

COMMENT ON COLUMN "small_business_banking"."account_signatories"."end_date" IS 'Date when the signing authority expires (if applicable)';

COMMENT ON TABLE "small_business_banking"."loans" IS 'Stores information about term loans issued to small businesses';

COMMENT ON COLUMN "small_business_banking"."loans"."small_business_banking_loan_id" IS 'Unique identifier for each loan';

COMMENT ON COLUMN "small_business_banking"."loans"."small_business_banking_business_id" IS 'Reference to the business receiving the loan';

COMMENT ON COLUMN "small_business_banking"."loans"."small_business_banking_account_id" IS 'Reference to the associated account for fund disbursement and payments';

COMMENT ON COLUMN "small_business_banking"."loans"."small_business_banking_product_id" IS 'Reference to the loan product';

COMMENT ON COLUMN "small_business_banking"."loans"."loan_number" IS 'Unique loan number visible to customers';

COMMENT ON COLUMN "small_business_banking"."loans"."loan_amount" IS 'Original principal amount of the loan';

COMMENT ON COLUMN "small_business_banking"."loans"."outstanding_balance" IS 'Current balance remaining on the loan';

COMMENT ON COLUMN "small_business_banking"."loans"."interest_rate" IS 'Annual interest rate for the loan';

COMMENT ON COLUMN "small_business_banking"."loans"."interest_type" IS 'Type of interest rate (fixed, variable, etc.)';

COMMENT ON COLUMN "small_business_banking"."loans"."reference_rate" IS 'Reference rate for variable rate loans (e.g., PRIME, SOFR)';

COMMENT ON COLUMN "small_business_banking"."loans"."rate_spread" IS 'Spread over the reference rate for variable rate loans';

COMMENT ON COLUMN "small_business_banking"."loans"."term_months" IS 'Duration of the loan in months';

COMMENT ON COLUMN "small_business_banking"."loans"."payment_frequency" IS 'Frequency of payments (weekly, monthly, quarterly)';

COMMENT ON COLUMN "small_business_banking"."loans"."payment_amount" IS 'Regular payment amount';

COMMENT ON COLUMN "small_business_banking"."loans"."balloon_payment" IS 'Final balloon payment amount (if applicable)';

COMMENT ON COLUMN "small_business_banking"."loans"."disbursal_date" IS 'Date when loan funds were disbursed';

COMMENT ON COLUMN "small_business_banking"."loans"."first_payment_date" IS 'Date when the first payment is due';

COMMENT ON COLUMN "small_business_banking"."loans"."maturity_date" IS 'Date when the loan is scheduled to be fully paid';

COMMENT ON COLUMN "small_business_banking"."loans"."purpose" IS 'Stated purpose of the loan';

COMMENT ON COLUMN "small_business_banking"."loans"."status" IS 'Current status of the loan (pending, active, paid, defaulted)';

COMMENT ON TABLE "small_business_banking"."credit_lines" IS 'Manages revolving credit facilities provided to small businesses';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."small_business_banking_credit_line_id" IS 'Unique identifier for each credit line';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."small_business_banking_business_id" IS 'Reference to the business that has the credit line';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."small_business_banking_account_id" IS 'Reference to the associated account for fund disbursement and payments';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."small_business_banking_product_id" IS 'Reference to the credit line product';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."credit_line_number" IS 'Unique credit line number visible to customers';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."credit_limit" IS 'Maximum amount that can be borrowed';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."available_credit" IS 'Current amount available to be drawn';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."outstanding_balance" IS 'Current balance owed on the credit line';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."interest_rate" IS 'Annual interest rate for the credit line';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."interest_type" IS 'Type of interest rate (fixed, variable)';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."reference_rate" IS 'Reference rate for variable rate credit lines (e.g., PRIME, SOFR)';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."rate_spread" IS 'Spread over the reference rate for variable rate credit lines';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."annual_fee" IS 'Annual fee charged for maintaining the credit line';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."draw_period_months" IS 'Duration in months of the draw period';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."repayment_period_months" IS 'Duration in months of the repayment period';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."minimum_payment_percentage" IS 'Minimum percentage of outstanding balance required as monthly payment';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."minimum_payment_amount" IS 'Minimum fixed amount required as monthly payment';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."start_date" IS 'Date when the credit line becomes available';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."renewal_date" IS 'Date when the credit line is up for renewal';

COMMENT ON COLUMN "small_business_banking"."credit_lines"."status" IS 'Current status of the credit line (active, inactive, frozen, closed)';

COMMENT ON TABLE "small_business_banking"."collateral" IS 'Tracks assets pledged as security for loans and credit facilities';

COMMENT ON COLUMN "small_business_banking"."collateral"."small_business_banking_collateral_id" IS 'Unique identifier for each collateral item';

COMMENT ON COLUMN "small_business_banking"."collateral"."small_business_banking_business_id" IS 'Reference to the business that owns the collateral';

COMMENT ON COLUMN "small_business_banking"."collateral"."collateral_type" IS 'Type of collateral (real estate, equipment, vehicle, inventory, etc.)';

COMMENT ON COLUMN "small_business_banking"."collateral"."description" IS 'Detailed description of the collateral';

COMMENT ON COLUMN "small_business_banking"."collateral"."value" IS 'Estimated or appraised value of the collateral';

COMMENT ON COLUMN "small_business_banking"."collateral"."valuation_date" IS 'Date when the value was determined';

COMMENT ON COLUMN "small_business_banking"."collateral"."valuation_type" IS 'Method of valuation (appraisal, estimate, purchase price)';

COMMENT ON COLUMN "small_business_banking"."collateral"."location" IS 'Physical location of the collateral item';

COMMENT ON COLUMN "small_business_banking"."collateral"."identification_number" IS 'Serial number, VIN, or other identifier for the collateral';

COMMENT ON COLUMN "small_business_banking"."collateral"."lien_position" IS 'Position of the bank''s lien on this collateral (1st, 2nd, etc.)';

COMMENT ON COLUMN "small_business_banking"."collateral"."lien_filing_number" IS 'Reference number for the lien filing';

COMMENT ON COLUMN "small_business_banking"."collateral"."insurance_provider" IS 'Name of insurance company covering this collateral';

COMMENT ON COLUMN "small_business_banking"."collateral"."insurance_policy_number" IS 'Insurance policy number for this collateral';

COMMENT ON COLUMN "small_business_banking"."collateral"."insurance_expiry_date" IS 'Expiration date of the insurance policy';

COMMENT ON COLUMN "small_business_banking"."collateral"."status" IS 'Current status of the collateral (active, sold, repossessed)';

COMMENT ON TABLE "small_business_banking"."loan_collateral" IS 'Junction table linking collateral items to specific loans they secure';

COMMENT ON COLUMN "small_business_banking"."loan_collateral"."small_business_banking_loan_collateral_id" IS 'Unique identifier for each loan-collateral association';

COMMENT ON COLUMN "small_business_banking"."loan_collateral"."small_business_banking_loan_id" IS 'Reference to the loan secured by the collateral';

COMMENT ON COLUMN "small_business_banking"."loan_collateral"."small_business_banking_collateral_id" IS 'Reference to the collateral item';

COMMENT ON COLUMN "small_business_banking"."loan_collateral"."collateral_percentage" IS 'Percentage of the collateral''s value assigned to this loan';

COMMENT ON TABLE "small_business_banking"."business_card_accounts" IS 'Links businesses to credit card accounts and stores business-specific attributes';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."small_business_banking_business_card_account_id" IS 'Unique identifier for each business credit card account';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."small_business_banking_business_id" IS 'Reference to the business that owns the credit card account';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."card_account_id" IS 'Reference to the primary credit card account in the credit_cards schema';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."credit_cards_product_id" IS 'Reference to the card product in credit_cards schema';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."account_type" IS 'Categorization of the account (business, corporate, etc.)';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."tax_id_reporting" IS 'Tax ID used for reporting purposes';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."business_structure" IS 'Legal structure of the business for credit purposes';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."ownership_type" IS 'Type of ownership for this card account (sole proprietor, partnership, corporation)';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."liability_type" IS 'Liability arrangement (business liability, joint liability, etc.)';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."linked_deposit_account_id" IS 'Reference to deposit account for automatic payments';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."relationship_manager_id" IS 'Reference to the relationship manager for this business';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."annual_review_date" IS 'Date when account should be reviewed annually';

COMMENT ON COLUMN "small_business_banking"."business_card_accounts"."expense_category_setup" IS 'Type of expense categorization setup (standard, custom)';

COMMENT ON TABLE "small_business_banking"."business_card_users" IS 'Manages employee and owner cards issued under a business credit card account';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."small_business_banking_business_card_user_id" IS 'Unique identifier for each business card user';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."small_business_banking_business_card_account_id" IS 'Reference to the business card account';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."enterprise_party_id" IS 'Reference to the enterprise party who is issued a card';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."credit_cards_card_id" IS 'Reference to the specific card in the credit_cards schema';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."role" IS 'Role of user in the business (owner, employee, accountant, etc.)';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."department" IS 'Department or cost center for this cardholder';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."employee_id" IS 'Employee ID within the business if applicable';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."spending_limit" IS 'Monthly spending limit for this cardholder';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."transaction_approval_required" IS 'Whether transactions require approval';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."merchant_category_restrictions" IS 'JSON object describing merchant category restrictions';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."can_view_all_transactions" IS 'Whether user can view all company transactions';

COMMENT ON COLUMN "small_business_banking"."business_card_users"."can_manage_all_cards" IS 'Whether user can manage all company cards';

COMMENT ON TABLE "small_business_banking"."business_expense_categories" IS 'Defines custom expense categories for business card transactions';

COMMENT ON COLUMN "small_business_banking"."business_expense_categories"."small_business_banking_category_id" IS 'Unique identifier for each expense category';

COMMENT ON COLUMN "small_business_banking"."business_expense_categories"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."business_expense_categories"."category_name" IS 'Name of the expense category';

COMMENT ON COLUMN "small_business_banking"."business_expense_categories"."category_description" IS 'Description of what expenses belong in this category';

COMMENT ON COLUMN "small_business_banking"."business_expense_categories"."parent_category_id" IS 'Reference to parent category for hierarchical categorization';

COMMENT ON COLUMN "small_business_banking"."business_expense_categories"."budget_amount" IS 'Monthly budget amount for this category';

COMMENT ON COLUMN "small_business_banking"."business_expense_categories"."is_tax_deductible" IS 'Whether expenses in this category are typically tax deductible';

COMMENT ON COLUMN "small_business_banking"."business_expense_categories"."gl_account_code" IS 'General ledger account code for accounting integration';

COMMENT ON TABLE "small_business_banking"."business_transaction_categories" IS 'Maps credit card transactions to business expense categories';

COMMENT ON COLUMN "small_business_banking"."business_transaction_categories"."small_business_banking_transaction_category_id" IS 'Unique identifier for each transaction categorization';

COMMENT ON COLUMN "small_business_banking"."business_transaction_categories"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."business_transaction_categories"."transaction_id" IS 'Reference to the transaction in credit_cards schema';

COMMENT ON COLUMN "small_business_banking"."business_transaction_categories"."small_business_banking_category_id" IS 'Reference to the business expense category';

COMMENT ON COLUMN "small_business_banking"."business_transaction_categories"."notes" IS 'Additional notes about this transaction categorization';

COMMENT ON COLUMN "small_business_banking"."business_transaction_categories"."receipt_image_path" IS 'Path to stored receipt image';

COMMENT ON COLUMN "small_business_banking"."business_transaction_categories"."tax_relevant" IS 'Flag indicating transaction is relevant for tax purposes';

COMMENT ON COLUMN "small_business_banking"."business_transaction_categories"."created_by_id" IS 'User who created this categorization';

COMMENT ON TABLE "small_business_banking"."transactions" IS 'Records all financial transactions across business accounts';

COMMENT ON COLUMN "small_business_banking"."transactions"."small_business_banking_transaction_id" IS 'Unique identifier for each transaction';

COMMENT ON COLUMN "small_business_banking"."transactions"."small_business_banking_account_id" IS 'Reference to the account where the transaction occurred';

COMMENT ON COLUMN "small_business_banking"."transactions"."transaction_type" IS 'Type of transaction (deposit, withdrawal, payment, fee, etc.)';

COMMENT ON COLUMN "small_business_banking"."transactions"."amount" IS 'Transaction amount';

COMMENT ON COLUMN "small_business_banking"."transactions"."running_balance" IS 'Account balance after this transaction';

COMMENT ON COLUMN "small_business_banking"."transactions"."currency" IS 'Currency of the transaction';

COMMENT ON COLUMN "small_business_banking"."transactions"."description" IS 'Transaction description';

COMMENT ON COLUMN "small_business_banking"."transactions"."reference_number" IS 'External reference for the transaction';

COMMENT ON COLUMN "small_business_banking"."transactions"."status" IS 'Status of the transaction (pending, completed, failed, reversed)';

COMMENT ON COLUMN "small_business_banking"."transactions"."transaction_date" IS 'Date of the transaction';

COMMENT ON COLUMN "small_business_banking"."transactions"."post_date" IS 'Date when the transaction was posted to the account';

COMMENT ON COLUMN "small_business_banking"."transactions"."created_by_id" IS 'User that created the transaction';

COMMENT ON TABLE "small_business_banking"."payments" IS 'Tracks payments made against loans, credit lines, credit cards, and between accounts';

COMMENT ON COLUMN "small_business_banking"."payments"."small_business_banking_payment_id" IS 'Unique identifier for each payment';

COMMENT ON COLUMN "small_business_banking"."payments"."source_account_id" IS 'Reference to the account funds are drawn from (for internal transfers)';

COMMENT ON COLUMN "small_business_banking"."payments"."destination_account_id" IS 'Reference to the account funds are deposited to (for internal transfers)';

COMMENT ON COLUMN "small_business_banking"."payments"."small_business_banking_loan_id" IS 'Reference to the loan being paid (for loan payments)';

COMMENT ON COLUMN "small_business_banking"."payments"."small_business_banking_credit_line_id" IS 'Reference to the credit line being paid (for credit line payments)';

COMMENT ON COLUMN "small_business_banking"."payments"."credit_card_id" IS 'Reference to the credit card being paid (for card payments)';

COMMENT ON COLUMN "small_business_banking"."payments"."payment_method" IS 'Method of payment (ACH, wire, internal transfer, check)';

COMMENT ON COLUMN "small_business_banking"."payments"."payment_type" IS 'Type of payment (principal, interest, fees, or combination)';

COMMENT ON COLUMN "small_business_banking"."payments"."amount" IS 'Payment amount';

COMMENT ON COLUMN "small_business_banking"."payments"."principal_portion" IS 'Portion of payment applied to principal';

COMMENT ON COLUMN "small_business_banking"."payments"."interest_portion" IS 'Portion of payment applied to interest';

COMMENT ON COLUMN "small_business_banking"."payments"."fees_portion" IS 'Portion of payment applied to fees';

COMMENT ON COLUMN "small_business_banking"."payments"."payment_date" IS 'Date the payment was made or scheduled';

COMMENT ON COLUMN "small_business_banking"."payments"."effective_date" IS 'Date the payment is applied to the account';

COMMENT ON COLUMN "small_business_banking"."payments"."status" IS 'Status of the payment (pending, processed, failed)';

COMMENT ON COLUMN "small_business_banking"."payments"."external_reference" IS 'External reference number for the payment';

COMMENT ON COLUMN "small_business_banking"."payments"."memo" IS 'Additional payment information or notes';

COMMENT ON TABLE "small_business_banking"."documents" IS 'Stores metadata about business documents with references to their file locations';

COMMENT ON COLUMN "small_business_banking"."documents"."small_business_banking_document_id" IS 'Unique identifier for each document record';

COMMENT ON COLUMN "small_business_banking"."documents"."small_business_banking_business_id" IS 'Reference to the business the document belongs to';

COMMENT ON COLUMN "small_business_banking"."documents"."document_type" IS 'Type of document (tax return, financial statement, business license, etc.)';

COMMENT ON COLUMN "small_business_banking"."documents"."description" IS 'Description of the document';

COMMENT ON COLUMN "small_business_banking"."documents"."file_name" IS 'Original file name of the document';

COMMENT ON COLUMN "small_business_banking"."documents"."file_path" IS 'Path to the stored document file';

COMMENT ON COLUMN "small_business_banking"."documents"."file_type" IS 'MIME type or format of the document';

COMMENT ON COLUMN "small_business_banking"."documents"."file_size" IS 'Size of the file in bytes';

COMMENT ON COLUMN "small_business_banking"."documents"."document_date" IS 'Date associated with the document content';

COMMENT ON COLUMN "small_business_banking"."documents"."upload_date" IS 'Date the document was uploaded';

COMMENT ON COLUMN "small_business_banking"."documents"."expiration_date" IS 'Date when the document expires (if applicable)';

COMMENT ON COLUMN "small_business_banking"."documents"."status" IS 'Status of the document (active, archived, expired)';

COMMENT ON COLUMN "small_business_banking"."documents"."created_by_id" IS 'User that created the document record';

COMMENT ON TABLE "small_business_banking"."regulatory_reports" IS 'Tracks required regulatory reports related to small business banking';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."small_business_banking_report_id" IS 'Unique identifier for each regulatory report';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."report_type" IS 'Type of regulatory report (CRA, HMDA, BSA, etc.)';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."period_start_date" IS 'Start date of the reporting period';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."period_end_date" IS 'End date of the reporting period';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."due_date" IS 'Date when the report is due to be submitted';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."status" IS 'Status of the report (pending, in progress, submitted, accepted, rejected)';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."regulatory_agency" IS 'Agency the report is submitted to (FDIC, Federal Reserve, CFPB, etc.)';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."report_owner" IS 'Department or individual responsible for the report';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."file_specification_version" IS 'Version of the regulatory reporting specification';

COMMENT ON COLUMN "small_business_banking"."regulatory_reports"."notes" IS 'Additional information about the report';

COMMENT ON TABLE "small_business_banking"."report_submissions" IS 'Records submissions of regulatory reports to authorities';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."small_business_banking_submission_id" IS 'Unique identifier for each report submission';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."small_business_banking_report_id" IS 'Reference to the regulatory report';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."submission_date" IS 'Date and time of submission';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."submission_method" IS 'Method of submission (portal, API, mail, etc.)';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."confirmation_number" IS 'Confirmation number received upon submission';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."submitted_by_id" IS 'Person who submitted the report';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."submission_file_path" IS 'Path to the submitted file';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."response_date" IS 'Date and time of regulator response';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."response_status" IS 'Status of the regulator''s response (accepted, rejected, need more info)';

COMMENT ON COLUMN "small_business_banking"."report_submissions"."response_details" IS 'Details of the regulator''s response';

COMMENT ON TABLE "small_business_banking"."regulatory_findings" IS 'Tracks regulatory findings, violations, and corrective actions';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."small_business_banking_finding_id" IS 'Unique identifier for each regulatory finding';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."small_business_banking_report_id" IS 'Associated regulatory report if applicable';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."small_business_banking_business_id" IS 'Associated business if finding is related to a specific customer';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."finding_date" IS 'Date the finding was identified or received';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."source" IS 'Source of the finding (exam, self-assessment, regulator, etc.)';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."finding_type" IS 'Type of finding (violation, concern, observation)';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."severity" IS 'Severity level (high, medium, low)';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."description" IS 'Detailed description of the finding';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."regulation_reference" IS 'Reference to specific regulation or law';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."corrective_action_required" IS 'Whether corrective action is required';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."corrective_action_description" IS 'Description of required corrective action';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."due_date" IS 'Deadline for corrective action';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."responsible_party" IS 'Department or individual responsible for resolution';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."status" IS 'Status of the finding (open, in progress, resolved, validated)';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."resolution_date" IS 'Date when the finding was resolved';

COMMENT ON COLUMN "small_business_banking"."regulatory_findings"."resolution_description" IS 'Description of how the finding was resolved';

COMMENT ON TABLE "small_business_banking"."compliance_cases" IS 'Tracks compliance cases related to small business accounts';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."small_business_banking_case_id" IS 'Unique identifier for each compliance case';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."case_type" IS 'Type of compliance case (AML, KYC, fraud, fair lending, etc.)';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."opened_date" IS 'Date the case was opened';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."priority" IS 'Priority level (high, medium, low)';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."status" IS 'Status of the case (open, in review, closed)';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."description" IS 'Description of the compliance case';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."assigned_to" IS 'Person or team assigned to the case';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."source" IS 'Source that initiated the case (system alert, manual review, exam)';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."resolution" IS 'Description of the resolution';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."closed_date" IS 'Date the case was closed';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."escalated" IS 'Whether the case was escalated';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."escalation_date" IS 'Date of escalation if applicable';

COMMENT ON COLUMN "small_business_banking"."compliance_cases"."escalation_reason" IS 'Reason for escalation';

COMMENT ON TABLE "small_business_banking"."compliance_requirements" IS 'Catalogs compliance requirements affecting small business banking';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."small_business_banking_requirement_id" IS 'Unique identifier for each compliance requirement';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."requirement_name" IS 'Name of the compliance requirement';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."regulation" IS 'Associated regulation or law';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."regulatory_authority" IS 'Authority that enforces the requirement';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."description" IS 'Detailed description of the requirement';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."business_impact" IS 'How the requirement impacts business banking';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."effective_date" IS 'Date when the requirement became effective';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."end_date" IS 'Date when the requirement expires (if applicable)';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."requirement_owner" IS 'Department or role responsible for compliance';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."verification_frequency" IS 'How often compliance is verified (daily, monthly, quarterly, annual)';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."verification_procedure" IS 'Description of the verification procedure';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."control_measures" IS 'Measures in place to ensure compliance';

COMMENT ON COLUMN "small_business_banking"."compliance_requirements"."is_active" IS 'Whether this requirement is currently active';

COMMENT ON TABLE "small_business_banking"."business_risk_assessments" IS 'Stores risk assessments performed on small business customers';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."small_business_banking_assessment_id" IS 'Unique identifier for each risk assessment';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."small_business_banking_business_id" IS 'Reference to the business being assessed';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."assessment_date" IS 'Date of the risk assessment';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."assessment_type" IS 'Type of assessment (AML, credit, operational, etc.)';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."conducted_by_id" IS 'Person or team that conducted the assessment';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."methodology" IS 'Methodology used for the assessment';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."industry_risk_score" IS 'Risk score based on industry (1-5 scale)';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."geographic_risk_score" IS 'Risk score based on geographic location (1-5 scale)';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."customer_risk_score" IS 'Risk score based on customer attributes (1-5 scale)';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."transaction_risk_score" IS 'Risk score based on transaction patterns (1-5 scale)';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."product_risk_score" IS 'Risk score based on products used (1-5 scale)';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."overall_risk_score" IS 'Combined overall risk score (1-5 scale)';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."risk_rating" IS 'Overall risk rating (low, medium, high)';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."rationale" IS 'Rationale for the risk scores and rating';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."mitigating_factors" IS 'Factors that mitigate the identified risks';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."recommended_actions" IS 'Actions recommended to address risks';

COMMENT ON COLUMN "small_business_banking"."business_risk_assessments"."next_review_date" IS 'Date when the next assessment should be conducted';

COMMENT ON TABLE "small_business_banking"."loan_fair_lending" IS 'Captures data required for small business lending fair lending analysis and reporting';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."small_business_banking_lending_record_id" IS 'Unique identifier for each fair lending record';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."small_business_banking_loan_id" IS 'Reference to the loan';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."application_date" IS 'Date the loan application was received';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."decision_date" IS 'Date of the credit decision';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."census_tract" IS 'Census tract of the business location';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."msa_md" IS 'Metropolitan Statistical Area/Metropolitan Division code';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."reported_revenue" IS 'Gross annual revenue of the business as reported';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."loan_type" IS 'Type of loan (term loan, line of credit, etc.)';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."loan_purpose" IS 'Purpose of the loan';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."loan_amount" IS 'Requested loan amount';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."amount_approved" IS 'Approved loan amount (if applicable)';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."action_taken" IS 'Action taken (approved, denied, withdrawn, etc.)';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."denial_reason_1" IS 'Primary reason for denial (if applicable)';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."denial_reason_2" IS 'Secondary reason for denial (if applicable)';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."denial_reason_3" IS 'Tertiary reason for denial (if applicable)';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."denial_reason_4" IS 'Quaternary reason for denial (if applicable)';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."rate_spread" IS 'Difference between APR and average prime offer rate';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."naics_code" IS 'North American Industry Classification System code';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."number_of_employees" IS 'Number of business employees';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."minority_owned" IS 'Whether business is minority-owned';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."women_owned" IS 'Whether business is women-owned';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."lgbtq_owned" IS 'Whether business is LGBTQ-owned';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."veteran_owned" IS 'Whether business is veteran-owned';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."exemption_claimed" IS 'Whether an exemption from reporting was claimed';

COMMENT ON COLUMN "small_business_banking"."loan_fair_lending"."exemption_reason" IS 'Reason for reporting exemption (if applicable)';

COMMENT ON TABLE "small_business_banking"."credit_decisions" IS 'Documents credit decisions for regulatory review and fair lending analysis';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."small_business_banking_decision_id" IS 'Unique identifier for each credit decision';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."product_type" IS 'Type of credit product (loan, line of credit, card)';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."application_id" IS 'Application identifier';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."decision_date" IS 'Date and time of the decision';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."decision_type" IS 'Type of decision (automated, manual, hybrid)';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."decision_outcome" IS 'Outcome of the decision (approved, declined, counter-offer)';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."decision_factors" IS 'Factors that influenced the decision';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."credit_score" IS 'Credit score used in decision';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."credit_score_model" IS 'Model used for credit score';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."annual_revenue" IS 'Annual revenue considered in decision';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."time_in_business" IS 'Time in business (months) considered in decision';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."collateral_value" IS 'Value of collateral (if applicable)';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."debt_service_coverage_ratio" IS 'Debt service coverage ratio calculated';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."loan_to_value_ratio" IS 'Loan to value ratio (if applicable)';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."exception_made" IS 'Whether an exception to policy was made';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."exception_reason" IS 'Reason for the exception (if applicable)';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."exception_approver" IS 'Person who approved the exception';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."decision_notes" IS 'Additional notes about the decision';

COMMENT ON COLUMN "small_business_banking"."credit_decisions"."decision_made_by_id" IS 'Person or system that made the decision';

COMMENT ON TABLE "small_business_banking"."adverse_action_notices" IS 'Tracks adverse action notices sent to declined applicants';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."small_business_banking_notice_id" IS 'Unique identifier for each adverse action notice';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."small_business_banking_decision_id" IS 'Reference to the credit decision';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."notice_date" IS 'Date the notice was generated';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."delivery_method" IS 'Method of delivery (mail, email, etc.)';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."delivery_address" IS 'Address or email where notice was sent';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."delivery_date" IS 'Date the notice was delivered';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."primary_reason" IS 'Primary reason for adverse action';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."secondary_reasons" IS 'Secondary reasons for adverse action';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."credit_score_disclosed" IS 'Whether credit score was disclosed';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."credit_score" IS 'Credit score disclosed (if applicable)';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."score_factors" IS 'Factors affecting the credit score';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."score_range_low" IS 'Low end of score range';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."score_range_high" IS 'High end of score range';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."ecoa_notice_included" IS 'Whether ECOA notice was included';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."fcra_notice_included" IS 'Whether FCRA notice was included';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."right_to_appraisal_notice" IS 'Whether right to appraisal notice was included';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."template_version" IS 'Version of the notice template used';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."generated_by_id" IS 'Person or system that generated the notice';

COMMENT ON COLUMN "small_business_banking"."adverse_action_notices"."notice_file_path" IS 'Path to stored copy of the notice';

COMMENT ON TABLE "small_business_banking"."business_due_diligence" IS 'Documents the due diligence process for business customers';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."small_business_banking_due_diligence_id" IS 'Unique identifier for each due diligence record';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."diligence_type" IS 'Type of due diligence (initial, ongoing, enhanced)';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."diligence_date" IS 'Date the due diligence was performed';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."performed_by_id" IS 'Person who performed the due diligence';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."business_verified" IS 'Whether business identity was verified';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."verification_method" IS 'Method used to verify business (documents, database, etc.)';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."legal_structure_verified" IS 'Whether legal structure was verified';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."business_documents_reviewed" IS 'List of business documents reviewed';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."address_verified" IS 'Whether business address was verified';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."tin_verified" IS 'Whether tax ID was verified';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."high_risk_factors" IS 'High-risk factors identified during diligence';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."expected_activity" IS 'Description of expected account activity';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."actual_activity_consistent" IS 'Whether actual activity is consistent with expected';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."screening_results" IS 'Results of screening against watchlists, PEPs, etc.';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."site_visit_conducted" IS 'Whether a site visit was conducted';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."site_visit_date" IS 'Date of site visit (if applicable)';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."site_visit_notes" IS 'Notes from site visit';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."risk_rating" IS 'Risk rating assigned (low, medium, high)';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."review_frequency" IS 'Frequency of ongoing reviews (monthly, quarterly, annual)';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."next_review_date" IS 'Date when next review is due';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."approval_status" IS 'Status of approval (pending, approved, rejected)';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."approved_by_id" IS 'Person who approved the due diligence';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."approval_date" IS 'Date of approval';

COMMENT ON COLUMN "small_business_banking"."business_due_diligence"."notes" IS 'Additional notes about the due diligence';

COMMENT ON TABLE "small_business_banking"."beneficial_owner_verification" IS 'Tracks verification of beneficial owners as required by FinCEN';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."small_business_banking_verification_id" IS 'Unique identifier for each verification record';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."small_business_banking_business_id" IS 'Reference to the business';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."small_business_banking_business_owner_id" IS 'Reference to the business owner';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."verification_date" IS 'Date the verification was performed';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."performed_by_id" IS 'Person who performed the verification';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."ownership_percentage_verified" IS 'Whether ownership percentage was verified';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."verification_method" IS 'Method used to verify beneficial ownership';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."id_type" IS 'Type of ID provided (driver''s license, passport, etc.)';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."id_number" IS 'ID number (masked for security)';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."id_issuing_country" IS 'Country that issued the ID';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."id_expiration_date" IS 'Expiration date of the ID';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."address_verified" IS 'Whether address was verified';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."ssn_verified" IS 'Whether SSN was verified (for US persons)';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."tin_verified" IS 'Whether TIN was verified (for non-US persons)';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."screening_conducted" IS 'Whether screening was conducted';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."screening_date" IS 'Date of screening';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."screening_system" IS 'System used for screening';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."screening_results" IS 'Results of screening';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."pep_status" IS 'Whether person is a politically exposed person';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."sanctions_hit" IS 'Whether person appears on sanctions lists';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."adverse_media_found" IS 'Whether adverse media was found';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."certification_received" IS 'Whether certification of beneficial ownership was received';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."certification_date" IS 'Date of certification';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."recertification_due_date" IS 'Date when recertification is due';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."verification_status" IS 'Status of verification (pending, completed, exception)';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."exception_reason" IS 'Reason for exception (if applicable)';

COMMENT ON COLUMN "small_business_banking"."beneficial_owner_verification"."notes" IS 'Additional notes about the verification';

COMMENT ON TABLE "small_business_banking"."suspicious_activity_reports" IS 'Tracks Suspicious Activity Reports filed with FinCEN';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."small_business_banking_sar_id" IS 'Unique identifier for each SAR';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."small_business_banking_business_id" IS 'Reference to the business if applicable';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."filing_date" IS 'Date the SAR was filed';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."activity_start_date" IS 'Date when suspicious activity began';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."activity_end_date" IS 'Date when suspicious activity ended';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."filing_institution" IS 'Name of filing institution';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."suspicious_activity_type" IS 'Type of suspicious activity';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."suspicious_activity_description" IS 'Detailed description of suspicious activity';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."amount_involved" IS 'Total amount involved in suspicious activity';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."structuring_involved" IS 'Whether structuring was involved';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."terrorist_financing_involved" IS 'Whether terrorist financing was involved';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."fraud_involved" IS 'Whether fraud was involved';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."money_laundering_involved" IS 'Whether money laundering was involved';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."insider_abuse_involved" IS 'Whether insider abuse was involved';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."other_involved" IS 'Whether other suspicious activity was involved';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."other_description" IS 'Description of other suspicious activity';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."law_enforcement_contacted" IS 'Whether law enforcement was contacted';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."law_enforcement_agency" IS 'Agency contacted (if applicable)';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."law_enforcement_contact_date" IS 'Date of law enforcement contact';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."law_enforcement_contact_name" IS 'Name of law enforcement contact';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."account_closed" IS 'Whether account was closed';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."account_closing_date" IS 'Date account was closed (if applicable)';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."prepared_by_id" IS 'Person who prepared the SAR';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."approved_by_id" IS 'Person who approved the SAR';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."bsa_officer_signature" IS 'Signature of BSA officer';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."fincen_acknowledgment" IS 'Acknowledgment received from FinCEN';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."sar_file_path" IS 'Path to stored copy of the SAR';

COMMENT ON COLUMN "small_business_banking"."suspicious_activity_reports"."supporting_documentation" IS 'List of supporting documentation';

COMMENT ON TABLE "data_quality"."validation_run" IS 'Represents a single execution instance of a data quality validation run, including metadata and links to errors found.';

COMMENT ON COLUMN "data_quality"."validation_run"."validation_run_id" IS 'Unique identifier for the validation run.';

COMMENT ON COLUMN "data_quality"."validation_run"."run_timestamp" IS 'Timestamp indicating when the validation run was executed or recorded.';

COMMENT ON COLUMN "data_quality"."validation_run"."source_identifier" IS 'Optional identifier for the source system, file, or event that triggered this validation run.';

COMMENT ON COLUMN "data_quality"."validation_run"."run_user" IS 'Identifier of the user who initiated or is associated with this validation run.';

COMMENT ON COLUMN "data_quality"."validation_run"."run_role" IS 'Role associated with the user who initiated this validation run.';

COMMENT ON COLUMN "data_quality"."validation_run"."operation_name" IS 'Name of the specific operation being validated, if applicable.';

COMMENT ON COLUMN "data_quality"."validation_run"."variables" IS 'Variables passed to the query, stored as a JSON string.';

COMMENT ON COLUMN "data_quality"."validation_run"."validation_config_data" IS 'Validation configuration flag: Indicates if the ''$data'' option (ajv) was enabled.';

COMMENT ON COLUMN "data_quality"."validation_run"."validation_config_verbose" IS 'Validation configuration flag: Indicates if the ''verbose'' option (ajv) was enabled.';

COMMENT ON COLUMN "data_quality"."validation_run"."validation_config_all_errors" IS 'Validation configuration flag: Indicates if the ''allErrors'' option (ajv) was enabled.';

COMMENT ON COLUMN "data_quality"."validation_run"."validation_config_strict" IS 'Validation configuration flag: Indicates if the ''strict'' option (ajv) was enabled.';

COMMENT ON COLUMN "data_quality"."validation_run"."query" IS 'The query string that was executed and validated.';

COMMENT ON COLUMN "data_quality"."validation_run"."validation_schema" IS 'The JSON schema used to validate the query results, stored as a JSON string.';

COMMENT ON COLUMN "data_quality"."validation_run"."total_errors" IS 'A summary count of the total number of validation errors found during this run.';

COMMENT ON TABLE "data_quality"."validation_error" IS 'Stores details for a single data quality validation error identified during a validation run.';

COMMENT ON COLUMN "data_quality"."validation_error"."validation_error_id" IS 'Unique identifier for the validation error record.';

COMMENT ON COLUMN "data_quality"."validation_error"."validation_run_id" IS 'Foreign key linking to the specific validation run (validation_run table) where this error occurred.';

COMMENT ON COLUMN "data_quality"."validation_error"."instance_path" IS 'JSON path within the validated data pointing to the element that failed validation.';

COMMENT ON COLUMN "data_quality"."validation_error"."schema_path" IS 'JSON path within the validation schema pointing to the rule/keyword that failed.';

COMMENT ON COLUMN "data_quality"."validation_error"."error_keyword" IS 'The specific JSON schema keyword (e.g., type, required, pattern) that triggered the validation failure.';

COMMENT ON COLUMN "data_quality"."validation_error"."error_message" IS 'The human-readable error message generated by the validator.';

COMMENT ON COLUMN "data_quality"."validation_error"."failed_data" IS 'String representation of the actual data value that failed the validation rule.';

COMMENT ON COLUMN "data_quality"."validation_error"."error_params" IS 'Parameters associated with the failed validation keyword (e.g., allowed values for enum), stored as a JSON string.';

COMMENT ON COLUMN "data_quality"."validation_error"."error_schema_detail" IS 'The specific part of the JSON schema definition that failed, stored as a JSON string.';

COMMENT ON COLUMN "data_quality"."validation_error"."error_parent_schema_detail" IS 'The parent schema object containing the failed rule, stored as a JSON string.';

COMMENT ON TABLE "data_quality"."api_calls" IS 'Records actual instances of API calls made to the system for auditing and lineage tracking. These records can be tied by business rules to validation runs. A validation run with the same query and timestamp of less than once second earlier is probably related to this API call.';

COMMENT ON COLUMN "data_quality"."api_calls"."api_call_id" IS 'Unique identifier for the API call.';

COMMENT ON COLUMN "data_quality"."api_calls"."method" IS 'HTTP method used for the API call (GET, POST, etc.).';

COMMENT ON COLUMN "data_quality"."api_calls"."path" IS 'API endpoint path that was called.';

COMMENT ON COLUMN "data_quality"."api_calls"."query_params" IS 'Query parameters sent with the API call, stored as TEXT.';

COMMENT ON COLUMN "data_quality"."api_calls"."request_headers" IS 'HTTP headers sent with the API call, stored as TEXT.';

COMMENT ON COLUMN "data_quality"."api_calls"."server_name" IS 'Server name associated with API call.';

COMMENT ON COLUMN "data_quality"."api_calls"."major_version" IS 'Server name API major version.';

COMMENT ON COLUMN "data_quality"."api_calls"."minor_version" IS 'Server name API minor version.';

COMMENT ON COLUMN "data_quality"."api_calls"."related_institution" IS 'An identifier of the institution associated with the API call.';

COMMENT ON COLUMN "data_quality"."api_calls"."created_at" IS 'Timestamp when the API call was made.';

COMMENT ON TABLE "data_quality"."record_transformations" IS 'Tracks actual instances of transformations applied to data records, linking input and output data.';

COMMENT ON COLUMN "data_quality"."record_transformations"."record_transformation_id" IS 'Unique identifier for the record transformation.';

COMMENT ON COLUMN "data_quality"."record_transformations"."input_type" IS 'The type/entity of the input record before transformation.';

COMMENT ON COLUMN "data_quality"."record_transformations"."output_type" IS 'The type/entity of the output record after transformation.';

COMMENT ON COLUMN "data_quality"."record_transformations"."description" IS 'Description of the transformation process or purpose.';

COMMENT ON COLUMN "data_quality"."record_transformations"."primary_key_names" IS 'Names of the primary key fields, comma-separated.';

COMMENT ON COLUMN "data_quality"."record_transformations"."primary_key_values" IS 'Values of the primary keys, comma-separated.';

COMMENT ON COLUMN "data_quality"."record_transformations"."created_at" IS 'Timestamp when the transformation was executed.';

COMMENT ON COLUMN "data_quality"."record_transformations"."api_call_id" IS 'Reference to the API call that triggered this transformation, if applicable.';

COMMENT ON TABLE "data_quality"."field_transformation_details" IS 'Detailed tracking of instances of field-level transformations within a record transformation.';

COMMENT ON COLUMN "data_quality"."field_transformation_details"."field_transformation_detail_id" IS 'Unique identifier for the field transformation detail.';

COMMENT ON COLUMN "data_quality"."field_transformation_details"."transform_description" IS 'Description of the specific transformation applied to this field.';

COMMENT ON COLUMN "data_quality"."field_transformation_details"."input_field_name" IS 'Name of the input field before transformation.';

COMMENT ON COLUMN "data_quality"."field_transformation_details"."input_field_value" IS 'Value of the input field before transformation.';

COMMENT ON COLUMN "data_quality"."field_transformation_details"."output_field_name" IS 'Name of the output field after transformation.';

COMMENT ON COLUMN "data_quality"."field_transformation_details"."output_field_value" IS 'Value of the output field after transformation.';

COMMENT ON COLUMN "data_quality"."field_transformation_details"."record_transformation_id" IS 'Reference to the parent record transformation.';

COMMENT ON TABLE "data_quality"."api_lineage" IS 'Represents historical documentation of API endpoint design. Documents the custom API endpoints available internally or externally, including Open Banking and FDX endpoints. Tracks the lineage of API calls for data governance and auditing purposes. The most recent API lineage records can be identified by an endDate of NULL. API''s may use a base path for both 1) separation of concerns and 2) versioning, typically the base path is ignored when analyzing compliance with regulator mandated API resource paths.';

COMMENT ON COLUMN "data_quality"."api_lineage"."api_lineage_id" IS 'Unique identifier for the API lineage record.';

COMMENT ON COLUMN "data_quality"."api_lineage"."server_name" IS 'Name of the server handling the API call.';

COMMENT ON COLUMN "data_quality"."api_lineage"."major_version" IS 'The major version assigned to the API';

COMMENT ON COLUMN "data_quality"."api_lineage"."minor_version" IS 'The minor version assigned to the API';

COMMENT ON COLUMN "data_quality"."api_lineage"."api_call" IS 'The API endpoint and method called.';

COMMENT ON COLUMN "data_quality"."api_lineage"."query" IS 'The DDN query that is used to source data for this API call. If this query is validated you can find its data validation runs by correlating by query. But its not guaranteed, there may be no validation runs and api''s can use the same query but produce different outputs.';

COMMENT ON COLUMN "data_quality"."api_lineage"."description" IS 'Description of the API call purpose or context.';

COMMENT ON COLUMN "data_quality"."api_lineage"."start_date" IS 'Timestamp when this API lineage tracking began.';

COMMENT ON COLUMN "data_quality"."api_lineage"."end_date" IS 'Timestamp when this API lineage tracking ended, if applicable.';

COMMENT ON COLUMN "data_quality"."api_lineage"."updated_at" IS 'Timestamp when this record was last updated.';

COMMENT ON TABLE "data_quality"."record_lineage" IS 'Maps the lineage (design) of data records through transformations for traceability.';

COMMENT ON COLUMN "data_quality"."record_lineage"."record_lineage_id" IS 'Unique identifier for the record lineage.';

COMMENT ON COLUMN "data_quality"."record_lineage"."input_type" IS 'The type/entity of input data in this lineage.';

COMMENT ON COLUMN "data_quality"."record_lineage"."output_type" IS 'The type/entity of output data in this lineage.';

COMMENT ON COLUMN "data_quality"."record_lineage"."description" IS 'General description of this data lineage relationship.';

COMMENT ON COLUMN "data_quality"."record_lineage"."input_description" IS 'Description of the input data source or format.';

COMMENT ON COLUMN "data_quality"."record_lineage"."output_description" IS 'Description of the output data destination or format.';

COMMENT ON COLUMN "data_quality"."record_lineage"."pk_names" IS 'Names of primary key fields used to track the record through transformations.';

COMMENT ON COLUMN "data_quality"."record_lineage"."api_lineage_id" IS 'Reference to the API lineage this record is part of.';

COMMENT ON TABLE "data_quality"."field_lineage" IS 'Tracks the lineage (design) of individual fields through data transformations. Field names use dot notation to represent nested fields';

COMMENT ON COLUMN "data_quality"."field_lineage"."field_lineage_id" IS 'Unique identifier for the field lineage.';

COMMENT ON COLUMN "data_quality"."field_lineage"."field_name" IS 'Name of the field being tracked. Dot notation is used for representing nested fields, for example: customer.code, would represent the code field within a customer object field.';

COMMENT ON COLUMN "data_quality"."field_lineage"."description" IS 'Description of this field lineage relationship.';

COMMENT ON COLUMN "data_quality"."field_lineage"."input_fields" IS 'Source fields that contribute to this field, comma-separated.';

COMMENT ON COLUMN "data_quality"."field_lineage"."record_lineage_id" IS 'Reference to the parent record lineage.';

ALTER TABLE "enterprise"."party_relationships" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "enterprise"."party_relationships" ADD FOREIGN KEY ("related_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "enterprise"."customer_demographics" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "enterprise"."customer_demographics" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "enterprise"."customer_demographics" ADD FOREIGN KEY ("credit_cards_card_accounts_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "enterprise"."party_entity_addresses" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "enterprise"."party_entity_addresses" ADD FOREIGN KEY ("enterprise_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "enterprise"."account_ownership" ADD FOREIGN KEY ("enterprise_account_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "enterprise"."account_ownership" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "enterprise"."associates" ADD FOREIGN KEY ("enterprise_department_id") REFERENCES "enterprise"."departments" ("enterprise_department_id");

ALTER TABLE "enterprise"."associates" ADD FOREIGN KEY ("manager_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "enterprise"."associates" ADD FOREIGN KEY ("enterprise_building_id") REFERENCES "enterprise"."buildings" ("enterprise_building_id");

ALTER TABLE "enterprise"."buildings" ADD FOREIGN KEY ("enterprise_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_banking"."accounts" ADD FOREIGN KEY ("enterprise_account_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "consumer_banking"."accounts" ADD FOREIGN KEY ("consumer_banking_product_id") REFERENCES "consumer_banking"."products" ("consumer_banking_product_id");

ALTER TABLE "consumer_banking"."accounts" ADD FOREIGN KEY ("currency_code") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."accounts" ADD FOREIGN KEY ("servicer_identifier_id") REFERENCES "enterprise"."identifiers" ("enterprise_identifier_id");

ALTER TABLE "consumer_banking"."account_access_consents" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."account_access_consents_permissions" ADD FOREIGN KEY ("consumer_banking_consent_id") REFERENCES "consumer_banking"."account_access_consents" ("consumer_banking_consent_id");

ALTER TABLE "consumer_banking"."account_access_consents_permissions" ADD FOREIGN KEY ("enterprise_permission_id") REFERENCES "enterprise"."permissions" ("enterprise_permission_id");

ALTER TABLE "consumer_banking"."balances" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."balances" ADD FOREIGN KEY ("currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."beneficiaries" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."beneficiary_creditor_agents" ADD FOREIGN KEY ("consumer_banking_beneficiary_id") REFERENCES "consumer_banking"."beneficiaries" ("consumer_banking_beneficiary_id");

ALTER TABLE "consumer_banking"."beneficiary_creditor_accounts" ADD FOREIGN KEY ("consumer_banking_beneficiary_id") REFERENCES "consumer_banking"."beneficiaries" ("consumer_banking_beneficiary_id");

ALTER TABLE "consumer_banking"."direct_debits" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."mandate_related_information" ADD FOREIGN KEY ("consumer_banking_direct_debit_id") REFERENCES "consumer_banking"."direct_debits" ("consumer_banking_direct_debit_id");

ALTER TABLE "consumer_banking"."offers" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."offers" ADD FOREIGN KEY ("amount_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."offers" ADD FOREIGN KEY ("fee_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."other_product_types" ADD FOREIGN KEY ("consumer_banking_product_id") REFERENCES "consumer_banking"."products" ("consumer_banking_product_id");

ALTER TABLE "consumer_banking"."scheduled_payments" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."scheduled_payments" ADD FOREIGN KEY ("instructed_amount_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."scheduled_payment_creditor_agents" ADD FOREIGN KEY ("consumer_banking_scheduled_payment_id") REFERENCES "consumer_banking"."scheduled_payments" ("consumer_banking_scheduled_payment_id");

ALTER TABLE "consumer_banking"."scheduled_payment_creditor_accounts" ADD FOREIGN KEY ("consumer_banking_scheduled_payment_id") REFERENCES "consumer_banking"."scheduled_payments" ("consumer_banking_scheduled_payment_id");

ALTER TABLE "consumer_banking"."standing_orders" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."standing_orders" ADD FOREIGN KEY ("first_payment_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."standing_orders" ADD FOREIGN KEY ("next_payment_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."standing_orders" ADD FOREIGN KEY ("last_payment_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."standing_orders" ADD FOREIGN KEY ("final_payment_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."standing_order_creditor_agents" ADD FOREIGN KEY ("consumer_banking_standing_order_id") REFERENCES "consumer_banking"."standing_orders" ("consumer_banking_standing_order_id");

ALTER TABLE "consumer_banking"."standing_order_creditor_accounts" ADD FOREIGN KEY ("consumer_banking_standing_order_id") REFERENCES "consumer_banking"."standing_orders" ("consumer_banking_standing_order_id");

ALTER TABLE "consumer_banking"."statements" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."statement_descriptions" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."statement_benefits" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."statement_fees" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."statement_fees" ADD FOREIGN KEY ("currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."statement_interests" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."statement_interests" ADD FOREIGN KEY ("currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."statement_amounts" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."statement_amounts" ADD FOREIGN KEY ("currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."statement_date_times" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."statement_rates" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."statement_values" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."transactions" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."transactions" ADD FOREIGN KEY ("consumer_banking_balance_id") REFERENCES "consumer_banking"."balances" ("consumer_banking_balance_id");

ALTER TABLE "consumer_banking"."transactions" ADD FOREIGN KEY ("currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."transactions" ADD FOREIGN KEY ("charge_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."transaction_statement_references" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_currency_exchanges" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_currency_exchanges" ADD FOREIGN KEY ("source_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."transaction_currency_exchanges" ADD FOREIGN KEY ("target_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."transaction_currency_exchanges" ADD FOREIGN KEY ("unit_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."transaction_currency_exchanges" ADD FOREIGN KEY ("instructed_amount_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."transaction_bank_transaction_codes" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."proprietary_transaction_codes" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_balances" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_balances" ADD FOREIGN KEY ("currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "consumer_banking"."transaction_merchant_details" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_creditor_agents" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_creditor_accounts" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_debtor_agents" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_debtor_accounts" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_card_instruments" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_ultimate_creditors" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."transaction_ultimate_debtors" ADD FOREIGN KEY ("consumer_banking_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "consumer_banking"."account_statement_preferences" ADD FOREIGN KEY ("consumer_banking_account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."account_statement_preferences" ADD FOREIGN KEY ("consumer_banking_statement_id") REFERENCES "consumer_banking"."statements" ("consumer_banking_statement_id");

ALTER TABLE "consumer_banking"."account_statement_preferences" ADD FOREIGN KEY ("enterprise_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_banking"."customer_interactions" ADD FOREIGN KEY ("customer_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "consumer_banking"."customer_interactions" ADD FOREIGN KEY ("account_id") REFERENCES "consumer_banking"."accounts" ("consumer_banking_account_id");

ALTER TABLE "consumer_banking"."customer_interactions" ADD FOREIGN KEY ("enterprise_associate_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_banking"."customer_interactions" ADD FOREIGN KEY ("related_transaction_id") REFERENCES "consumer_banking"."transactions" ("consumer_banking_transaction_id");

ALTER TABLE "mortgage_services"."application_borrowers" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."application_borrowers" ADD FOREIGN KEY ("mortgage_services_borrower_id") REFERENCES "mortgage_services"."borrowers" ("mortgage_services_borrower_id");

ALTER TABLE "mortgage_services"."borrowers" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "mortgage_services"."borrowers" ADD FOREIGN KEY ("current_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "mortgage_services"."borrowers" ADD FOREIGN KEY ("mailing_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "mortgage_services"."borrowers" ADD FOREIGN KEY ("previous_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "mortgage_services"."borrower_employments" ADD FOREIGN KEY ("mortgage_services_borrower_id") REFERENCES "mortgage_services"."borrowers" ("mortgage_services_borrower_id");

ALTER TABLE "mortgage_services"."borrower_incomes" ADD FOREIGN KEY ("mortgage_services_borrower_id") REFERENCES "mortgage_services"."borrowers" ("mortgage_services_borrower_id");

ALTER TABLE "mortgage_services"."borrower_assets" ADD FOREIGN KEY ("mortgage_services_borrower_id") REFERENCES "mortgage_services"."borrowers" ("mortgage_services_borrower_id");

ALTER TABLE "mortgage_services"."borrower_liabilities" ADD FOREIGN KEY ("mortgage_services_borrower_id") REFERENCES "mortgage_services"."borrowers" ("mortgage_services_borrower_id");

ALTER TABLE "mortgage_services"."properties" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."applications" ADD FOREIGN KEY ("mortgage_services_loan_product_id") REFERENCES "mortgage_services"."loan_products" ("mortgage_services_loan_product_id");

ALTER TABLE "mortgage_services"."applications" ADD FOREIGN KEY ("loan_officer_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "mortgage_services"."applications" ADD FOREIGN KEY ("branch_id") REFERENCES "enterprise"."buildings" ("enterprise_building_id");

ALTER TABLE "mortgage_services"."loans" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."loans" ADD FOREIGN KEY ("enterprise_account_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "mortgage_services"."loan_rate_locks" ADD FOREIGN KEY ("mortgage_services_loan_id") REFERENCES "mortgage_services"."loans" ("mortgage_services_loan_id");

ALTER TABLE "mortgage_services"."documents" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."documents" ADD FOREIGN KEY ("reviewer_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "mortgage_services"."conditions" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."conditions" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "mortgage_services"."conditions" ADD FOREIGN KEY ("cleared_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "mortgage_services"."appraisals" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."appraisals" ADD FOREIGN KEY ("mortgage_services_property_id") REFERENCES "mortgage_services"."properties" ("mortgage_services_property_id");

ALTER TABLE "mortgage_services"."credit_reports" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."credit_reports" ADD FOREIGN KEY ("mortgage_services_borrower_id") REFERENCES "mortgage_services"."borrowers" ("mortgage_services_borrower_id");

ALTER TABLE "mortgage_services"."closing_disclosures" ADD FOREIGN KEY ("mortgage_services_loan_id") REFERENCES "mortgage_services"."loans" ("mortgage_services_loan_id");

ALTER TABLE "mortgage_services"."closing_appointments" ADD FOREIGN KEY ("mortgage_services_loan_id") REFERENCES "mortgage_services"."loans" ("mortgage_services_loan_id");

ALTER TABLE "mortgage_services"."closing_appointments" ADD FOREIGN KEY ("location_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "mortgage_services"."closed_loans" ADD FOREIGN KEY ("mortgage_services_loan_id") REFERENCES "mortgage_services"."loans" ("mortgage_services_loan_id");

ALTER TABLE "mortgage_services"."servicing_accounts" ADD FOREIGN KEY ("mortgage_services_loan_id") REFERENCES "mortgage_services"."loans" ("mortgage_services_loan_id");

ALTER TABLE "mortgage_services"."payments" ADD FOREIGN KEY ("mortgage_services_servicing_account_id") REFERENCES "mortgage_services"."servicing_accounts" ("mortgage_services_servicing_account_id");

ALTER TABLE "mortgage_services"."escrow_disbursements" ADD FOREIGN KEY ("mortgage_services_servicing_account_id") REFERENCES "mortgage_services"."servicing_accounts" ("mortgage_services_servicing_account_id");

ALTER TABLE "mortgage_services"."escrow_analyses" ADD FOREIGN KEY ("mortgage_services_servicing_account_id") REFERENCES "mortgage_services"."servicing_accounts" ("mortgage_services_servicing_account_id");

ALTER TABLE "mortgage_services"."insurance_policies" ADD FOREIGN KEY ("mortgage_services_servicing_account_id") REFERENCES "mortgage_services"."servicing_accounts" ("mortgage_services_servicing_account_id");

ALTER TABLE "mortgage_services"."loan_modifications" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "mortgage_services"."loan_modifications" ADD FOREIGN KEY ("approved_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "mortgage_services"."customer_communications" ADD FOREIGN KEY ("mortgage_services_servicing_account_id") REFERENCES "mortgage_services"."servicing_accounts" ("mortgage_services_servicing_account_id");

ALTER TABLE "mortgage_services"."customer_communications" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."hmda_records" ADD FOREIGN KEY ("mortgage_services_application_id") REFERENCES "mortgage_services"."applications" ("mortgage_services_application_id");

ALTER TABLE "mortgage_services"."hmda_records" ADD FOREIGN KEY ("mortgage_services_loan_id") REFERENCES "mortgage_services"."loans" ("mortgage_services_loan_id");

ALTER TABLE "mortgage_services"."hmda_records" ADD FOREIGN KEY ("mortgage_services_loan_product_id") REFERENCES "mortgage_services"."loan_products" ("mortgage_services_loan_product_id");

ALTER TABLE "mortgage_services"."hmda_applicant_demographics" ADD FOREIGN KEY ("mortgage_services_hmda_record_id") REFERENCES "mortgage_services"."hmda_records" ("mortgage_services_hmda_record_id");

ALTER TABLE "mortgage_services"."hmda_edits" ADD FOREIGN KEY ("mortgage_services_hmda_record_id") REFERENCES "mortgage_services"."hmda_records" ("mortgage_services_hmda_record_id");

ALTER TABLE "mortgage_services"."hmda_edits" ADD FOREIGN KEY ("resolved_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "mortgage_services"."hmda_submissions" ADD FOREIGN KEY ("submitted_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."loan_applications" ADD FOREIGN KEY ("customer_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "consumer_lending"."loan_applications" ADD FOREIGN KEY ("officer_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."loan_applications" ADD FOREIGN KEY ("branch_id") REFERENCES "enterprise"."buildings" ("enterprise_building_id");

ALTER TABLE "consumer_lending"."application_applicants" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."application_applicants" ADD FOREIGN KEY ("consumer_lending_applicant_id") REFERENCES "consumer_lending"."applicants" ("consumer_lending_applicant_id");

ALTER TABLE "consumer_lending"."applicants" ADD FOREIGN KEY ("current_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_lending"."applicants" ADD FOREIGN KEY ("mailing_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_lending"."applicants" ADD FOREIGN KEY ("previous_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_lending"."applicant_employments" ADD FOREIGN KEY ("consumer_lending_applicant_id") REFERENCES "consumer_lending"."applicants" ("consumer_lending_applicant_id");

ALTER TABLE "consumer_lending"."applicant_employments" ADD FOREIGN KEY ("enterprise_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_lending"."applicant_incomes" ADD FOREIGN KEY ("consumer_lending_applicant_id") REFERENCES "consumer_lending"."applicants" ("consumer_lending_applicant_id");

ALTER TABLE "consumer_lending"."applicant_assets" ADD FOREIGN KEY ("consumer_lending_applicant_id") REFERENCES "consumer_lending"."applicants" ("consumer_lending_applicant_id");

ALTER TABLE "consumer_lending"."applicant_assets" ADD FOREIGN KEY ("property_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_lending"."applicant_liabilities" ADD FOREIGN KEY ("consumer_lending_applicant_id") REFERENCES "consumer_lending"."applicants" ("consumer_lending_applicant_id");

ALTER TABLE "consumer_lending"."product_eligibility_criteria" ADD FOREIGN KEY ("consumer_lending_loan_product_id") REFERENCES "consumer_lending"."loan_products" ("consumer_lending_loan_product_id");

ALTER TABLE "consumer_lending"."risk_based_pricing_tiers" ADD FOREIGN KEY ("consumer_lending_loan_product_id") REFERENCES "consumer_lending"."loan_products" ("consumer_lending_loan_product_id");

ALTER TABLE "consumer_lending"."credit_reports" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."credit_reports" ADD FOREIGN KEY ("consumer_lending_applicant_id") REFERENCES "consumer_lending"."applicants" ("consumer_lending_applicant_id");

ALTER TABLE "consumer_lending"."credit_report_tradelines" ADD FOREIGN KEY ("consumer_lending_credit_report_id") REFERENCES "consumer_lending"."credit_reports" ("consumer_lending_credit_report_id");

ALTER TABLE "consumer_lending"."credit_inquiries" ADD FOREIGN KEY ("consumer_lending_credit_report_id") REFERENCES "consumer_lending"."credit_reports" ("consumer_lending_credit_report_id");

ALTER TABLE "consumer_lending"."public_records" ADD FOREIGN KEY ("consumer_lending_credit_report_id") REFERENCES "consumer_lending"."credit_reports" ("consumer_lending_credit_report_id");

ALTER TABLE "consumer_lending"."application_decisions" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."application_decisions" ADD FOREIGN KEY ("decision_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."application_decisions" ADD FOREIGN KEY ("consumer_lending_model_id") REFERENCES "consumer_lending"."decision_models" ("consumer_lending_model_id");

ALTER TABLE "consumer_lending"."application_decisions" ADD FOREIGN KEY ("consumer_lending_pricing_tier_id") REFERENCES "consumer_lending"."risk_based_pricing_tiers" ("consumer_lending_pricing_tier_id");

ALTER TABLE "consumer_lending"."decision_reasons" ADD FOREIGN KEY ("consumer_lending_decision_id") REFERENCES "consumer_lending"."application_decisions" ("consumer_lending_decision_id");

ALTER TABLE "consumer_lending"."adverse_action_notices" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."vehicles" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."vehicles" ADD FOREIGN KEY ("dealer_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_lending"."loan_accounts" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."loan_accounts" ADD FOREIGN KEY ("consumer_lending_loan_product_id") REFERENCES "consumer_lending"."loan_products" ("consumer_lending_loan_product_id");

ALTER TABLE "consumer_lending"."payment_schedules" ADD FOREIGN KEY ("consumer_lending_loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."payment_schedules" ADD FOREIGN KEY ("actual_payment_id") REFERENCES "consumer_lending"."loan_payments" ("consumer_lending_payment_id");

ALTER TABLE "consumer_lending"."disbursements" ADD FOREIGN KEY ("consumer_lending_loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."loan_payments" ADD FOREIGN KEY ("consumer_lending_loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."loan_fees" ADD FOREIGN KEY ("consumer_lending_loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."loan_fees" ADD FOREIGN KEY ("waived_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."loan_fees" ADD FOREIGN KEY ("consumer_lending_payment_id") REFERENCES "consumer_lending"."loan_payments" ("consumer_lending_payment_id");

ALTER TABLE "consumer_lending"."loan_collateral" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."loan_collateral" ADD FOREIGN KEY ("vehicle_id") REFERENCES "consumer_lending"."vehicles" ("vehicle_id");

ALTER TABLE "consumer_lending"."loan_collateral" ADD FOREIGN KEY ("property_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_lending"."loan_collateral" ADD FOREIGN KEY ("deposit_account_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "consumer_lending"."loan_insurance" ADD FOREIGN KEY ("consumer_lending_loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."loan_insurance" ADD FOREIGN KEY ("consumer_lending_collateral_id") REFERENCES "consumer_lending"."loan_collateral" ("consumer_lending_collateral_id");

ALTER TABLE "consumer_lending"."loan_documents" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."loan_documents" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."loan_communications" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."loan_communications" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."loan_statements" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."collection_accounts" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."collection_actions" ADD FOREIGN KEY ("consumer_lending_collection_id") REFERENCES "consumer_lending"."collection_accounts" ("consumer_lending_collection_id");

ALTER TABLE "consumer_lending"."collection_actions" ADD FOREIGN KEY ("action_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."payment_arrangements" ADD FOREIGN KEY ("consumer_lending_collection_id") REFERENCES "consumer_lending"."collection_accounts" ("consumer_lending_collection_id");

ALTER TABLE "consumer_lending"."payment_arrangements" ADD FOREIGN KEY ("approved_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."loan_modifications" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."loan_modifications" ADD FOREIGN KEY ("approved_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."reg_z_disclosures" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."reg_z_disclosures" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."adverse_action_details" ADD FOREIGN KEY ("consumer_lending_notice_id") REFERENCES "consumer_lending"."adverse_action_notices" ("consumer_lending_notice_id");

ALTER TABLE "consumer_lending"."adverse_action_details" ADD FOREIGN KEY ("user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."ecoa_monitoring" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."ecoa_monitoring" ADD FOREIGN KEY ("consumer_lending_applicant_id") REFERENCES "consumer_lending"."applicants" ("consumer_lending_applicant_id");

ALTER TABLE "consumer_lending"."ecoa_monitoring" ADD FOREIGN KEY ("submitted_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."fairlending_analysis" ADD FOREIGN KEY ("consumer_lending_loan_product_id") REFERENCES "consumer_lending"."loan_products" ("consumer_lending_loan_product_id");

ALTER TABLE "consumer_lending"."fairlending_analysis" ADD FOREIGN KEY ("analyst") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."fairlending_analysis" ADD FOREIGN KEY ("reviewer") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."reg_b_notices" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."reg_b_notices" ADD FOREIGN KEY ("user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."appraisal_disclosures" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."appraisal_disclosures" ADD FOREIGN KEY ("property_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "consumer_lending"."appraisal_disclosures" ADD FOREIGN KEY ("user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."military_lending_checks" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."military_lending_checks" ADD FOREIGN KEY ("consumer_lending_applicant_id") REFERENCES "consumer_lending"."applicants" ("consumer_lending_applicant_id");

ALTER TABLE "consumer_lending"."military_lending_checks" ADD FOREIGN KEY ("user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."high_cost_mortgage_tests" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."high_cost_mortgage_tests" ADD FOREIGN KEY ("user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."compliance_exceptions" ADD FOREIGN KEY ("consumer_lending_application_id") REFERENCES "consumer_lending"."loan_applications" ("consumer_lending_application_id");

ALTER TABLE "consumer_lending"."compliance_exceptions" ADD FOREIGN KEY ("loan_account_id") REFERENCES "consumer_lending"."loan_accounts" ("consumer_lending_loan_account_id");

ALTER TABLE "consumer_lending"."compliance_exceptions" ADD FOREIGN KEY ("identified_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "consumer_lending"."compliance_exceptions" ADD FOREIGN KEY ("remediated_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "credit_cards"."fraud_cases" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."fraud_cases" ADD FOREIGN KEY ("credit_cards_card_id") REFERENCES "credit_cards"."cards" ("credit_cards_card_id");

ALTER TABLE "credit_cards"."fraud_cases" ADD FOREIGN KEY ("investigator_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "credit_cards"."fraud_transactions" ADD FOREIGN KEY ("credit_cards_case_id") REFERENCES "credit_cards"."fraud_cases" ("credit_cards_case_id");

ALTER TABLE "credit_cards"."fraud_transactions" ADD FOREIGN KEY ("credit_cards_transaction_id") REFERENCES "credit_cards"."transactions" ("credit_cards_transaction_id");

ALTER TABLE "credit_cards"."security_blocks" ADD FOREIGN KEY ("credit_cards_card_id") REFERENCES "credit_cards"."cards" ("credit_cards_card_id");

ALTER TABLE "credit_cards"."security_blocks" ADD FOREIGN KEY ("removed_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "credit_cards"."credit_card_applications_hmda" ADD FOREIGN KEY ("credit_cards_application_id") REFERENCES "credit_cards"."applications" ("credit_cards_application_id");

ALTER TABLE "credit_cards"."reg_z_credit_card_disclosures" ADD FOREIGN KEY ("credit_cards_application_id") REFERENCES "credit_cards"."applications" ("credit_cards_application_id");

ALTER TABLE "credit_cards"."reg_z_credit_card_disclosures" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."ability_to_pay_assessments" ADD FOREIGN KEY ("credit_cards_application_id") REFERENCES "credit_cards"."applications" ("credit_cards_application_id");

ALTER TABLE "credit_cards"."ability_to_pay_assessments" ADD FOREIGN KEY ("performed_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "credit_cards"."consumer_complaints" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."card_product_features" ADD FOREIGN KEY ("credit_cards_product_id") REFERENCES "credit_cards"."card_products" ("credit_cards_product_id");

ALTER TABLE "credit_cards"."card_product_reward_categories" ADD FOREIGN KEY ("credit_cards_product_id") REFERENCES "credit_cards"."card_products" ("credit_cards_product_id");

ALTER TABLE "credit_cards"."applications" ADD FOREIGN KEY ("customer_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "credit_cards"."applications" ADD FOREIGN KEY ("credit_cards_product_id") REFERENCES "credit_cards"."card_products" ("credit_cards_product_id");

ALTER TABLE "credit_cards"."card_accounts" ADD FOREIGN KEY ("customer_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "credit_cards"."card_accounts" ADD FOREIGN KEY ("enterprise_account_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "credit_cards"."card_accounts" ADD FOREIGN KEY ("credit_cards_product_id") REFERENCES "credit_cards"."card_products" ("credit_cards_product_id");

ALTER TABLE "credit_cards"."card_accounts" ADD FOREIGN KEY ("credit_cards_application_id") REFERENCES "credit_cards"."applications" ("credit_cards_application_id");

ALTER TABLE "credit_cards"."cards" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."cards" ADD FOREIGN KEY ("user_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "credit_cards"."authorized_users" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."authorized_users" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "credit_cards"."transactions" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."transactions" ADD FOREIGN KEY ("credit_cards_card_id") REFERENCES "credit_cards"."cards" ("credit_cards_card_id");

ALTER TABLE "credit_cards"."transactions" ADD FOREIGN KEY ("original_currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "credit_cards"."statements" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."fees" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."fees" ADD FOREIGN KEY ("credit_cards_transaction_id") REFERENCES "credit_cards"."transactions" ("credit_cards_transaction_id");

ALTER TABLE "credit_cards"."fees" ADD FOREIGN KEY ("credit_cards_statement_id") REFERENCES "credit_cards"."statements" ("credit_cards_statement_id");

ALTER TABLE "credit_cards"."interest_charges" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."interest_charges" ADD FOREIGN KEY ("credit_cards_statement_id") REFERENCES "credit_cards"."statements" ("credit_cards_statement_id");

ALTER TABLE "credit_cards"."rewards" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."rewards" ADD FOREIGN KEY ("credit_cards_transaction_id") REFERENCES "credit_cards"."transactions" ("credit_cards_transaction_id");

ALTER TABLE "credit_cards"."reward_redemptions" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."reward_redemptions" ADD FOREIGN KEY ("shipping_address_id") REFERENCES "enterprise"."addresses" ("enterprise_address_id");

ALTER TABLE "credit_cards"."promotional_offers" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."balance_transfers" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."balance_transfers" ADD FOREIGN KEY ("credit_cards_transaction_id") REFERENCES "credit_cards"."transactions" ("credit_cards_transaction_id");

ALTER TABLE "credit_cards"."balance_transfers" ADD FOREIGN KEY ("credit_cards_offer_id") REFERENCES "credit_cards"."promotional_offers" ("credit_cards_offer_id");

ALTER TABLE "credit_cards"."payment_methods" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."autopay_settings" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."autopay_settings" ADD FOREIGN KEY ("credit_cards_payment_method_id") REFERENCES "credit_cards"."payment_methods" ("credit_cards_payment_method_id");

ALTER TABLE "credit_cards"."credit_limit_changes" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."credit_limit_changes" ADD FOREIGN KEY ("approved_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "credit_cards"."card_alerts" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "credit_cards"."card_alerts" ADD FOREIGN KEY ("credit_cards_card_id") REFERENCES "credit_cards"."cards" ("credit_cards_card_id");

ALTER TABLE "credit_cards"."disputed_transactions" ADD FOREIGN KEY ("credit_cards_transaction_id") REFERENCES "credit_cards"."transactions" ("credit_cards_transaction_id");

ALTER TABLE "credit_cards"."disputed_transactions" ADD FOREIGN KEY ("credit_cards_card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "small_business_banking"."businesses" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "small_business_banking"."business_owners" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."business_owners" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "small_business_banking"."accounts" ADD FOREIGN KEY ("enterprise_account_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "small_business_banking"."accounts" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."accounts" ADD FOREIGN KEY ("small_business_banking_product_id") REFERENCES "small_business_banking"."products" ("small_business_banking_product_id");

ALTER TABLE "small_business_banking"."accounts" ADD FOREIGN KEY ("currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "small_business_banking"."account_signatories" ADD FOREIGN KEY ("small_business_banking_account_id") REFERENCES "small_business_banking"."accounts" ("small_business_banking_account_id");

ALTER TABLE "small_business_banking"."account_signatories" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "small_business_banking"."loans" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."loans" ADD FOREIGN KEY ("small_business_banking_account_id") REFERENCES "small_business_banking"."accounts" ("small_business_banking_account_id");

ALTER TABLE "small_business_banking"."loans" ADD FOREIGN KEY ("small_business_banking_product_id") REFERENCES "small_business_banking"."products" ("small_business_banking_product_id");

ALTER TABLE "small_business_banking"."credit_lines" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."credit_lines" ADD FOREIGN KEY ("small_business_banking_account_id") REFERENCES "small_business_banking"."accounts" ("small_business_banking_account_id");

ALTER TABLE "small_business_banking"."credit_lines" ADD FOREIGN KEY ("small_business_banking_product_id") REFERENCES "small_business_banking"."products" ("small_business_banking_product_id");

ALTER TABLE "small_business_banking"."collateral" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."loan_collateral" ADD FOREIGN KEY ("small_business_banking_loan_id") REFERENCES "small_business_banking"."loans" ("small_business_banking_loan_id");

ALTER TABLE "small_business_banking"."loan_collateral" ADD FOREIGN KEY ("small_business_banking_collateral_id") REFERENCES "small_business_banking"."collateral" ("small_business_banking_collateral_id");

ALTER TABLE "small_business_banking"."business_card_accounts" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."business_card_accounts" ADD FOREIGN KEY ("card_account_id") REFERENCES "credit_cards"."card_accounts" ("credit_cards_card_account_id");

ALTER TABLE "small_business_banking"."business_card_accounts" ADD FOREIGN KEY ("credit_cards_product_id") REFERENCES "credit_cards"."card_products" ("credit_cards_product_id");

ALTER TABLE "small_business_banking"."business_card_accounts" ADD FOREIGN KEY ("linked_deposit_account_id") REFERENCES "small_business_banking"."accounts" ("small_business_banking_account_id");

ALTER TABLE "small_business_banking"."business_card_users" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."business_card_users" ADD FOREIGN KEY ("small_business_banking_business_card_account_id") REFERENCES "small_business_banking"."business_card_accounts" ("small_business_banking_business_card_account_id");

ALTER TABLE "small_business_banking"."business_card_users" ADD FOREIGN KEY ("enterprise_party_id") REFERENCES "enterprise"."parties" ("enterprise_party_id");

ALTER TABLE "small_business_banking"."business_card_users" ADD FOREIGN KEY ("credit_cards_card_id") REFERENCES "credit_cards"."cards" ("credit_cards_card_id");

ALTER TABLE "small_business_banking"."business_expense_categories" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."business_expense_categories" ADD FOREIGN KEY ("parent_category_id") REFERENCES "small_business_banking"."business_expense_categories" ("small_business_banking_category_id");

ALTER TABLE "small_business_banking"."business_transaction_categories" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."business_transaction_categories" ADD FOREIGN KEY ("small_business_banking_category_id") REFERENCES "small_business_banking"."business_expense_categories" ("small_business_banking_category_id");

ALTER TABLE "small_business_banking"."business_transaction_categories" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."transactions" ADD FOREIGN KEY ("small_business_banking_account_id") REFERENCES "small_business_banking"."accounts" ("small_business_banking_account_id");

ALTER TABLE "small_business_banking"."transactions" ADD FOREIGN KEY ("currency") REFERENCES "enterprise"."currency" ("code");

ALTER TABLE "small_business_banking"."transactions" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."payments" ADD FOREIGN KEY ("source_account_id") REFERENCES "small_business_banking"."accounts" ("small_business_banking_account_id");

ALTER TABLE "small_business_banking"."payments" ADD FOREIGN KEY ("destination_account_id") REFERENCES "small_business_banking"."accounts" ("small_business_banking_account_id");

ALTER TABLE "small_business_banking"."payments" ADD FOREIGN KEY ("small_business_banking_loan_id") REFERENCES "small_business_banking"."loans" ("small_business_banking_loan_id");

ALTER TABLE "small_business_banking"."payments" ADD FOREIGN KEY ("small_business_banking_credit_line_id") REFERENCES "small_business_banking"."credit_lines" ("small_business_banking_credit_line_id");

ALTER TABLE "small_business_banking"."payments" ADD FOREIGN KEY ("credit_card_id") REFERENCES "small_business_banking"."business_card_accounts" ("small_business_banking_business_card_account_id");

ALTER TABLE "small_business_banking"."documents" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."documents" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."regulatory_reports" ADD FOREIGN KEY ("report_owner") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."report_submissions" ADD FOREIGN KEY ("small_business_banking_report_id") REFERENCES "small_business_banking"."regulatory_reports" ("small_business_banking_report_id");

ALTER TABLE "small_business_banking"."report_submissions" ADD FOREIGN KEY ("submitted_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."regulatory_findings" ADD FOREIGN KEY ("small_business_banking_report_id") REFERENCES "small_business_banking"."regulatory_reports" ("small_business_banking_report_id");

ALTER TABLE "small_business_banking"."regulatory_findings" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."regulatory_findings" ADD FOREIGN KEY ("responsible_party") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."compliance_cases" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."compliance_cases" ADD FOREIGN KEY ("assigned_to") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."compliance_requirements" ADD FOREIGN KEY ("requirement_owner") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."business_risk_assessments" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."business_risk_assessments" ADD FOREIGN KEY ("conducted_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."loan_fair_lending" ADD FOREIGN KEY ("small_business_banking_loan_id") REFERENCES "small_business_banking"."loans" ("small_business_banking_loan_id");

ALTER TABLE "small_business_banking"."loan_fair_lending" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."credit_decisions" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."credit_decisions" ADD FOREIGN KEY ("exception_approver") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."credit_decisions" ADD FOREIGN KEY ("decision_made_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."adverse_action_notices" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."adverse_action_notices" ADD FOREIGN KEY ("small_business_banking_decision_id") REFERENCES "small_business_banking"."credit_decisions" ("small_business_banking_decision_id");

ALTER TABLE "small_business_banking"."adverse_action_notices" ADD FOREIGN KEY ("generated_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."business_due_diligence" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."business_due_diligence" ADD FOREIGN KEY ("performed_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."business_due_diligence" ADD FOREIGN KEY ("approved_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."beneficial_owner_verification" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."beneficial_owner_verification" ADD FOREIGN KEY ("small_business_banking_business_owner_id") REFERENCES "small_business_banking"."business_owners" ("small_business_banking_business_owner_id");

ALTER TABLE "small_business_banking"."beneficial_owner_verification" ADD FOREIGN KEY ("performed_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."suspicious_activity_reports" ADD FOREIGN KEY ("small_business_banking_business_id") REFERENCES "small_business_banking"."businesses" ("small_business_banking_business_id");

ALTER TABLE "small_business_banking"."suspicious_activity_reports" ADD FOREIGN KEY ("prepared_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."suspicious_activity_reports" ADD FOREIGN KEY ("approved_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "small_business_banking"."suspicious_activity_reports" ADD FOREIGN KEY ("bsa_officer_signature") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."identity_roles" ADD FOREIGN KEY ("security_identity_id") REFERENCES "security"."identities" ("security_identity_id");

ALTER TABLE "security"."identity_roles" ADD FOREIGN KEY ("security_role_id") REFERENCES "security"."roles" ("security_role_id");

ALTER TABLE "security"."identity_roles" ADD FOREIGN KEY ("assigned_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."roles" ADD FOREIGN KEY ("managing_application_id") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "security"."roles" ADD FOREIGN KEY ("owner_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."roles" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."security_account_roles" ADD FOREIGN KEY ("security_account_id") REFERENCES "security"."accounts" ("security_account_id");

ALTER TABLE "security"."security_account_roles" ADD FOREIGN KEY ("security_role_id") REFERENCES "security"."roles" ("security_role_id");

ALTER TABLE "security"."security_account_roles" ADD FOREIGN KEY ("assigned_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."security_account_enterprise_accounts" ADD FOREIGN KEY ("security_account_id") REFERENCES "security"."accounts" ("security_account_id");

ALTER TABLE "security"."security_account_enterprise_accounts" ADD FOREIGN KEY ("enterprise_account_id") REFERENCES "enterprise"."accounts" ("enterprise_account_id");

ALTER TABLE "security"."security_account_enterprise_accounts" ADD FOREIGN KEY ("assigned_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."role_entitlements" ADD FOREIGN KEY ("security_role_id") REFERENCES "security"."roles" ("security_role_id");

ALTER TABLE "security"."role_entitlements" ADD FOREIGN KEY ("security_entitlement_id") REFERENCES "security"."enhanced_entitlements" ("security_entitlement_id");

ALTER TABLE "security"."role_entitlements" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."role_entitlements" ADD FOREIGN KEY ("updated_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."enhanced_entitlements" ADD FOREIGN KEY ("managing_application_id") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "security"."enhanced_entitlements" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."entitlement_resources" ADD FOREIGN KEY ("security_entitlement_id") REFERENCES "security"."enhanced_entitlements" ("security_entitlement_id");

ALTER TABLE "security"."entitlement_resources" ADD FOREIGN KEY ("security_resource_id") REFERENCES "security"."resource_definitions" ("security_resource_id");

ALTER TABLE "security"."entitlement_resources" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."resource_definitions" ADD FOREIGN KEY ("application_id") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "security"."resource_definitions" ADD FOREIGN KEY ("host_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."resource_definitions" ADD FOREIGN KEY ("network_device_id") REFERENCES "security"."devices" ("security_device_id");

ALTER TABLE "security"."resource_definitions" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."network_events" ADD FOREIGN KEY ("security_device_id") REFERENCES "security"."devices" ("security_device_id");

ALTER TABLE "security"."policies" ADD FOREIGN KEY ("created_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."policies" ADD FOREIGN KEY ("updated_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."policy_attributes" ADD FOREIGN KEY ("security_policy_id") REFERENCES "security"."policies" ("security_policy_id");

ALTER TABLE "security"."policy_rules" ADD FOREIGN KEY ("security_policy_id") REFERENCES "security"."policies" ("security_policy_id");

ALTER TABLE "security"."accounts" ADD FOREIGN KEY ("security_identity_id") REFERENCES "security"."identities" ("security_identity_id");

ALTER TABLE "security"."accounts" ADD FOREIGN KEY ("security_source_id") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "security"."governance_groups" ADD FOREIGN KEY ("owner_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."iam_logins" ADD FOREIGN KEY ("security_account_id") REFERENCES "security"."accounts" ("security_account_id");

ALTER TABLE "security"."identities" ADD FOREIGN KEY ("owner_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "security"."identities" ADD FOREIGN KEY ("security_identity_profile_id") REFERENCES "security"."identity_profiles" ("security_identity_profile_id");

ALTER TABLE "security"."file_accesses" ADD FOREIGN KEY ("security_system_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."file_accesses" ADD FOREIGN KEY ("security_file_id") REFERENCES "security"."files" ("security_file_id");

ALTER TABLE "security"."file_accesses" ADD FOREIGN KEY ("security_process_execution_id") REFERENCES "security"."process_executions" ("security_process_execution_id");

ALTER TABLE "security"."files" ADD FOREIGN KEY ("security_host_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."installed_applications" ADD FOREIGN KEY ("security_host_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."installed_applications" ADD FOREIGN KEY ("app_mgmt_application_id") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "security"."network_connections" ADD FOREIGN KEY ("security_host_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."network_connections" ADD FOREIGN KEY ("security_process_execution_id") REFERENCES "security"."process_executions" ("security_process_execution_id");

ALTER TABLE "security"."open_ports" ADD FOREIGN KEY ("security_host_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."process_executions" ADD FOREIGN KEY ("security_host_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."running_services" ADD FOREIGN KEY ("security_host_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."system_stats" ADD FOREIGN KEY ("security_host_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."usb_device_usage" ADD FOREIGN KEY ("security_system_id") REFERENCES "security"."hosts" ("security_host_id");

ALTER TABLE "security"."cpe" ADD FOREIGN KEY ("cve") REFERENCES "security"."cvss" ("cve");

ALTER TABLE "security"."cve_problem" ADD FOREIGN KEY ("cve") REFERENCES "security"."cvss" ("cve");

ALTER TABLE "security"."cve_problem" ADD FOREIGN KEY ("cwe_id") REFERENCES "security"."cwe" ("cwe_id");

ALTER TABLE "app_mgmt"."architectures" ADD FOREIGN KEY ("approved_by_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."architectures" ADD FOREIGN KEY ("sdlc_process_id") REFERENCES "app_mgmt"."sdlc_processes" ("app_mgmt_sdlc_process_id");

ALTER TABLE "app_mgmt"."architectures" ADD FOREIGN KEY ("created_by_user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."architectures" ADD FOREIGN KEY ("modified_by_user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."sdlc_processes" ADD FOREIGN KEY ("process_owner") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."sdlc_processes" ADD FOREIGN KEY ("app_mgmt_team_id") REFERENCES "app_mgmt"."teams" ("app_mgmt_team_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("enterprise_department_id") REFERENCES "enterprise"."departments" ("enterprise_department_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("operated_by_team_id") REFERENCES "app_mgmt"."teams" ("app_mgmt_team_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("maintained_by_team_id") REFERENCES "app_mgmt"."teams" ("app_mgmt_team_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("created_by_team_id") REFERENCES "app_mgmt"."teams" ("app_mgmt_team_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("application_owner_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("architecture_id") REFERENCES "app_mgmt"."architectures" ("app_mgmt_architecture_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("sdlc_process_id") REFERENCES "app_mgmt"."sdlc_processes" ("app_mgmt_sdlc_process_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("created_by_user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."applications" ADD FOREIGN KEY ("modified_by_user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."components" ADD FOREIGN KEY ("app_mgmt_license_id") REFERENCES "app_mgmt"."licenses" ("app_mgmt_license_id");

ALTER TABLE "app_mgmt"."components" ADD FOREIGN KEY ("created_by_user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."components" ADD FOREIGN KEY ("modified_by_user_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."component_dependencies" ADD FOREIGN KEY ("parent_component_id") REFERENCES "app_mgmt"."components" ("app_mgmt_component_id");

ALTER TABLE "app_mgmt"."component_dependencies" ADD FOREIGN KEY ("child_component_id") REFERENCES "app_mgmt"."components" ("app_mgmt_component_id");

ALTER TABLE "app_mgmt"."application_components" ADD FOREIGN KEY ("app_mgmt_application_id") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "app_mgmt"."application_components" ADD FOREIGN KEY ("app_mgmt_component_id") REFERENCES "app_mgmt"."components" ("app_mgmt_component_id");

ALTER TABLE "app_mgmt"."application_relationships" ADD FOREIGN KEY ("application_id_1") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "app_mgmt"."application_relationships" ADD FOREIGN KEY ("application_id_2") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "app_mgmt"."application_licenses" ADD FOREIGN KEY ("app_mgmt_application_id") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "app_mgmt"."application_licenses" ADD FOREIGN KEY ("app_mgmt_license_id") REFERENCES "app_mgmt"."licenses" ("app_mgmt_license_id");

ALTER TABLE "app_mgmt"."teams" ADD FOREIGN KEY ("team_lead_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "app_mgmt"."team_members" ADD FOREIGN KEY ("app_mgmt_team_id") REFERENCES "app_mgmt"."teams" ("app_mgmt_team_id");

ALTER TABLE "app_mgmt"."team_members" ADD FOREIGN KEY ("enterprise_associate_id") REFERENCES "enterprise"."associates" ("enterprise_associate_id");

ALTER TABLE "data_quality"."validation_error" ADD FOREIGN KEY ("validation_run_id") REFERENCES "data_quality"."validation_run" ("validation_run_id");

ALTER TABLE "data_quality"."record_transformations" ADD FOREIGN KEY ("api_call_id") REFERENCES "data_quality"."api_calls" ("api_call_id");

ALTER TABLE "data_quality"."field_transformation_details" ADD FOREIGN KEY ("record_transformation_id") REFERENCES "data_quality"."record_transformations" ("record_transformation_id");

ALTER TABLE "data_quality"."api_lineage" ADD FOREIGN KEY ("app_mgmt_application_id") REFERENCES "app_mgmt"."applications" ("app_mgmt_application_id");

ALTER TABLE "data_quality"."api_lineage" ADD FOREIGN KEY ("security_host_id", "host_app_mgmt_application_id") REFERENCES "security"."installed_applications" ("security_host_id", "app_mgmt_application_id");

ALTER TABLE "data_quality"."record_lineage" ADD FOREIGN KEY ("api_lineage_id") REFERENCES "data_quality"."api_lineage" ("api_lineage_id");

ALTER TABLE "data_quality"."field_lineage" ADD FOREIGN KEY ("record_lineage_id") REFERENCES "data_quality"."record_lineage" ("record_lineage_id");
