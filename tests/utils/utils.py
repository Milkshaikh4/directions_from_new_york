from datetime import datetime, timedelta
from pytz import UTC

def getFutureDate(weeks=2):
    current_date = datetime.now(UTC)
    future_date = current_date + timedelta(weeks=2)

    return future_date.isoformat()