from db import conn  # Import koneksi database

# Fungsi untuk mendapatkan semua data kegiatan
def get_all_kegiatan():
    with conn.cursor() as cursor:  # Membuat kursor database
        cursor.execute("SELECT id_kegiatan, jenis_kegiatan, tanggal_kegiatan, lokasi_kegiatan, id_admin FROM kegiatan")  # Eksekusi query SQL
        items = []  # Inisialisasi list untuk menyimpan data kegiatan
        for item in cursor.fetchall():  # Loop melalui setiap baris hasil
            # Tambahkan data kegiatan ke dalam list
            items.append({
                "id_kegiatan": item[0],
                "jenis_kegiatan": item[1],
                "tanggal_kegiatan": item[2],
                "lokasi_kegiatan": item[3],
                "id_admin": item[4]
            })
        return items  # Kembalikan list data kegiatan

# Fungsi untuk menemukan data kegiatan berdasarkan ID
def find_by_id(id_kegiatan: int):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menemukan data kegiatan berdasarkan ID
        connection.execute("SELECT id_kegiatan, jenis_kegiatan, tanggal_kegiatan, lokasi_kegiatan, id_admin FROM kegiatan WHERE id_kegiatan=%s", (id_kegiatan,))
        item = connection.fetchone()  # Ambil satu baris hasil
        if item is None:
            return None  # Kembalikan None jika tidak ditemukan

        # Buat kamus dari baris hasil
        return {
            "id_kegiatan": item[0],
            "jenis_kegiatan": item[1],
            "tanggal_kegiatan": item[2],
            "lokasi_kegiatan": item[3],
            "id_admin": item[4]
        }
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk menambahkan kegiatan baru
def new_kegiatan(jenis_kegiatan: str, lokasi_kegiatan: str, id_admin: int):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menambahkan kegiatan baru
        connection.execute('INSERT INTO kegiatan (jenis_kegiatan, lokasi_kegiatan, id_admin) VALUES (%(jenis_kegiatan)s, %(lokasi_kegiatan)s, %(id_admin)s)',
                    {
                        "jenis_kegiatan":jenis_kegiatan,
                        "lokasi_kegiatan":lokasi_kegiatan,
                        "id_admin":id_admin
                    },)
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk mengedit data kegiatan
def edit_kegiatan(id_kegiatan, jenis_kegiatan: str, lokasi_kegiatan: str, id_admin):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk mengedit data kegiatan
        connection.execute('UPDATE kegiatan SET jenis_kegiatan = %s, lokasi_kegiatan = %s WHERE id_kegiatan = %s AND id_admin = %s', (jenis_kegiatan, lokasi_kegiatan, id_kegiatan, id_admin,))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk menghapus data kegiatan
def del_kegiatan(id_kegiatan, id_admin):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menghapus data kegiatan
        connection.execute('DELETE FROM kegiatan WHERE id_kegiatan = %s AND id_admin = %s', (id_kegiatan,id_admin))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai
