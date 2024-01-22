from models import gambar_binatang
from models import binatang
from flask import request
from controllers.validator import validate_binatang, ValidateError
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

def new_binatang():
    try:
        nama_binatang = request.form.get("nama_binatang")
        jenis_kelamin = request.form.get("jenis_kelamin")
        jenis_hewan = request.form.get("jenis_hewan")
        id_admin = request.form.get("id_admin")

        validate = validate_binatang (nama_binatang, jenis_kelamin, jenis_hewan, id_admin)
        if validate is not None:
                return validate, 404
        
        binatang.new_binatang(nama_binatang, jenis_kelamin, jenis_hewan, id_admin)
        return {"msg": "Binatang berhasil ditambah"}
    except ValidateError as e:
        return str(e), 400

def edit_binatang(id_binatang: int):
    nama_binatang = request.form.get("nama_binatang")
    jenis_kelamin = request.form.get("jenis_kelamin")
    jenis_hewan = request.form.get("jenis_hewan")
    id_admin = request.form.get("id_admin")

    binatang.edit_binatang(id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, id_admin)
    return {"msg": "Binatang berhasil diubah"}, 200

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
    images = request.files.getlist("images")
    if images is None:
        return {"msg": "Images dibutuhkan"}, 400
    
    for image in images:
        if image.content_type not in ["image/jpeg", "image/jpg", "image/webp", "image/png"]:
            return "File type not allowed"
        
        lokasi_gambar = "static/images/" + image.filename  # Perbaikan disini
        image.save(lokasi_gambar)

        gambar_binatang.upload_gambar(id_binatang, lokasi_gambar)
    return {"message": "Gambar berhasil ditambah"}, 201

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
