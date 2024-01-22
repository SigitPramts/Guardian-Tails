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
        elif ' ' in password:
            errors.append("Password tidak boleh mengandung spasi")


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
    
def validate_binatang(nama_binatang, jenis_kelamin, jenis_hewan, id_admin):
    errors = []

    if nama_binatang is None or len(jenis_hewan) <= 0:
        errors.append("Nama binatang tidak boleh kosong")

    if jenis_kelamin is None or len(jenis_hewan) <= 0 or jenis_kelamin.lower() not in ['jantan','betina']:
        errors.append("Jenis Kelamin harus di isi dan hanya boleh jantan atau betina")

    if jenis_hewan is None or len(jenis_hewan) <= 0:
        errors.append("Jenis hewan harus di isi")

    if id_admin is None:
        errors.append("id admin harus di isi")
    else:
        if len(nama_binatang) <= 0:
            errors.append("Nama binatang harus di isi")

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))