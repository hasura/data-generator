import logging
import random
from typing import Dict, Any, Optional
import psycopg2
logger = logging.getLogger(__name__)
from data_generator import DataGenerator


def generate_random_hmda_applicant_demographics(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate random HMDA applicant demographic information.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_hmda_record_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated HMDA applicant demographic data
    """
    # Extract the HMDA record ID from the id_fields dictionary
    hmda_record_id = id_fields.get("mortgage_services_hmda_record_id")

    # Determine if record is for primary applicant or co-applicant
    applicant_types = ["primary", "co-applicant"]
    applicant_type_weights = [0.7, 0.3]  # 70% primary, 30% co-applicant
    applicant_type = random.choices(applicant_types, weights=applicant_type_weights, k=1)[0]

    # Get HMDA record information to make demographic data reasonable
    conn = dg.conn
    hmda_record_info = get_hmda_record_info(hmda_record_id, conn)

    # Generate ethnicity information
    ethnicity_data = generate_ethnicity_data()

    # Generate race information
    race_data = generate_race_data()

    # Generate sex information
    sex_data = generate_sex_data()

    # Generate age (typically 18-85 for borrowers)
    age = random.randint(18, 85)

    # Generate income (in thousands of dollars)
    # Income data can come from application if available
    if hmda_record_info and 'annual_income' in hmda_record_info and hmda_record_info['annual_income']:
        # Convert to thousands and round to nearest thousand
        income = round(float(hmda_record_info['annual_income']) / 1000)
    else:
        # Generate realistic income distribution
        income_brackets = [
            (20, 50, 0.2),  # $20k-$50k: 20% probability
            (50, 75, 0.25),  # $50k-$75k: 25% probability
            (75, 100, 0.25),  # $75k-$100k: 25% probability
            (100, 150, 0.15),  # $100k-$150k: 15% probability
            (150, 250, 0.1),  # $150k-$250k: 10% probability
            (250, 500, 0.05)  # $250k-$500k: 5% probability
        ]

        # Select income bracket based on probability distribution
        bracket_selection = random.random()
        cumulative_prob = 0
        selected_bracket = None

        for bracket_min, bracket_max, probability in income_brackets:
            cumulative_prob += probability
            if bracket_selection <= cumulative_prob:
                selected_bracket = (bracket_min, bracket_max)
                break

        # Generate income within selected bracket
        income = random.randint(selected_bracket[0], selected_bracket[1])

    # Generate debt-to-income ratio (typically 10-60%)
    dti_ratio = round(random.uniform(10.0, 60.0), 1)

    # Create the HMDA applicant demographics record
    demographics = {
        "mortgage_services_hmda_record_id": hmda_record_id,
        "applicant_type": applicant_type,
        "ethnicity_1": ethnicity_data.get("ethnicity_1"),
        "ethnicity_2": ethnicity_data.get("ethnicity_2"),
        "ethnicity_3": ethnicity_data.get("ethnicity_3"),
        "ethnicity_4": ethnicity_data.get("ethnicity_4"),
        "ethnicity_5": ethnicity_data.get("ethnicity_5"),
        "ethnicity_free_form": ethnicity_data.get("ethnicity_free_form"),
        "ethnicity_observed": ethnicity_data.get("ethnicity_observed"),
        "race_1": race_data.get("race_1"),
        "race_2": race_data.get("race_2"),
        "race_3": race_data.get("race_3"),
        "race_4": race_data.get("race_4"),
        "race_5": race_data.get("race_5"),
        "race_free_form": race_data.get("race_free_form"),
        "race_observed": race_data.get("race_observed"),
        "sex": sex_data.get("sex"),
        "sex_observed": sex_data.get("sex_observed"),
        "age": age,
        "income": income,
        "debt_to_income_ratio": dti_ratio
    }

    # Print debug information
    logger.debug(
        f"Generated HMDA Demographics - Applicant Type: {applicant_type}, Age: {age}, Income: {income}k, DTI: {dti_ratio}%")

    return demographics


def get_hmda_record_info(hmda_record_id: int, conn) -> Optional[Dict[str, Any]]:
    """
    Get HMDA record information to make demographic data reasonable.

    Args:
        hmda_record_id: The ID of the HMDA record
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing HMDA record and related application information or empty dict if not found
    """
    try:
        cursor = conn.cursor()

        # Get HMDA record data
        cursor.execute("""
            SELECT 
                h.reporting_year,
                h.loan_amount,
                h.action_taken,
                ma.mortgage_services_application_id
            FROM mortgage_services.hmda_records h
            LEFT JOIN mortgage_services.applications ma ON h.mortgage_services_application_id = ma.mortgage_services_application_id
            WHERE h.mortgage_services_hmda_record_id = %s
        """, (hmda_record_id,))

        result = cursor.fetchone()

        if result:
            # Create the base result dictionary with values we know exist
            hmda_info = {
                "reporting_year": result[0],
                "loan_amount": float(result[1]) if result[1] is not None else None,
                "action_taken": result[2],
                "mortgage_services_application_id": result[3]
                # annual_income will be added only if we can find it
            }

            application_id = result[3]

            # Only try to get income if application_id exists
            if application_id:
                try:
                    # Check if borrower_employments records exist (might be 0 records)
                    cursor.execute("""
                        SELECT EXISTS(
                            SELECT 1 
                            FROM mortgage_services.application_borrowers ab
                            JOIN mortgage_services.borrowers b ON ab.mortgage_services_borrower_id = b.mortgage_services_borrower_id
                            JOIN mortgage_services.borrower_employments be ON b.mortgage_services_borrower_id = be.mortgage_services_borrower_id
                            WHERE ab.mortgage_services_application_id = %s
                        )
                    """, (application_id,))

                    employment_exists = cursor.fetchone()[0]
                    employment_income = 0.0

                    if employment_exists:
                        # Get income from borrower_employments (monthly income * 12)
                        cursor.execute("""
                            SELECT COALESCE(SUM(be.monthly_income), 0) * 12
                            FROM mortgage_services.application_borrowers ab
                            JOIN mortgage_services.borrowers b ON ab.mortgage_services_borrower_id = b.mortgage_services_borrower_id
                            JOIN mortgage_services.borrower_employments be ON b.mortgage_services_borrower_id = be.mortgage_services_borrower_id
                            WHERE ab.mortgage_services_application_id = %s AND be.is_current = TRUE
                        """, (application_id,))

                        employment_income_result = cursor.fetchone()
                        if employment_income_result and employment_income_result[0]:
                            employment_income = float(employment_income_result[0])

                    # Check if borrower_incomes records exist (might be 0 records)
                    cursor.execute("""
                        SELECT EXISTS(
                            SELECT 1 
                            FROM mortgage_services.application_borrowers ab
                            JOIN mortgage_services.borrowers b ON ab.mortgage_services_borrower_id = b.mortgage_services_borrower_id
                            JOIN mortgage_services.borrower_incomes bi ON b.mortgage_services_borrower_id = bi.mortgage_services_borrower_id
                            WHERE ab.mortgage_services_application_id = %s
                        )
                    """, (application_id,))

                    additional_income_exists = cursor.fetchone()[0]
                    additional_income = 0.0

                    if additional_income_exists:
                        # Get additional income from borrower_incomes table with proper frequency conversion
                        cursor.execute("""
                            SELECT COALESCE(SUM(CASE
                                WHEN bi.frequency = 'monthly' THEN bi.amount * 12
                                WHEN bi.frequency = 'annually' THEN bi.amount
                                WHEN bi.frequency = 'weekly' THEN bi.amount * 52
                                WHEN bi.frequency = 'bi-weekly' THEN bi.amount * 26
                                WHEN bi.frequency = 'semi-monthly' THEN bi.amount * 24
                                WHEN bi.frequency = 'one-time' THEN bi.amount
                                ELSE bi.amount  -- Default case
                            END), 0)
                            FROM mortgage_services.application_borrowers ab
                            JOIN mortgage_services.borrowers b ON ab.mortgage_services_borrower_id = b.mortgage_services_borrower_id
                            JOIN mortgage_services.borrower_incomes bi ON b.mortgage_services_borrower_id = bi.mortgage_services_borrower_id
                            WHERE ab.mortgage_services_application_id = %s
                        """, (application_id,))

                        additional_income_result = cursor.fetchone()
                        if additional_income_result and additional_income_result[0]:
                            additional_income = float(additional_income_result[0])

                    # Only add annual_income to the result if we found any income
                    total_income = employment_income + additional_income
                    if total_income > 0:
                        hmda_info["annual_income"] = total_income

                except Exception as income_error:
                    # If we encounter an error processing incomes, log it but don't fail the entire function
                    print(f"Error processing income data: {income_error}")
                    # Just continue without annual_income in the result

            cursor.close()
            return hmda_info
        else:
            cursor.close()
            return {}

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching HMDA record information: {error}")
        return {}


def generate_ethnicity_data() -> Dict[str, Any]:
    """
    Generate random ethnicity data following HMDA reporting rules.

    Returns:
        Dictionary with ethnicity fields
    """

    # Decide the reporting approach
    reporting_approach = random.choices(
        ["provided", "not_provided", "observed", "not_applicable"],
        weights=[0.7, 0.15, 0.1, 0.05],
        k=1
    )[0]

    ethnicity_2 = None
    ethnicity_3 = None
    ethnicity_4 = None
    ethnicity_5 = None
    ethnicity_free_form = None

    if reporting_approach == "provided":
        # Applicant provided ethnicity information
        is_hispanic = random.random() < 0.2  # 20% chance of being Hispanic or Latino

        if is_hispanic:
            ethnicity_1 = "1"  # Hispanic or Latino

            # Decide if specific Hispanic or Latino origins are reported
            if random.random() < 0.7:  # 70% chance to specify origins
                # Possible specific Hispanic origins
                hispanic_origins = ["11", "12", "13", "14"]

                # Choose 1-3 specific origins without replacement
                num_origins = random.randint(1, min(3, len(hispanic_origins)))
                selected_origins = random.sample(hispanic_origins, num_origins)

                if len(selected_origins) >= 1:
                    ethnicity_2 = selected_origins[0]
                if len(selected_origins) >= 2:
                    ethnicity_3 = selected_origins[1]
                if len(selected_origins) >= 3:
                    ethnicity_4 = selected_origins[2]

                # Possibly include free-form text for "Other Hispanic or Latino"
                if "14" in selected_origins and random.random() < 0.5:
                    ethnicity_free_form = "South American"

        else:
            ethnicity_1 = "2"  # Not Hispanic or Latino

        ethnicity_observed = "2"  # Not collected based on visual observation

    elif reporting_approach == "not_provided":
        # Applicant did not provide ethnicity information
        ethnicity_1 = "3"  # Information not provided
        ethnicity_observed = random.choices(["1", "2"], weights=[0.6, 0.4], k=1)[0]

    elif reporting_approach == "observed":
        # Financial institution reported based on observation
        ethnicity_1 = random.choices(["1", "2"], weights=[0.2, 0.8], k=1)[0]
        ethnicity_observed = "1"  # Collected based on visual observation

    else:  # not_applicable
        ethnicity_1 = "4"  # Not applicable
        ethnicity_observed = "3"  # Not applicable

    return {
        "ethnicity_1": ethnicity_1,
        "ethnicity_2": ethnicity_2,
        "ethnicity_3": ethnicity_3,
        "ethnicity_4": ethnicity_4,
        "ethnicity_5": ethnicity_5,
        "ethnicity_free_form": ethnicity_free_form,
        "ethnicity_observed": ethnicity_observed
    }


def generate_race_data() -> Dict[str, Any]:
    """
    Generate random race data following HMDA reporting rules.

    Returns:
        Dictionary with race fields
    """

    # Decide the reporting approach
    reporting_approach = random.choices(
        ["provided", "not_provided", "observed", "not_applicable"],
        weights=[0.7, 0.15, 0.1, 0.05],
        k=1
    )[0]

    race_2 = None
    race_3 = None
    race_4 = None
    race_5 = None
    race_free_form = None

    if reporting_approach == "provided":
        # Distribution based roughly on US demographics
        race_categories = [
            ("5", 0.6),  # White (60%)
            ("3", 0.13),  # Black (13%)
            ("2", 0.06),  # Asian (6%)
            ("1", 0.01),  # American Indian (1%)
            ("4", 0.01),  # Pacific Islander (1%)
            ("multi", 0.19)  # Multiracial (19%)
        ]

        race_selection = random.choices(
            [category[0] for category in race_categories],
            weights=[category[1] for category in race_categories],
            k=1
        )[0]

        if race_selection == "multi":
            # Multiracial selection - pick 2-5 races
            available_races = ["1", "2", "3", "4", "5"]
            num_races = random.randint(2, 5)
            selected_races = random.sample(available_races, num_races)

            race_1 = selected_races[0]
            if len(selected_races) >= 2:
                race_2 = selected_races[1]
            if len(selected_races) >= 3:
                race_3 = selected_races[2]
            if len(selected_races) >= 4:
                race_4 = selected_races[3]
            if len(selected_races) >= 5:
                race_5 = selected_races[4]

        elif race_selection == "2":  # Asian
            race_1 = "2"  # Asian

            # Decide if specific Asian races are reported
            if random.random() < 0.7:  # 70% chance to specify
                # Possible specific Asian races
                asian_races = ["21", "22", "23", "24", "25", "26", "27"]

                # Choose 1-3 specific Asian races without replacement
                num_races = random.randint(1, 3)
                selected_races = random.sample(asian_races, num_races)

                if len(selected_races) >= 1:
                    race_2 = selected_races[0]
                if len(selected_races) >= 2:
                    race_3 = selected_races[1]
                if len(selected_races) >= 3:
                    race_4 = selected_races[2]

                # Possibly include free-form text for "Other Asian"
                if "27" in selected_races and random.random() < 0.5:
                    race_free_form = "Cambodian"

        elif race_selection == "4":  # Pacific Islander
            race_1 = "4"  # Native Hawaiian or Other Pacific Islander

            # Decide if specific Pacific Islander races are reported
            if random.random() < 0.7:  # 70% chance to specify
                # Possible specific Pacific Islander races
                pi_races = ["41", "42", "43", "44"]

                # Choose 1-3 specific Pacific Islander races without replacement
                num_races = random.randint(1, len(pi_races))
                selected_races = random.sample(pi_races, num_races)

                if len(selected_races) >= 1:
                    race_2 = selected_races[0]
                if len(selected_races) >= 2:
                    race_3 = selected_races[1]
                if len(selected_races) >= 3:
                    race_4 = selected_races[2]

                # Possibly include free-form text for "Other Pacific Islander"
                if "44" in selected_races and random.random() < 0.5:
                    race_free_form = "Fijian"

        elif race_selection == "1":  # American Indian
            race_1 = "1"  # American Indian or Alaska Native

            # Include tribal affiliation for American Indian
            if random.random() < 0.7:  # 70% chance to specify
                tribal_affiliations = ["Cherokee", "Navajo", "Sioux", "Chippewa", "Apache"]
                race_free_form = random.choice(tribal_affiliations)

        else:
            # Single race (White or Black)
            race_1 = race_selection

        race_observed = "2"  # Not collected based on visual observation

    elif reporting_approach == "not_provided":
        # Applicant did not provide race information
        race_1 = "6"  # Information not provided
        race_observed = random.choices(["1", "2"], weights=[0.6, 0.4], k=1)[0]

    elif reporting_approach == "observed":
        # Financial institution reported based on observation
        observed_race_probs = [
            ("5", 0.6),  # White (60%)
            ("3", 0.20),  # Black (20%)
            ("2", 0.15),  # Asian (15%)
            ("1", 0.03),  # American Indian (3%)
            ("4", 0.02)  # Pacific Islander (2%)
        ]

        race_1 = random.choices(
            [race[0] for race in observed_race_probs],
            weights=[race[1] for race in observed_race_probs],
            k=1
        )[0]

        race_observed = "1"  # Collected based on visual observation

    else:  # not_applicable
        race_1 = "7"  # Not applicable
        race_observed = "3"  # Not applicable

    return {
        "race_1": race_1,
        "race_2": race_2,
        "race_3": race_3,
        "race_4": race_4,
        "race_5": race_5,
        "race_free_form": race_free_form,
        "race_observed": race_observed
    }


def generate_sex_data() -> Dict[str, Any]:
    """
    Generate random sex data following HMDA reporting rules.

    Returns:
        Dictionary with sex fields
    """

    # Decide the reporting approach
    reporting_approach = random.choices(
        ["provided", "not_provided", "observed", "not_applicable"],
        weights=[0.7, 0.15, 0.1, 0.05],
        k=1
    )[0]

    if reporting_approach == "provided":
        # Applicant provided sex information
        sex_probs = [
            ("1", 0.49),  # Male (49%)
            ("2", 0.49),  # Female (49%)
            ("6", 0.02)  # Both (2%)
        ]

        sex = random.choices(
            [s[0] for s in sex_probs],
            weights=[s[1] for s in sex_probs],
            k=1
        )[0]

        sex_observed = "2"  # Not collected based on visual observation

    elif reporting_approach == "not_provided":
        # Applicant did not provide sex information
        sex = "3"  # Information not provided
        sex_observed = random.choices(["1", "2"], weights=[0.6, 0.4], k=1)[0]

    elif reporting_approach == "observed":
        # Financial institution reported based on observation
        sex = random.choices(["1", "2"], weights=[0.5, 0.5], k=1)[0]
        sex_observed = "1"  # Collected based on visual observation

    else:  # not_applicable
        sex = "4"  # Not applicable
        sex_observed = "3"  # Not applicable

    return {
        "sex": sex,
        "sex_observed": sex_observed
    }
