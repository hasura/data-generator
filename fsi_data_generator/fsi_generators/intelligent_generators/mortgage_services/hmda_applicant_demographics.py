from .enums import (HmdaAgeGroup, HmdaApplicantPresent, HmdaApplicantType,
                    HmdaCollectionMethod, HmdaEthnicity, HmdaEthnicityDetail,
                    HmdaRace, HmdaRaceAsianDetail,
                    HmdaRacePacificIslanderDetail, HmdaSex)
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import logging
import psycopg2
import random

logger = logging.getLogger(__name__)
from data_generator import DataGenerator, SkipRowGenerationError

# Global set to track processed HMDA records
processed_hmda_records = set()


def generate_random_hmda_applicant_demographics(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate random HMDA applicant demographic information.

    Args:
        _id_fields: Dictionary containing the required ID fields (not used anymore)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated HMDA applicant demographic data
    """
    # Get an unused HMDA record ID
    hmda_record_id = _get_unused_hmda_record_id(dg.conn)

    # If no unused HMDA records are available, return None
    if hmda_record_id is None:
        raise SkipRowGenerationError

    # Add this record to the processed set
    processed_hmda_records.add(hmda_record_id)

    # Determine applicant type using get_random()
    applicant_type = HmdaApplicantType.get_random().value

    # Get HMDA record information to make demographic data reasonable
    hmda_record_info = _get_hmda_record_info(hmda_record_id, dg.conn)

    # Generate ethnicity information
    ethnicity_data = _generate_ethnicity_data()

    # Generate race information
    race_data = _generate_race_data()

    # Generate sex information
    sex_data = _generate_sex_data()

    # Generate age (typically 18-85 for borrowers)
    age = random.randint(18, 85)

    # Determine age group based on the generated age
    age_group = _get_age_group(age)

    # Generate income (in thousands of dollars)
    # Income data can come from application if available
    if hmda_record_info and 'annual_income' in hmda_record_info and hmda_record_info['annual_income']:
        # Convert to thousands and round to nearest thousandths
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

    # Determine if applicant was present using get_random()
    applicant_present = HmdaApplicantPresent.get_random().value

    # Generate plausible created and modified dates
    # If HMDA record has a date, use that as reference, otherwise use a recent date
    current_date = datetime.now(timezone.utc)

    if hmda_record_info and 'action_taken_date' in hmda_record_info and hmda_record_info['action_taken_date']:
        # Use action_taken_date as reference and add 1-15 days for created_date
        reference_date = hmda_record_info['action_taken_date']
        days_after = random.randint(1, 15)
        created_date = reference_date + timedelta(days=days_after)

        # Ensure created_date is not in the future
        if created_date > current_date:
            created_date = current_date - timedelta(days=random.randint(1, 30))
    else:
        # Use a date within the last 180 days
        days_ago = random.randint(1, 180)
        created_date = current_date - timedelta(days=days_ago)

    # 30% chance of having a modified date
    modified_date = None
    if random.random() < 0.3:
        # Modified date is 1-60 days after created_date but not in the future
        days_after_creation = random.randint(1, 60)
        potential_modified_date = created_date + timedelta(days=days_after_creation)

        # Ensure modified_date is not in the future
        if potential_modified_date <= current_date:
            modified_date = potential_modified_date

    # Create the HMDA applicant demographics record with all required fields
    demographics = {
        "mortgage_services_hmda_record_id": hmda_record_id,
        "applicant_type": applicant_type,

        # Ethnicity fields
        "ethnicity_1": ethnicity_data.get("ethnicity_1"),
        "ethnicity_2": ethnicity_data.get("ethnicity_2"),
        "ethnicity_3": ethnicity_data.get("ethnicity_3"),
        "ethnicity_4": ethnicity_data.get("ethnicity_4"),
        "ethnicity_5": ethnicity_data.get("ethnicity_5"),
        "ethnicity_free_form": ethnicity_data.get("ethnicity_free_form"),
        "ethnicity_observed": ethnicity_data.get("ethnicity_observed"),

        # Race fields
        "race_1": race_data.get("race_1"),
        "race_2": race_data.get("race_2"),
        "race_3": race_data.get("race_3"),
        "race_4": race_data.get("race_4"),
        "race_5": race_data.get("race_5"),
        "race_detail_1": None,  # Default to None - these are filled based on race selections
        "race_detail_2": None,
        "race_detail_3": None,
        "race_detail_4": None,
        "race_detail_5": None,
        "race_free_form": race_data.get("race_free_form"),
        "race_observed": race_data.get("race_observed"),

        # Sex fields
        "sex": sex_data.get("sex"),
        "sex_observed": sex_data.get("sex_observed"),

        # Age fields
        "age": age,
        "age_group": age_group,

        # Income and debt-to-income ratio
        "income": income,
        "debt_to_income_ratio": dti_ratio,

        # Additional fields
        "applicant_present": applicant_present,
        "created_date": created_date,
        "modified_date": modified_date
    }

    # Add race detail fields if appropriate
    # Typically race_detail_1 would be filled if race_1 is Asian or Pacific Islander
    if race_data.get("race_1") == HmdaRace.ASIAN.value:
        demographics["race_detail_1"] = HmdaRaceAsianDetail.get_random().value
    elif race_data.get("race_1") == HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER.value:
        demographics["race_detail_1"] = HmdaRacePacificIslanderDetail.get_random().value

    # Similar logic for race_2 through race_5 if they exist
    if race_data.get("race_2") == HmdaRace.ASIAN.value:
        demographics["race_detail_2"] = HmdaRaceAsianDetail.get_random().value
    elif race_data.get("race_2") == HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER.value:
        demographics["race_detail_2"] = HmdaRacePacificIslanderDetail.get_random().value

    if race_data.get("race_3") == HmdaRace.ASIAN.value:
        demographics["race_detail_3"] = HmdaRaceAsianDetail.get_random().value
    elif race_data.get("race_3") == HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER.value:
        demographics["race_detail_3"] = HmdaRacePacificIslanderDetail.get_random().value

    if race_data.get("race_4") == HmdaRace.ASIAN.value:
        demographics["race_detail_4"] = HmdaRaceAsianDetail.get_random().value
    elif race_data.get("race_4") == HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER.value:
        demographics["race_detail_4"] = HmdaRacePacificIslanderDetail.get_random().value

    if race_data.get("race_5") == HmdaRace.ASIAN.value:
        demographics["race_detail_5"] = HmdaRaceAsianDetail.get_random().value
    elif race_data.get("race_5") == HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER.value:
        demographics["race_detail_5"] = HmdaRacePacificIslanderDetail.get_random().value

    # Print debug information
    logger.info(f"Generated HMDA Demographics for record {hmda_record_id} - Applicant Type: {applicant_type}")

    return demographics


def _get_unused_hmda_record_id(conn) -> Optional[int]:
    """
    Get an HMDA record ID that hasn't been used yet for demographics.

    Args:
        conn: PostgreSQL connection object

    Returns:
        An unused HMDA record ID or None if no unused records are available
    """
    try:
        cursor = conn.cursor()

        # Get all HMDA record IDs
        cursor.execute("SELECT mortgage_services_hmda_record_id FROM mortgage_services.hmda_records")

        all_hmda_records = [row.get('mortgage_services_hmda_record_id') for row in cursor.fetchall()]
        cursor.close()

        # Find the first HMDA record ID that isn't in the processed set
        for hmda_record_id in all_hmda_records:
            if hmda_record_id not in processed_hmda_records:
                return hmda_record_id

        # If no unused records are found, return None
        return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching unused HMDA record ID: {error}")
        return None


def _get_hmda_record_info(hmda_record_id: int, conn) -> Optional[Dict[str, Any]]:
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
            hmda_info = dict(result)

            application_id = hmda_info.get('mortgage_services_application_id')

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
                        ) AS exists
                    """, (application_id,))

                    employment_exists = cursor.fetchone()
                    employment_income = 0.0

                    if employment_exists and employment_exists['exists']:
                        # Get income from borrower_employments (monthly income * 12)
                        cursor.execute("""
                            SELECT COALESCE(SUM(be.monthly_income), 0) * 12 as income
                            FROM mortgage_services.application_borrowers ab
                            JOIN mortgage_services.borrowers b ON ab.mortgage_services_borrower_id = b.mortgage_services_borrower_id
                            JOIN mortgage_services.borrower_employments be ON b.mortgage_services_borrower_id = be.mortgage_services_borrower_id
                            WHERE ab.mortgage_services_application_id = %s AND be.is_current = TRUE
                        """, (application_id,))

                        employment_income_result = cursor.fetchone()
                        if employment_income_result and employment_income_result['income']:
                            employment_income = employment_income_result['income']

                    # Check if borrower_incomes records exist (might be 0 records)
                    cursor.execute("""
                        SELECT EXISTS(
                            SELECT 1 
                            FROM mortgage_services.application_borrowers ab
                            JOIN mortgage_services.borrowers b ON ab.mortgage_services_borrower_id = b.mortgage_services_borrower_id
                            JOIN mortgage_services.borrower_incomes bi ON b.mortgage_services_borrower_id = bi.mortgage_services_borrower_id
                            WHERE ab.mortgage_services_application_id = %s
                        ) AS exists
                    """, (application_id,))

                    additional_income_exists = cursor.fetchone()
                    additional_income = 0.0

                    if additional_income_exists and additional_income_exists['exists']:
                        # Get additional income from borrower_incomes table with proper frequency conversion
                        cursor.execute("""
                            SELECT COALESCE(SUM(CASE
                                WHEN frequency = 'MONTHLY' THEN amount * 12
                                WHEN frequency = 'ANNUALLY' THEN amount
                                WHEN frequency = 'SEMI_ANNUALLY' THEN amount * 2
                                WHEN frequency = 'QUARTERLY' THEN amount * 4
                                WHEN frequency = 'WEEKLY' THEN amount * 52
                                WHEN frequency = 'BI_WEEKLY' THEN amount * 26
                                WHEN frequency = 'SEMI_MONTHLY' THEN amount * 24
                                ELSE amount  -- Default case
                            END), 0) as income
                            FROM mortgage_services.application_borrowers ab
                            JOIN mortgage_services.borrowers b ON ab.mortgage_services_borrower_id = b.mortgage_services_borrower_id
                            JOIN mortgage_services.borrower_incomes bi ON b.mortgage_services_borrower_id = bi.mortgage_services_borrower_id
                            WHERE ab.mortgage_services_application_id = %s
                        """, (application_id,))

                        additional_income_result = cursor.fetchone()
                        if additional_income_result and additional_income_result['income']:
                            additional_income = additional_income_result['income']

                    # Only add annual_income to the result if we found any income
                    total_income = employment_income + additional_income
                    if total_income > 0:
                        hmda_info["annual_income"] = total_income

                except Exception as income_error:
                    # If we encounter an error processing incomes, log it but don't fail the entire function
                    logger.error(f"Error processing income data: {income_error}")
                    # Just continue without annual_income in the result

            cursor.close()
            return hmda_info
        else:
            cursor.close()
            return {}

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching HMDA record information: {error}")
        return {}


def _get_age_group(age: int) -> str:
    """
    Determine the HMDA age group based on the age.

    Args:
        age: Age in years

    Returns:
        HMDA age group code
    """
    if age < 25:
        return HmdaAgeGroup.LESS_THAN_25.value
    elif 25 <= age <= 34:
        return HmdaAgeGroup.AGE_25_TO_34.value
    elif 35 <= age <= 44:
        return HmdaAgeGroup.AGE_35_TO_44.value
    elif 45 <= age <= 54:
        return HmdaAgeGroup.AGE_45_TO_54.value
    elif 55 <= age <= 64:
        return HmdaAgeGroup.AGE_55_TO_64.value
    elif 65 <= age <= 74:
        return HmdaAgeGroup.AGE_65_TO_74.value
    else:  # age > 74
        return HmdaAgeGroup.GREATER_THAN_74.value


def _generate_ethnicity_data() -> Dict[str, Any]:
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
            ethnicity_1 = HmdaEthnicity.HISPANIC_OR_LATINO.value

            # Decide if specific Hispanic or Latino origins are reported
            if random.random() < 0.7:  # 70% chance to specify origins
                # Get possible specific Hispanic origins using get_random()
                hispanic_details = [
                    HmdaEthnicityDetail.MEXICAN,
                    HmdaEthnicityDetail.PUERTO_RICAN,
                    HmdaEthnicityDetail.CUBAN,
                    HmdaEthnicityDetail.OTHER_HISPANIC_OR_LATINO
                ]

                # Choose 1-3 specific origins without replacement
                num_origins = random.randint(1, 3)
                selected_origins = random.sample(hispanic_details, num_origins)

                if len(selected_origins) >= 1:
                    ethnicity_2 = selected_origins[0].value
                if len(selected_origins) >= 2:
                    ethnicity_3 = selected_origins[1].value
                if len(selected_origins) >= 3:
                    ethnicity_4 = selected_origins[2].value

                # Possibly include free-form text for "Other Hispanic or Latino"
                if HmdaEthnicityDetail.OTHER_HISPANIC_OR_LATINO in selected_origins and random.random() < 0.5:
                    ethnicity_free_form = "South American"
        else:
            ethnicity_1 = HmdaEthnicity.NOT_HISPANIC_OR_LATINO.value

        ethnicity_observed = HmdaCollectionMethod.NOT_COLLECTED_ON_VISUAL_OBSERVATION.value

    elif reporting_approach == "not_provided":
        # Applicant did not provide ethnicity information
        ethnicity_1 = HmdaEthnicity.INFORMATION_NOT_PROVIDED.value

        observation_methods = [
            HmdaCollectionMethod.VISUAL_OBSERVATION_OR_SURNAME,
            HmdaCollectionMethod.NOT_COLLECTED_ON_VISUAL_OBSERVATION
        ]
        weights = [0.6, 0.4]
        ethnicity_observed = random.choices(observation_methods, weights=weights, k=1)[0].value

    elif reporting_approach == "observed":
        # Financial institution reported based on observation
        ethnicities = [
            HmdaEthnicity.HISPANIC_OR_LATINO,
            HmdaEthnicity.NOT_HISPANIC_OR_LATINO
        ]
        weights = [0.2, 0.8]
        ethnicity_1 = random.choices(ethnicities, weights=weights, k=1)[0].value
        ethnicity_observed = HmdaCollectionMethod.VISUAL_OBSERVATION_OR_SURNAME.value

    else:  # not_applicable
        ethnicity_1 = HmdaEthnicity.NOT_APPLICABLE.value
        ethnicity_observed = HmdaCollectionMethod.NOT_APPLICABLE.value

    return {
        "ethnicity_1": ethnicity_1,
        "ethnicity_2": ethnicity_2,
        "ethnicity_3": ethnicity_3,
        "ethnicity_4": ethnicity_4,
        "ethnicity_5": ethnicity_5,
        "ethnicity_free_form": ethnicity_free_form,
        "ethnicity_observed": ethnicity_observed
    }


def _generate_race_data() -> Dict[str, Any]:
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
            (HmdaRace.WHITE, 0.6),  # White (60%)
            (HmdaRace.BLACK_OR_AFRICAN_AMERICAN, 0.13),  # Black (13%)
            (HmdaRace.ASIAN, 0.06),  # Asian (6%)
            (HmdaRace.AMERICAN_INDIAN_OR_ALASKA_NATIVE, 0.01),  # American Indian (1%)
            (HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER, 0.01),  # Pacific Islander (1%)
            ("multi", 0.19)  # Multiracial (19%)
        ]

        race_selection = random.choices(
            [category[0] for category in race_categories],
            weights=[category[1] for category in race_categories],
            k=1
        )[0]

        if race_selection == "multi":
            # Multiracial selection - pick 2-5 races
            available_races = [
                HmdaRace.AMERICAN_INDIAN_OR_ALASKA_NATIVE,
                HmdaRace.ASIAN,
                HmdaRace.BLACK_OR_AFRICAN_AMERICAN,
                HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER,
                HmdaRace.WHITE
            ]
            num_races = random.randint(2, 5)
            selected_races = random.sample(available_races, num_races)

            race_1 = selected_races[0].value
            if len(selected_races) >= 2:
                race_2 = selected_races[1].value
            if len(selected_races) >= 3:
                race_3 = selected_races[2].value
            if len(selected_races) >= 4:
                race_4 = selected_races[3].value
            if len(selected_races) >= 5:
                race_5 = selected_races[4].value

        elif race_selection == HmdaRace.ASIAN:
            race_1 = HmdaRace.ASIAN.value

            # Decide if specific Asian races are reported
            if random.random() < 0.7:  # 70% chance to specify
                # Choose 1-3 specific Asian races without replacement
                num_races = random.randint(1, 3)
                asian_detail_options = [race for race in HmdaRaceAsianDetail if isinstance(race.value, str)]
                selected_races = random.sample(asian_detail_options, min(num_races, len(asian_detail_options)))

                if len(selected_races) >= 1:
                    race_2 = selected_races[0].value
                if len(selected_races) >= 2:
                    race_3 = selected_races[1].value
                if len(selected_races) >= 3:
                    race_4 = selected_races[2].value

                # Possibly include free-form text for "Other Asian"
                if HmdaRaceAsianDetail.OTHER_ASIAN in selected_races and random.random() < 0.5:
                    race_free_form = "Cambodian"

        elif race_selection == HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER:
            race_1 = HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER.value

            # Decide if specific Pacific Islander races are reported
            if random.random() < 0.7:  # 70% chance to specify
                # Choose 1-3 specific Pacific Islander races without replacement
                num_races = random.randint(1, 3)
                pi_detail_options = list(HmdaRacePacificIslanderDetail)
                selected_races = random.sample(pi_detail_options, min(num_races, len(pi_detail_options)))

                if len(selected_races) >= 1:
                    race_2 = selected_races[0].value
                if len(selected_races) >= 2:
                    race_3 = selected_races[1].value
                if len(selected_races) >= 3:
                    race_4 = selected_races[2].value

                # Possibly include free-form text for "Other Pacific Islander"
                if HmdaRacePacificIslanderDetail.OTHER_PACIFIC_ISLANDER in selected_races and random.random() < 0.5:
                    race_free_form = "Fijian"

        elif race_selection == HmdaRace.AMERICAN_INDIAN_OR_ALASKA_NATIVE:
            race_1 = HmdaRace.AMERICAN_INDIAN_OR_ALASKA_NATIVE.value

            # Include tribal affiliation for American Indian
            if random.random() < 0.7:  # 70% chance to specify
                tribal_affiliations = ["Cherokee", "Navajo", "Sioux", "Chippewa", "Apache"]
                race_free_form = random.choice(tribal_affiliations)

        else:
            # Single race (White or Black)
            race_1 = race_selection.value

        race_observed = HmdaCollectionMethod.NOT_COLLECTED_ON_VISUAL_OBSERVATION.value

    elif reporting_approach == "not_provided":
        # Applicant did not provide race information
        race_1 = HmdaRace.INFORMATION_NOT_PROVIDED.value

        observation_methods = [
            HmdaCollectionMethod.VISUAL_OBSERVATION_OR_SURNAME,
            HmdaCollectionMethod.NOT_COLLECTED_ON_VISUAL_OBSERVATION
        ]
        weights = [0.6, 0.4]
        race_observed = random.choices(observation_methods, weights=weights, k=1)[0].value

    elif reporting_approach == "observed":
        # Financial institution reported based on observation
        observed_race_options = [
            HmdaRace.WHITE,
            HmdaRace.BLACK_OR_AFRICAN_AMERICAN,
            HmdaRace.ASIAN,
            HmdaRace.AMERICAN_INDIAN_OR_ALASKA_NATIVE,
            HmdaRace.NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER
        ]
        observed_race_weights = [0.6, 0.2, 0.15, 0.03, 0.02]

        race_1 = random.choices(observed_race_options, weights=observed_race_weights, k=1)[0].value
        race_observed = HmdaCollectionMethod.VISUAL_OBSERVATION_OR_SURNAME.value

    else:  # not_applicable
        race_1 = HmdaRace.NOT_APPLICABLE.value
        race_observed = HmdaCollectionMethod.NOT_APPLICABLE.value

    return {
        "race_1": race_1,
        "race_2": race_2,
        "race_3": race_3,
        "race_4": race_4,
        "race_5": race_5,
        "race_free_form": race_free_form,
        "race_observed": race_observed
    }


def _generate_sex_data() -> Dict[str, Any]:
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
        sex_options = [
            HmdaSex.MALE,
            HmdaSex.FEMALE,
            HmdaSex.APPLICANT_SELECTED_BOTH
        ]
        sex_weights = [0.49, 0.49, 0.02]
        sex = random.choices(sex_options, weights=sex_weights, k=1)[0].value
        sex_observed = HmdaCollectionMethod.NOT_COLLECTED_ON_VISUAL_OBSERVATION.value

    elif reporting_approach == "not_provided":
        # Applicant did not provide sex information
        sex = HmdaSex.INFORMATION_NOT_PROVIDED.value

        observation_methods = [
            HmdaCollectionMethod.VISUAL_OBSERVATION_OR_SURNAME,
            HmdaCollectionMethod.NOT_COLLECTED_ON_VISUAL_OBSERVATION
        ]
        weights = [0.6, 0.4]
        sex_observed = random.choices(observation_methods, weights=weights, k=1)[0].value

    elif reporting_approach == "observed":
        # Financial institution reported based on observation
        sex_options = [HmdaSex.MALE, HmdaSex.FEMALE]
        sex = random.choices(sex_options, weights=[0.5, 0.5], k=1)[0].value
        sex_observed = HmdaCollectionMethod.VISUAL_OBSERVATION_OR_SURNAME.value

    else:  # not_applicable
        sex = HmdaSex.NOT_APPLICABLE.value
        sex_observed = HmdaCollectionMethod.NOT_APPLICABLE.value

    return {
        "sex": sex,
        "sex_observed": sex_observed
    }
