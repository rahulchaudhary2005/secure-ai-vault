from email_validator import (
    validate_email,
    EmailNotValidError
)


class EmailValidator:

    @staticmethod
    def validate(
        email: str
    ):

        try:

            valid = validate_email(
                email,
                check_deliverability=False
            )

            return valid.email

        except EmailNotValidError:

            return None