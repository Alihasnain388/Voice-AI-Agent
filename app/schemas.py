from datetime import date, datetime
from typing import Optional, Generic, TypeVar
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


VALID_SEXES = {
    "Male",
    "Female",
    "Other",
    "Decline to Answer",
}


US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI",
    "DC",
}


def validate_phone(value: str) -> str:
    """
    Normalize and validate a US phone number.

    Accepts:
    - 1234567890
    - (123) 456-7890
    - 123-456-7890
    - +1 123 456 7890
    """

    digits = "".join(char for char in value if char.isdigit())

    # Remove US country code if provided
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) != 10:
        raise ValueError(
            "Phone number must be a valid US 10-digit number."
        )

    return digits


class PatientBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    date_of_birth: date

    sex: str

    phone_number: str

    email: Optional[EmailStr] = None

    address_line_1: str = Field(
        ...,
        min_length=1
    )

    address_line_2: Optional[str] = None

    city: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    state: str

    zip_code: str

    insurance_provider: Optional[str] = None

    insurance_member_id: Optional[str] = None

    preferred_language: Optional[str] = "English"

    emergency_contact_name: Optional[str] = None

    emergency_contact_phone: Optional[str] = None

    # --------------------------------------------------
    # NAME VALIDATION
    # --------------------------------------------------

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty.")

        if not all(
            char.isalpha() or char in "-' "
            for char in value
        ):
            raise ValueError(
                "Name can only contain letters, spaces, "
                "hyphens, and apostrophes."
            )

        return value

    # --------------------------------------------------
    # DATE OF BIRTH VALIDATION
    # --------------------------------------------------

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        if value > date.today():
            raise ValueError(
                "Date of birth cannot be in the future."
            )

        return value

    # --------------------------------------------------
    # SEX VALIDATION
    # --------------------------------------------------

    @field_validator("sex")
    @classmethod
    def validate_sex(cls, value: str) -> str:
        value = value.strip()

        if value not in VALID_SEXES:
            raise ValueError(
                "Sex must be Male, Female, Other, "
                "or Decline to Answer."
            )

        return value

    # --------------------------------------------------
    # PHONE VALIDATION
    # --------------------------------------------------

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        return validate_phone(value)

    # --------------------------------------------------
    # EMAIL VALIDATION
    # IMPORTANT:
    # Vapi may send "" for an optional field.
    # Convert "" → None before EmailStr validation.
    # --------------------------------------------------

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_to_none(cls, value):
        if value == "":
            return None

        return value

    # --------------------------------------------------
    # EMERGENCY PHONE VALIDATION
    # IMPORTANT:
    # Convert "" → None.
    # --------------------------------------------------

    @field_validator(
        "emergency_contact_phone",
        mode="before"
    )
    @classmethod
    def validate_emergency_phone(
        cls,
        value: Optional[str]
    ) -> Optional[str]:

        if value == "":
            return None

        if value is None:
            return None

        return validate_phone(value)

    # --------------------------------------------------
    # STATE VALIDATION
    # --------------------------------------------------

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        value = value.upper().strip()

        if value not in US_STATES:
            raise ValueError(
                "Invalid US state abbreviation."
            )

        return value

    # --------------------------------------------------
    # ZIP CODE VALIDATION
    # --------------------------------------------------

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, value: str) -> str:
        value = value.strip()

        valid_5_digit = (
            len(value) == 5
            and value.isdigit()
        )

        valid_zip_plus_4 = (
            len(value) == 10
            and value[5] == "-"
            and value[:5].isdigit()
            and value[6:].isdigit()
        )

        if not (valid_5_digit or valid_zip_plus_4):
            raise ValueError(
                "ZIP code must be 5 digits or ZIP+4 format."
            )

        return value


# ======================================================
# CREATE PATIENT
# ======================================================

class PatientCreate(PatientBase):
    pass


# ======================================================
# UPDATE PATIENT
# ======================================================

class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50
    )

    last_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50
    )

    date_of_birth: Optional[date] = None

    sex: Optional[str] = None

    phone_number: Optional[str] = None

    email: Optional[EmailStr] = None

    address_line_1: Optional[str] = None

    address_line_2: Optional[str] = None

    city: Optional[str] = None

    state: Optional[str] = None

    zip_code: Optional[str] = None

    insurance_provider: Optional[str] = None

    insurance_member_id: Optional[str] = None

    preferred_language: Optional[str] = None

    emergency_contact_name: Optional[str] = None

    emergency_contact_phone: Optional[str] = None

    # --------------------------------------------------
    # NAME VALIDATION
    # --------------------------------------------------

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value):
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Name cannot be empty."
            )

        if not all(
            char.isalpha() or char in "-' "
            for char in value
        ):
            raise ValueError(
                "Name can only contain letters, spaces, "
                "hyphens, and apostrophes."
            )

        return value

    # --------------------------------------------------
    # DATE OF BIRTH
    # --------------------------------------------------

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value):
        if value is not None and value > date.today():
            raise ValueError(
                "Date of birth cannot be in the future."
            )

        return value

    # --------------------------------------------------
    # SEX
    # --------------------------------------------------

    @field_validator("sex")
    @classmethod
    def validate_sex(cls, value):
        if value is None:
            return None

        value = value.strip()

        if value not in VALID_SEXES:
            raise ValueError(
                "Sex must be Male, Female, Other, "
                "or Decline to Answer."
            )

        return value

    # --------------------------------------------------
    # PHONE NUMBERS
    # --------------------------------------------------

    @field_validator(
        "phone_number",
        "emergency_contact_phone",
        mode="before"
    )
    @classmethod
    def validate_phones(cls, value):

        if value is None:
            return None

        if value == "":
            return None

        return validate_phone(value)

    # --------------------------------------------------
    # EMAIL
    # --------------------------------------------------

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_to_none(cls, value):

        if value == "":
            return None

        return value

    # --------------------------------------------------
    # STATE
    # --------------------------------------------------

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):

        if value is None:
            return None

        value = value.upper().strip()

        if value not in US_STATES:
            raise ValueError(
                "Invalid US state abbreviation."
            )

        return value

    # --------------------------------------------------
    # ZIP CODE
    # --------------------------------------------------

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, value):

        if value is None:
            return None

        value = value.strip()

        valid_5_digit = (
            len(value) == 5
            and value.isdigit()
        )

        valid_zip_plus_4 = (
            len(value) == 10
            and value[5] == "-"
            and value[:5].isdigit()
            and value[6:].isdigit()
        )

        if not (valid_5_digit or valid_zip_plus_4):
            raise ValueError(
                "ZIP code must be 5 digits or ZIP+4 format."
            )

        return value


# ======================================================
# PATIENT RESPONSE
# ======================================================

class PatientResponse(PatientBase):
    model_config = ConfigDict(
        from_attributes=True
    )

    patient_id: UUID

    created_at: datetime

    updated_at: datetime

    deleted_at: Optional[datetime] = None


# ======================================================
# RESPONSE ENVELOPE
# ======================================================

T = TypeVar("T")


class ResponseEnvelope(BaseModel, Generic[T]):
    data: Optional[T] = None

    error: Optional[str] = None