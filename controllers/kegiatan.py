from models import kegiatan
from flask import request

def get_all_kegiatan():
    return kegiatan.get_all_kegiatan()

def find_by_id(id_kegiatan: int):
    find_by_id_kegiatan = kegiatan.find_by_id(id_kegiatan)
    if find_by_id_kegiatan is None:
        return {"msg": "Kegiatan tidak ditemukan"}, 404
    
    return find_by_id_kegiatan

def new_kegiatan():
    jenis_kegiatan = request.form.get("jenis_kegiatan")
    lokasi_kegiatan = request.form.get("lokasi_kegiatan")
    id_admin = request.form.get("id_admin")

    kegiatan.new_kegiatan(jenis_kegiatan,lokasi_kegiatan,id_admin)
    return {"message": "Kegiatan berhasil ditambah"},200

def edit_kegiatan(id_kegiatan):
    jenis_kegiatan = request.form.get("jenis_kegiatan")
    lokasi_kegiatan = request.form.get("lokasi_kegiatan")
    id_admin = request.form.get("id_admin")

    kegiatan.edit_kegiatan(id_kegiatan, jenis_kegiatan, lokasi_kegiatan, id_admin)
    return {"message": "Kegiatan berhasil diubah"},200

def del_kegiatan(id_kegiatan):
    kegiatan.del_kegiatan(id_kegiatan)
    return {"message": "Kegiatan berhasil di hapus"},404