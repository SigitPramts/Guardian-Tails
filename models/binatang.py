from db import conn

def get_all_binatang():
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
        return items
    
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
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO binatang (nama_binatang, jenis_kelamin, jenis_hewan, id_admin) VALUES (%(nama_binatang)s, %(jenis_kelamin)s, %(jenis_hewan)s, %(id_admin)s)",
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
        cur.close()

def edit_binatang(id_binatang, nama_binatang: str, jenis_kelamin: str, jenis_hewan: str, id_admin: int):
    cur = conn.cursor()
    try:
        cur.execute('UPDATE binatang SET nama_binatang =%s, jenis_kelamin =%s, jenis_hewan =%s, id_admin =%s WHERE id_binatang = %s',(nama_binatang,jenis_kelamin,jenis_hewan,id_admin,id_binatang))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def del_binatang(id_binatang):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM binatang WHERE id_binatang = %s', (id_binatang,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()