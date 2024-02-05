from models import kegiatan
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from validator import kegiatan as kegiatan_validator
from validator.kegiatan import ValidateError

def get_all_kegiatan():
    return kegiatan.get_all_kegiatan()

def find_by_id(id_kegiatan: int):
    find_by_id_kegiatan = kegiatan.find_by_id(id_kegiatan)
    if find_by_id_kegiatan is None:
        return {"msg": "Kegiatan tidak ditemukan"}, 404
    
    return find_by_id_kegiatan

def new_kegiatan():
    try:
        jenis_kegiatan = request.form.get("jenis_kegiatan")
        lokasi_kegiatan = request.form.get("lokasi_kegiatan")
        id_admin = request.form.get("id_admin")

        validate = kegiatan_validator.vcreate_kegiatan(
            jenis_kegiatan=jenis_kegiatan,
            lokasi_kegiatan=lokasi_kegiatan,
            id_admin=id_admin
        )

        if validate is not None:
            return {"errors": validate}, 422

        kegiatan.new_kegiatan(jenis_kegiatan,lokasi_kegiatan,id_admin)
        return {"message": "Kegiatan berhasil ditambah"},200
    except ValueError as e:
        return str(e), 400
    
@jwt_required
def edit_kegiatan():
    try:
        admin_saat_ini = get_jwt_identity().get('id_admin')
        jenis_kegiatan = request.form.get("jenis_kegiatan")
        lokasi_kegiatan = request.form.get("lokasi_kegiatan")
        id_admin = request.form.get("id_admin")

        if admin_saat_ini != get_jwt_identity()['id_admin']:
            return {"error": "Tidak diizinkan untuk mengubah informasi admin lain"}, 403
        
        validate = kegiatan_validator.vedit_kegiatan(
            jenis_kegiatan=jenis_kegiatan,
            lokasi_kegiatan=lokasi_kegiatan,
            id_admin=id_admin
        )

        if validate is not None:
            return {"errors": validate}, 422

        kegiatan.edit_kegiatan(admin_saat_ini, id_kegiatan, jenis_kegiatan, lokasi_kegiatan, id_admin)
        return {"message": "Kegiatan berhasil diubah"},200
    except ValidateError as e:
        return str(e), 400

def del_kegiatan(id_kegiatan):
    kegiatan.del_kegiatan(id_kegiatan)
    return {"message": "Kegiatan berhasil di hapus"},404