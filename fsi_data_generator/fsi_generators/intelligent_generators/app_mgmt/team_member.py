from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict, Set, Tuple

import logging
import psycopg2
import random
import sys

# Track team member assignments to prevent duplicates
team_member_assignments: Set[Tuple[str, int]] = set()
logger = logging.getLogger(__name__)


def generate_random_team_member(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt.team_members record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (app_mgmt_team_id, enterprise_associate_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random team member record
        (without ID fields)
    """
    # Extract required ID fields
    app_mgmt_team_id = id_fields.get("app_mgmt_team_id")
    enterprise_associate_id = id_fields.get("enterprise_associate_id")

    if not app_mgmt_team_id or not enterprise_associate_id:
        raise ValueError("Both app_mgmt_team_id and enterprise_associate_id are required")

    # Check for duplicate team member assignments
    team_member_pair = (str(app_mgmt_team_id), int(enterprise_associate_id))
    if team_member_pair in team_member_assignments:
        # Skip this record - this associate is already a member of this team
        raise SkipRowGenerationError("Duplicate team member assignment")

    # Track this assignment
    team_member_assignments.add(team_member_pair)

    # Try to fetch associate information if possible
    associate_info = _fetch_associate_info(enterprise_associate_id, dg)
    team_info = _fetch_team_info(app_mgmt_team_id, dg)

    # Generate a function (role) for this team member
    function = _generate_team_function(associate_info, team_info)

    # Construct the team member record
    team_member = {
        "function": function
    }

    return team_member


def _fetch_associate_info(associate_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch associate information from the database

    Args:
        associate_id: ID of the associate
        dg: DataGenerator instance

    Returns:
        Dictionary with associate information, or empty dict if not found
    """
    if not associate_id:
        return {}

    try:
        query = """
        SELECT first_name, last_name, email, job_title, enterprise_department_id
        FROM enterprise.associates
        WHERE enterprise_associate_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (associate_id,))
            result = cursor.fetchone()

        return result

    except psycopg2.ProgrammingError as e:
        # Log the critical error
        logger.critical(f"Programming error detected in the SQL query: {e}")

        # Exit the program immediately with a non-zero status code
        sys.exit(1)


def _fetch_team_info(team_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch team information from the database

    Args:
        team_id: ID of the team
        dg: DataGenerator instance

    Returns:
        Dictionary with team information, or empty dict if not found
    """
    if not team_id:
        return {}

    try:
        query = """
        SELECT team_name, description, team_lead_id
        FROM app_mgmt.teams
        WHERE app_mgmt_team_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (team_id,))
            result = cursor.fetchone()

        return result

    except psycopg2.ProgrammingError as e:
        # Log the critical error
        logger.critical(f"Programming error detected in the SQL query: {e}")

        # Exit the program immediately with a non-zero status code
        sys.exit(1)


def _generate_team_function(associate_info: Dict[str, Any], team_info: Dict[str, Any]) -> str:
    """
    Generate a reasonable function (role) for the team member based on available information

    Args:
        associate_info: Dictionary with associate information
        team_info: Dictionary with team information

    Returns:
        A role description
    """
    # Check if this associate is the team lead
    if team_info and 'team_lead_id' in team_info and associate_info:
        team_lead_id = team_info.get('team_lead_id')
        if team_lead_id and team_lead_id == associate_info.get('enterprise_associate_id'):
            return "Team Lead"

    # Use job title if available
    if associate_info and 'job_title' in associate_info and associate_info['job_title']:
        job_title = associate_info['job_title'].lower()

        # Create a function based on job title keywords
        if 'developer' in job_title or 'engineer' in job_title:
            return random.choice([
                "Developer",
                "Software Engineer",
                "Backend Developer",
                "Frontend Developer",
                "Full Stack Developer",
                "DevOps Engineer"
            ])

        elif 'architect' in job_title:
            return "Software Architect"

        elif 'data' in job_title or 'analytics' in job_title:
            return random.choice([
                "Data Engineer",
                "Data Analyst",
                "Data Scientist",
                "Business Intelligence"
            ])

        elif 'qa' in job_title or 'test' in job_title or 'quality' in job_title:
            return random.choice([
                "QA Engineer",
                "Tester",
                "Quality Assurance"
            ])

        elif 'security' in job_title:
            return random.choice([
                "Security Engineer",
                "Security Analyst",
                "Security Architect"
            ])

        elif 'product' in job_title or 'manager' in job_title:
            return random.choice([
                "Product Owner",
                "Product Manager",
                "Project Manager"
            ])

        elif 'ux' in job_title or 'ui' in job_title or 'design' in job_title:
            return random.choice([
                "UX Designer",
                "UI Designer",
                "User Experience"
            ])

        else:
            # Return a slightly modified version of the job title
            return associate_info['job_title']

    # Generic team roles if no job title is available
    return random.choice([
        "Developer",
        "Team Member",
        "Analyst",
        "Specialist",
        "Coordinator",
        "Consultant",
        "Subject Matter Expert",
        "Support Staff",
        "Technical Lead",
        "Documentation Specialist",
        "Quality Assurance"
    ])
