import re
from datetime import date


def validate_full_name(name: str):
    name = name.strip()
    if not name:
        return False, "Full name cannot be empty."
    if len(name) < 2:
        return False, "Full name must be at least 2 characters."
    if not re.match(r"^[A-Za-z\s.\-']+$", name):
        return False, "Full name should only contain letters, spaces, or hyphens."
    return True, None


def validate_email(email: str):
    email = email.strip()
    if not email:
        return False, "Email address cannot be empty."
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Please enter a valid email address (e.g. john@example.com)."
    return True, None


def validate_dob(dob):
    if dob is None:
        return False, "Date of birth is required."
    today = date.today()
    if dob >= today:
        return False, "Date of birth cannot be today or a future date."
    age_years = (today - dob).days / 365.25
    if age_years > 130:
        return False, "Please enter a valid date of birth."
    if age_years < 0.1:
        return False, "Patient age seems too young. Please check the date."
    return True, None


def validate_blood_value(value, field_name: str, min_val=0.1, max_val=9999.0):
    if value is None:
        return False, f"{field_name} is required."
    try:
        val = float(value)
    except (TypeError, ValueError):
        return False, f"{field_name} must be a numeric value."
    if val <= 0:
        return False, f"{field_name} must be greater than 0."
    if val > max_val:
        return False, f"{field_name} value seems unusually high. Please double-check."
    return True, None


def validate_all_fields(full_name, dob, email, glucose, haemoglobin, cholesterol):
    errors = []
    ok, msg = validate_full_name(full_name)
    if not ok:
        errors.append(msg)
    ok, msg = validate_email(email)
    if not ok:
        errors.append(msg)
    ok, msg = validate_dob(dob)
    if not ok:
        errors.append(msg)
    ok, msg = validate_blood_value(glucose, "Glucose", max_val=600.0)
    if not ok:
        errors.append(msg)
    ok, msg = validate_blood_value(haemoglobin, "Haemoglobin", max_val=25.0)
    if not ok:
        errors.append(msg)
    ok, msg = validate_blood_value(cholesterol, "Cholesterol", max_val=1000.0)
    if not ok:
        errors.append(msg)
    return errors


def calculate_age(dob) -> int:
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age