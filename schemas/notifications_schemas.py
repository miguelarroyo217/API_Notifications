from datetime import datetime
from marshmallow import fields, validates, ValidationError

class NotifSchema:
    due = fields.String(required=True)

    @validates('due')
    def validate_due(self, value):
        """
        Validates the due date format.

        Args:
            value: The due date string.

        Raises:
            ValidationError: If the due date does not have the format "YYYY-MM-DD HH:mm:ss".
        """
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValidationError('Due date must have the format "YYYY-MM-DD HH:mm:ss".')

