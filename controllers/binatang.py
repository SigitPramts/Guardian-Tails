from models import gambar_binatang
from models import binatang

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from validator import binatang as binatang_validator
from validator.donatur import ValidateError
import os

#----------------------------------------------------------------------------
#Fungsi untuk mendapatkan semua data binatang
@jwt_required()
def get_all_binatang():
    #Mendapatkan parameter pencarian (keyword), batasan data (limit), dan halaman (page)
    keyword = request.args.get("keyword")
    limit = int(request.args.get("limit", 5))
    page = int(request.args.get("page", 1))
    admin_saat_ini = get_jwt_identity().get('id_admin')

    return binatang.get_all_binatang(keyword=keyword, limit=limit, page=page, id_admin=admin_saat_ini)

#Fungsi untuk melakukan pencarian berdasarkan keyword
def search():
    #Mendapatkan semua data binatang
    items = get_all_binatang()

    if request.args.get('keyword') is not None:
        keyword = request.args.get('keyword')

        #Membuat list kosong untuk menyimpan hasil pencarian
        _items = []
        for item in items:
            if keyword in item['nama_binatang'].lower():
                _items.append(item)

        items=_items #Menyimpan hasil pencarian
    return items

#Fungsi untuk melakukan pencarian multi-keyword
def multi_search():
    #Mendapatkan semua data binatang
    items = get_all_binatang()

    #Jika terdapat satu atau lebih keyword yang diberikan dalam parameter URL
    if len(request.args.getlist('keyword')) > 0:
        keywords = request.args.getlist('keyword')

        #Membuat list kosong untuk menyimpan hasil pencarian multi-keyword
        _items = []
        for keyword in keywords:
            for item in items:
                #Jika keyword cocok dengan nama binatang maka tambahkan ke hasil pencarian
                if keyword in item['nama_binatang'].lower():
                    _items.append(item)

        items=_items
    return items

#Fungsi untuk menemukan binatang berdasarkan ID
def find_id_binatang(id_binatang: int):
    #Mencari data binatang berdasarkan ID
    find_id_binatang = binatang.find_id_binatang(id_binatang)
    if find_id_binatang is None:
        return {"msg": "Binatang tidak ditemukan"}, 404
    
    return find_id_binatang

#Fungsi untuk menambahkan binatang baru
@jwt_required()
def new_binatang():
    try:
        admin_saat_ini = get_jwt_identity().get('id_admin') #Mendapatkan identitas admin dari token JWT

        #Mengambil inputan user
        nama_binatang = request.form.get("nama_binatang")
        jenis_kelamin = request.form.get("jenis_kelamin")
        jenis_hewan = request.form.get("jenis_hewan")

        #Validasi jika memiliki kesalahan
        validate = binatang_validator.vcreate_binatang(
            nama_binatang=nama_binatang,
            jenis_kelamin=jenis_kelamin,
            jenis_hewan=jenis_hewan,
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        #Tambahkan binatang baru ke dalam database
        binatang.new_binatang(nama_binatang, jenis_kelamin, jenis_hewan, admin_saat_ini)
        return {"msg": "Binatang berhasil ditambah"}, 200
    except ValidateError as e:
        return str(e), 400

# Fungsi untuk mengedit data binatang
@jwt_required()
def edit_binatang(id_binatang: int):
    try:
        #Mendapatkan identitas admin dari token JWT
        admin_saat_ini = get_jwt_identity()['id_admin']

        #Mengambil inputan user
        nama_binatang = request.form.get("nama_binatang")
        jenis_kelamin = request.form.get("jenis_kelamin")
        jenis_hewan = request.form.get("jenis_hewan")
        
        #Memeriksa izin admin untuk mengedit binatang
        binatang_data = binatang.find_id_binatang(id_binatang)
        if binatang_data is None or binatang_data['id_admin'] != admin_saat_ini:
            return {"error": "Anda tidak memiliki izin untuk mengubah binatang ini"}, 403

        #Validasi jika memiliki kesalahan
        validate = binatang_validator.vedit_binatang(
            nama_binatang=nama_binatang,
            jenis_kelamin=jenis_kelamin,
            jenis_hewan=jenis_hewan,
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        #Mengedit data binatang
        binatang.edit_binatang(id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, admin_saat_ini)
        return {"msg": "Binatang berhasil diubah"}, 200
    except ValidateError as e:
        return str(e), 400

#Fungsi untuk menghapus data binatang
@jwt_required()
def del_binatang(id_binatang: int):
    try:
        admin_saat_ini = get_jwt_identity()['id_admin']  #Mendapatkan identitas admin dari token JWT

        # Validasi pemilik token
        binatang_data = binatang.find_id_binatang(id_binatang)
        if binatang_data is None or binatang_data['id_admin'] != admin_saat_ini:
            return {"error": "Anda tidak memiliki izin untuk menghapus binatang ini"}, 403

        # Menghapus data binatang dari database
        binatang.del_binatang(id_binatang, admin_saat_ini)
        return {"msg": "Berhasil dihapus"}, 200
    except Exception as e:
        return str(e), 400


#----------------------------------------------------------------------------
#Gambar_binatang
    
#Fungsi untuk mendapatkan semua data gambar binatang
def get_all_gambar():
    return gambar_binatang.get_all_gambar()

#Fungsi untuk menemukan gambar binatang berdasarkan ID
def find_id_gambar(id_gambar: int):
    find_id_gambar = gambar_binatang.find_id_gambar(id_gambar)
    if find_id_gambar is None:
        return {"msg": "Gambar tidak ditemukan"}, 404
    
    return find_id_gambar

#Fungsi untuk mengunggah gambar binatang
def upload_gambar(id_binatang: int):
    try:
        #Mendapatkan daftar file gambar yang diunggah
        images = request.files.getlist("images")
        if not images:
            return {"msg": "Images dibutuhkan"}, 400
        
        #Validasi gambar yang diunggah
        validate = binatang_validator.vcreate_gambar_binatang(
            images=images,
            id_binatang=id_binatang,
        )
        
        if validate is not None:
            return {"errors": validate}, 422

        #Untuk setiap gambar yang diunggah
        for image in images:
            try:
                #Memeriksa tipe file gambar yang diunggah
                if image.content_type not in ["image/jpeg", "image/jpg", "image/webp", "image/png"]:
                    return {"message": "File type not allowed"}, 415
                
                #Menyimpan gambar ke dalam folder statis
                lokasi_gambar = "static/images/" + image.filename
                image.save(lokasi_gambar)

                #Menambahkan informasi lokasi gambar ke dalam database
                gambar_binatang.upload_gambar(id_binatang, lokasi_gambar)
            except Exception as e:
                #Menangani kesalahan spesifik jika diperlukan
                return {"error": f"Error menyimpan gambar: {str(e)}"}, 500

        return {"message": "Gambar berhasil ditambah"}, 200
    except Exception as e:
        #Menangani kesalahan spesifik jika diperlukan
        return {"error": f"Error memproses gambar: {str(e)}"}, 500


#Fungsi untuk menghapus gambar binatang
def del_gambar(id_gambar: int):
    #Menemukan informasi gambar berdasarkan ID
    image = find_id_gambar(id_gambar)
    if image is None:
        return {"msg": "Gambar tidak ditemukan atau tidak ada informasi lokasi gambar"}, 404
    
    #Mendapatkan lokasi gambar dari informasi yang ditemukan
    lokasi_gambar = image.get('lokasi_gambar', '')

    #Menghapus gambar dari database
    gambar_binatang.del_gambar(id_gambar)

    #Menghapus gambar dari folder statis jika lokasi gambar ada
    if os.path.exists(lokasi_gambar):
        os.remove(lokasi_gambar)
    else:
        return {"msg": "Lokasi gambar tidak ditemukan"}, 404

    return {"message": "Gambar berhasil dihapus"}, 200
