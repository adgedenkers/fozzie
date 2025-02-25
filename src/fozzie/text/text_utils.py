import re

def sanitize_name(name):
    """
    Formats a name into a standard 'First Middle Last' format.
    
    - Converts uppercase names to title case.
    - Reorders names from 'Last, First Middle' to 'First Middle Last' if necessary.

    Args:
        name (str): The name to sanitize.

    Returns:
        str: A properly formatted name.
    """
    name = name.strip().title()
    
    if "," in name:
        parts = name.split(",", 1)
        last_name = parts[0].strip()
        first_middle = parts[1].strip()
        return f"{first_middle} {last_name}"
    
    return name


def text_to_snake(identifier):
    """
    Sanitizes a string for safe use as a database table or field name.
    
    - Replaces spaces and hyphens with underscores.
    - Removes special characters (except underscores).
    - Ensures the identifier starts with a letter.

    Args:
        identifier (str): The identifier to sanitize.

    Returns:
        str: A sanitized identifier suitable for databases.
    """
    identifier = identifier.strip()
    identifier = re.sub(r"[\s-]", "_", identifier)
    identifier = re.sub(r"[^a-zA-Z0-9_]", "", identifier)
    
    if not identifier[0].isalpha():
        identifier = f"f_{identifier}"
    
    return identifier
