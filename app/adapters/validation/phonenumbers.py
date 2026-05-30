import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat

from app.application.ports import PhoneNumberValidator
from app.domain.exceptions import InvalidHospitalDataError


class PhonenumbersPhoneNumberValidator(PhoneNumberValidator):
    def normalize(self, phone_number: str) -> str:
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
        except NumberParseException as exc:
            raise InvalidHospitalDataError(
                "Hospital phone must be a valid international phone number"
            ) from exc

        if not phonenumbers.is_valid_number(parsed_number):
            raise InvalidHospitalDataError(
                "Hospital phone must be a valid international phone number"
            )

        return phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
