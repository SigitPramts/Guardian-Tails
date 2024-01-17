from models import donatur 
from flask import request

def get_all_donatur():
    return donatur.get_all_donatur()

def find_id_donatur(id_donatur: int):
    find_id_donatur = donatur.find_id_donatur(id_donatur)
    if find_id_donatur is None:
        return {"msg": "donasi tidak ditemukan"}, 404
    
    return find_id_donatur

def new_donatur():
    nama_donatur = request.form.get("nama_donatur")
    email_donatur = request.form.get("email_donatur")
    jumlah_donasi = request.form.get("jumlah_donasi")
    id_kegiatan = request.form.get("id_kegiatan")
    
    donatur.new_donatur(nama_donatur, email_donatur, jumlah_donasi, id_kegiatan)
    return {"message": "Donatur berhasil ditambah"}, 200

def edit_donatur(id_donatur: int):
    nama_donatur = request.form.get("nama_donatur")
    email_donatur = request.form.get("email_donatur")
    jumlah_donasi = request.form.get("jumlah_donasi")
    id_kegiatan = request.form.get("id_kegiatan")
    
    donatur.edit_donatur(id_donatur, nama_donatur, email_donatur, jumlah_donasi, id_kegiatan)
    return {"message": "Donatur berhasil diubah"}, 200

def del_donatur(id_donatur: int):
    donatur.del_donatur(id_donatur)
    return {"msg": "Berhasil dihapus"}, 404