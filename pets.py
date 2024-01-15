from db import conn
import time
from flask import request
from psycopg2.errors import DatabaseError

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

def upload_gambar(lokasi_gambar):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO gambar (lokasi_gambar) VALUES (%s)", (lokasi_gambar))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

#----------------------------------------------------------------------------
#Login Done
def auth(email, password):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
        pets = cur.fetchone()
        conn.commit()
        if pets is None:
            return None
        return{
            'email':pets[0],
            'password':pets[1]
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

#Register Done
def register(username: str, password: str, nama_lengkap: str, email: str):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO admin (username, password, nama_lengkap, email) VALUES (%(username)s, %(password)s, %(nama_lengkap)s, %(email)s)',
                    {
                        "username":username,
                        "password":password,
                        "nama_lengkap":nama_lengkap,
                        "email":email,
                    },)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

#----------------------------------------------------------------------------
def new_donatur(nama_donatur: str, email_donatur: str, jumlah_donasi: int):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO donatur (nama_donatur, email_donatur, jumlah_donasi) VALUES (%(nama_donatur)s, %(email_donatur)s, %(jumlah_donasi)s)',
                    {
                        "nama_donatur":nama_donatur,
                        "email_donatur":email_donatur,
                        "jumlah_donasi":jumlah_donasi,
                    },)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def edit_donatur(id_donatur, nama_donatur: str, email_donatur: str, jumlah_donasi: int):
    cur = conn.cursor()
    try:
        cur.execute('UPDATE donatur SET nama_donatur =%s, email_donatur =%s, jumlah_donasi =%s WHERE id_donatur = %s',(nama_donatur,email_donatur,jumlah_donasi,id_donatur))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def del_donatur(id_donatur):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM donatur WHERE id_donatur = %s', (id_donatur,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


#----------------------------------------------------------------------------
def new_kegiatan(jenis_kegiatan: str, lokasi_kegiatan: str):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO kegiatan (jenis_kegiatan, lokasi_kegiatan) VALUES (%(jenis_kegiatan)s, %(lokasi_kegiatan)s)',
                    {
                        "jenis_kegiatan":jenis_kegiatan,
                        "lokasi_kegiatan":lokasi_kegiatan,
                    },)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def edit_kegiatan(id_kegiatan, jenis_kegiatan: str, lokasi_kegiatan: str):
    cur = conn.cursor()
    try:
        cur.execute('UPDATE kegiatan SET jenis_kegiatan =%s, lokasi_kegiatan =%s WHERE id_kegiatan = %s',(jenis_kegiatan,lokasi_kegiatan,id_kegiatan))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def del_kegiatan(id_kegiatan):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM kegiatan WHERE id_kegiatan = %s', (id_kegiatan,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


#----------------------------------------------------------------------------
def new_penyelamatan(lokasi_penyelamatan: str, nama_penyelamatan: str):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO penyelamatan (lokasi_penyelamatan, nama_penyelamatan) VALUES (%(lokasi_penyelamatan)s, %(nama_penyelamatan)s)',
                    {
                        "lokasi_penyelamatan":lokasi_penyelamatan,
                        "nama_penyelamatan":nama_penyelamatan,
                    },)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def edit_penuyelamatan(id_penyelamatan, lokasi_penyelamatan: str, nama_penyelamatan: str):
    cur = conn.cursor()
    try:
        cur.execute('UPDATE penyelamatan SET lokasi_penyelamatan =%s, nama_penyelamatan =%s WHERE id_penyelamatan = %s',(lokasi_penyelamatan,nama_penyelamatan,id_penyelamatan))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def del_penyelamatan(id_penyelamatan):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM penyelamatan WHERE id_penyelamatan = %s', (id_penyelamatan,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()