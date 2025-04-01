from faker import Faker
from typing import Dict

import re


def parse_address(full_address: str) -> Dict[str, str]:
    """
    Parse a full address into components, including military addresses and PO Boxes.

    Args:
        full_address: A full address string from Faker

    Returns:
        Dictionary with address components
    """
    # Check for PO Box pattern
    po_box_pattern = r'^(?:P\.?O\.?\s+Box|PO\s+Box|P\.?O\.?\.?\s*#|Post\s+Office\s+Box)\s+(\d+)[,\s]+(.+?)[,\s]+([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$'
    po_box_match = re.match(po_box_pattern, full_address, re.IGNORECASE)

    if po_box_match:
        return {
            'street_address': f"PO Box {po_box_match.group(1)}",
            'city': po_box_match.group(2),
            'state': po_box_match.group(3),
            'post_code': po_box_match.group(4)
        }

    # Check for military address pattern
    military_pattern = r'^(?:USN|USMC|USA|USAF|USCG|USPS|USNV)\s+(.+?)\s+(?:APO|FPO|DPO)\s+(?:AP|AE|AA)\s+(\d{5}(?:-\d{4})?)$'
    military_match = re.match(military_pattern, full_address.strip())

    if military_match:
        return {
            'street_address': military_match.group(1),
            'city': 'FPO' if 'FPO' in full_address else ('APO' if 'APO' in full_address else 'DPO'),
            'state': 'AE' if 'AE' in full_address else ('AP' if 'AP' in full_address else 'AA'),
            'post_code': military_match.group(2)
        }

    # Handle simpler PO Box format that might not have all components
    simple_po_box = r'^(?:P\.?O\.?\s+Box|PO\s+Box|P\.?O\.?\.?\s*#|Post\s+Office\s+Box)\s+(\d+)'
    simple_po_match = re.match(simple_po_box, full_address, re.IGNORECASE)

    if simple_po_match:
        parts = full_address.split(',')
        if len(parts) >= 3:
            city = parts[1].strip()
            state_zip = parts[2].strip().split()
            if len(state_zip) >= 2:
                return {
                    'street_address': parts[0].strip(),
                    'city': city,
                    'state': state_zip[0],
                    'post_code': state_zip[1]
                }
        elif len(parts) == 2:
            city_state_zip = parts[1].strip().split()
            if len(city_state_zip) >= 3:
                return {
                    'street_address': parts[0].strip(),
                    'city': ' '.join(city_state_zip[:-2]),
                    'state': city_state_zip[-2],
                    'post_code': city_state_zip[-1]
                }

    # Use Faker again to ensure consistent parsing
    fake = Faker('en_US')

    # Try to handle standard address formats
    # First pattern: number + street, city, state zip
    standard_pattern = r'^(\d+\s+.+?),\s*(.+?),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$'
    standard_match = re.match(standard_pattern, full_address)

    if standard_match:
        return {
            'street_address': standard_match.group(1),
            'city': standard_match.group(2),
            'state': standard_match.group(3),
            'post_code': standard_match.group(4)
        }

    # Second pattern: street address on line 1, city, state zip on line 2
    multiline_pattern = r'(.+)\n(.+),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$'
    multiline_match = re.match(multiline_pattern, full_address, re.DOTALL)

    if multiline_match:
        return {
            'street_address': multiline_match.group(1).strip(),
            'city': multiline_match.group(2).strip(),
            'state': multiline_match.group(3),
            'post_code': multiline_match.group(4)
        }

    # If structured patterns fail, try to break it down by commas and spaces
    parts = full_address.split(',')

    if len(parts) >= 2:
        street_address = parts[0].strip()
        location_parts = parts[-1].strip().split()

        # Handle case where we have at least state and zip
        if len(location_parts) >= 2 and re.match(r'[A-Z]{2}', location_parts[-2]) and re.match(r'\d{5}(?:-\d{4})?',
                                                                                               location_parts[-1]):
            city = parts[1].strip() if len(parts) > 2 else ' '.join(location_parts[:-2])
            return {
                'street_address': street_address,
                'city': city,
                'state': location_parts[-2],
                'post_code': location_parts[-1]
            }

    # Last resort for addresses without commas
    parts = full_address.split()
    if len(parts) >= 4:
        # Check if the second-to-last part looks like a state code
        if re.match(r'^[A-Z]{2}$', parts[-2]):
            # Check if the last part looks like a zip code
            if re.match(r'^\d{5}(?:-\d{4})?$', parts[-1]):
                return {
                    'street_address': ' '.join(parts[:-3]),
                    'city': parts[-3],
                    'state': parts[-2],
                    'post_code': parts[-1]
                }

    # Use existing content if possible
    if 'FPO' in full_address or 'APO' in full_address or 'DPO' in full_address:
        parts = full_address.split()
        service_branch = parts[0] if parts and re.match(r'^(USN|USMC|USA|USAF|USCG|USPS|USNV)', parts[0]) else ""
        name = ' '.join(parts[1:-3]) if len(parts) > 4 else ""
        box_type = parts[-3] if len(parts) > 3 else ""
        state_code = parts[-2] if len(parts) > 2 else ""
        zip_code = parts[-1] if len(parts) > 1 and re.match(r'\d{5}(?:-\d{4})?', parts[-1]) else ""

        return {
            'street_address': f"{service_branch} {name}".strip(),
            'city': box_type,
            'state': state_code,
            'post_code': zip_code
        }

    # Absolute last resort: generate random address
    # In production, you might want to raise an exception instead
    fake_addr = fake
    return {
        'street_address': fake_addr.street_address(),
        'city': fake_addr.city(),
        'state': fake_addr.state_abbr(),
        'post_code': fake_addr.postcode(),
        'parsing_error': 'Could not parse original address: ' + full_address
    }
