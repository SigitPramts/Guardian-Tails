from models import user as user_model
from models import binatang as binatang_model

import json

class ValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)

def vcreate_penyelamatan(**kwargs):
    lokasi_penyelamatan = kwargs.get("lokasi_penyelamatan")
    nama_penyelamatan = kwargs.get("nama_penyelamatan")
    id_binatang = kwargs.get("id_binatang")
    id_admin = kwargs.get("id_admin")

    errors = []

    if lokasi_penyelamatan is None or len(lokasi_penyelamatan) <= 0:
        errors.append("Lokasi penyelamatan tidak boleh kosong")

    if nama_penyelamatan is None or len(nama_penyelamatan) <= 0:
        errors.append("Nama penyelamatan tidak boleh kosong")

    if id_binatang is None or str(id_binatang).strip() == '':
        errors.append("id binatang harus di isi")
        return {"errors": errors}

    try:
        id_binatang = int(id_binatang)
    except ValueError:
        errors.append("id binatang harus berupa angka")
        return {"errors": errors}

    binatang = binatang_model.find_id_binatang(id_binatang)
    if binatang is None:
        errors.append("id binatang tidak ditemukan")
        return {"errors": errors}
    
    #Error
    if id_admin is None or str(id_admin).strip() == '':
        errors.append("id admin harus di isi")
        return {"errors": errors}

    try:
        id_admin = int(id_admin)
    except ValueError:
        errors.append("id admin harus berupa angka")
        return {"errors": errors}

    user = user_model.find_id_user(id_admin)
    if user is None:
        errors.append("id admin tidak ditemukan")
        return {"errors": errors}
    
    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))
    
def vedit_penyelamatan(**kwargs):
    lokasi_penyelamatan = kwargs.get("lokasi_penyelamatan")
    nama_penyelamatan = kwargs.get("nama_penyelamatan")
    id_binatang = kwargs.get("id_binatang")
    id_admin = kwargs.get("id_admin")

    errors = []

    if lokasi_penyelamatan is None or len(lokasi_penyelamatan) <= 0:
        errors.append("Lokasi penyelamatan tidak boleh kosong")

    if nama_penyelamatan is None or len(nama_penyelamatan) <= 0:
        errors.append("Nama penyelamatan tidak boleh kosong")

    if id_binatang is None or str(id_binatang).strip() == '':
        errors.append("id binatang harus di isi")
        return {"errors": errors}

    try:
        id_binatang = int(id_binatang)
    except ValueError:
        errors.append("id binatang harus berupa angka")
        return {"errors": errors}

    binatang = binatang_model.find_id_binatang(id_binatang)
    if binatang is None:
        errors.append("id binatang tidak ditemukan")
        return {"errors": errors}
    
    if id_admin is None or str(id_admin).strip() == '':
        errors.append("id admin harus di isi")
        return {"errors": errors}

    try:
        id_admin = int(id_admin)
    except ValueError:
        errors.append("id admin harus berupa angka")
        return {"errors": errors}

    user = user_model.find_id_user(id_admin)
    if user is None:
        errors.append("id admin tidak ditemukan")
        return {"errors": errors}
    
    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))