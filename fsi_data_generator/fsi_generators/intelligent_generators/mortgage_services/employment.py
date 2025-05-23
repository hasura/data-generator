from .enums import EmploymentType, VerificationStatus
from dateutil.relativedelta import relativedelta
from faker import Faker
from typing import Any, Dict, Optional

import datetime
import logging
import psycopg2
import random

# Initialize Faker
fake = Faker()
logger = logging.getLogger(__name__)


def generate_random_borrower_employment(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services borrower employment record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_borrower_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated borrower employment data (without ID fields)
    """
    # Get borrower information and application status to make employment data reasonable
    conn = dg.conn
    borrower_info = _get_borrower_info(id_fields.get("mortgage_services_borrower_id"), conn)
    application_info = _get_application_info_for_borrower(id_fields.get("mortgage_services_borrower_id"), conn)

    # Determine if current employment based on borrower info
    is_current = True  # Default to current employment
    if borrower_info and random.random() < 0.2:  # 20% chance of past employment
        is_current = False

    # Select employment type
    employment_type = EmploymentType.get_random()

    # Generate employer name using Faker
    employer_name = fake.company()

    # Generate position based on employment type
    positions_by_type = {
        EmploymentType.FULL_TIME: [
            "Software Engineer", "Project Manager", "Sales Representative", "Accountant",
            "Marketing Specialist", "Human Resources Manager", "Operations Director",
            "Financial Analyst", "Customer Service Representative", "Administrative Assistant",
            "Product Manager", "Business Analyst", "Systems Administrator", "Research Scientist",
            "Data Scientist", "Quality Assurance Analyst", "Executive Assistant", "Account Manager",
            "Supply Chain Manager", "Legal Counsel", "Corporate Trainer", "Network Engineer",
            "Compliance Officer", "UX Designer", "Brand Manager", "IT Support Specialist",
            "Web Developer", "Benefits Administrator", "Public Relations Specialist", "Sales Engineer"
        ],
        EmploymentType.PART_TIME: [
            "Sales Associate", "Office Assistant", "Customer Service Rep", "Cashier",
            "Delivery Driver", "Warehouse Associate", "Retail Associate", "Server",
            "Tutor", "Security Guard", "Barista", "Receptionist", "Bank Teller", "Data Entry Clerk",
            "Library Assistant", "Dental Assistant", "Medical Receptionist", "Tour Guide",
            "Research Assistant", "Brand Ambassador", "Caregiver", "Fitness Instructor",
            "Teaching Assistant", "Pharmacy Technician", "Event Staff", "Restaurant Host",
            "Retail Merchandiser", "Social Media Moderator", "Call Center Representative", "Museum Guide"
        ],
        EmploymentType.SELF_EMPLOYED: [
            "Independent Consultant", "Freelance Designer", "Business Owner", "Contractor",
            "Realtor", "Attorney", "Photographer", "Writer", "Therapist", "Handyman",
            "Personal Trainer", "Life Coach", "Mobile App Developer", "Tax Preparer",
            "Interior Designer", "Event Planner", "Videographer", "Social Media Manager",
            "Private Tutor", "Landscaper", "Home Inspector", "Translator",
            "Private Chef", "Career Coach", "Music Teacher", "Wedding Planner",
            "E-commerce Store Owner", "Notary Public", "Yoga Instructor", "Web Designer"
        ],
        EmploymentType.CONTRACTOR: [
            "IT Consultant", "Project Coordinator", "Content Writer", "Web Developer",
            "Graphic Designer", "Technical Writer", "Marketing Consultant", "Data Analyst",
            "Software Developer", "UX/UI Designer", "Systems Architect", "SEO Specialist",
            "Quality Assurance Tester", "Cybersecurity Analyst", "Network Consultant", "DevOps Engineer",
            "Business Intelligence Analyst", "Database Administrator", "Technical Recruiter", "Legal Consultant",
            "Engineering Consultant", "Financial Auditor", "Healthcare Consultant", "Training Consultant",
            "Video Editor", "Virtual Assistant", "Social Media Strategist", "Product Designer",
            "Market Research Analyst", "Scientific Researcher", "Curriculum Developer", "Interim Manager"
        ],
        EmploymentType.SEASONAL: [
            "Tax Preparer", "Retail Sales Associate", "Delivery Driver", "Resort Staff",
            "Landscaper", "Agricultural Worker", "Camp Counselor", "Tour Guide",
            "Election Worker", "Snow Removal Technician", "Ski Instructor", "Holiday Gift Wrapper",
            "Inventory Specialist", "Festival Staff", "Halloween Store Associate", "Theme Park Attendant",
            "Fishing Guide", "Harvest Worker", "Holiday Decorator", "Lifeguard",
            "Summer Camp Director", "Cruise Ship Staff", "National Park Ranger", "Beach Attendant",
            "Event Security", "Christmas Tree Lot Worker", "Sports Venue Staff", "Tax Season Accountant",
            "Seasonal Baker", "Pumpkin Patch Worker", "Flower Shop Assistant", "Hotel Housekeeper"
        ],
        EmploymentType.COMMISSION: [
            "Sales Representative", "Real Estate Agent", "Insurance Agent", "Financial Advisor",
            "Mortgage Broker", "Car Salesperson", "Retail Sales Associate", "Travel Agent",
            "Account Executive", "Business Development Representative", "Recruiter", "Art Dealer",
            "Advertising Sales Representative", "Luxury Goods Consultant", "Stockbroker", "Investment Advisor",
            "Direct Sales Consultant", "Pharmaceutical Sales Rep", "Jewelry Sales Associate", "Territory Manager",
            "Electronics Sales Associate", "Solar Energy Consultant", "Home Improvement Sales", "Franchise Sales",
            "Membership Sales Specialist", "Timeshare Sales Executive", "Furniture Sales Associate",
            "Medical Device Sales",
            "Software Sales Representative", "Telecom Sales Representative", "B2B Sales Executive", "Yacht Broker"
        ],
        EmploymentType.RETIRED: [
            "Retired Teacher", "Retired Executive", "Retired Military Officer", "Retired Physician",
            "Retired Civil Servant", "Retired Engineer", "Retired Business Owner", "Retired Professor",
            "Retired Nurse", "Retired Police Officer", "Retired Firefighter", "Retired Accountant",
            "Retired Attorney", "Retired Dentist", "Retired Pilot", "Retired Judge",
            "Retired Architect", "Retired Psychologist", "Retired Postal Worker", "Retired Electrician",
            "Retired Banker", "Retired Sales Manager", "Retired Principal", "Retired Government Official",
            "Retired Chef", "Retired Pharmacist", "Retired Social Worker", "Retired Journalist",
            "Retired Administrator", "Retired Construction Manager", "Retired Financial Planner",
            "Retired IT Professional"
        ],
        EmploymentType.MILITARY: [
            "Army Officer", "Navy Officer", "Air Force Officer", "Marine Corps Officer",
            "Army Enlisted", "Navy Enlisted", "Air Force Enlisted", "Marine Corps Enlisted",
            "Military Specialist", "Military Technician", "Military Instructor", "Military Logistics",
            "Military Intelligence", "Combat Medic", "Military Police", "Aviation Mechanic",
            "Communications Specialist", "Cyber Operations Specialist", "Special Forces", "Combat Engineer",
            "Military Recruiter", "Tank Crew Member", "Missile Defense Crew", "Naval Operations Specialist",
            "Air Traffic Controller", "Aircraft Crew", "Tactical Operations Officer", "Military Research Scientist",
            "Weapons Specialist", "Field Artillery", "Infantry", "Explosive Ordnance Disposal"
        ],
        EmploymentType.UNEMPLOYED: [
            "Previously Employed", "Job Seeker", "Recent Graduate", "Career Changer",
            "Temporarily Unemployed", "Returning to Workforce", "Between Jobs", "Recent Retiree",
            "Recently Relocated", "Recent Medical Leave", "Full-time Student", "Former Business Owner",
            "Former Military", "Former Contractor", "Recently Laid Off", "Former Self-Employed",
            "Former Seasonal Worker", "Recent Caregiver", "Former Commission Worker", "Newly Graduated",
            "Former Part-time Worker", "Recent Travel Break", "Former Freelancer", "After Sabbatical",
            "Job Transition", "Following Relocation", "After Company Closure", "Former Startup Founder",
            "Career Break", "Marketplace Transition", "Industry Change", "Skill Development Phase"
        ],
        EmploymentType.OTHER: [
            "Gig Worker", "Intern", "Volunteer", "Board Member", "Advisor",
            "Entrepreneur", "Student Worker", "Apprentice", "Fellow", "Grant Recipient",
            "Research Assistant", "Graduate Assistant", "Visiting Professor", "Scholar-in-Residence",
            "Artist-in-Residence",
            "Elected Official", "Peace Corps Volunteer", "AmeriCorps Member", "Exchange Program Participant", "Clergy",
            "Diplomatic Staff", "Foreign Service Officer", "Non-profit Director", "Cooperative Member",
            "Professional Athlete",
            "Performance Artist", "Author", "Composer", "Inventor", "Professional Speaker",
            "Venture Capitalist", "Angel Investor", "Disability Pension Recipient", "Researcher", "Sabbatical"
        ]
    }

    position = random.choice(positions_by_type.get(employment_type, positions_by_type[EmploymentType.FULL_TIME]))

    # Generate reasonable employment dates
    today = datetime.date.today()

    # Start date - typically 0-20 years ago
    years_ago = random.randint(0, 20)
    months_ago = random.randint(0, 11)
    start_date = today - relativedelta(years=years_ago, months=months_ago)

    # End date - only for past employment
    end_date = None
    if not is_current:
        # Calculate minimum duration of employment (6 months)
        min_months = 6

        # Calculate maximum duration based on start date
        max_months = (today.year - start_date.year) * 12 + (today.month - start_date.month) - 1

        # Ensure we have a valid range
        if max_months < min_months:
            # Calculate a valid start_date using relativedelta
            start_date = today - relativedelta(months=min_months)

            # Add a buffer of at least 2 months to max_months for randomization
            max_months = min_months + 2
            
        # Randomly pick months to add
        months_after_start = random.randint(min_months, max_months)

        # Add months safely using relativedelta
        end_date = start_date + relativedelta(months=months_after_start)

    # Generate years in profession (maybe longer than current job)
    if employment_type == EmploymentType.SELF_EMPLOYED:
        # Self-employed people often have many years in profession
        years_in_profession = random.randint(years_ago, min(years_ago + 15, 40))
    else:
        # Other employment types might be close to current job duration
        years_in_profession = random.randint(years_ago, min(years_ago + 5, 30))

    # Generate monthly income based on employment type
    if employment_type == EmploymentType.FULL_TIME:
        monthly_income = round(random.uniform(3000, 12000), 2)
    elif employment_type == EmploymentType.PART_TIME:
        monthly_income = round(random.uniform(1000, 3000), 2)
    elif employment_type == EmploymentType.SELF_EMPLOYED:
        monthly_income = round(random.uniform(4000, 18000), 2)
    elif employment_type == EmploymentType.CONTRACTOR:
        monthly_income = round(random.uniform(4000, 15000), 2)
    elif employment_type == EmploymentType.SEASONAL:
        monthly_income = round(random.uniform(2000, 6000), 2)
    elif employment_type == EmploymentType.COMMISSION:
        monthly_income = round(random.uniform(5000, 20000), 2)
    elif employment_type == EmploymentType.RETIRED:
        monthly_income = round(random.uniform(2000, 8000), 2)
    elif employment_type == EmploymentType.MILITARY:
        monthly_income = round(random.uniform(3500, 10000), 2)
    elif employment_type == EmploymentType.UNEMPLOYED:
        monthly_income = round(random.uniform(0, 1000), 2)
    else:  # OTHER
        monthly_income = round(random.uniform(2000, 5000), 2)

    # Get a random address ID for the employer - use the updated function
    enterprise_address_id = _get_random_business_address_id(conn)

    # Generate phone with Faker
    phone = fake.phone_number()

    # Determine verification status based on application status and is_current
    if application_info and 'status' in application_info:
        app_status = application_info['status']

        if app_status in ["approved", "conditionally approved", "closing", "closed"]:
            # For approved applications, current employment must be verified
            if is_current:
                verification_status = VerificationStatus.VERIFIED
                verification_date = application_info.get('submission_date')
                if not verification_date:
                    # If no submission date, set verification date to 1-30 days before today
                    days_ago = random.randint(1, 30)
                    verification_date = today - datetime.timedelta(days=days_ago)
            else:
                # Past employment for approved apps might be verified or not
                verification_status = VerificationStatus.get_random([0.7, 0.0, 0.0, 0.3, 0.0, 0.0])
                if verification_status == VerificationStatus.VERIFIED:
                    days_ago = random.randint(1, 60)
                    verification_date = today - datetime.timedelta(days=days_ago)
                else:
                    verification_date = None
        elif app_status in ["submitted", "in review"]:
            # For in-process applications, verification could be pending or completed
            if is_current:
                verification_status = VerificationStatus.get_random([0.3, 0.7, 0.0, 0.0, 0.0, 0.0])
            else:
                verification_status = VerificationStatus.get_random([0.2, 0.3, 0.0, 0., 0.0, 0.0])

            if verification_status == VerificationStatus.VERIFIED:
                days_ago = random.randint(1, 30)
                verification_date = today - datetime.timedelta(days=days_ago)
            else:
                verification_date = None
        elif app_status == "denied":
            # Denied applications might have failed verification
            if is_current and random.random() < 0.3:  # 30% chance current job verification failed
                verification_status = VerificationStatus.FAILED
                days_ago = random.randint(1, 30)
                verification_date = today - datetime.timedelta(days=days_ago)
            else:
                verification_status = VerificationStatus.get_random([0.2, 0.2, 0.1, 0.5, 0.0, 0.0])
                if verification_status in [VerificationStatus.VERIFIED, VerificationStatus.FAILED]:
                    days_ago = random.randint(1, 60)
                    verification_date = today - datetime.timedelta(days=days_ago)
                else:
                    verification_date = None
        else:  # draft or other status
            # For draft applications, often no verification yet
            verification_status = VerificationStatus.get_random([0.1, 0.2, 0.0, 0.7, 0.0, 0.0])
            if verification_status == VerificationStatus.VERIFIED:
                days_ago = random.randint(1, 30)
                verification_date = today - datetime.timedelta(days=days_ago)
            else:
                verification_date = None
    else:
        # If no application info, use default verification distribution
        verification_status = VerificationStatus.get_random([0.3, 0.2, 0.1, 0.4, 0.0, 0.0])
        if verification_status == VerificationStatus.VERIFIED:
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
        "employment_type": employment_type.value,  # Use .value to get the string value
        "start_date": start_date,
        "end_date": end_date,
        "is_current": is_current,
        "years_in_profession": years_in_profession,
        "monthly_income": float(monthly_income),
        "verification_status": verification_status.value,  # Use .value to get the string value
        "verification_date": verification_date
    }

    return borrower_employment


def _get_borrower_info(borrower_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
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

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching borrower information: {error}")
        return None


def _get_application_info_for_borrower(borrower_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
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
        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching application information: {error}")
        return None


def _get_random_business_address_id(conn) -> Optional[int]:
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

        return result.get('enterprise_address_id')


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
        return _get_random_business_address_id(conn)

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
