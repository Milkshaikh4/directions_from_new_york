from mongoengine import Document, StringField, ListField, FloatField, DateTimeField, ValidationError
from datetime import datetime, timedelta
from pytz import UTC

class Item(Document):
    name = StringField(required=True, max_length=50)
    postcode = StringField(required=True, regex=r"^\d{5}(-\d{4})?$")
    longitude = FloatField(required=False)
    latitude = FloatField(required=False)
    direction_from_new_york = StringField(choices=["NE", "NW", "SE", "SW"], required=False)
    title = StringField(required=False)
    users = ListField(StringField(max_length=50))
    start_date = DateTimeField(required=False)

    def clean(self):
        """
        Validates the longitude, latitude, and start_date fields.
        """
        # Validate latitude range
        if not (-90 <= self.latitude <= 90):
            raise ValidationError("Invalid latitude. Must be between -90 and 90.")

        # Validate longitude range
        if not (-180 <= self.longitude <= 180):
            raise ValidationError("Invalid longitude. Must be between -180 and 180.")

        if self.start_date:
            # Ensure current_date is UTC-aware
            current_date = datetime.now(UTC)
            one_week_later = current_date + timedelta(weeks=1)

            # Ensure self.start_date is also UTC-aware
            if self.start_date.tzinfo is None:
                raise ValidationError("startDate must be a timezone-aware datetime.")

            # Validation: start_date must be at least 1 week from now
            if self.start_date < one_week_later:
                raise ValidationError("startDate must be at least 1 week from the current date.")