import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2
from faker import Faker

# Initialize Faker
fake = Faker()
logger = logging.getLogger(__name__)


def generate_random_borrower_employment(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services borrower employment record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_borrower_id)
        dg: DataGenertor instance

    Returns:
        Dictionary containing randomly generated borrower employment data (without ID fields)
    """
    # Get borrower information and application status to make employment data reasonable
    conn = dg.conn
    borrower_info = get_borrower_info(id_fields.get("mortgage_services_borrower_id"), conn)
    application_info = get_application_info_for_borrower(id_fields.get("mortgage_services_borrower_id"), conn)

    # Define possible values for categorical fields
    employment_types = [
        "full-time",
        "part-time",
        "self-employed",
        "contract",
        "seasonal"
    ]

    employment_type_weights = [0.7, 0.1, 0.15, 0.03, 0.02]  # Full-time is most common

    verification_statuses = [
        "verified",
        "pending verification",
        "verification failed",
        "not verified"
    ]

    # Determine if current employment based on borrower info
    is_current = True  # Default to current employment
    if borrower_info and random.random() < 0.2:  # 20% chance of past employment
        is_current = False

    # Select employment type
    employment_type = random.choices(employment_types, weights=employment_type_weights, k=1)[0]

    # Generate employer name using Faker
    employer_name = fake.company()

    # Generate position based on employment type
    positions_by_type = {
        "full-time": [
            "Software Engineer", "Project Manager", "Sales Representative", "Accountant",
            "Marketing Specialist", "Human Resources Manager", "Operations Director",
            "Financial Analyst", "Customer Service Representative", "Administrative Assistant",
            "Product Manager", "Business Analyst", "Systems Administrator", "Research Scientist",
            "Data Scientist", "Quality Assurance Analyst", "Executive Assistant", "Account Manager",
            "Supply Chain Manager", "Legal Counsel", "Corporate Trainer", "Network Engineer",
            "Compliance Officer", "UX Designer", "Brand Manager", "IT Support Specialist",
            "Web Developer", "Benefits Administrator", "Public Relations Specialist", "Sales Engineer"
        ],
        "part-time": [
            "Sales Associate", "Office Assistant", "Customer Service Rep", "Cashier",
            "Delivery Driver", "Warehouse Associate", "Retail Associate", "Server",
            "Tutor", "Security Guard",
            "Barista", "Receptionist", "Bank Teller", "Data Entry Clerk",
            "Library Assistant", "Dental Assistant", "Medical Receptionist", "Tour Guide",
            "Research Assistant", "Brand Ambassador", "Caregiver", "Fitness Instructor",
            "Teaching Assistant", "Pharmacy Technician", "Event Staff", "Restaurant Host",
            "Retail Merchandiser", "Social Media Moderator", "Call Center Representative", "Museum Guide"
        ],
        "self-employed": [
            "Independent Consultant", "Freelance Designer", "Business Owner", "Contractor",
            "Realtor", "Attorney", "Photographer", "Writer", "Therapist", "Handyman",
            "Personal Trainer", "Life Coach", "Mobile App Developer", "Tax Preparer",
            "Interior Designer", "Event Planner", "Videographer", "Social Media Manager",
            "Private Tutor", "Landscaper", "Home Inspector", "Translator",
            "Private Chef", "Career Coach", "Music Teacher", "Wedding Planner",
            "E-commerce Store Owner", "Notary Public", "Yoga Instructor", "Web Designer"
        ],
        "contract": [
            "IT Consultant", "Project Coordinator", "Content Writer", "Web Developer",
            "Graphic Designer", "Technical Writer", "Marketing Consultant", "Data Analyst",
            "Software Developer", "UX/UI Designer", "Systems Architect", "SEO Specialist",
            "Quality Assurance Tester", "Cybersecurity Analyst", "Network Consultant", "DevOps Engineer",
            "Business Intelligence Analyst", "Database Administrator", "Technical Recruiter", "Legal Consultant",
            "Engineering Consultant", "Financial Auditor", "Healthcare Consultant", "Training Consultant",
            "Video Editor", "Virtual Assistant", "Social Media Strategist", "Product Designer",
            "Market Research Analyst", "Scientific Researcher", "Curriculum Developer", "Interim Manager"
        ],
        "seasonal": [
            "Tax Preparer", "Retail Sales Associate", "Delivery Driver", "Resort Staff",
            "Landscaper", "Agricultural Worker", "Camp Counselor", "Tour Guide",
            "Election Worker", "Snow Removal Technician", "Ski Instructor", "Holiday Gift Wrapper",
            "Inventory Specialist", "Festival Staff", "Halloween Store Associate", "Theme Park Attendant",
            "Fishing Guide", "Harvest Worker", "Holiday Decorator", "Lifeguard",
            "Summer Camp Director", "Cruise Ship Staff", "National Park Ranger", "Beach Attendant",
            "Event Security", "Christmas Tree Lot Worker", "Sports Venue Staff", "Tax Season Accountant",
            "Seasonal Baker", "Pumpkin Patch Worker", "Flower Shop Assistant", "Hotel Housekeeper"
        ]
    }

    position = random.choice(positions_by_type.get(employment_type, positions_by_type["full-time"]))

    # Generate reasonable employment dates
    today = datetime.date.today()

    # Start date - typically 0-20 years ago
    years_ago = random.randint(0, 20)
    months_ago = random.randint(0, 11)
    start_date = today.replace(year=today.year - years_ago)
    start_date = start_date.replace(month=((today.month - months_ago - 1) % 12) + 1)

    # End date - only for past employment
    end_date = None
    if not is_current:
        # Calculate minimum duration of employment (6 months)
        min_months = 6

        # Calculate maximum duration based on start date
        max_months = (today.year - start_date.year) * 12 + (today.month - start_date.month) - 1

        # Ensure we have a valid range
        if max_months < min_months:
            # If this happens, it means the start date is too recent for past employment
            # We should adjust the start date to be earlier
            start_date = today.replace(month=((today.month - min_months - 1) % 12) + 1)
            if (today.month - min_months) <= 0:
                # If we need to go back to previous year
                start_date = start_date.replace(year=today.year - 1)
            max_months = min_months + 2  # Give a little buffer for randomization

        months_after_start = random.randint(min_months, max_months)
        end_year = start_date.year + (months_after_start // 12)
        end_month = ((start_date.month + months_after_start - 1) % 12) + 1
        end_date = datetime.date(end_year, end_month,
                                 min(start_date.day, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][end_month - 1]))

    # Generate years in profession (may be longer than current job)
    if employment_type == "self-employed":
        # Self-employed people often have many years in profession
        years_in_profession = random.randint(years_ago, min(years_ago + 15, 40))
    else:
        # Other employment types might be close to current job duration
        years_in_profession = random.randint(years_ago, min(years_ago + 5, 30))

    # Generate monthly income
    if employment_type == "full-time":
        monthly_income = round(random.uniform(3000, 12000), 2)
    elif employment_type == "part-time":
        monthly_income = round(random.uniform(1000, 3000), 2)
    elif employment_type == "self-employed":
        monthly_income = round(random.uniform(4000, 18000), 2)
    elif employment_type == "contract":
        monthly_income = round(random.uniform(4000, 15000), 2)
    else:  # seasonal
        monthly_income = round(random.uniform(2000, 6000), 2)

    # Get a random address ID for the employer - use the updated function
    enterprise_address_id = get_random_business_address_id(conn)

    # Generate phone with Faker
    phone = fake.phone_number()

    # Determine verification status based on application status and is_current
    if application_info and 'status' in application_info:
        app_status = application_info['status']

        if app_status in ["approved", "conditionally approved", "closing", "closed"]:
            # For approved applications, current employment must be verified
            if is_current:
                verification_status = "verified"
                verification_date = application_info.get('submission_date')
                if not verification_date:
                    # If no submission date, set verification date to 1-30 days before today
                    days_ago = random.randint(1, 30)
                    verification_date = today - datetime.timedelta(days=days_ago)
            else:
                # Past employment for approved apps might be verified or not
                verification_status_weights = [0.7, 0.0, 0.0, 0.3]  # Mostly verified or not verified
                verification_status = random.choices(verification_statuses, weights=verification_status_weights, k=1)[0]
                if verification_status == "verified":
                    days_ago = random.randint(1, 60)
                    verification_date = today - datetime.timedelta(days=days_ago)
                else:
                    verification_date = None
        elif app_status in ["submitted", "in review"]:
            # For in-process applications, verification could be pending or completed
            if is_current:
                verification_status_weights = [0.3, 0.7, 0.0, 0.0]  # Mostly pending
                verification_status = random.choices(verification_statuses, weights=verification_status_weights, k=1)[0]
            else:
                verification_status_weights = [0.2, 0.3, 0.0, 0.5]  # Past jobs often not verified
                verification_status = random.choices(verification_statuses, weights=verification_status_weights, k=1)[0]

            if verification_status == "verified":
                days_ago = random.randint(1, 30)
                verification_date = today - datetime.timedelta(days=days_ago)
            else:
                verification_date = None
        elif app_status == "denied":
            # Denied applications might have failed verification
            if is_current and random.random() < 0.3:  # 30% chance current job verification failed
                verification_status = "verification failed"
                days_ago = random.randint(1, 30)
                verification_date = today - datetime.timedelta(days=days_ago)
            else:
                verification_status_weights = [0.2, 0.2, 0.1, 0.5]  # Mix of statuses
                verification_status = random.choices(verification_statuses, weights=verification_status_weights, k=1)[0]
                if verification_status in ["verified", "verification failed"]:
                    days_ago = random.randint(1, 60)
                    verification_date = today - datetime.timedelta(days=days_ago)
                else:
                    verification_date = None
        else:  # draft or other status
            # For draft applications, often no verification yet
            verification_status_weights = [0.1, 0.2, 0.0, 0.7]  # Mostly not verified
            verification_status = random.choices(verification_statuses, weights=verification_status_weights, k=1)[0]
            if verification_status == "verified":
                days_ago = random.randint(1, 30)
                verification_date = today - datetime.timedelta(days=days_ago)
            else:
                verification_date = None
    else:
        # If no application info, use default verification distribution
        verification_status_weights = [0.3, 0.2, 0.1, 0.4]
        verification_status = random.choices(verification_statuses, weights=verification_status_weights, k=1)[0]
        if verification_status == "verified":
            days_ago = random.randint(1, 60)
            verification_date = today - datetime.timedelta(days=days_ago)
        else:
            verification_date = None

    # Create the borrower employment record
    borrower_employment = {
        "employer_name": employer_name,
        "position": position,
        "enterprise_address_id": enterprise_address_id,
        "phone": phone,
        "employment_type": employment_type,
        "start_date": start_date,
        "end_date": end_date,
        "is_current": is_current,
        "years_in_profession": years_in_profession,
        "monthly_income": float(monthly_income),
        "verification_status": verification_status,
        "verification_date": verification_date
    }

    return borrower_employment


def get_borrower_info(borrower_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get borrower information to make employment data reasonable.

    Args:
        borrower_id: The ID of the borrower
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing borrower information or None if borrower_id is None or borrower not found
    """
    if not borrower_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT b.enterprise_party_id, p.name, p.date_of_birth
            FROM mortgage_services.borrowers b
            JOIN enterprise.parties p ON b.enterprise_party_id = p.enterprise_party_id
            WHERE b.mortgage_services_borrower_id = %s
        """, (borrower_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "enterprise_party_id": result[0],
                "name": result[1],
                "date_of_birth": result[2]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching borrower information: {error}")
        return None


def get_application_info_for_borrower(borrower_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get application information for a borrower to make employment data reasonable.

    Args:
        borrower_id: The ID of the borrower
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing application information or None if borrower_id is None or not found
    """
    if not borrower_id:
        return None

    try:
        cursor = conn.cursor()

        # Modified query to use submission_date_time instead of decision_date
        cursor.execute("""
            SELECT a.mortgage_services_application_id, a.status, a.submission_date_time
            FROM mortgage_services.applications a
            JOIN mortgage_services.application_borrowers ab 
              ON a.mortgage_services_application_id = ab.mortgage_services_application_id
            WHERE ab.mortgage_services_borrower_id = %s
            ORDER BY a.creation_date_time DESC
            LIMIT 1
        """, (borrower_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "mortgage_services_application_id": result[0],
                "status": result[1],
                "submission_date": result[2]  # Changed from decision_date to submission_date
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching application information: {error}")
        return None


def get_random_business_address_id(conn) -> Optional[int]:
    """
    Get a random business address ID from the database.

    Args:
        conn: PostgreSQL connection object

    Returns:
        Random business address ID or None if query fails
    """
    try:
        cursor = conn.cursor()

        # Try to get an address for a business building
        cursor.execute("""
            SELECT a.enterprise_address_id 
            FROM enterprise.addresses a
            JOIN enterprise.buildings b ON a.enterprise_address_id = b.enterprise_address_id
            WHERE b.building_type IN ('ADMINISTRATIVE', 'HEADQUARTERS')
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()

        if not result:
            # If no business buildings found, try to get a business relationship address
            cursor.execute("""
                SELECT a.enterprise_address_id 
                FROM enterprise.addresses a
                JOIN enterprise.party_entity_addresses pea ON a.enterprise_address_id = pea.enterprise_address_id
                WHERE pea.relationship_type = 'BUSINESS'
                ORDER BY RANDOM()
                LIMIT 1
            """)

            result = cursor.fetchone()

            if not result:
                # Last resort - get any address
                cursor.execute("""
                    SELECT enterprise_address_id 
                    FROM enterprise.addresses
                    ORDER BY RANDOM()
                    LIMIT 1
                """)
                result = cursor.fetchone()

        cursor.close()

        if result:
            return result[0]
        else:
            # If no addresses found, return None
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching random business address ID: {error}")
        return None


# Keep the original function for backward compatibility, but make it call the new function
def get_random_address_id(conn, is_business: bool = False) -> Optional[int]:
    """
    Get a random address ID from the database, optionally filtering for business addresses.

    This function is maintained for backward compatibility.

    Args:
        conn: PostgreSQL connection object
        is_business: Whether to prefer business addresses

    Returns:
        Random address ID or None if query fails
    """
    if is_business:
        return get_random_business_address_id(conn)

    try:
        cursor = conn.cursor()

        # Get any random address
        cursor.execute("""
            SELECT enterprise_address_id 
            FROM enterprise.addresses
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            # If no addresses found, return None
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching random address ID: {error}")
        return None
