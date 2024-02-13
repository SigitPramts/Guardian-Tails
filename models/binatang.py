from db import conn  #Import koneksi database

def get_all_binatang(page: int, limit: int, id_admin: int, keyword: str = None):
    connection = conn.cursor()  #Membuat kursor database

    try:
        page = (page - 1) * limit  #Menghitung offset
        wherekeyword = ""  #Inisialisasi string klausul WHERE
        values = {"limit": limit, "offset": page, "id_admin": id_admin}  #Nilai parameter

        if keyword is not None:
            wherekeyword = " WHERE nama_binatang ILIKE %(keyword)s "  #Menyiapkan klausul WHERE jika ada keyword
            values['keyword'] = '%' + keyword + '%'  #Menyiapkan nilai parameter untuk pencarian

        #Query SQL untuk mendapatkan data binatang
        query = """
                SELECT id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, tanggal_ditemukan, id_admin
                FROM binatang WHERE id_admin= %(id_admin)s
                """ + wherekeyword + """ 
                ORDER BY id_binatang
                LIMIT %(limit)s
                OFFSET %(offset)s
                """
        print(query, values)  #Cetak query SQL dan nilai parameter
        connection.execute(query, values)  #Eksekusi query SQL dengan parameter
        binatang = connection.fetchall()  #Ambil semua baris hasil query
        result = []  #Inisialisasi list untuk menyimpan hasil

        #Loop melalui setiap baris hasil dan buat kamus untuk setiap baris
        for row in binatang:
            new_binatang = {
                "id_binatang": row[0],
                "nama_binatang": row[1],
                "jenis_kelamin": row[2],
                "jenis_hewan": row[3],
                "tanggal_ditemukan": str(row[4]),  #Konversi tanggal ke string 
                "id_admin": row[5]
            }
            result.append(new_binatang)  #Tambahkan kamus ke dalam list hasil

    except Exception as e:
        conn.rollback()  #Lakukan rollback jika terjadi kesalahan
        raise e  #Angkat kembali kesalahan
    finally:
        connection.close()  #Tutup koneksi database setelah selesai

    return result  #Kembalikan hasil pencarian

#Fungsi untuk menemukan binatang berdasarkan ID
def find_id_binatang(id_binatang: int):
    with conn.cursor() as cursor:  #Membuat kursor database
        cursor.execute("SELECT id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, tanggal_ditemukan, id_admin FROM binatang WHERE id_binatang=%s",(id_binatang,))
        item = cursor.fetchone()  #Ambil satu baris hasil
        
        if item is None:
            return None  #Kembalikan None jika tidak ditemukan

        #Buat kamus dari baris hasil
        return {
            "id_binatang": item[0],
            "nama_binatang": item[1],
            "jenis_kelamin": item[2],
            "jenis_hewan": item[3],
            "tanggal_ditemukan": item[4],
            "id_admin": item[5]
        }

#Fungsi untuk menambahkan binatang baru
def new_binatang(nama_binatang: str, jenis_kelamin: str, jenis_hewan: str, id_admin: int):
    connection = conn.cursor()  #Membuat kursor database
    try:
        #Eksekusi pernyataan SQL untuk menambahkan binatang baru
        connection.execute("INSERT INTO binatang (nama_binatang, jenis_kelamin, jenis_hewan, id_admin) VALUES (%(nama_binatang)s, %(jenis_kelamin)s, %(jenis_hewan)s, %(id_admin)s)",
                    {
                        "nama_binatang":nama_binatang,
                        "jenis_kelamin":jenis_kelamin,
                        "jenis_hewan":jenis_hewan,
                        "id_admin":id_admin
                    })
        conn.commit()  #Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  #Angkat kembali kesalahan
    finally:
        connection.close()  #Tutup koneksi database setelah selesai

#Fungsi untuk mengedit binatang
def edit_binatang(id_binatang, nama_binatang: str, jenis_kelamin: str, jenis_hewan: str, id_admin):
    connection = conn.cursor()  #Membuat kursor database
    try:
        #Eksekusi pernyataan SQL untuk mengedit binatang
        connection.execute('UPDATE binatang SET nama_binatang =%s, jenis_kelamin =%s, jenis_hewan =%s, id_admin =%s WHERE id_binatang = %s',(nama_binatang,jenis_kelamin,jenis_hewan,id_binatang,id_admin))
        conn.commit()  #Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  #Lakukan rollback jika terjadi kesalahan
        raise e  #Angkat kembali kesalahan
    finally:
        connection.close()  # utup koneksi database setelah selesai

#Fungsi untuk menghapus binatang
def del_binatang(id_binatang, id_admin):
    connection = conn.cursor()  #Membuat kursor database
    try:
        #Eksekusi pernyataan SQL untuk menghapus binatang
        connection.execute('DELETE FROM binatang WHERE id_binatang = %s AND id_admin = %s', (id_binatang,id_admin))
        conn.commit()  #Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  #Lakukan rollback jika terjadi kesalahan
        raise e  #Angkat kembali kesalahan
    finally:
        connection.close()  #Tutup koneksi database setelah selesai
