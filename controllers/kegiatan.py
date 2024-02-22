from models import kegiatan
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from validator import kegiatan as kegiatan_validator
from validator.kegiatan import ValidateError

#Fungsi untuk mendapatkan semua data kegiatan
def get_all_kegiatan():
    return kegiatan.get_all_kegiatan()

#Fungsi untuk menemukan kegiatan berdasarkan ID
def find_by_id(id_kegiatan: int):
    find_by_id_kegiatan = kegiatan.find_by_id(id_kegiatan)
    if find_by_id_kegiatan is None:
        return {"msg": "Kegiatan tidak ditemukan"}, 404
    
    return find_by_id_kegiatan

#Fungsi untuk menambahkan data kegiatan baru
@jwt_required()
def new_kegiatan():
    try:
        #Mengambil inputan user
        admin_saat_ini = get_jwt_identity().get('id_admin') #Mengambil user ID dari JWT token
        jenis_kegiatan = request.form.get("jenis_kegiatan")
        lokasi_kegiatan = request.form.get("lokasi_kegiatan")

        #Validasi jika memiliki kesalahan
        validate = kegiatan_validator.vcreate_kegiatan(
            jenis_kegiatan=jenis_kegiatan,
            lokasi_kegiatan=lokasi_kegiatan,
        )

        if validate is not None:
            return {"errors": validate}, 422

        #Tambahkan kegiatan baru ke dalam database
        kegiatan.new_kegiatan(jenis_kegiatan,lokasi_kegiatan,admin_saat_ini)
        return {"message": "Kegiatan berhasil ditambah"},200
    except ValueError as e:
        return str(e), 400
    
#Fungsi untuk mengedit data kegiatan
@jwt_required()
def edit_kegiatan(id_kegiatan):
    try:
        #Mengambil inputan user
        admin_saat_ini = get_jwt_identity().get('id_admin') #Mengambil user ID dari JWT token
        jenis_kegiatan = request.form.get("jenis_kegiatan")
        lokasi_kegiatan = request.form.get("lokasi_kegiatan")

        # Validasi pemilik token
        binatang_data = kegiatan.find_by_id(id_kegiatan)
        if binatang_data is None or binatang_data['id_admin'] != admin_saat_ini:
            return {"error": "Anda tidak memiliki izin untuk menghapus kegiatan ini"}, 403

        #Validasi jika memiliki kesalahan
        validate = kegiatan_validator.vedit_kegiatan(
            jenis_kegiatan=jenis_kegiatan,
            lokasi_kegiatan=lokasi_kegiatan,
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        #Edit data kegiatan
        kegiatan.edit_kegiatan(id_kegiatan, jenis_kegiatan, lokasi_kegiatan, admin_saat_ini)
        return {"message": "Kegiatan berhasil diubah"},200
    except ValidateError as e:
        return str(e), 400

#Fungsi untuk menghapus data kegiatan
@jwt_required()
def del_kegiatan(id_kegiatan):
    try:
        admin_saat_ini = get_jwt_identity()['id_admin'] #Mengambil user ID dari JWT token

        # Validasi pemilik token
        binatang_data = kegiatan.find_by_id(id_kegiatan)
        if binatang_data is None or binatang_data['id_admin'] != admin_saat_ini:
            return {"error": "Anda tidak memiliki izin untuk menghapus kegiatan ini"}, 403
        
        #Hapus kegiatan
        kegiatan.del_kegiatan(id_kegiatan, admin_saat_ini)
        return {"message": "Kegiatan berhasil di hapus"}, 200
    except Exception as e:
        return str(e), 400