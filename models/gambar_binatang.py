from db import conn  # Import koneksi database

# Fungsi untuk mendapatkan semua data gambar
def get_all_gambar():
    with conn.cursor() as cursor:  # Membuat kursor database
        cursor.execute("SELECT id_gambar, lokasi_gambar, id_binatang FROM gambar")  # Eksekusi query SQL
        items = []  # Inisialisasi list untuk menyimpan data gambar
        for item in cursor.fetchall():  # Loop melalui setiap baris hasil
            # Tambahkan data gambar ke dalam list
            items.append({
                "id_gambar": item[0],
                "lokasi_gambar": item[1],
                "id_binatang": item[2],
            })
        return items  # Kembalikan list data gambar

# Fungsi untuk menemukan data gambar berdasarkan ID
def find_id_gambar(id_gambar: int):
    with conn.cursor() as cursor:  # Membuat kursor database
        cursor.execute("SELECT id_gambar, lokasi_gambar, id_binatang FROM gambar WHERE id_gambar=%s", (id_gambar,))  # Eksekusi query SQL dengan parameter ID
        item = cursor.fetchone()  # Ambil satu baris hasil
        if item is None:
            return None  # Kembalikan None jika tidak ditemukan
        
        # Buat kamus dari baris hasil
        return {
            "id_gambar": item[0],
            "lokasi_gambar": item[1],
            "id_binatang": item[2],
        }

# Fungsi untuk mengunggah gambar baru
def upload_gambar(id_binatang, lokasi_gambar):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk mengunggah gambar baru
        connection.execute("INSERT INTO gambar (id_binatang,lokasi_gambar) VALUES (%s, %s)", (id_binatang,lokasi_gambar))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk mengedit data gambar
def edit_gambar(id_gambar: int, lokasi_gambar: str):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk mengedit data gambar
        connection.execute("UPDATE gambar SET lokasi_gambar =%s WHERE id_gambar =%s", (lokasi_gambar,id_gambar))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk menghapus data gambar
def del_gambar(id_gambar: int):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menghapus data gambar
        connection.execute('DELETE FROM gambar WHERE id_gambar = %s', (id_gambar,))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai
