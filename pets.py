from db import conn
import time
from flask import request
from psycopg2.errors import DatabaseError

#----------------------------------------------------------------------------
#Get * Binatang Done
def get_binatang():
    cur = conn.cursor()
    try:
        cur.execute("SELECT id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, tanggal_ditemukan, lokasi_gambar, id_admin FROM binatang")
        pets = cur.fetchall()

        # Convert tuple to dictionary
        # Karena python mereturn tipe data tuple. Maka kita harus mengubahnya menjadi dictionary
        simpan_pets = []
        for pet in pets:
            pet_dict = {
                "id_binatang": pet[0],
                "nama_binatang": pet[1],
                "jenis_kelamin": pet[2],
                "jenis_hewan": pet[3],
                "tanggal_ditemukan": pet[4],
                "lokasi_gambar": pet[5],
                "id_admin": pet[6]
            }
            simpan_pets.append(pet_dict)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    return simpan_pets

def get_pet_id(id):
    cur = conn.cursor()
    try:
        # %s adalah placeholder. Jika ada 2 placeholder maka harus ada 2 parameter, harus urut dan harus tuple
        cur.execute("SELECT id, image, name, bio, status, date_discovered, image FROM pets WHERE id = %s", (id,))
        pet = cur.fetchone()

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    if pet is None:
        return None

    # Convert tuple to dictionary
    return {
        "id": pet[0],
        "image": pet[1],
        "name": pet[2],
        "bio": pet[3],
        "status": pet[4],
        "date_discovered": pet[5]
    }

def upload_gambar(id_binatang, lokasi_gambar):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO gambar (id_binatang,lokasi_gambar) VALUES (%s, %s)", (id_binatang,lokasi_gambar))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def edit_gambar(id_gambar: int, lokasi_gambar: str):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE gambar SET lokasi_gambar =%s WHERE id_gambar =%s", (lokasi_gambar,id_gambar))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
#Belum selesai
def del_gambar(id_gambar: int, id_binatang):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM gambar WHERE id_gambar = %s', (id_gambar,id_binatang,))
        pet = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
        
    if pet is None:
        return None
