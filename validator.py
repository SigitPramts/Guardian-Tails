import json

class ValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_register(username, password, nama_lengkap, email):
    errors = []

    if username is None:
        errors.append("Username harus di isi")
    else:
        if len(username) < 8:
            errors.append("Username harus lebih dari 8 karakter")

    if password is None:
        errors.append("Password harus di isi")
    else:
        if len(password) < 8:
            errors.append("Password harus lebih dari 8 karakter")

    if nama_lengkap is None:
        errors.append("Nama lengkap harus di isi")

    if email is None or not email.strip():
        errors.append("Email harus diisi")
    else:
        # You can add more sophisticated email validation if needed
        # For a simple check, you can use a regular expression
        import re
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(email):
            errors.append("Format email tidak valid")
    
    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))