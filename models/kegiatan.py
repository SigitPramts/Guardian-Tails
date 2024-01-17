from db import conn

def get_all_kegiatan():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_kegiatan, jenis_kegiatan, tanggal_kegiatan, lokasi_kegiatan, id_admin FROM kegiatan")
        items = []
        for item in cursor.fetchall():
            items.append({
                "id_kegiatan": item[0],
                "jenis_kegiatan": item[1],
                "tanggal_kegiatan": item[2],
                "lokasi_kegiatan": item[3],
                "id_admin": item[4]})
            
        return items    
    
def find_by_id(id_kegiatan: int):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_kegiatan, jenis_kegiatan, tanggal_kegiatan, lokasi_kegiatan, id_admin FROM kegiatan WHERE id_kegiatan=%s", (id_kegiatan,))
        item = cursor.fetchone()
        if item is None:
            return None

        return {"id_kegiatan": item[0], "jenis_kegiatan": item[1], "tanggal_kegiatan": item[2], "lokasi_kegiatan": item[3], "id_admin": item[4]}

def new_kegiatan(jenis_kegiatan: str, lokasi_kegiatan: str, id_admin: int):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO kegiatan (jenis_kegiatan, lokasi_kegiatan, id_admin) VALUES (%(jenis_kegiatan)s, %(lokasi_kegiatan)s, %(id_admin)s)',
                    {
                        "jenis_kegiatan":jenis_kegiatan,
                        "lokasi_kegiatan":lokasi_kegiatan,
                        "id_admin":id_admin
                    },)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
    
def edit_kegiatan(id_kegiatan, jenis_kegiatan: str, lokasi_kegiatan: str, id_admin: int):
    cur = conn.cursor()
    try:
        cur.execute('UPDATE kegiatan SET jenis_kegiatan =%s, lokasi_kegiatan =%s, id_admin =%s WHERE id_kegiatan = %s',(jenis_kegiatan,lokasi_kegiatan,id_admin,id_kegiatan))
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