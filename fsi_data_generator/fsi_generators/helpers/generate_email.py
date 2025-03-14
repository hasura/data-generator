def generate_email(row_values, _table, _column):
    """Generate email based on first and last name"""
    if 'first_name' in row_values and 'last_name' in row_values:
        first = row_values['first_name'].lower()
        last = row_values['last_name'].lower()
        return f"{first}.{last}@example.com"
    elif 'username' in row_values:
        return f"{row_values['username']}@example.com"
    elif 'name' in row_values:
        return f"{row_values['name']}@example.com"
    return "unknown@example.com"
