from models import user as user_model

import json

class ValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)

def vcreate_kegiatan(**kwargs):
    jenis_kegiatan = kwargs.get("jenis_kegiatan")
    lokasi_kegiatan = kwargs.get("lokasi_kegiatan")
    id_admin = kwargs.get("id_admin")

    errors = []

    if jenis_kegiatan is None or len(jenis_kegiatan) <= 0:
        errors.append("Jenis kegiatan tidak boleh kosong")

    if lokasi_kegiatan is None or len(lokasi_kegiatan) <= 0:
        errors.append("Lokasi kegiatan tidak boleh kosong")


    if id_admin is None or str(id_admin).strip() == '':
        errors.append("id admin harus di isi")
        return {"errors": errors}

    try:
        id_admin = int(id_admin)
    except ValueError:
        errors.append("id kegiatan harus berupa angka")
        return {"errors": errors}

    user = user_model.find_id_user(id_admin)
    if user is None:
        errors.append("id admin tidak ditemukan")
        return {"errors": errors}

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))

def vedit_kegiatan(**kwargs):
    jenis_kegiatan = kwargs.get("jenis_kegiatan")
    lokasi_kegiatan = kwargs.get("lokasi_kegiatan")
    id_admin = kwargs.get("id_admin")

    errors = []

    if jenis_kegiatan is None or len(jenis_kegiatan) <= 0:
        errors.append("Jenis kegiatan tidak boleh kosong")

    if lokasi_kegiatan is None or len(lokasi_kegiatan) <= 0:
        errors.append("Lokasi kegiatan tidak boleh kosong")


    if id_admin is None or str(id_admin).strip() == '':
        errors.append("id admin harus di isi")
        return {"errors": errors}

    try:
        id_admin = int(id_admin)
    except ValueError:
        errors.append("id kegiatan harus berupa angka")
        return {"errors": errors}

    user = user_model.find_id_user(id_admin)
    if user is None:
        errors.append("id admin tidak ditemukan")
        return {"errors": errors}

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))