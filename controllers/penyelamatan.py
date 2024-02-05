from models import penyelamatan
from flask import request

from validator import penyelamatan as penyelamatan_validator
from validator.penyelamatan import ValidateError

def get_all_penyelamatan():
    return penyelamatan.get_all_penyelamatan()

def find_id_penyelamatan(id_penyelamatan: int):
    find_id_penyelamatan = penyelamatan.find_id_penyelamatan(id_penyelamatan)
    if find_id_penyelamatan is None:
        return {"msg": "Penyelamatan tidak ditemukan"}, 404
    
    return find_id_penyelamatan

def new_penyelamatan():
    try:
        lokasi_penyelamatan = request.form.get("lokasi_penyelamatan")
        nama_penyelamatan = request.form.get("nama_penyelamatan")
        id_binatang = request.form.get("id_binatang")
        id_admin = request.form.get("id_admin")

        validate = penyelamatan_validator.vcreate_penyelamatan(
            lokasi_penyelamatan=lokasi_penyelamatan,
            nama_penyelamatan=nama_penyelamatan,
            id_binatang=id_binatang,
            id_admin=id_admin
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        penyelamatan.new_penyelamatan(lokasi_penyelamatan, nama_penyelamatan, id_binatang, id_admin)
        return {"message": "Penyelamatan berhasil ditambah"}, 200
    except ValidateError as e:
        return str(e), 400

def edit_penyelamatan(id_penyelamatan: int):
    try:
        lokasi_penyelamatan = request.form.get("lokasi_penyelamatan")
        nama_penyelamatan = request.form.get("nama_penyelamatan")
        id_binatang = request.form.get("id_binatang")
        id_admin = request.form.get("id_admin")

        validate = penyelamatan_validator.vedit_penyelamatan(
            lokasi_penyelamatan=lokasi_penyelamatan,
            nama_penyelamatan=nama_penyelamatan,
            id_binatang=id_binatang,
            id_admin=id_admin
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        penyelamatan.edit_penyelamatan(id_penyelamatan, lokasi_penyelamatan, nama_penyelamatan, id_binatang, id_admin)
        return {"msg": "Penyelamatan berhasil diubah"}, 200
    except ValidateError as e:
        return str(e), 400

def del_penyelamatan(id_penyelamatan: int):
    penyelamatan.del_penyelamatan(id_penyelamatan)
    return {"msg": "Berhasil dihapus"}, 404