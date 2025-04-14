import datetime
import random
from typing import Any, Dict

from data_generator import DataGenerator, SkipRowGenerationError
from .enums import (EducationLevel, IncomeBracket, OccupationCategory,
                    HomeownershipStatus, PoliticalAffiliation, FamilyLifeStage,
                    LifestyleSegment, CreditRiskTier)


def generate_random_customer_demographics(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate random customer demographic data with plausible values and correlations.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated customer demographic data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'enterprise_party_id' not in id_fields:
        raise ValueError("enterprise_party_id is required")

    # Fetch the party to verify it exists and get additional context
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT p.enterprise_party_id, p.party_type, p.name, p.date_of_birth,
                   p.marital_status, p.citizenship_status, p.party_status
            FROM enterprise.parties p
            WHERE p.enterprise_party_id = %s
        """, (id_fields['enterprise_party_id'],))

        party = cursor.fetchone()

        if not party:
            raise ValueError(f"No party found with ID {id_fields['enterprise_party_id']}")

        # Extract party details to inform demographics
        party_type = party.get('party_type')
        name = party.get('name')
        date_of_birth = party.get('date_of_birth')
        marital_status = party.get('marital_status')
        citizenship_status = party.get('citizenship_status')
        party_status = party.get('party_status')

        # Skip if this is not an individual party
        if party_type != 'INDIVIDUAL':
            raise SkipRowGenerationError("Demographics only generated for individual parties")

        # Calculate age from date of birth if available
        age = None
        if date_of_birth:
            today = datetime.date.today()
            age = today.year - date_of_birth.year - (
                    (today.month, today.day) < (date_of_birth.month, date_of_birth.day))

        # Data sources for demographic data
        data_sources = [
            "Experian", "TransUnion", "Equifax",
            "Acxiom", "Epsilon", "Oracle Data Cloud",
            "Nielsen", "IXI Services", "CoreLogic",
            "LexisNexis Risk Solutions", "Altair", "Verisk Analytics",
            "First American", "Black Knight", "AnalyticsIQ",
            "InfoGroup", "Merkle", "Attom Data Solutions"
        ]

        data_source = random.choice(data_sources)

        # Last updated date (between 1 and 365 days ago)
        today = datetime.date.today()
        days_back = random.randint(1, 365)
        last_updated = today - datetime.timedelta(days=days_back)

        # EDUCATION LEVEL GENERATION
        # Age-correlated education level distribution
        education_level = None
        if age:
            if age < 25:
                # Younger people less likely to have completed higher education
                education_weights = {
                    EducationLevel.NO_FORMAL_EDUCATION: 2,
                    EducationLevel.PRIMARY_EDUCATION: 3,
                    EducationLevel.SECONDARY_EDUCATION: 45,
                    EducationLevel.VOCATIONAL_TRAINING: 15,
                    EducationLevel.ASSOCIATE_DEGREE: 15,
                    EducationLevel.BACHELORS_DEGREE: 15,
                    EducationLevel.MASTERS_DEGREE: 3,
                    EducationLevel.DOCTORATE: 1,
                    EducationLevel.PROFESSIONAL_DEGREE: 1,
                    EducationLevel.OTHER: 1,
                    EducationLevel.UNKNOWN: 0
                }
            elif 25 <= age < 40:
                # Mid-age range more likely to have completed higher education
                education_weights = {
                    EducationLevel.NO_FORMAL_EDUCATION: 1,
                    EducationLevel.PRIMARY_EDUCATION: 2,
                    EducationLevel.SECONDARY_EDUCATION: 25,
                    EducationLevel.VOCATIONAL_TRAINING: 15,
                    EducationLevel.ASSOCIATE_DEGREE: 15,
                    EducationLevel.BACHELORS_DEGREE: 30,
                    EducationLevel.MASTERS_DEGREE: 8,
                    EducationLevel.DOCTORATE: 2,
                    EducationLevel.PROFESSIONAL_DEGREE: 2,
                    EducationLevel.OTHER: 1,
                    EducationLevel.UNKNOWN: 0
                }
            elif 40 <= age < 65:
                # Middle-aged population with varied education levels
                education_weights = {
                    EducationLevel.NO_FORMAL_EDUCATION: 2,
                    EducationLevel.PRIMARY_EDUCATION: 3,
                    EducationLevel.SECONDARY_EDUCATION: 35,
                    EducationLevel.VOCATIONAL_TRAINING: 12,
                    EducationLevel.ASSOCIATE_DEGREE: 12,
                    EducationLevel.BACHELORS_DEGREE: 25,
                    EducationLevel.MASTERS_DEGREE: 7,
                    EducationLevel.DOCTORATE: 2,
                    EducationLevel.PROFESSIONAL_DEGREE: 2,
                    EducationLevel.OTHER: 1,
                    EducationLevel.UNKNOWN: 0
                }
            else:
                # Older population generally has lower higher education rates
                education_weights = {
                    EducationLevel.NO_FORMAL_EDUCATION: 4,
                    EducationLevel.PRIMARY_EDUCATION: 8,
                    EducationLevel.SECONDARY_EDUCATION: 45,
                    EducationLevel.VOCATIONAL_TRAINING: 10,
                    EducationLevel.ASSOCIATE_DEGREE: 8,
                    EducationLevel.BACHELORS_DEGREE: 15,
                    EducationLevel.MASTERS_DEGREE: 5,
                    EducationLevel.DOCTORATE: 2,
                    EducationLevel.PROFESSIONAL_DEGREE: 2,
                    EducationLevel.OTHER: 1,
                    EducationLevel.UNKNOWN: 0
                }
        else:
            # If age is unknown, use default distribution
            education_level = EducationLevel.get_random()

        # If we have age and weights, select education level
        if age and 'education_weights' in locals():
            education_level_values = list(education_weights.keys())
            education_weights_values = list(education_weights.values())
            education_level = random.choices(education_level_values, weights=education_weights_values, k=1)[0]

        # INCOME BRACKET GENERATION
        # Check accounts and loans to estimate income
        # Correlate with education level
        income_bracket = None

        # Get balances data from accounts to correlate with income
        cursor.execute("""
            SELECT SUM(a.current_balance) as total_balance, 
                   COUNT(a.consumer_banking_account_id) as account_count
            FROM enterprise.account_ownership ao
            JOIN consumer_banking.accounts a ON ao.enterprise_account_id = a.enterprise_account_id
            WHERE ao.enterprise_party_id = %s
        """, (id_fields['enterprise_party_id'],))

        account_data = cursor.fetchone()
        total_balance = account_data.get('total_balance') if account_data else 0
        account_count = account_data.get('account_count') if account_data else 0

        # Get loan data
        cursor.execute("""
            SELECT SUM(l.loan_amount) as total_loans
            FROM mortgage_services.loans l
            JOIN mortgage_services.application_borrowers ab ON l.mortgage_services_application_id = ab.mortgage_services_application_id
            JOIN mortgage_services.borrowers b ON ab.mortgage_services_borrower_id = b.mortgage_services_borrower_id
            WHERE b.enterprise_party_id = %s
        """, (id_fields['enterprise_party_id'],))

        loan_data = cursor.fetchone()
        total_loans = loan_data.get('total_loans') if loan_data else 0

        # Determine income potential based on account balances, loans and education
        income_potential = 0

        # Balance factor
        if total_balance:
            if total_balance < 5000:
                income_potential += 1
            elif total_balance < 20000:
                income_potential += 2
            elif total_balance < 50000:
                income_potential += 3
            elif total_balance < 100000:
                income_potential += 4
            else:
                income_potential += 5

        # Loan factor
        if total_loans:
            if total_loans < 100000:
                income_potential += 1
            elif total_loans < 250000:
                income_potential += 2
            elif total_loans < 500000:
                income_potential += 3
            elif total_loans < 1000000:
                income_potential += 4
            else:
                income_potential += 5

        # Education factor
        if education_level == EducationLevel.NO_FORMAL_EDUCATION:
            income_potential += 1
        elif education_level in [EducationLevel.PRIMARY_EDUCATION, EducationLevel.SECONDARY_EDUCATION]:
            income_potential += 2
        elif education_level in [EducationLevel.VOCATIONAL_TRAINING, EducationLevel.ASSOCIATE_DEGREE]:
            income_potential += 3
        elif education_level == EducationLevel.BACHELORS_DEGREE:
            income_potential += 4
        elif education_level in [EducationLevel.MASTERS_DEGREE,
                                 EducationLevel.DOCTORATE,
                                 EducationLevel.PROFESSIONAL_DEGREE]:
            income_potential += 5

        # Map income potential score to income bracket
        if income_potential <= 3:
            income_bracket_weights = {
                IncomeBracket.UNDER_15K: 40,
                IncomeBracket.INCOME_15K_25K: 30,
                IncomeBracket.INCOME_25K_35K: 20,
                IncomeBracket.INCOME_35K_50K: 10,
                IncomeBracket.INCOME_50K_75K: 0,
                IncomeBracket.INCOME_75K_100K: 0,
                IncomeBracket.INCOME_100K_150K: 0,
                IncomeBracket.INCOME_150K_200K: 0,
                IncomeBracket.INCOME_200K_250K: 0,
                IncomeBracket.INCOME_250K_PLUS: 0
            }
        elif income_potential <= 6:
            income_bracket_weights = {
                IncomeBracket.UNDER_15K: 10,
                IncomeBracket.INCOME_15K_25K: 25,
                IncomeBracket.INCOME_25K_35K: 30,
                IncomeBracket.INCOME_35K_50K: 25,
                IncomeBracket.INCOME_50K_75K: 10,
                IncomeBracket.INCOME_75K_100K: 0,
                IncomeBracket.INCOME_100K_150K: 0,
                IncomeBracket.INCOME_150K_200K: 0,
                IncomeBracket.INCOME_200K_250K: 0,
                IncomeBracket.INCOME_250K_PLUS: 0
            }
        elif income_potential <= 9:
            income_bracket_weights = {
                IncomeBracket.UNDER_15K: 5,
                IncomeBracket.INCOME_15K_25K: 5,
                IncomeBracket.INCOME_25K_35K: 10,
                IncomeBracket.INCOME_35K_50K: 25,
                IncomeBracket.INCOME_50K_75K: 30,
                IncomeBracket.INCOME_75K_100K: 15,
                IncomeBracket.INCOME_100K_150K: 10,
                IncomeBracket.INCOME_150K_200K: 0,
                IncomeBracket.INCOME_200K_250K: 0,
                IncomeBracket.INCOME_250K_PLUS: 0
            }
        elif income_potential <= 12:
            income_bracket_weights = {
                IncomeBracket.UNDER_15K: 0,
                IncomeBracket.INCOME_15K_25K: 0,
                IncomeBracket.INCOME_25K_35K: 5,
                IncomeBracket.INCOME_35K_50K: 10,
                IncomeBracket.INCOME_50K_75K: 20,
                IncomeBracket.INCOME_75K_100K: 30,
                IncomeBracket.INCOME_100K_150K: 25,
                IncomeBracket.INCOME_150K_200K: 10,
                IncomeBracket.INCOME_200K_250K: 0,
                IncomeBracket.INCOME_250K_PLUS: 0
            }
        else:
            income_bracket_weights = {
                IncomeBracket.UNDER_15K: 0,
                IncomeBracket.INCOME_15K_25K: 0,
                IncomeBracket.INCOME_25K_35K: 0,
                IncomeBracket.INCOME_35K_50K: 0,
                IncomeBracket.INCOME_50K_75K: 5,
                IncomeBracket.INCOME_75K_100K: 10,
                IncomeBracket.INCOME_100K_150K: 30,
                IncomeBracket.INCOME_150K_200K: 25,
                IncomeBracket.INCOME_200K_250K: 20,
                IncomeBracket.INCOME_250K_PLUS: 10
            }

        # Select income bracket based on weights
        income_bracket_values = list(income_bracket_weights.keys())
        income_weights_values = list(income_bracket_weights.values())
        income_bracket = random.choices(income_bracket_values, weights=income_weights_values, k=1)[0]

        # OCCUPATION CATEGORY GENERATION
        # Correlate with education and income
        occupation_category = None

        # Higher education typically leads to professional occupations
        if education_level in [EducationLevel.DOCTORATE,
                               EducationLevel.PROFESSIONAL_DEGREE,
                               EducationLevel.MASTERS_DEGREE]:
            occupation_weights = {
                OccupationCategory.MANAGEMENT: 20,
                OccupationCategory.BUSINESS_FINANCIAL: 15,
                OccupationCategory.COMPUTER_MATHEMATICAL: 15,
                OccupationCategory.ARCHITECTURE_ENGINEERING: 10,
                OccupationCategory.SCIENCE: 15,
                OccupationCategory.LEGAL: 15,
                OccupationCategory.EDUCATION: 15,
                OccupationCategory.HEALTHCARE_PRACTITIONERS: 15,
                OccupationCategory.RETIRED: 5,
                OccupationCategory.OTHER: 5,
                OccupationCategory.UNKNOWN: 0
            }
        elif education_level == EducationLevel.BACHELORS_DEGREE:
            occupation_weights = {
                OccupationCategory.MANAGEMENT: 15,
                OccupationCategory.BUSINESS_FINANCIAL: 15,
                OccupationCategory.COMPUTER_MATHEMATICAL: 12,
                OccupationCategory.ARCHITECTURE_ENGINEERING: 8,
                OccupationCategory.EDUCATION: 10,
                OccupationCategory.HEALTHCARE_PRACTITIONERS: 10,
                OccupationCategory.SALES: 10,
                OccupationCategory.OFFICE_ADMIN: 10,
                OccupationCategory.COMMUNITY_SOCIAL_SERVICE: 5,
                OccupationCategory.LEGAL: 5,
                OccupationCategory.RETIRED: 5,
                OccupationCategory.OTHER: 5,
                OccupationCategory.UNKNOWN: 0
            }
        elif education_level in [EducationLevel.ASSOCIATE_DEGREE,
                                 EducationLevel.VOCATIONAL_TRAINING]:
            occupation_weights = {
                OccupationCategory.HEALTHCARE_SUPPORT: 15,
                OccupationCategory.INSTALLATION_MAINTENANCE_REPAIR: 15,
                OccupationCategory.PRODUCTION: 10,
                OccupationCategory.CONSTRUCTION: 10,
                OccupationCategory.OFFICE_ADMIN: 15,
                OccupationCategory.SALES: 10,
                OccupationCategory.PROTECTIVE_SERVICE: 5,
                OccupationCategory.TRANSPORTATION: 10,
                OccupationCategory.RETIRED: 5,
                OccupationCategory.OTHER: 5,
                OccupationCategory.UNKNOWN: 0
            }
        elif education_level == EducationLevel.SECONDARY_EDUCATION:
            occupation_weights = {
                OccupationCategory.OFFICE_ADMIN: 10,
                OccupationCategory.SALES: 15,
                OccupationCategory.FOOD_SERVICE: 15,
                OccupationCategory.CONSTRUCTION: 10,
                OccupationCategory.TRANSPORTATION: 10,
                OccupationCategory.PRODUCTION: 10,
                OccupationCategory.BUILDING_MAINTENANCE: 5,
                OccupationCategory.PERSONAL_CARE: 5,
                OccupationCategory.STUDENT: 5,
                OccupationCategory.RETIRED: 5,
                OccupationCategory.HOMEMAKER: 5,
                OccupationCategory.UNEMPLOYED: 5,
                OccupationCategory.OTHER: 5,
                OccupationCategory.UNKNOWN: 0
            }
        else:
            occupation_weights = {
                OccupationCategory.FOOD_SERVICE: 20,
                OccupationCategory.BUILDING_MAINTENANCE: 15,
                OccupationCategory.PERSONAL_CARE: 10,
                OccupationCategory.CONSTRUCTION: 10,
                OccupationCategory.FARMING_FISHING_FORESTRY: 5,
                OccupationCategory.TRANSPORTATION: 10,
                OccupationCategory.PRODUCTION: 10,
                OccupationCategory.HOMEMAKER: 5,
                OccupationCategory.UNEMPLOYED: 10,
                OccupationCategory.OTHER: 5,
                OccupationCategory.UNKNOWN: 0
            }

        # Adjust for age - retirement more likely for older individuals
        if age and age >= 65:
            # Increase likelihood of retirement and reduce others proportionally
            for key in occupation_weights:
                if key == OccupationCategory.RETIRED:
                    occupation_weights[key] = 60  # High weight for retirement
                else:
                    occupation_weights[key] = max(0, occupation_weights.get(key, 0) * 0.5)  # Reduce others

        # Select occupation based on weights
        occupation_values = list(occupation_weights.keys())
        occupation_weights_values = list(occupation_weights.values())
        occupation_category = random.choices(occupation_values, weights=occupation_weights_values, k=1)[0]

        # Generate employer if appropriate
        employer = None
        if occupation_category not in [OccupationCategory.RETIRED, OccupationCategory.STUDENT,
                                       OccupationCategory.HOMEMAKER, OccupationCategory.UNEMPLOYED]:
            # List of plausible employers by category
            employers = {
                OccupationCategory.MANAGEMENT: ["Acme Corp", "Global Industries", "TechVision Inc",
                                                "Summit Group", "Horizon Enterprises", "Pinnacle Management",
                                                "Strategic Solutions Inc", "Executive Partners LLC"],

                OccupationCategory.BUSINESS_FINANCIAL: ["First National Bank", "Capital Financial",
                                                        "Prosperity Advisors", "Baker Tilly", "Grant Thornton",
                                                        "Deloitte", "PwC", "KPMG", "EY", "Morgan Stanley"],

                OccupationCategory.COMPUTER_MATHEMATICAL: ["TechCorp", "Innovations Inc", "DataWorks",
                                                           "Quantum Computing", "Silicon Systems",
                                                           "Google", "Microsoft", "Amazon", "Meta", "Apple"],

                OccupationCategory.ARCHITECTURE_ENGINEERING: ["BuildRight Architects", "Engineering Solutions",
                                                              "Design Group", "Structural Innovations",
                                                              "AECOM", "Jacobs", "Fluor", "Bechtel"],

                OccupationCategory.SCIENCE: ["Research Laboratories", "BioTech Innovations",
                                             "Scientific Discovery Inc", "Environmental Solutions",
                                             "Merck", "Pfizer", "Johnson & Johnson"],

                OccupationCategory.COMMUNITY_SOCIAL_SERVICE: ["Community Action", "Social Services Agency",
                                                              "Family Services", "Youth Outreach Center",
                                                              "Red Cross", "Salvation Army"],

                OccupationCategory.LEGAL: ["Smith & Associates", "Legal Partners LLC",
                                           "Justice Law Firm", "Legal Aid Society",
                                           "Baker McKenzie", "DLA Piper", "Skadden"],

                OccupationCategory.EDUCATION: ["Springfield School District", "Central University",
                                               "Academy of Learning", "Educational Services Inc",
                                               "State University", "Community College"],

                OccupationCategory.ARTS_ENTERTAINMENT: ["Creative Productions", "Media Group",
                                                        "Entertainment Network", "Artistic Designs",
                                                        "Disney", "Netflix", "Warner Bros"],

                OccupationCategory.HEALTHCARE_PRACTITIONERS: ["Memorial Hospital", "Medical Center",
                                                              "Health Partners", "Wellness Clinic",
                                                              "Mayo Clinic", "Cleveland Clinic"],

                OccupationCategory.HEALTHCARE_SUPPORT: ["CaringHands Agency", "Medical Assistance Inc",
                                                        "Patient Support Services", "Healthcare Staffing"],

                OccupationCategory.PROTECTIVE_SERVICE: ["Security Solutions", "Protection Services",
                                                        "Safety First", "Guardian Security",
                                                        "Local Police Department", "Sheriff's Office"],

                OccupationCategory.FOOD_SERVICE: ["Good Eats Restaurant", "Culinary Delights",
                                                  "Tasty Treats Café", "Food Services Inc",
                                                  "McDonald's", "Starbucks", "Chipotle"],

                OccupationCategory.BUILDING_MAINTENANCE: ["Maintenance Masters", "Facility Services",
                                                          "CleanRight", "Building Care Inc",
                                                          "ServiceMaster", "ABM Industries"],

                OccupationCategory.PERSONAL_CARE: ["Beauty Salon", "Personal Care Services",
                                                   "Wellness Spa", "Care Providers Inc"],

                OccupationCategory.SALES: ["Retail Solutions", "Sales Associates",
                                           "Marketing Group", "Consumer Products Inc",
                                           "Walmart", "Target", "Amazon", "Best Buy"],

                OccupationCategory.OFFICE_ADMIN: ["Business Services Inc", "Office Solutions",
                                                  "Administrative Partners", "Corporate Services LLC"],

                OccupationCategory.FARMING_FISHING_FORESTRY: ["Green Acres Farms", "Harvest Time",
                                                              "Woodland Enterprises", "Ocean Catch Fisheries"],

                OccupationCategory.CONSTRUCTION: ["BuildRight Construction", "Development Co",
                                                  "Structural Solutions", "Homes & More Builders"],

                OccupationCategory.INSTALLATION_MAINTENANCE_REPAIR: ["Fix-It Services", "Maintenance Pros",
                                                                     "Repair Solutions", "Technical Services Inc"],

                OccupationCategory.PRODUCTION: ["Manufacturing Inc", "Production Systems",
                                                "Assembly Solutions", "Industrial Products Co"],

                OccupationCategory.TRANSPORTATION: ["Transport Solutions", "Delivery Services",
                                                    "Logistics Inc", "Moving Experts",
                                                    "UPS", "FedEx", "DHL", "USPS"],

                OccupationCategory.MILITARY: ["U.S. Army", "U.S. Navy", "U.S. Air Force",
                                              "U.S. Marine Corps", "U.S. Coast Guard",
                                              "Department of Defense"]
            }

            if occupation_category in employers:
                employer = random.choice(employers[occupation_category])

        # Generate employment length (correlated with age)
        employment_length_years = None
        if occupation_category not in [OccupationCategory.RETIRED, OccupationCategory.STUDENT,
                                       OccupationCategory.HOMEMAKER, OccupationCategory.UNEMPLOYED]:
            if age:
                # Maximum employment length based on age
                working_years = max(0, age - 18)  # Assume working age starts at 18
                max_length = min(working_years, 40)  # Cap at 40 years

                # More likely to have shorter employment at current employer
                if max_length > 0:
                    # Skew toward shorter tenures
                    employment_length_years = min(max_length, int(random.betavariate(1.5, 4) * max_length) + 1)
            else:
                # If age unknown, generate reasonable employment length
                employment_length_years = random.randint(1, 20)

        # HOUSEHOLD AND FAMILY DATA GENERATION
        # Correlate with marital status and age

        # Determine household size
        household_size = None
        number_of_children = None

        if marital_status == 'MARRIED' or marital_status == 'DOMESTIC_PARTNERSHIP':
            base_household_size = 2  # Partner + self
        else:
            base_household_size = 1  # Just self

        # Add children based on age and marital status
        if age:
            if 25 <= age <= 45 and (marital_status == 'MARRIED' or marital_status == 'DOMESTIC_PARTNERSHIP'):
                # Prime child-raising age for couples
                children_weights = [0.2, 0.2, 0.3, 0.2, 0.07, 0.02, 0.01]  # 0 to 6+ children
                number_of_children = random.choices(range(7), weights=children_weights, k=1)[0]
            elif 25 <= age <= 45:
                # Single parents have fewer children on average
                children_weights = [0.4, 0.4, 0.15, 0.04, 0.01, 0, 0]  # 0 to 6+ children
                number_of_children = random.choices(range(7), weights=children_weights, k=1)[0]
            elif 46 <= age <= 65:
                # Older parents, children may have moved out
                children_weights = [0.3, 0.3, 0.25, 0.1, 0.04, 0.01, 0]  # 0 to 6+ children
                number_of_children = random.choices(range(7), weights=children_weights, k=1)[0]
            else:
                # Very young or elderly less likely to have children at home
                children_weights = [0.8, 0.15, 0.04, 0.01, 0, 0, 0]  # 0 to 6+ children
                number_of_children = random.choices(range(7), weights=children_weights, k=1)[0]
        else:
            # If age unknown, use general distribution
            children_weights = [0.4, 0.3, 0.2, 0.07, 0.02, 0.01, 0]  # 0 to 6+ children
            number_of_children = random.choices(range(7), weights=children_weights, k=1)[0]

        # Children living at home depends on family life stage
        children_at_home = number_of_children
        if age and age > 50:
            # Older parents may have adult children who moved out
            children_at_home = int(number_of_children * random.uniform(0, 0.5))

        household_size = base_household_size + children_at_home

        # Add potential other family members (5% chance)
        if random.random() < 0.05:
            household_size += random.randint(1, 2)

        # FAMILY LIFE STAGE GENERATION
        # Determine based on age, marital status, and children
        family_life_stage = None

        if not age:
            family_life_stage = FamilyLifeStage.get_random()
        else:
            if age >= 65:
                if marital_status in ['MARRIED', 'DOMESTIC_PARTNERSHIP']:
                    family_life_stage = FamilyLifeStage.RETIRED
                else:
                    family_life_stage = FamilyLifeStage.RETIRED
            elif marital_status in ['MARRIED', 'DOMESTIC_PARTNERSHIP']:
                if number_of_children == 0:
                    if age < 35:
                        family_life_stage = FamilyLifeStage.COUPLE_NO_CHILDREN
                    else:
                        # 70% chance of empty nest, 30% never had children
                        if random.random() < 0.7:
                            family_life_stage = FamilyLifeStage.EMPTY_NEST
                        else:
                            family_life_stage = FamilyLifeStage.COUPLE_NO_CHILDREN
                elif children_at_home > 0:
                    if age <= 35:
                        family_life_stage = FamilyLifeStage.FAMILY_YOUNG_CHILDREN
                    elif age <= 55:
                        family_life_stage = FamilyLifeStage.FAMILY_SCHOOL_CHILDREN
                    else:
                        family_life_stage = FamilyLifeStage.FAMILY_ADULT_CHILDREN
                else:
                    family_life_stage = FamilyLifeStage.EMPTY_NEST
            else:  # Single
                if number_of_children == 0:
                    family_life_stage = FamilyLifeStage.SINGLE_NO_CHILDREN
                elif children_at_home > 0:
                    if age <= 35:
                        family_life_stage = FamilyLifeStage.FAMILY_YOUNG_CHILDREN
                    elif age <= 55:
                        family_life_stage = FamilyLifeStage.FAMILY_SCHOOL_CHILDREN
                    else:
                        family_life_stage = FamilyLifeStage.FAMILY_ADULT_CHILDREN
                else:
                    family_life_stage = FamilyLifeStage.SINGLE_NO_CHILDREN

        # HOMEOWNERSHIP STATUS GENERATION
        # Correlate with age, income, and family status
        homeownership_status = None

        if income_bracket in [IncomeBracket.INCOME_250K_PLUS, IncomeBracket.INCOME_200K_250K,
                              IncomeBracket.INCOME_150K_200K, IncomeBracket.INCOME_100K_150K]:
            # Higher income more likely to own home
            homeownership_weights = {
                HomeownershipStatus.OWNER: 40,
                HomeownershipStatus.MORTGAGED: 50,
                HomeownershipStatus.RENTER: 7,
                HomeownershipStatus.LIVING_WITH_FAMILY: 2,
                HomeownershipStatus.OTHER: 1,
                HomeownershipStatus.UNKNOWN: 0
            }
        elif income_bracket in [IncomeBracket.INCOME_75K_100K, IncomeBracket.INCOME_50K_75K]:
            # Middle income more likely to have mortgage
            homeownership_weights = {
                HomeownershipStatus.OWNER: 20,
                HomeownershipStatus.MORTGAGED: 55,
                HomeownershipStatus.RENTER: 20,
                HomeownershipStatus.LIVING_WITH_FAMILY: 3,
                HomeownershipStatus.OTHER: 2,
                HomeownershipStatus.UNKNOWN: 0
            }
        elif income_bracket in [IncomeBracket.INCOME_35K_50K, IncomeBracket.INCOME_25K_35K]:
            # Lower middle income mix of renting and owning
            homeownership_weights = {
                HomeownershipStatus.OWNER: 10,
                HomeownershipStatus.MORTGAGED: 40,
                HomeownershipStatus.RENTER: 40,
                HomeownershipStatus.LIVING_WITH_FAMILY: 7,
                HomeownershipStatus.OTHER: 3,
                HomeownershipStatus.UNKNOWN: 0
            }
        else:
            # Lower income more likely to rent
            homeownership_weights = {
                HomeownershipStatus.OWNER: 5,
                HomeownershipStatus.MORTGAGED: 15,
                HomeownershipStatus.RENTER: 60,
                HomeownershipStatus.LIVING_WITH_FAMILY: 15,
                HomeownershipStatus.OTHER: 5,
                HomeownershipStatus.UNKNOWN: 0
            }

        # Age adjustments
        if age:
            if age < 25:
                # Young adults more likely to rent or live with family
                homeownership_weights[HomeownershipStatus.OWNER] = max(0, homeownership_weights[
                    HomeownershipStatus.OWNER] - 10)
                homeownership_weights[HomeownershipStatus.MORTGAGED] = max(0, homeownership_weights[
                    HomeownershipStatus.MORTGAGED] - 15)
                homeownership_weights[HomeownershipStatus.RENTER] = min(100, homeownership_weights[
                    HomeownershipStatus.RENTER] + 15)
                homeownership_weights[HomeownershipStatus.LIVING_WITH_FAMILY] = min(100, homeownership_weights[
                    HomeownershipStatus.LIVING_WITH_FAMILY] + 10)
            elif age >= 65:
                # Older adults more likely to own outright
                homeownership_weights[HomeownershipStatus.OWNER] = min(100, homeownership_weights[
                    HomeownershipStatus.OWNER] + 20)
                homeownership_weights[HomeownershipStatus.MORTGAGED] = max(0, homeownership_weights[
                    HomeownershipStatus.MORTGAGED] - 20)

        # Family stage adjustments
        if family_life_stage in [FamilyLifeStage.FAMILY_SCHOOL_CHILDREN, FamilyLifeStage.FAMILY_YOUNG_CHILDREN]:
            # Families with children more likely to have stable housing
            homeownership_weights[HomeownershipStatus.RENTER] = max(0, homeownership_weights[
                HomeownershipStatus.RENTER] - 10)
            homeownership_weights[HomeownershipStatus.MORTGAGED] = min(100, homeownership_weights[
                HomeownershipStatus.MORTGAGED] + 10)

        homeownership_values = list(homeownership_weights.keys())
        homeownership_weights_values = list(homeownership_weights.values())
        homeownership_status = random.choices(homeownership_values, weights=homeownership_weights_values, k=1)[0]

        # Generate years at residence (correlated with age and homeownership)
        years_at_residence = None
        if age:
            # Maximum years at residence based on age
            adult_years = max(0, age - 18)  # Count years since adulthood
            max_years = min(adult_years, 30)  # Cap at 30 years for realism

            # Homeowners tend to stay longer
            if homeownership_status in [HomeownershipStatus.OWNER, HomeownershipStatus.MORTGAGED]:
                years_at_residence = min(max_years, max(1, int(random.betavariate(2, 3) * max_years)))
            else:
                # Renters tend to move more frequently
                years_at_residence = min(max_years, max(1, int(random.betavariate(1, 4) * max_years)))
        else:
            # If age unknown, generate reasonable residence length
            if homeownership_status in [HomeownershipStatus.OWNER, HomeownershipStatus.MORTGAGED]:
                years_at_residence = random.randint(2, 15)
            else:
                years_at_residence = random.randint(1, 7)

        # Estimated home value (for owners and mortgaged)
        estimated_home_value = None
        if homeownership_status in [HomeownershipStatus.OWNER, HomeownershipStatus.MORTGAGED]:
                # Base value on income
                if income_bracket == IncomeBracket.INCOME_250K_PLUS:
                    base_value = random.randint(750000, 2000000)
                elif income_bracket == IncomeBracket.INCOME_200K_250K:
                    base_value = random.randint(600000, 1000000)
                elif income_bracket == IncomeBracket.INCOME_150K_200K:
                    base_value = random.randint(450000, 750000)
                elif income_bracket == IncomeBracket.INCOME_100K_150K:
                    base_value = random.randint(350000, 600000)
                elif income_bracket == IncomeBracket.INCOME_75K_100K:
                    base_value = random.randint(250000, 450000)
                elif income_bracket == IncomeBracket.INCOME_50K_75K:
                    base_value = random.randint(180000, 350000)
                elif income_bracket == IncomeBracket.INCOME_35K_50K:
                    base_value = random.randint(120000, 250000)
                else:
                    base_value = random.randint(80000, 180000)

                # Add some randomness
                variation = random.uniform(0.85, 1.15)
                estimated_home_value = int(base_value * variation)
                # Round to nearest $1000
                estimated_home_value = round(estimated_home_value / 1000) * 1000

        # TOTAL HOUSEHOLD INCOME GENERATION
        # Based on income bracket and household size
        total_household_income = None

        # Map income bracket to average individual income
        income_means = {
            IncomeBracket.UNDER_15K: 10000,
            IncomeBracket.INCOME_15K_25K: 20000,
            IncomeBracket.INCOME_25K_35K: 30000,
            IncomeBracket.INCOME_35K_50K: 42500,
            IncomeBracket.INCOME_50K_75K: 62500,
            IncomeBracket.INCOME_50K_75K: 62500,
            IncomeBracket.INCOME_75K_100K: 87500,
            IncomeBracket.INCOME_100K_150K: 125000,
            IncomeBracket.INCOME_150K_200K: 175000,
            IncomeBracket.INCOME_200K_250K: 225000,
            IncomeBracket.INCOME_250K_PLUS: 350000
        }

        # Get mean income for bracket
        if income_bracket in income_means:
            mean_income = income_means[income_bracket]

            # Add income for other household members if applicable
            if household_size > 1:
                # Spouse or partner contributes significantly
                if marital_status in ['MARRIED', 'DOMESTIC_PARTNERSHIP']:
                    # Partner contribution varies based on primary income
                    if mean_income > 100000:
                        partner_factor = random.uniform(0.5, 1.2)  # Higher earners often have high-earning partners
                    else:
                        partner_factor = random.uniform(0.3, 0.9)

                    household_income = mean_income + (mean_income * partner_factor)

                    # Add small amounts for working-age children if present
                    children_contribution = 0
                    if children_at_home > 0 and age and age > 40:
                        working_children = min(children_at_home, random.randint(0, 2))
                        children_contribution = working_children * random.randint(5000, 15000)

                    total_household_income = household_income + children_contribution
                else:
                    # Single parent or other arrangement
                    total_household_income = mean_income

                    # Add contributions from other adults
                    if household_size > 1 + children_at_home:  # Other adults besides children
                        other_adults = household_size - 1 - children_at_home
                        other_contribution = other_adults * random.randint(10000, 30000)
                        total_household_income += other_contribution
            else:
                # Single person household
                total_household_income = mean_income

            # Add some randomness
            variation = random.uniform(0.9, 1.1)
            total_household_income = total_household_income * variation
            # Round to nearest $100
            total_household_income = round(total_household_income / 100) * 100

            # NET WORTH ESTIMATE GENERATION
            # Based on income, age, and homeownership
            net_worth_estimate = None

            # Base net worth on income and age
            if income_bracket in income_means and age:
                base_income = income_means[income_bracket]

                # Net worth to income multiplier increases with age
                if age < 30:
                    multiplier = random.uniform(0.5, 2)
                elif age < 40:
                    multiplier = random.uniform(1, 4)
                elif age < 50:
                    multiplier = random.uniform(2, 6)
                elif age < 60:
                    multiplier = random.uniform(3, 8)
                else:
                    multiplier = random.uniform(4, 12)

                # Calculate base net worth
                base_net_worth = base_income * multiplier

                # Add home equity if applicable
                if homeownership_status == HomeownershipStatus.OWNER and estimated_home_value:
                    base_net_worth += estimated_home_value
                elif homeownership_status == HomeownershipStatus.MORTGAGED and estimated_home_value:
                    # Add partial home value (assuming some mortgage paid off)
                    mortgage_progress = min(1.0, years_at_residence / 30)  # Assume 30-year mortgage
                    equity_percentage = 0.1 + (mortgage_progress * 0.9)  # 10% down payment + progress
                    base_net_worth += estimated_home_value * equity_percentage

                # Add randomness
                variation = random.uniform(0.8, 1.2)
                net_worth_estimate = base_net_worth * variation
                # Round to nearest $1000
                net_worth_estimate = round(net_worth_estimate / 1000) * 1000

            # POLITICAL AFFILIATION GENERATION
            # Varies by region, income, education, age
            political_affiliation = None

            # Without having clear region data, use a combination of other factors
            # Education correlation
            if education_level in [EducationLevel.BACHELORS_DEGREE,
                                   EducationLevel.MASTERS_DEGREE,
                                   EducationLevel.DOCTORATE,
                                   EducationLevel.PROFESSIONAL_DEGREE]:
                political_weights = {
                    PoliticalAffiliation.DEMOCRAT: 35,
                    PoliticalAffiliation.REPUBLICAN: 25,
                    PoliticalAffiliation.INDEPENDENT: 25,
                    PoliticalAffiliation.LIBERTARIAN: 5,
                    PoliticalAffiliation.GREEN: 5,
                    PoliticalAffiliation.OTHER: 2,
                    PoliticalAffiliation.NONE: 3,
                    PoliticalAffiliation.UNKNOWN: 0
                }
            elif education_level in [EducationLevel.ASSOCIATE_DEGREE,
                                     EducationLevel.VOCATIONAL_TRAINING,
                                     EducationLevel.SECONDARY_EDUCATION]:
                political_weights = {
                    PoliticalAffiliation.DEMOCRAT: 30,
                    PoliticalAffiliation.REPUBLICAN: 35,
                    PoliticalAffiliation.INDEPENDENT: 25,
                    PoliticalAffiliation.LIBERTARIAN: 4,
                    PoliticalAffiliation.GREEN: 2,
                    PoliticalAffiliation.OTHER: 1,
                    PoliticalAffiliation.NONE: 3,
                    PoliticalAffiliation.UNKNOWN: 0
                }
            else:
                political_weights = {
                    PoliticalAffiliation.DEMOCRAT: 30,
                    PoliticalAffiliation.REPUBLICAN: 30,
                    PoliticalAffiliation.INDEPENDENT: 20,
                    PoliticalAffiliation.LIBERTARIAN: 2,
                    PoliticalAffiliation.GREEN: 1,
                    PoliticalAffiliation.OTHER: 2,
                    PoliticalAffiliation.NONE: 15,
                    PoliticalAffiliation.UNKNOWN: 0
                }

            # Income-based adjustments
            if income_bracket in [IncomeBracket.INCOME_150K_200K,
                                  IncomeBracket.INCOME_200K_250K,
                                  IncomeBracket.INCOME_250K_PLUS]:
                # Higher income slightly more Republican
                political_weights[PoliticalAffiliation.REPUBLICAN] = min(100, political_weights[
                    PoliticalAffiliation.REPUBLICAN] + 10)
                political_weights[PoliticalAffiliation.DEMOCRAT] = max(0, political_weights[
                    PoliticalAffiliation.DEMOCRAT] - 5)
            elif income_bracket in [IncomeBracket.UNDER_15K,
                                    IncomeBracket.INCOME_15K_25K,
                                    IncomeBracket.INCOME_25K_35K]:
                # Lower income slightly more Democratic
                political_weights[PoliticalAffiliation.DEMOCRAT] = min(100, political_weights[
                    PoliticalAffiliation.DEMOCRAT] + 10)
                political_weights[PoliticalAffiliation.REPUBLICAN] = max(0, political_weights[
                    PoliticalAffiliation.REPUBLICAN] - 5)

            # Age-based adjustments
            if age:
                if age >= 65:
                    # Older voters slightly more Republican
                    political_weights[PoliticalAffiliation.REPUBLICAN] = min(100, political_weights[
                        PoliticalAffiliation.REPUBLICAN] + 5)
                    political_weights[PoliticalAffiliation.DEMOCRAT] = max(0, political_weights[
                        PoliticalAffiliation.DEMOCRAT] - 2)
                elif age <= 30:
                    # Younger voters slightly more Democratic or Independent
                    political_weights[PoliticalAffiliation.DEMOCRAT] = min(100, political_weights[
                        PoliticalAffiliation.DEMOCRAT] + 5)
                    political_weights[PoliticalAffiliation.INDEPENDENT] = min(100, political_weights[
                        PoliticalAffiliation.INDEPENDENT] + 5)
                    political_weights[PoliticalAffiliation.REPUBLICAN] = max(0, political_weights[
                        PoliticalAffiliation.REPUBLICAN] - 5)

            # Select political affiliation based on weights
            political_values = list(political_weights.keys())
            political_weights_values = list(political_weights.values())
            political_affiliation = random.choices(political_values, weights=political_weights_values, k=1)[0]

            # LIFESTYLE SEGMENT GENERATION
            # Based on income, occupation, education, family stage
            lifestyle_segment = None

            # Start with base weights for all segments
            lifestyle_weights = {
                LifestyleSegment.URBAN_PROFESSIONAL: 5,
                LifestyleSegment.SUBURBAN_FAMILY: 10,
                LifestyleSegment.RURAL_TRADITIONAL: 5,
                LifestyleSegment.BUDGET_CONSCIOUS: 10,
                LifestyleSegment.LUXURY_SEEKER: 2,
                LifestyleSegment.ECO_CONSCIOUS: 5,
                LifestyleSegment.TECH_SAVVY: 10,
                LifestyleSegment.EXPERIENTIAL: 5,
                LifestyleSegment.HEALTH_FOCUSED: 5,
                LifestyleSegment.CONVENIENCE_SEEKER: 10,
                LifestyleSegment.TRADITIONAL_BANKING: 10,
                LifestyleSegment.DIGITAL_FIRST: 10,
                LifestyleSegment.COMMUNITY_ORIENTED: 5,
                LifestyleSegment.CREDIT_REBUILDER: 5,
                LifestyleSegment.WEALTH_BUILDER: 5,
                LifestyleSegment.RETIREMENT_FOCUSED: 5,
                LifestyleSegment.OTHER: 3,
                LifestyleSegment.UNKNOWN: 0
            }

            # Income-based adjustments
            if income_bracket in [IncomeBracket.INCOME_150K_200K,
                                  IncomeBracket.INCOME_200K_250K,
                                  IncomeBracket.INCOME_250K_PLUS]:
                # High income more likely to be luxury seekers, wealth builders
                lifestyle_weights[LifestyleSegment.LUXURY_SEEKER] = 20
                lifestyle_weights[LifestyleSegment.WEALTH_BUILDER] = 20
                lifestyle_weights[LifestyleSegment.URBAN_PROFESSIONAL] = 15
                lifestyle_weights[LifestyleSegment.BUDGET_CONSCIOUS] = 2
            elif income_bracket in [IncomeBracket.INCOME_75K_100K,
                                    IncomeBracket.INCOME_100K_150K]:
                # Upper middle income focused on experiences, suburban lifestyle
                lifestyle_weights[LifestyleSegment.SUBURBAN_FAMILY] = 15
                lifestyle_weights[LifestyleSegment.EXPERIENTIAL] = 12
                lifestyle_weights[LifestyleSegment.WEALTH_BUILDER] = 15
                lifestyle_weights[LifestyleSegment.URBAN_PROFESSIONAL] = 10
            elif income_bracket in [IncomeBracket.UNDER_15K,
                                    IncomeBracket.INCOME_15K_25K,
                                    IncomeBracket.INCOME_25K_35K]:
                # Lower income more budget conscious
                lifestyle_weights[LifestyleSegment.BUDGET_CONSCIOUS] = 25
                lifestyle_weights[LifestyleSegment.CREDIT_REBUILDER] = 15
                lifestyle_weights[LifestyleSegment.TRADITIONAL_BANKING] = 15
                lifestyle_weights[LifestyleSegment.LUXURY_SEEKER] = 0

            # Occupation-based adjustments
            if occupation_category in [OccupationCategory.COMPUTER_MATHEMATICAL,
                                       OccupationCategory.ARCHITECTURE_ENGINEERING,
                                       OccupationCategory.SCIENCE]:
                # Technical fields more tech-savvy
                lifestyle_weights[LifestyleSegment.TECH_SAVVY] = 25
                lifestyle_weights[LifestyleSegment.DIGITAL_FIRST] = 20
            elif occupation_category in [OccupationCategory.HEALTHCARE_PRACTITIONERS,
                                         OccupationCategory.HEALTHCARE_SUPPORT]:
                # Healthcare workers more health-focused
                lifestyle_weights[LifestyleSegment.HEALTH_FOCUSED] = 20
            elif occupation_category == OccupationCategory.RETIRED:
                # Retirees focused on retirement planning
                lifestyle_weights[LifestyleSegment.RETIREMENT_FOCUSED] = 30
                lifestyle_weights[LifestyleSegment.TRADITIONAL_BANKING] = 20
                lifestyle_weights[LifestyleSegment.TECH_SAVVY] = 5

            # Family stage adjustments
            if family_life_stage in [FamilyLifeStage.FAMILY_YOUNG_CHILDREN,
                                     FamilyLifeStage.FAMILY_SCHOOL_CHILDREN]:
                # Families with children often suburban and convenience-seeking
                lifestyle_weights[LifestyleSegment.SUBURBAN_FAMILY] = 25
                lifestyle_weights[LifestyleSegment.CONVENIENCE_SEEKER] = 20
            elif family_life_stage == FamilyLifeStage.RETIRED:
                lifestyle_weights[LifestyleSegment.RETIREMENT_FOCUSED] = 30

            # Education-based adjustments
            if education_level in [EducationLevel.MASTERS_DEGREE,
                                   EducationLevel.DOCTORATE,
                                   EducationLevel.PROFESSIONAL_DEGREE]:
                # Higher education correlated with eco-conscious, urban professionals
                lifestyle_weights[LifestyleSegment.ECO_CONSCIOUS] = 15
                lifestyle_weights[LifestyleSegment.URBAN_PROFESSIONAL] = 20

            # Select lifestyle segment based on weights
            lifestyle_values = list(lifestyle_weights.keys())
            lifestyle_weights_values = list(lifestyle_weights.values())
            lifestyle_segment = random.choices(lifestyle_values, weights=lifestyle_weights_values, k=1)[0]

            # CREDIT RISK TIER GENERATION
            # Based on income, age, occupation stability
            credit_risk_tier = None

            cursor.execute("""
                SELECT COUNT(cc.credit_cards_card_account_id) AS credit_account_count,
                       AVG(cc.credit_limit) AS avg_credit_limit,
                       AVG(cc.current_balance / NULLIF(cc.credit_limit, 0)) AS avg_utilization,
                       COUNT(CASE WHEN cc.days_past_due > 30 THEN 1 END) AS past_due_accounts
                FROM enterprise.account_ownership ao
                JOIN credit_cards.card_accounts cc ON ao.enterprise_account_id = cc.enterprise_account_id
                WHERE ao.enterprise_party_id = %s
            """, (id_fields['enterprise_party_id'],))

            credit_data = cursor.fetchone()

            if credit_data and credit_data['credit_account_count'] > 0:
                # Use internal data as baseline
                internal_account_count = credit_data.get('credit_account_count', 0)
                internal_avg_credit_limit = credit_data.get('avg_credit_limit', 5000)
                internal_avg_utilization = credit_data.get('avg_utilization', 0.3)
                internal_past_due_accounts = credit_data.get('past_due_accounts', 0)

                # Assume external accounts exist—realistically adding additional behavior
                external_account_count = random.choices([0, 1, 2, 3], weights=[20, 40, 25, 15], k=1)[0]

                # Blended values
                credit_account_count = internal_account_count + external_account_count

                # Average external credit limits slightly higher or lower based on random variance
                external_credit_limit = internal_avg_credit_limit * random.uniform(0.8, 1.5)
                avg_credit_limit = round((internal_avg_credit_limit + external_credit_limit) / 2, 2)

                # Adjust utilization with a slight random variance
                external_avg_utilization = min(0.9, internal_avg_utilization + random.uniform(-0.1, 0.3))
                avg_utilization = round((internal_avg_utilization + external_avg_utilization) / 2, 2)

                # Add some external past-due accounts probabilistically
                external_past_due_accounts = random.choices([0, 1], weights=[90, 10], k=1)[0]
                past_due_accounts = internal_past_due_accounts + external_past_due_accounts

            else:
                # Completely mock data if no internal accounts
                credit_account_count = random.choices([0, 1, 2, 3], weights=[20, 40, 25, 15], k=1)[0]
                avg_credit_limit = random.choice([3000, 5000, 10000, 15000, 20000])
                avg_utilization = round(random.uniform(0.05, 0.8), 2)
                past_due_accounts = random.choices([0, 1, 2], weights=[85, 10, 5], k=1)[0]

            # Start with base credit scoring
            credit_score = 0

            # Income factor (0-25 points)
            if income_bracket == IncomeBracket.INCOME_250K_PLUS:
                credit_score += 25
            elif income_bracket == IncomeBracket.INCOME_200K_250K:
                credit_score += 23
            elif income_bracket == IncomeBracket.INCOME_150K_200K:
                credit_score += 21
            elif income_bracket == IncomeBracket.INCOME_100K_150K:
                credit_score += 19
            elif income_bracket == IncomeBracket.INCOME_75K_100K:
                credit_score += 17
            elif income_bracket == IncomeBracket.INCOME_50K_75K:
                credit_score += 15
            elif income_bracket == IncomeBracket.INCOME_35K_50K:
                credit_score += 12
            elif income_bracket == IncomeBracket.INCOME_25K_35K:
                credit_score += 8
            elif income_bracket == IncomeBracket.INCOME_15K_25K:
                credit_score += 5
            else:
                credit_score += 2

            # Credit history factors (0-35 points)
            if credit_account_count >= 5:
                credit_score += 15
            elif credit_account_count >= 3:
                credit_score += 10
            elif credit_account_count >= 1:
                credit_score += 5

            if avg_credit_limit > 20000:
                credit_score += 10
            elif avg_credit_limit > 10000:
                credit_score += 8
            elif avg_credit_limit > 5000:
                credit_score += 5
            elif avg_credit_limit > 0:
                credit_score += 2

            if past_due_accounts == 0:
                credit_score += 10
            elif past_due_accounts == 1:
                credit_score += 5

            # Utilization factor (0-15 points)
            if avg_utilization is not None:
                if avg_utilization < 0.1:
                    credit_score += 15
                elif avg_utilization < 0.3:
                    credit_score += 12
                elif avg_utilization < 0.5:
                    credit_score += 8
                elif avg_utilization < 0.7:
                    credit_score += 4
                elif avg_utilization < 0.9:
                    credit_score += 2

            # Age and employment stability factor (0-25 points)
            if age and employment_length_years:
                if age >= 35 and employment_length_years >= 5:
                    credit_score += 25
                elif age >= 30 and employment_length_years >= 3:
                    credit_score += 20
                elif age >= 25 and employment_length_years >= 2:
                    credit_score += 15
                elif age >= 21:
                    credit_score += 10
                else:
                    credit_score += 5
            elif age and age >= 21:
                credit_score += 10

            # Map score to credit risk tier
            if credit_score >= 85:
                credit_risk_tier = CreditRiskTier.SUPER_PRIME
            elif credit_score >= 70:
                credit_risk_tier = CreditRiskTier.PRIME
            elif credit_score >= 55:
                credit_risk_tier = CreditRiskTier.NEAR_PRIME
            elif credit_score >= 40:
                credit_risk_tier = CreditRiskTier.SUBPRIME
            elif credit_score >= 1:
                credit_risk_tier = CreditRiskTier.DEEP_SUBPRIME
            else:
                credit_risk_tier = CreditRiskTier.NO_SCORE

            # Add some randomness to avoid perfect correlation
            random_factor = random.random()
            if random_factor < 0.1:  # 10% chance to shift one tier
                if credit_risk_tier == CreditRiskTier.SUPER_PRIME:
                    credit_risk_tier = CreditRiskTier.PRIME
                elif credit_risk_tier == CreditRiskTier.PRIME:
                    if random.random() < 0.5:
                        credit_risk_tier = CreditRiskTier.SUPER_PRIME
                    else:
                        credit_risk_tier = CreditRiskTier.NEAR_PRIME
                elif credit_risk_tier == CreditRiskTier.NEAR_PRIME:
                    if random.random() < 0.5:
                        credit_risk_tier = CreditRiskTier.PRIME
                    else:
                        credit_risk_tier = CreditRiskTier.SUBPRIME
                elif credit_risk_tier == CreditRiskTier.SUBPRIME:
                    if random.random() < 0.5:
                        credit_risk_tier = CreditRiskTier.NEAR_PRIME
                    else:
                        credit_risk_tier = CreditRiskTier.DEEP_SUBPRIME
                elif credit_risk_tier == CreditRiskTier.DEEP_SUBPRIME:
                    credit_risk_tier = CreditRiskTier.SUBPRIME

            # DISCRETIONARY SPENDING GENERATION
            # Based on income and household size
            discretionary_spending_estimate = None

            if total_household_income:
                # Essential expenses typically account for 50-70% of income
                essential_percentage = random.uniform(0.5, 0.7)
                essential_expenses = total_household_income * essential_percentage

                # Remaining is discretionary
                discretionary_spending_estimate = (total_household_income - essential_expenses) / 12  # Monthly amount

                # Adjust based on household size
                if household_size > 2:
                    # Larger households have higher essential costs
                    adjustment_factor = 1 - (0.05 * (household_size - 2))
                    discretionary_spending_estimate *= max(0.5, adjustment_factor)

                # Round to nearest $10
                discretionary_spending_estimate = round(discretionary_spending_estimate / 10) * 10

            # INVESTMENT PROFILE GENERATION
            # Goals and risk tolerance based on age, income, credit
            primary_investment_goals = None
            risk_tolerance = None

            # Investment goals candidates
            investment_goals_options = [
                "Retirement", "Wealth Accumulation", "Income Generation",
                "Education Funding", "Major Purchase", "Legacy Planning",
                "Business Development", "Tax Optimization", "Financial Security"
            ]

            # Age-based investment goals
            if age:
                if age < 30:
                    goal_weights = {
                        "Retirement": 30,
                        "Wealth Accumulation": 30,
                        "Education Funding": 10,
                        "Major Purchase": 20,
                        "Business Development": 5,
                        "Financial Security": 5
                    }
                elif age < 45:
                    goal_weights = {
                        "Retirement": 35,
                        "Wealth Accumulation": 25,
                        "Education Funding": 15,
                        "Income Generation": 5,
                        "Major Purchase": 10,
                        "Business Development": 5,
                        "Tax Optimization": 5
                    }
                elif age < 60:
                    goal_weights = {
                        "Retirement": 40,
                        "Income Generation": 15,
                        "Wealth Accumulation": 15,
                        "Tax Optimization": 10,
                        "Financial Security": 10,
                        "Legacy Planning": 5,
                        "Education Funding": 5
                    }
                else:
                    goal_weights = {
                        "Retirement": 30,
                        "Income Generation": 30,
                        "Financial Security": 15,
                        "Legacy Planning": 15,
                        "Tax Optimization": 10
                    }
            else:
                # Default if age unknown
                goal_weights = {
                    "Retirement": 30,
                    "Wealth Accumulation": 20,
                    "Income Generation": 15,
                    "Education Funding": 10,
                    "Major Purchase": 10,
                    "Financial Security": 10,
                    "Tax Optimization": 5
                }

            # Select 1-3 investment goals
            goal_count = random.choices([1, 2, 3], weights=[20, 50, 30], k=1)[0]
            selected_goals = []

            for _ in range(goal_count):
                if goal_weights:
                    goal_options = list(goal_weights.keys())
                    goal_weights_values = list(goal_weights.values())
                    selected_goal = random.choices(goal_options, weights=goal_weights_values, k=1)[0]
                    selected_goals.append(selected_goal)

                    # Remove selected goal for next iteration
                    del goal_weights[selected_goal]

            primary_investment_goals = ", ".join(selected_goals)

            # Risk tolerance determination
            risk_options = ["Conservative", "Moderately Conservative", "Moderate", "Moderately Aggressive",
                            "Aggressive"]

            # Base risk on age and income
            risk_index = 2  # Default to Moderate

            # Age factor
            if age:
                if age < 30:
                    risk_index += 1  # Younger investors can take more risk
                elif age >= 60:
                    risk_index -= 1  # Older investors typically more conservative

            # Income factor
            if income_bracket in [IncomeBracket.INCOME_150K_200K,
                                  IncomeBracket.INCOME_200K_250K,
                                  IncomeBracket.INCOME_250K_PLUS]:
                risk_index += 1  # Higher income allows more risk
            elif income_bracket in [IncomeBracket.UNDER_15K,
                                    IncomeBracket.INCOME_15K_25K]:
                risk_index -= 1  # Lower income necessitates more caution

            # Credit factor
            if credit_risk_tier in [CreditRiskTier.SUPER_PRIME, CreditRiskTier.PRIME]:
                risk_index += 0.5
            elif credit_risk_tier in [CreditRiskTier.SUBPRIME, CreditRiskTier.DEEP_SUBPRIME]:
                risk_index -= 0.5

            # Add some random variation
            risk_index += random.uniform(-0.5, 0.5)

            # Bound the index to valid range
            risk_index = max(0, min(4, int(round(risk_index))))

            # Set risk tolerance
            risk_tolerance = risk_options[risk_index]

            # DIGITAL ENGAGEMENT SCORE GENERATION
            # Measures likelihood to use digital channels
            digital_engagement_score = None

            # Base score (1-100)
            base_score = 50

            # Age factor
            if age:
                if age < 30:
                    base_score += 25  # Digital natives
                elif age < 45:
                    base_score += 15  # Digital adopters
                elif age < 60:
                    base_score += 5  # Mixed usage
                else:
                    base_score -= 15  # Traditional preference

            # Education factor
            if education_level in [EducationLevel.BACHELORS_DEGREE,
                                   EducationLevel.MASTERS_DEGREE,
                                   EducationLevel.DOCTORATE,
                                   EducationLevel.PROFESSIONAL_DEGREE]:
                base_score += 10  # Higher education correlates with digital comfort

            # Lifestyle factor
            if lifestyle_segment in [LifestyleSegment.TECH_SAVVY, LifestyleSegment.DIGITAL_FIRST]:
                base_score += 20
            elif lifestyle_segment in [LifestyleSegment.URBAN_PROFESSIONAL, LifestyleSegment.EXPERIENTIAL]:
                base_score += 10
            elif lifestyle_segment == LifestyleSegment.TRADITIONAL_BANKING:
                base_score -= 20

            # Add randomness
            base_score += random.randint(-10, 10)

            # Bound to 1-100 range
            digital_engagement_score = max(1, min(100, base_score))

            # CUSTOMER LIFETIME VALUE GENERATION
            # Estimated value of customer relationship
            customer_lifetime_value = None

            # Check account balances and loan amounts
            total_relationship_value = total_balance if total_balance else 0
            total_relationship_value += total_loans if total_loans else 0

            # Base CLV on current relationship, income, and credit quality
            if total_relationship_value > 0 or income_bracket != IncomeBracket.UNKNOWN:
                base_clv = 0

                # Relationship component
                if total_relationship_value > 1000000:
                    base_clv += 50000
                elif total_relationship_value > 500000:
                    base_clv += 25000
                elif total_relationship_value > 250000:
                    base_clv += 15000
                elif total_relationship_value > 100000:
                    base_clv += 10000
                elif total_relationship_value > 50000:
                    base_clv += 5000
                elif total_relationship_value > 10000:
                    base_clv += 2000
                else:
                    base_clv += 500

                # Income component
                if income_bracket in income_means:
                    income_value = income_means[income_bracket]
                    income_component = income_value * 0.1  # 10% of annual income
                    base_clv += income_component

                # Credit quality component
                if credit_risk_tier == CreditRiskTier.SUPER_PRIME:
                    base_clv *= 1.5
                elif credit_risk_tier == CreditRiskTier.PRIME:
                    base_clv *= 1.3
                elif credit_risk_tier == CreditRiskTier.NEAR_PRIME:
                    base_clv *= 1.0
                elif credit_risk_tier == CreditRiskTier.SUBPRIME:
                    base_clv *= 0.7
                elif credit_risk_tier == CreditRiskTier.DEEP_SUBPRIME:
                    base_clv *= 0.5

                # Age component (years of potential relationship)
                if age:
                    remaining_years = max(5, 85 - age)  # Assume relationship until age 85
                    yearly_value = base_clv / 10  # Spread value over 10 years
                    age_component = yearly_value * remaining_years
                    customer_lifetime_value = age_component
                else:
                    # Default to 20-year relationship if age unknown
                    customer_lifetime_value = base_clv * 2

                # Add randomness
                variation = random.uniform(0.8, 1.2)
                customer_lifetime_value = customer_lifetime_value * variation

                # Round to nearest $100
                customer_lifetime_value = round(customer_lifetime_value / 100) * 100

            # CHURN RISK SCORE GENERATION
            # Likelihood of customer leaving
            churn_risk_score = None

            # Base score (1-100, higher = higher risk)
            base_risk = 50

            # Relationship tenure factor
            if years_at_residence:
                if years_at_residence > 10:
                    base_risk -= 20  # Long relationship reduces risk
                elif years_at_residence > 5:
                    base_risk -= 10
                elif years_at_residence < 2:
                    base_risk += 15  # New relationships have higher churn

            # Account activity factor
            if account_count > 3:
                base_risk -= 15  # Multiple accounts reduce churn
            elif account_count > 1:
                base_risk -= 5

            # Credit quality factor
            if credit_risk_tier in [CreditRiskTier.SUPER_PRIME, CreditRiskTier.PRIME]:
                base_risk -= 10  # Better credit customers less likely to churn
            elif credit_risk_tier in [CreditRiskTier.SUBPRIME, CreditRiskTier.DEEP_SUBPRIME]:
                base_risk += 15  # Credit issues increase churn risk

            # Negative experiences factor
            if past_due_accounts > 0:
                base_risk += past_due_accounts * 10  # Each past due account increases risk

            # Add randomness
            base_risk += random.randint(-10, 10)

            # Bound to 1-100 range
            churn_risk_score = max(1, min(100, base_risk))

            # CROSS-SELL PROPENSITY SCORE GENERATION
            # Likelihood to purchase additional products
            cross_sell_propensity = None

            # Base score (1-100, higher = higher likelihood)
            base_propensity = 50

            # Existing relationship factor
            if account_count == 1:
                base_propensity += 10  # Single product customers have room to grow
            elif account_count == 2:
                base_propensity += 5  # Some room to expand
            elif account_count > 3:
                base_propensity -= 10  # Already has many products

            # Digital engagement factor
            if digital_engagement_score:
                if digital_engagement_score > 75:
                    base_propensity += 15  # Digitally engaged customers more receptive
                elif digital_engagement_score > 50:
                    base_propensity += 5

            # Credit quality factor
            if credit_risk_tier in [CreditRiskTier.SUPER_PRIME, CreditRiskTier.PRIME]:
                base_propensity += 10  # Better credit provides more options
            elif credit_risk_tier == CreditRiskTier.NEAR_PRIME:
                base_propensity += 0
            else:
                base_propensity -= 15  # Limited options for poor credit

            # Life stage factor
            if family_life_stage in [FamilyLifeStage.FAMILY_YOUNG_CHILDREN,
                                     FamilyLifeStage.FAMILY_SCHOOL_CHILDREN]:
                base_propensity += 15  # Families have more financial needs
            elif family_life_stage == FamilyLifeStage.RETIRED:
                base_propensity -= 10  # Retirees less likely to add products

            # Add randomness
            base_propensity += random.randint(-10, 10)

            # Bound to 1-100 range
            cross_sell_propensity = max(1, min(100, base_propensity))

            # CHANNEL PREFERENCE GENERATION
            # Preferred method of interaction
            channel_preference = None

            channel_options = ["Mobile", "Online", "Branch", "Phone", "ATM"]

            # Default weights
            channel_weights = {
                "Mobile": 25,
                "Online": 25,
                "Branch": 25,
                "Phone": 20,
                "ATM": 5
            }

            # Age-based adjustments
            if age:
                if age < 30:
                    # Younger customers prefer digital
                    channel_weights["Mobile"] += 25
                    channel_weights["Online"] += 15
                    channel_weights["Branch"] -= 20
                    channel_weights["Phone"] -= 15
                elif age < 45:
                    # Middle-aged balance of digital and traditional
                    channel_weights["Mobile"] += 15
                    channel_weights["Online"] += 10
                    channel_weights["Branch"] -= 10
                    channel_weights["Phone"] -= 10
                elif age < 60:
                    # Older middle-aged slight preference for traditional
                    channel_weights["Mobile"] -= 5
                    channel_weights["Branch"] += 10
                else:
                    # Seniors prefer traditional channels
                    channel_weights["Mobile"] -= 15
                    channel_weights["Online"] -= 10
                    channel_weights["Branch"] += 20
                    channel_weights["Phone"] += 10

            # Digital engagement adjustment
            if digital_engagement_score:
                if digital_engagement_score > 75:
                    # High digital engagement
                    channel_weights["Mobile"] += 25
                    channel_weights["Online"] += 15
                    channel_weights["Branch"] -= 20
                    channel_weights["Phone"] -= 15
                elif digital_engagement_score < 25:
                    # Low digital engagement
                    channel_weights["Mobile"] -= 15
                    channel_weights["Online"] -= 10
                    channel_weights["Branch"] += 20
                    channel_weights["Phone"] += 10

            # Lifestyle adjustment
            if lifestyle_segment == LifestyleSegment.TECH_SAVVY or lifestyle_segment == LifestyleSegment.DIGITAL_FIRST:
                channel_weights["Mobile"] += 20
                channel_weights["Online"] += 10
                channel_weights["Branch"] -= 15
                channel_weights["Phone"] -= 10
            elif lifestyle_segment == LifestyleSegment.TRADITIONAL_BANKING:
                channel_weights["Mobile"] -= 15
                channel_weights["Online"] -= 10
                channel_weights["Branch"] += 20
                channel_weights["Phone"] += 10

            # Ensure all weights are positive
            for channel in channel_weights:
                channel_weights[channel] = max(1, channel_weights[channel])

            # Select channel preference
            channel_options = list(channel_weights.keys())
            channel_weights_values = list(channel_weights.values())
            channel_preference = random.choices(channel_options, weights=channel_weights_values, k=1)[0]

            # DATA CONSENT GENERATION
            # Level of permission for data usage
            data_consent_level = None
            data_usage_restriction = None

            # Consent options
            consent_options = ["Full", "Limited", "Marketing Only", "Essential Only", "Minimal"]

            # Privacy concern by age
            privacy_concern = 50  # Base level

            if age:
                if age < 30:
                    privacy_concern -= 10  # Younger less concerned
                elif age > 60:
                    privacy_concern += 15  # Older more concerned

            # Education factor
            if education_level in [EducationLevel.BACHELORS_DEGREE,
                                   EducationLevel.MASTERS_DEGREE,
                                   EducationLevel.DOCTORATE,
                                   EducationLevel.PROFESSIONAL_DEGREE]:
                privacy_concern += 10  # Higher education more aware of privacy

            # Digital engagement factor
            if digital_engagement_score:
                if digital_engagement_score > 75:
                    privacy_concern -= 5  # Very digital users used to data sharing
                elif digital_engagement_score < 25:
                    privacy_concern += 10  # Traditional users more privacy-conscious

            # Map concern level to consent level
            if privacy_concern < 30:
                consent_weights = [70, 20, 5, 5, 0]  # Mostly Full
            elif privacy_concern < 50:
                consent_weights = [30, 40, 20, 10, 0]  # Mix of Full and Limited
            elif privacy_concern < 70:
                consent_weights = [5, 30, 40, 20, 5]  # More restricted
            else:
                consent_weights = [0, 10, 30, 40, 20]  # Very restricted

            data_consent_level = random.choices(consent_options, weights=consent_weights, k=1)[0]

            # Generate specific restrictions based on consent level
            restriction_options = [
                "No restrictions",
                "No third-party sharing",
                "No marketing use",
                "Essential services only",
                "No automated processing",
                "No profiling",
                "Time-limited consent",
                "Specific product use only"
            ]

            if data_consent_level == "Full":
                data_usage_restriction = "No restrictions"
            elif data_consent_level == "Limited":
                restriction_choices = ["No third-party sharing", "No marketing use", "No profiling"]
                restriction_count = random.randint(1, 2)
                selected_restrictions = random.sample(restriction_choices,
                                                      min(restriction_count, len(restriction_choices)))
                data_usage_restriction = "; ".join(selected_restrictions)
            elif data_consent_level == "Marketing Only":
                data_usage_restriction = "Essential services and marketing only; No third-party sharing"
            elif data_consent_level == "Essential Only":
                data_usage_restriction = "Essential services only; No marketing use; No profiling"
            else:  # Minimal
                data_usage_restriction = "Essential services only; No data sharing; No marketing; No automated processing; Time-limited consent"

        # Construct the final demographics dictionary
        demographics = {
            'consumer_banking_account_id': None,
            'credit_cards_card_accounts_id': None,
            'enterprise_party_id': id_fields['enterprise_party_id'],
            'data_source': data_source,
            'last_updated': last_updated,
            'education_level': education_level.value,
            'income_bracket': income_bracket.value,
            'occupation_category': occupation_category.value,
            'employer': employer,
            'employment_length_years': employment_length_years,
            'total_household_income': total_household_income,
            'household_size': household_size,
            'homeownership_status': homeownership_status.value,
            'estimated_home_value': estimated_home_value,
            'years_at_residence': years_at_residence,
            'net_worth_estimate': net_worth_estimate,
            'political_affiliation': political_affiliation.value,
            'number_of_children': number_of_children,
            'family_life_stage': family_life_stage.value,
            'lifestyle_segment': lifestyle_segment.value,
            'credit_risk_tier': credit_risk_tier.value,
            'discretionary_spending_estimate': discretionary_spending_estimate,
            'primary_investment_goals': primary_investment_goals,
            'risk_tolerance': risk_tolerance,
            'digital_engagement_score': digital_engagement_score,
            'customer_lifetime_value': customer_lifetime_value,
            'churn_risk_score': churn_risk_score,
            'cross_sell_propensity': cross_sell_propensity,
            'channel_preference': channel_preference,
            'data_consent_level': data_consent_level,
            'data_usage_restriction': data_usage_restriction
        }

    finally:
        cursor.close()

    return demographics
