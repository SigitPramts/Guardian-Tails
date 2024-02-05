from models import kegiatan as kegiatan_model

import json

class ValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)

def vcreate_donatur(**kwargs):
    nama_donatur = kwargs.get("nama_donatur")
    email_donatur = kwargs.get("email_donatur")
    jumlah_donasi = kwargs.get("jumlah_donasi")
    id_kegiatan = kwargs.get("id_kegiatan")

    errors = []

    if nama_donatur is None or len(nama_donatur) <= 0:
        errors.append("Nama donatur tidak boleh kosong")

    if email_donatur is None or not email_donatur.strip():
        errors.append("Email harus diisi")
    else:
        import re
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(email_donatur):
            errors.append("Format email tidak valid")

    if jumlah_donasi is None or len(jumlah_donasi) <= 0:
        errors.append("Jumlah donasi harus di isi")
    elif not jumlah_donasi.isdigit():
        errors.append("Jumlah donasi harus berupa angka")

    if id_kegiatan is None or str(id_kegiatan).strip() == '':
        errors.append("id kegiatan harus di isi")
        return {"errors": errors}

    try:
        id_kegiatan = int(id_kegiatan)
    except ValueError:
        errors.append("id kegiatan harus berupa angka")
        return {"errors": errors}

    kegiatan = kegiatan_model.find_by_id(id_kegiatan)
    if kegiatan is None:
        errors.append("id kegiatan tidak ditemukan")
        return {"errors": errors}

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))


def vedit_donatur(**kwargs):
    nama_donatur = kwargs.get("nama_donatur")
    email_donatur = kwargs.get("email_donatur")
    jumlah_donasi = kwargs.get("jumlah_donasi")
    id_kegiatan = kwargs.get("id_kegiatan")

    errors = []

    if nama_donatur is None or len(nama_donatur) <= 0:
        errors.append("Nama donatur tidak boleh kosong")

    if email_donatur is None or not email_donatur.strip():
        errors.append("Email harus diisi")
    else:
        import re
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_pattern.match(email_donatur):
            errors.append("Format email tidak valid")

    if jumlah_donasi is None or len(jumlah_donasi) <= 0:
        errors.append("Jumlah donasi harus di isi")
    elif not jumlah_donasi.isdigit():
        errors.append("Jumlah donasi harus berupa angka")

    if id_kegiatan is None or str(id_kegiatan).strip() == '':
        errors.append("id kegiatan harus di isi")
        return {"errors": errors}

    try:
        id_kegiatan = int(id_kegiatan)
    except ValueError:
        errors.append("id kegiatan harus berupa angka")
        return {"errors": errors}

    kegiatan = kegiatan_model.find_by_id(id_kegiatan)
    if kegiatan is None:
        errors.append("id kegiatan tidak ditemukan")
        return {"errors": errors}

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))
