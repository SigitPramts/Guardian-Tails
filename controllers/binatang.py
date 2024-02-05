from models import gambar_binatang
from models import binatang

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest

from validator import binatang as binatang_validator
from validator.donatur import ValidateError
import os

#----------------------------------------------------------------------------
#Binatang
def get_all_binatang():
    keyword = request.args.get("keyword")
    limit = int(request.args.get("limit", 5))
    page = int(request.args.get("page", 1))

    return binatang.get_all_binatang(keyword=keyword, limit=limit, page=page)

def search():
    items = get_all_binatang()

    if request.args.get('keyword') is not None:
        keyword = request.args.get('keyword')

        _items = []
        for item in items:
            if keyword in item['nama_binatang'].lower():
                _items.append(item)

        items=_items
    return items

def multi_search():
    items = get_all_binatang()

    if len(request.args.getlist('keyword')) > 0:
        keywords = request.args.getlist('keyword')

        _items = []
        for keyword in keywords:
            for item in items:
                if keyword in item['nama_binatang'].lower():
                    _items.append(item)

        items=_items
    return items

def find_id_binatang(id_binatang: int):
    find_id_binatang = binatang.find_id_binatang(id_binatang)
    if find_id_binatang is None:
        return {"msg": "Binatang tidak ditemukan"}, 404
    
    return find_id_binatang

@jwt_required
def new_binatang():
    try:
        admin_saat_ini = get_jwt_identity().get('id_admin')
        nama_binatang = request.form.get("nama_binatang")
        jenis_kelamin = request.form.get("jenis_kelamin")
        jenis_hewan = request.form.get("jenis_hewan")
        id_admin = request.form.get("id_admin")

        if admin_saat_ini != id_admin:
            return {"error": "Tidak diizinkan untuk mengubah informasi admin lain"}, 403

        validate = binatang_validator.vcreate_binatang(
            nama_binatang=nama_binatang,
            jenis_kelamin=jenis_kelamin,
            jenis_hewan=jenis_hewan,
            id_admin=id_admin
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        binatang.new_binatang(nama_binatang, jenis_kelamin, jenis_hewan, id_admin)
        return {"msg": "Binatang berhasil ditambah"}
    except ValidateError as e:
        return str(e), 400

@jwt_required
def edit_binatang(id_binatang: int):
    try:
        admin_saat_ini = get_jwt_identity()
        nama_binatang = request.form.get("nama_binatang")
        jenis_kelamin = request.form.get("jenis_kelamin")
        jenis_hewan = request.form.get("jenis_hewan")
        id_admin = request.form.get("id_admin")

        if admin_saat_ini != int(id_admin):
            return {"message": "Tidak diizinkan untuk mengubah informasi admin lain"}

        validate = binatang_validator.vedit_binatang(
            nama_binatang=nama_binatang,
            jenis_kelamin=jenis_kelamin,
            jenis_hewan=jenis_hewan,
            id_admin=id_admin
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        binatang.edit_binatang(id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, id_admin)
        return {"msg": "Binatang berhasil diubah"}, 200
    except ValidateError as e:
        return str(e), 400

def del_binatang(id_binatang: int):
    binatang.del_binatang(id_binatang)
    return {"msg": "Berhasil dihapus"}, 404


#----------------------------------------------------------------------------
#Gambar_binatang
def get_all_gambar():
    return gambar_binatang.get_all_gambar()

def find_id_gambar(id_gambar: int):
    find_id_gambar = gambar_binatang.find_id_gambar(id_gambar)
    if find_id_gambar is None:
        return {"msg": "Gambar tidak ditemukan"}, 404
    
    return find_id_gambar

def upload_gambar(id_binatang: int):
    try:
        images = request.files.getlist("images")
        if not images:
            return {"msg": "Images dibutuhkan"}, 400
        
        validate = binatang_validator.vcreate_gambar_binatang(
            images=images,
            id_binatang=id_binatang,
        )
        
        if validate is not None:
            return {"errors": validate}, 422

        for image in images:
            try:
                if image.content_type not in ["image/jpeg", "image/jpg", "image/webp", "image/png"]:
                    return {"message": "File type not allowed"}, 415
                
                lokasi_gambar = "static/images/" + image.filename
                image.save(lokasi_gambar)

                gambar_binatang.upload_gambar(id_binatang, lokasi_gambar)
            except Exception as e:
                # Handle specific exceptions if needed
                return {"error": f"Error menyimpan gambar: {str(e)}"}, 500

        return {"message": "Gambar berhasil ditambah"}, 201
    except Exception as e:
        # Handle specific exceptions if needed
        return {"error": f"Error memproses gambar: {str(e)}"}, 500



def del_gambar(id_gambar: int):
    # Menghapus gambar dari folder
    image = find_id_gambar(id_gambar)
    if image is None:
        return {"msg": "Gambar tidak ditemukan atau tidak ada informasi lokasi gambar"}, 404
    
    lokasi_gambar = image.get('lokasi_gambar', '')

    # Menghapus gambar dari database
    gambar_binatang.del_gambar(id_gambar)

    if os.path.exists(lokasi_gambar):
        os.remove(lokasi_gambar)
    else:
        return {"msg": "Lokasi gambar tidak ditemukan"}, 404

    return {"message": "Gambar berhasil dihapus"}, 200
