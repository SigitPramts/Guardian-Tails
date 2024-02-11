from db import conn

def get_all_penyelamatan():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_penyelamatan, tanggal_penyelamatan, lokasi_penyelamatan, nama_penyelamatan, id_binatang, id_admin FROM penyelamatan")
        items = []
        for item in cursor.fetchall():
            items.append({
                "id_penyelamatan": item[0],
                "tanggal_penyelamatan": item[1],
                "lokasi_penyelamatan": item[2],
                "nama_penyelamatan": item[3],
                "id_binatang": item[4],
                "id_admin": item[5]
            })
        return items
    
def find_id_penyelamatan(id_penyelamatan: int):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_penyelamatan, tanggal_penyelamatan, lokasi_penyelamatan, nama_penyelamatan, id_binatang, id_admin FROM penyelamatan WHERE id_penyelamatan=%s", (id_penyelamatan,))
        item = cursor.fetchone()
        if item is None:
            return None
        
        return {"id_penyelamatan": item[0], "tanggal_penyelamatan": item[1], "lokasi_penyelamatan": item[2], "nama_penyelamatan": item[3], "id_binatang": item[4], "id_admin": item[5]}

def new_penyelamatan(lokasi_penyelamatan: str, nama_penyelamatan: str, id_binatang: int, id_admin: int):
    connection = conn.cursor()
    try:
        connection.execute('INSERT INTO penyelamatan (lokasi_penyelamatan, nama_penyelamatan, id_binatang, id_admin) VALUES (%(lokasi_penyelamatan)s, %(nama_penyelamatan)s, %(id_binatang)s, %(id_admin)s)',
                    {
                        "lokasi_penyelamatan": lokasi_penyelamatan,
                        "nama_penyelamatan": nama_penyelamatan,
                        "id_binatang": id_binatang,
                        "id_admin": id_admin
                    })
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()

def edit_penyelamatan(id_penyelamatan, lokasi_penyelamatan: str, nama_penyelamatan: str, id_binatang: int, id_admin):
    connection = conn.cursor()
    try:
        connection.execute('UPDATE penyelamatan SET lokasi_penyelamatan =%s, nama_penyelamatan =%s, id_binatang =%s, id_admin =%s WHERE id_penyelamatan = %s',(lokasi_penyelamatan,nama_penyelamatan,id_binatang,id_penyelamatan,id_admin))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()

def del_penyelamatan(id_penyelamatan, id_admin):
    connection = conn.cursor()
    try:
        connection.execute('DELETE FROM penyelamatan WHERE id_penyelamatan = %s AND id_admin = %s', (id_penyelamatan,id_admin))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()