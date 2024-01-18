from db import conn

def get_all_gambar():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_gambar, lokasi_gambar, id_binatang FROM gambar")
        items = []
        for item in cursor.fetchall():
            items.append({
                "id_gambar": item[0],
                "lokasi_gambar": item[1],
                "id_binatang": item[2],
            })
        return items

def find_id_gambar(id_gambar: int):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_gambar, lokasi_gambar, id_binatang FROM gambar WHERE id_gambar=%s", (id_gambar,))
        item = cursor.fetchone()
        
        if item is None:
            return None

        return {
            "id_gambar": item[0],
            "lokasi_gambar": item[1],
            "id_binatang": item[2],
        }

def upload_gambar(id_binatang, lokasi_gambar):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO gambar (id_binatang,lokasi_gambar) VALUES (%s, %s)", (id_binatang,lokasi_gambar))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def edit_gambar(id_gambar: int, lokasi_gambar: str):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE gambar SET lokasi_gambar =%s WHERE id_gambar =%s", (lokasi_gambar,id_gambar))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        
def del_gambar(id_gambar: int):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM gambar WHERE id_gambar = %s', (id_gambar,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
