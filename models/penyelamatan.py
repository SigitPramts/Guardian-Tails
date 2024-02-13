from db import conn  # Import koneksi database

# Fungsi untuk mendapatkan semua data penyelamatan
def get_all_penyelamatan():
    with conn.cursor() as cursor:  # Membuka kursor database
        cursor.execute("SELECT id_penyelamatan, tanggal_penyelamatan, lokasi_penyelamatan, nama_penyelamatan, id_binatang, id_admin FROM penyelamatan")  # Eksekusi query SQL
        items = []  # Inisialisasi list untuk menyimpan data penyelamatan
        for item in cursor.fetchall():  # Loop melalui setiap baris hasil
            # Tambahkan data penyelamatan ke dalam list
            items.append({
                "id_penyelamatan": item[0],
                "tanggal_penyelamatan": item[1],
                "lokasi_penyelamatan": item[2],
                "nama_penyelamatan": item[3],
                "id_binatang": item[4],
                "id_admin": item[5]
            })
        return items  # Kembalikan list data penyelamatan

# Fungsi untuk menemukan data penyelamatan berdasarkan ID
def find_id_penyelamatan(id_penyelamatan: int):
    with conn.cursor() as cursor:  # Membuka kursor database
        cursor.execute("SELECT id_penyelamatan, tanggal_penyelamatan, lokasi_penyelamatan, nama_penyelamatan, id_binatang, id_admin FROM penyelamatan WHERE id_penyelamatan=%s", (id_penyelamatan,))  # Eksekusi query SQL dengan parameter
        item = cursor.fetchone()  # Ambil satu baris hasil
        if item is None:
            return None  # Kembalikan None jika tidak ditemukan
        
        # Buat kamus dari baris hasil
        return {
            "id_penyelamatan": item[0],
            "tanggal_penyelamatan": item[1],
            "lokasi_penyelamatan": item[2],
            "nama_penyelamatan": item[3],
            "id_binatang": item[4],
            "id_admin": item[5]
        }

# Fungsi untuk menambahkan data penyelamatan baru
def new_penyelamatan(lokasi_penyelamatan: str, nama_penyelamatan: str, id_binatang: int, id_admin: int):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menambahkan data penyelamatan baru
        connection.execute('INSERT INTO penyelamatan (lokasi_penyelamatan, nama_penyelamatan, id_binatang, id_admin) VALUES (%(lokasi_penyelamatan)s, %(nama_penyelamatan)s, %(id_binatang)s, %(id_admin)s)',
                    {
                        "lokasi_penyelamatan": lokasi_penyelamatan,
                        "nama_penyelamatan": nama_penyelamatan,
                        "id_binatang": id_binatang,
                        "id_admin": id_admin
                    })
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk mengedit data penyelamatan
def edit_penyelamatan(id_penyelamatan, lokasi_penyelamatan: str, nama_penyelamatan: str, id_binatang: int, id_admin):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk mengedit data penyelamatan
        connection.execute('UPDATE penyelamatan SET lokasi_penyelamatan =%s, nama_penyelamatan =%s, id_binatang =%s, id_admin =%s WHERE id_penyelamatan = %s',(lokasi_penyelamatan,nama_penyelamatan,id_binatang,id_penyelamatan,id_admin))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk menghapus data penyelamatan
def del_penyelamatan(id_penyelamatan, id_admin):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menghapus data penyelamatan
        connection.execute('DELETE FROM penyelamatan WHERE id_penyelamatan = %s AND id_admin = %s', (id_penyelamatan,id_admin))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai
