from datetime import datetime
import pytz
from fastapi import HTTPException

def validate_start_date(start_date_str: str) -> datetime:
    """
    Validates and converts `startDate` into a timezone-aware datetime object.

    :param start_date_str: The input startDate string from the request.
    :return: A valid timezone-aware datetime object.
    :raises HTTPException: If the date is not in the correct format.
    """
    try:
        parsed_date = datetime.fromisoformat(start_date_str)

        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=pytz.UTC)

        return parsed_date

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid 'startDate'. Provide a valid ISO 8601 string.")
