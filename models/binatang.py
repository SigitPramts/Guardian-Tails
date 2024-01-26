from db import conn

'''def get_all_binatang():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, tanggal_ditemukan, id_admin FROM binatang")
        items = []
        for item in cursor.fetchall():
            items.append({
                "id_binatang": item[0],
                "nama_binatang": item[1],
                "jenis_kelamin": item[2],
                "jenis_hewan": item[3],
                "tanggal_ditemukan": item[4],
                "id_admin": item[5]
            })
        return items'''
    
def get_all_binatang(page: int, limit: int, keyword: str = None):
    connection = conn.cursor()

    try:
        page = (page - 1) * limit
        wherekeyword = ""
        values = {"limit": limit, "offset": page}

        if keyword is not None:
            wherekeyword = " WHERE nama_binatang ILIKE %(keyword)s "
            values['keyword'] = '%' + keyword + '%'

        query = """
                SELECT id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, tanggal_ditemukan, id_admin
                FROM binatang
                """ + wherekeyword + """
                ORDER BY id_binatang
                LIMIT %(limit)s
                OFFSET %(offset)s
                """
        print(query, values)
        connection.execute(query, values)
        binatang = connection.fetchall()
        result = []  # Buat daftar baru untuk menyimpan kamus

        for row in binatang:
            new_binatang = {
                "id_binatang": row[0],
                "nama_binatang": row[1],
                "jenis_kelamin": row[2],
                "jenis_hewan": row[3],
                "tanggal_ditemukan": str(row[4]),  # Konversi tanggal menjadi string jika diperlukan
                "id_admin": row[5]
            }
            result.append(new_binatang)

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()

    return result

    
def find_id_binatang(id_binatang: int):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_binatang, nama_binatang, jenis_kelamin, jenis_hewan, tanggal_ditemukan, id_admin FROM binatang WHERE id_binatang=%s",(id_binatang,))
        item = cursor.fetchone()
        
        if item is None:
            return None

        return {
            "id_binatang": item[0],
            "nama_binatang": item[1],
            "jenis_kelamin": item[2],
            "jenis_hewan": item[3],
            "tanggal_ditemukan": item[4],
            "id_admin": item[5]
        }

def new_binatang(nama_binatang: str, jenis_kelamin: str, jenis_hewan: str, id_admin: int):
    connection = conn.cursor()
    try:
        connection.execute("INSERT INTO binatang (nama_binatang, jenis_kelamin, jenis_hewan, id_admin) VALUES (%(nama_binatang)s, %(jenis_kelamin)s, %(jenis_hewan)s, %(id_admin)s)",
                    {
                        "nama_binatang":nama_binatang,
                        "jenis_kelamin":jenis_kelamin,
                        "jenis_hewan":jenis_hewan,
                        "id_admin":id_admin
                    })
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()

def edit_binatang(id_binatang, nama_binatang: str, jenis_kelamin: str, jenis_hewan: str, id_admin: int):
    connection = conn.cursor()
    try:
        connection.execute('UPDATE binatang SET nama_binatang =%s, jenis_kelamin =%s, jenis_hewan =%s, id_admin =%s WHERE id_binatang = %s',(nama_binatang,jenis_kelamin,jenis_hewan,id_admin,id_binatang))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()

def del_binatang(id_binatang):
    connection = conn.cursor()
    try:
        connection.execute('DELETE FROM binatang WHERE id_binatang = %s', (id_binatang,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()