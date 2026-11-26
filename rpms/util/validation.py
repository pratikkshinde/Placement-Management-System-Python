from datetime import date


def require_non_empty(value, field_name):
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return str(value).strip()


def validate_email(email, field_name="Email"):
    clean_email = require_non_empty(email, field_name).lower()
    if " " in clean_email or clean_email.count("@") != 1:
        raise ValueError(f"Invalid {field_name.lower()} format: {email}")
    local_part, domain_part = clean_email.split("@")
    if (
        not local_part
        or not domain_part
        or "." not in domain_part
        or domain_part.startswith(".")
        or domain_part.endswith(".")
    ):
        raise ValueError(f"Invalid {field_name.lower()} format: {email}")
    return clean_email


def validate_mobile(mobile):
    clean_mobile = require_non_empty(mobile, "Mobile number")
    if not clean_mobile.isdigit() or len(clean_mobile) != 10:
        raise ValueError("Mobile number must be a valid 10-digit number.")
    return clean_mobile


def validate_passing_year(passing_year, field_name="Passing year"):
    year = int(passing_year)
    if year < 1990 or year > 2100:
        raise ValueError(f"{field_name} must be between 1990 and 2100.")
    return year


def validate_iso_date(date_text, field_name="Date"):
    clean_date = require_non_empty(date_text, field_name)
    try:
        return date.fromisoformat(clean_date)
    except ValueError:
        raise ValueError(f"{field_name} must be in YYYY-MM-DD format.")
