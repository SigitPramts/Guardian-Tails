from models import penyelamatan
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from validator import penyelamatan as penyelamatan_validator
from validator.penyelamatan import ValidateError

def get_all_penyelamatan():
    return penyelamatan.get_all_penyelamatan()

def find_id_penyelamatan(id_penyelamatan: int):
    find_id_penyelamatan = penyelamatan.find_id_penyelamatan(id_penyelamatan)
    if find_id_penyelamatan is None:
        return {"msg": "Penyelamatan tidak ditemukan"}, 404
    
    return find_id_penyelamatan

@jwt_required()
def new_penyelamatan():
    try:
        admin_saat_ini = get_jwt_identity()['id_admin']
        lokasi_penyelamatan = request.form.get("lokasi_penyelamatan")
        nama_penyelamatan = request.form.get("nama_penyelamatan")
        id_binatang = request.form.get("id_binatang")

        validate = penyelamatan_validator.vcreate_penyelamatan(
            lokasi_penyelamatan=lokasi_penyelamatan,
            nama_penyelamatan=nama_penyelamatan,
            id_binatang=id_binatang,
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        penyelamatan.new_penyelamatan(lokasi_penyelamatan, nama_penyelamatan, id_binatang, admin_saat_ini)
        return {"message": "Penyelamatan berhasil ditambah"}, 200
    except ValidateError as e:
        return str(e), 400

@jwt_required()
def edit_penyelamatan(id_penyelamatan: int):
    try:
        admin_saat_ini = get_jwt_identity()['id_admin']
        lokasi_penyelamatan = request.form.get("lokasi_penyelamatan")
        nama_penyelamatan = request.form.get("nama_penyelamatan")
        id_binatang = request.form.get("id_binatang")

        validate = penyelamatan_validator.vedit_penyelamatan(
            lokasi_penyelamatan=lokasi_penyelamatan,
            nama_penyelamatan=nama_penyelamatan,
            id_binatang=id_binatang,
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        penyelamatan.edit_penyelamatan(id_penyelamatan, lokasi_penyelamatan, nama_penyelamatan, id_binatang, admin_saat_ini)
        return {"msg": "Penyelamatan berhasil diubah"}, 200
    except ValidateError as e:
        return str(e), 400

@jwt_required()
def del_penyelamatan(id_penyelamatan: int):
    try:
        admin_saat_ini = get_jwt_identity()['id_admin']
        penyelamatan.del_penyelamatan(id_penyelamatan, admin_saat_ini)
        return {"msg": "Berhasil dihapus"}, 404
    
    except Exception as e:
        return str(e), 400