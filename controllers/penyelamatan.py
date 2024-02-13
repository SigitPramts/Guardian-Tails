from models import penyelamatan
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from validator import penyelamatan as penyelamatan_validator
from validator.penyelamatan import ValidateError

#Fungsi untuk mendapatkan semua data penyelamatan
@jwt_required()
def get_all_penyelamatan():
    #Mendapatkan parameter pencarian dari permintaan
    keyword = request.args.get("keyword")
    limit = int(request.args.get("limit", 5))
    page = int(request.args.get("page", 1))
    admin_saat_ini = get_jwt_identity().get('id_admin')
    
    return penyelamatan.get_all_penyelamatan(keyword=keyword, limit=limit, page=page, id_admin=admin_saat_ini)

#Fungsi untuk menemukan penyelamatan berdasarkan ID
def find_id_penyelamatan(id_penyelamatan: int):
    find_id_penyelamatan = penyelamatan.find_id_penyelamatan(id_penyelamatan)
    if find_id_penyelamatan is None:
        return {"msg": "Penyelamatan tidak ditemukan"}, 404
    
    return find_id_penyelamatan

#Fungsi untuk menambahkan data penyelamatan baru
@jwt_required()
def new_penyelamatan():
    try:
        admin_saat_ini = get_jwt_identity()['id_admin'] #Mengambil user ID dari JWT token
        lokasi_penyelamatan = request.form.get("lokasi_penyelamatan")
        nama_penyelamatan = request.form.get("nama_penyelamatan")
        id_binatang = request.form.get("id_binatang")

        #Validasi jika memiliki kesalahan
        validate = penyelamatan_validator.vcreate_penyelamatan(
            lokasi_penyelamatan=lokasi_penyelamatan,
            nama_penyelamatan=nama_penyelamatan,
            id_binatang=id_binatang,
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        #Tambahkan penyelamatan baru ke dalam database
        penyelamatan.new_penyelamatan(lokasi_penyelamatan, nama_penyelamatan, id_binatang, admin_saat_ini)
        return {"message": "Penyelamatan berhasil ditambah"}, 200
    except ValidateError as e:
        return str(e), 400

#Fungsi untuk mengedit data penyelamatan
@jwt_required()
def edit_penyelamatan(id_penyelamatan: int):
    try:
        admin_saat_ini = get_jwt_identity()['id_admin'] #Mengambil user ID dari JWT token
        lokasi_penyelamatan = request.form.get("lokasi_penyelamatan")
        nama_penyelamatan = request.form.get("nama_penyelamatan")
        id_binatang = request.form.get("id_binatang")

        # Validasi pemilik token
        binatang_data = penyelamatan.find_id_penyelamatan(id_penyelamatan)
        if binatang_data is None or binatang_data['id_admin'] != admin_saat_ini:
            return {"error": "Anda tidak memiliki izin untuk menghapus penyelamatan ini"}, 403

        #Validasi jika memiliki kesalahan
        validate = penyelamatan_validator.vedit_penyelamatan(
            lokasi_penyelamatan=lokasi_penyelamatan,
            nama_penyelamatan=nama_penyelamatan,
            id_binatang=id_binatang,
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        #Edit data penyelamatan
        penyelamatan.edit_penyelamatan(id_penyelamatan, lokasi_penyelamatan, nama_penyelamatan, id_binatang, admin_saat_ini)
        return {"msg": "Penyelamatan berhasil diubah"}, 200
    except ValidateError as e:
        return str(e), 400

#Fungsi untuk menghapus data penyelamatan
@jwt_required()
def del_penyelamatan(id_penyelamatan: int):
    try:
        admin_saat_ini = get_jwt_identity()['id_admin'] #Mengambil user ID dari JWT token

        # Validasi pemilik token
        binatang_data = penyelamatan.find_id_penyelamatan(id_penyelamatan)
        if binatang_data is None or binatang_data['id_admin'] != admin_saat_ini:
            return {"error": "Anda tidak memiliki izin untuk menghapus penyelamatan ini"}, 403
        
        #Hapus penyelamatan
        penyelamatan.del_penyelamatan(id_penyelamatan, admin_saat_ini)
        return {"msg": "Berhasil dihapus"}, 404
    except Exception as e:
        return str(e), 400