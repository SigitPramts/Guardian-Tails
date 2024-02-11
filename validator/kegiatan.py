from models import user as user_model

import json

class ValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)

def vcreate_kegiatan(**kwargs):
    jenis_kegiatan = kwargs.get("jenis_kegiatan")
    lokasi_kegiatan = kwargs.get("lokasi_kegiatan")

    errors = []

    if jenis_kegiatan is None or len(jenis_kegiatan) <= 0:
        errors.append("Jenis kegiatan tidak boleh kosong")

    if lokasi_kegiatan is None or len(lokasi_kegiatan) <= 0:
        errors.append("Lokasi kegiatan tidak boleh kosong")

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))

def vedit_kegiatan(**kwargs):
    jenis_kegiatan = kwargs.get("jenis_kegiatan")
    lokasi_kegiatan = kwargs.get("lokasi_kegiatan")
    
    errors = []

    if jenis_kegiatan is None or len(jenis_kegiatan) <= 0:
        errors.append("Jenis kegiatan tidak boleh kosong")

    if lokasi_kegiatan is None or len(lokasi_kegiatan) <= 0:
        errors.append("Lokasi kegiatan tidak boleh kosong")

    if len(errors) > 0:
        raise ValidateError(json.dumps({"errors": errors}))