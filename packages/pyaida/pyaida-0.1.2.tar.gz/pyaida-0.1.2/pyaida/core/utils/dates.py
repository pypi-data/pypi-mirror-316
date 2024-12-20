from datetime import datetime, timezone
from typing import Optional


def now():
    return datetime.now(tz=None)


def utc_now():
    return datetime.now(tz=timezone.utc)


def coerce_to_date(date_str: str) -> Optional[datetime.date]:
    """
    Coerce a string into a date object, supporting common date formats.

    Supported formats:
        - YYYY-MM-DD
        - DD/MM/YYYY
        - MM/DD/YYYY
        - DD-MM-YYYY
        - YYYY/MM/DD
        - Month DD, YYYY
        - ISO 8601 format

    Args:
        date_str (str): Input date string.

    Returns:
        Optional[datetime.date]: Parsed date object or None if unsuccessful.

    Raises:
        ValueError: If no matching format is found.
    """
    if not date_str or not isinstance(date_str, str):
        date_str = str(date_str)

    # List of common date formats to attempt
    date_formats = [
        "%Y-%m-%d",  # ISO Date: 2024-09-20
        "%d/%m/%Y",  # European Date: 20/09/2024
        "%m/%d/%Y",  # US Date: 09/20/2024
        "%d-%m-%Y",  # Hyphenated European: 20-09-2024
        "%Y/%m/%d",  # Slashed ISO: 2024/09/20
        "%B %d, %Y",  # Month Name: September 20, 2024
        "%b %d, %Y",  # Short Month Name: Sep 20, 2024
        "%Y-%m-%dT%H:%M:%S",  # ISO 8601 with time: 2024-09-20T12:30:45
    ]

    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.date()  # Return only the date part
        except ValueError:
            continue  # Try the next format

    # If all formats fail
    raise ValueError(f"Unable to parse date string: '{date_str}'")
