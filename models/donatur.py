from db import conn  # Import koneksi database

# Fungsi untuk mendapatkan semua data donatur
def get_all_donatur():
    with conn.cursor() as cursor:  # Membuat kursor database
        cursor.execute("SELECT id_donatur, nama_donatur, email_donatur, jumlah_donasi, id_kegiatan FROM donatur")  # Eksekusi query SQL
        items = []  # Inisialisasi list untuk menyimpan data donatur
        for item in cursor.fetchall():  # Loop melalui setiap baris hasil
            # Tambahkan data donatur ke dalam list
            items.append({
                "id_donatur": item[0],
                "nama_donatur": item[1],
                "email_donatur": item[2],
                "jumlah_donasi": item[3],
                "id_kegiatan": item[4]
            })
        return items  # Kembalikan list data donatur

# Fungsi untuk menemukan data donatur berdasarkan ID
def find_id_donatur(id_donatur: int):
    with conn.cursor() as cursor:  # Membuat kursor database
        cursor.execute("SELECT id_donatur, nama_donatur, email_donatur, jumlah_donasi, id_kegiatan FROM donatur WHERE id_donatur=%s", (id_donatur,))  # Eksekusi query SQL dengan parameter ID
        item = cursor.fetchone()  # Ambil satu baris hasil
        if item is None:
            return None  # Kembalikan None jika tidak ditemukan
        
        # Buat kamus dari baris hasil
        return {"id_donatur": item[0], "nama_donatur": item[1], "email_donatur": item[2], "jumlah_donasi": item[3], "id_kegiatan": item[4]}

# Fungsi untuk menambahkan data donatur baru
def new_donatur(nama_donatur: str, email_donatur: str, jumlah_donasi: int, id_kegiatan: int):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menambahkan data donatur baru
        connection.execute('INSERT INTO donatur (nama_donatur, email_donatur, jumlah_donasi, id_kegiatan) VALUES (%(nama_donatur)s, %(email_donatur)s, %(jumlah_donasi)s, %(id_kegiatan)s)',
                    {
                        "nama_donatur":nama_donatur,
                        "email_donatur":email_donatur,
                        "jumlah_donasi":jumlah_donasi,
                        "id_kegiatan": id_kegiatan,
                    },)
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk mengedit data donatur
def edit_donatur(id_donatur, nama_donatur: str, email_donatur: str, jumlah_donasi: int, id_kegiatan):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk mengedit data donatur
        connection.execute('UPDATE donatur SET nama_donatur =%s, email_donatur =%s, jumlah_donasi =%s, id_kegiatan =%s WHERE id_donatur = %s',(nama_donatur,email_donatur,jumlah_donasi,id_kegiatan,id_donatur))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk menghapus data donatur
def del_donatur(id_donatur):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menghapus data donatur
        connection.execute('DELETE FROM donatur WHERE id_donatur = %s', (id_donatur,))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai
