from data_generator import DataGenerator
from faker import Faker
from typing import Any, Dict

import hashlib
import logging
import random

# Set up logger
logger = logging.getLogger(__name__)


def generate_random_file_threat(id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.file_threats record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_file_threat_hash)
        _dg: DataGenerator instance

    Returns:
        Dict containing a random file threat record
    """
    fake = Faker()

    # Use predefined hash if provided, otherwise generate one
    file_hash = id_fields.get('security_file_threat_hash')
    if not file_hash:
        # Generate a random SHA-256 hash (64 characters)
        file_content = fake.text().encode('utf-8')
        file_hash = hashlib.sha256(file_content).hexdigest()

    # Define threat levels with weighted probabilities
    # More common to have low threats than high ones
    threat_levels = [
        ("HIGH", 10),  # Least common: high severity threats
        ("MEDIUM", 25),  # Medium frequency: medium severity threats
        ("LOW", 40),  # Common: low severity threats
        ("INFORMATIONAL", 20),  # Less common: just informational notices
        ("UNKNOWN", 5)  # Rare: unknown threat levels
    ]

    # Choose threat level based on weights
    threat_level = random.choices(
        [level[0] for level in threat_levels],
        weights=[level[1] for level in threat_levels],
        k=1
    )[0]

    # Generate a realistic threat description based on the threat level
    threat_descriptions = {
        "HIGH": [
            "Advanced persistent threat (APT) code with data exfiltration capabilities",
            "Ransomware with strong encryption and network propagation functionality",
            "Zero-day exploit targeting critical system vulnerability",
            "Rootkit with kernel-level access and anti-detection mechanisms",
            "Banking trojan with keylogging and screen capture capabilities",
            "Remote access trojan (RAT) with command-and-control functionality",
            "Polymorphic malware evading signature-based detection",
            "Supply chain attack vector targeting enterprise systems",
            "Credential harvester targeting multiple authentication systems",
            "Critical vulnerability exploit for privilege escalation"
        ],
        "MEDIUM": [
            "Spyware with limited data collection capabilities",
            "Adware with aggressive popup behavior",
            "Potentially unwanted program with system modification features",
            "Outdated software with known security vulnerabilities",
            "Browser extension with excessive permission requirements",
            "Cryptocurrency mining script with moderate system resource usage",
            "Network scanner with enumeration capabilities",
            "Unauthorized remote access utility",
            "Macro-enabled document with suspicious code execution",
            "Known vulnerability exploit with limited impact"
        ],
        "LOW": [
            "Tracking cookie with privacy implications",
            "Legacy software with minor security weaknesses",
            "Outdated security certificate",
            "Unsigned executable from non-verified publisher",
            "Software with outdated dependencies",
            "Weak encryption implementation",
            "Non-critical configuration issue",
            "Minor information disclosure vulnerability",
            "System utility with elevated privileges",
            "Third-party component with patch available"
        ],
        "INFORMATIONAL": [
            "Diagnostic tool with administrative capabilities",
            "Developer tool with system access features",
            "Network monitoring utility",
            "Security scanning software",
            "Penetration testing tool",
            "Administrative script with elevated privileges",
            "Remote management utility",
            "System backup software",
            "Virtualization or containerization tool",
            "Password storage application"
        ],
        "UNKNOWN": [
            "Unclassified binary with unusual behavior patterns",
            "Recently compiled executable with limited detection history",
            "File with suspicious entropy characteristics pending analysis",
            "Obfuscated code requiring manual review",
            "Previously unseen binary pattern requiring further analysis",
            "Suspicious file reported by user pending verification",
            "File with conflicting scan results from multiple engines",
            "Potentially malicious file with insufficient detection data",
            "New variant with behavior similarities to known threats",
            "Anomalous file requiring dynamic analysis"
        ]
    }

    threat_description = random.choice(threat_descriptions[threat_level])

    # For medium and high threats, add more details to the description
    if threat_level in ["HIGH", "MEDIUM"]:
        detection_dates = [
            f"Initially detected on {fake.date_this_year().strftime('%Y-%m-%d')}",
            f"First observed in the wild {fake.date_this_year().strftime('%B %Y')}",
            f"Identified by security researchers in {fake.date_this_year().strftime('%B %Y')}",
            f"Active in targeted campaigns since {fake.date_this_year().strftime('%Q%Y')}"
        ]

        impact_details = [
            "May lead to complete system compromise",
            "Can result in unauthorized data access",
            "Enables persistent unauthorized access",
            "Potential for lateral movement within network",
            "May bypass standard security controls",
            "Capable of evading traditional antivirus detection",
            "Known to disable security software"
        ]

        mitigation_advice = [
            "Immediate isolation and system rebuild recommended",
            "Requires full system scan and credential rotation",
            "Update all security patches and implement application whitelisting",
            "Network traffic analysis recommended to identify command and control channels",
            "Implement enhanced monitoring and endpoint protection",
            "Block associated network indicators at perimeter"
        ]

        additional_details = []
        if random.random() < 0.8:  # 80% chance to add detection date
            additional_details.append(random.choice(detection_dates))

        if threat_level == "HIGH":  # Always add impact details for HIGH threats
            additional_details.append(random.choice(impact_details))
        elif random.random() < 0.5:  # 50% chance for MEDIUM threats
            additional_details.append(random.choice(impact_details))

        if threat_level == "HIGH":  # Always add mitigation advice for HIGH threats
            additional_details.append(random.choice(mitigation_advice))
        elif random.random() < 0.3:  # 30% chance for MEDIUM threats
            additional_details.append(random.choice(mitigation_advice))

        # Add the additional details to the description
        if additional_details:
            threat_description += ". " + " ".join(additional_details)

    # Occasionally add MITRE ATT&CK references for higher threats
    if threat_level in ["HIGH", "MEDIUM"] and random.random() < 0.6:
        mitre_techniques = [
            "T1566 (Phishing)",
            "T1486 (Data Encrypted for Impact)",
            "T1059 (Command and Scripting Interpreter)",
            "T1078 (Valid Accounts)",
            "T1053 (Scheduled Task/Job)",
            "T1027 (Obfuscated Files or Information)",
            "T1218 (System Binary Proxy Execution)",
            "T1055 (Process Injection)",
            "T1569 (System Services)",
            "T1543 (Create or Modify System Process)"
        ]
        threat_description += f". MITRE ATT&CK reference: {random.choice(mitre_techniques)}"

    # Construct the file threat record
    file_threat = {
        "security_file_threat_hash": file_hash,  # Include the hash as part of the return value
        "threat_level": threat_level,
        "threat_description": threat_description
    }

    return file_threat


def _generate_sha256_hash() -> str:
    """
    Generate a random SHA-256 hash string.

    Returns:
        String containing a valid SHA-256 hash
    """
    random_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=64))
    hash_object = hashlib.sha256(random_data.encode())
    return hash_object.hexdigest()
