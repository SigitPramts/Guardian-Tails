from models import donatur 
from flask import request

from validator import donatur as donatur_validator
from validator.donatur import ValidateError

#Fungsi untuk mendapatkan semua data donatur
def get_all_donatur():
    return donatur.get_all_donatur()

#Fungsi untuk menemukan donatur berdasarkan ID
def find_id_donatur(id_donatur: int):
    find_id_donatur = donatur.find_id_donatur(id_donatur)
    if find_id_donatur is None:
        return {"msg": "donasi tidak ditemukan"}, 404
    
    return find_id_donatur

#Fungsi untuk menambahkan data donatur baru
def new_donatur():
    try:
        #Mengambil inputan user
        nama_donatur = request.form.get("nama_donatur")
        email_donatur = request.form.get("email_donatur")
        jumlah_donasi = request.form.get("jumlah_donasi")
        id_kegiatan = request.form.get("id_kegiatan")
        
        #Validasi jika memiliki kesalahan
        validate = donatur_validator.vcreate_donatur(
            nama_donatur=nama_donatur,
            email_donatur=email_donatur,
            jumlah_donasi=jumlah_donasi,
            id_kegiatan=id_kegiatan
        )

        if validate is not None:
            return {"errors": validate}, 422
        
        #Tambahkan donatur baru ke dalam database
        donatur.new_donatur(nama_donatur, email_donatur, jumlah_donasi, id_kegiatan)
        return {"message": "Donatur berhasil ditambah"}, 200
    except ValidateError as e:
         return str(e), 400

#Fungsi untuk mengedit data donatur
def edit_donatur(id_donatur: int):
    try:
        #Mendapatkan data donatur dari formulir
        nama_donatur = request.form.get("nama_donatur")
        email_donatur = request.form.get("email_donatur")
        jumlah_donasi = request.form.get("jumlah_donasi")
        id_kegiatan = request.form.get("id_kegiatan")
        
        #Validasi jika memiliki kesalahan
        validate = donatur_validator.vedit_donatur(
            nama_donatur=nama_donatur,
            email_donatur=email_donatur,
            jumlah_donasi=jumlah_donasi,
            id_kegiatan=id_kegiatan
        )

        if validate is not None:
            return {"errors": validate}, 422

        #Edit data donatur
        donatur.edit_donatur(id_donatur, nama_donatur, email_donatur, jumlah_donasi, id_kegiatan)
        return {"message": "Donatur berhasil diubah"}, 200
    except ValidateError as e:
         return str(e), 400

#Fungsi untuk menghapus data donatur
def del_donatur(id_donatur: int):
    try:
        donatur_validator.vdelete_donatur(id_donatur)

        # Jika validasi berhasil, lanjutkan untuk menghapus donatur
        donatur.del_donatur(id_donatur)
        
        # Memberikan respons sukses
        return {"msg": "Berhasil dihapus"}, 200
    except ValidateError as e:
        # Jika terjadi kesalahan validasi, kembalikan pesan kesalahan
        return {"error": str(e)}, 400