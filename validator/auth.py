import json, re
from models.user import is_username_email_unique

class ValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_register(username, password, nama_lengkap, email):
    errors = []

    if not username or username.strip() == "":
        errors.append("Username harus diisi")
    elif len(username) < 8:
        errors.append("Username harus terdiri dari minimal 8 karakter")
    elif not is_username_email_unique(username, email):
        errors.append("Username sudah digunakan")

    if not password or password.strip() == "":
        errors.append("Password harus diisi")
    elif len(password) < 8:
        errors.append("Password harus terdiri dari minimal 8 karakter")
    elif ' ' in password:
        errors.append("Password tidak boleh mengandung spasi")

    if not nama_lengkap or nama_lengkap.strip() == "":
        errors.append("Nama lengkap harus diisi")

    if not email or email.strip() == "":
        errors.append("Email harus diisi")
    else:
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(email):
            errors.append("Format email tidak valid")
        elif not is_username_email_unique(username, email):
            errors.append("Email sudah digunakan")

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))


def validate_edit(username, password, nama_lengkap, email):
    errors = []

    if not username or username.strip() == "":
        errors.append("Username harus diisi")
    elif len(username) < 8:
        errors.append("Username harus terdiri dari minimal 8 karakter")
    elif not is_username_email_unique(username, email):
        errors.append("Username sudah digunakan")

    if not password or password.strip() == "":
        errors.append("Password harus diisi")
    elif len(password) < 8:
        errors.append("Password harus terdiri dari minimal 8 karakter")
    elif ' ' in password:
        errors.append("Password tidak boleh mengandung spasi")

    if not nama_lengkap or nama_lengkap.strip() == "":
        errors.append("Nama lengkap harus diisi")

    if not email or email.strip() == "":
        errors.append("Email harus diisi")
    else:
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(email):
            errors.append("Format email tidak valid")
        elif not is_username_email_unique(username, email):
            errors.append("Email sudah digunakan")
    
    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))