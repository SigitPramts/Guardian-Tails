from db import conn

def get_all_donatur():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_donatur, nama_donatur, email_donatur, jumlah_donasi, id_kegiatan FROM donatur")
        items = []
        for item in cursor.fetchall():
            items.append({
                "id_donatur": item[0],
                "nama_donatur": item[1],
                "email_donatur": item[2],
                "jumlah_donasi": item[3],
                "id_kegiatan": item[4]
            })
        return items

def find_id_donatur(id_donatur: int):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_donatur, nama_donatur, email_donatur, jumlah_donasi, id_kegiatan FROM donatur WHERE id_donatur=%s", (id_donatur,))
        item = cursor.fetchone()
        if item is None:
            return None
        
        return {"id_donatur": item[0], "nama_donatur": item[1], "email_donatur": item[2], "jumlah_donasi": item[3], "id_kegiatan": item[4]}

def new_donatur(nama_donatur: str, email_donatur: str, jumlah_donasi: int, id_kegiatan: int):
    connection = conn.cursor()
    try:
        connection.execute('INSERT INTO donatur (nama_donatur, email_donatur, jumlah_donasi, id_kegiatan) VALUES (%(nama_donatur)s, %(email_donatur)s, %(jumlah_donasi)s, %(id_kegiatan)s)',
                    {
                        "nama_donatur":nama_donatur,
                        "email_donatur":email_donatur,
                        "jumlah_donasi":jumlah_donasi,
                        "id_kegiatan": id_kegiatan,
                    },)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()

def edit_donatur(id_donatur, nama_donatur: str, email_donatur: str, jumlah_donasi: int, id_kegiatan):
    connection = conn.cursor()
    try:
        connection.execute('UPDATE donatur SET nama_donatur =%s, email_donatur =%s, jumlah_donasi =%s, id_kegiatan =%s WHERE id_donatur = %s',(nama_donatur,email_donatur,jumlah_donasi,id_kegiatan,id_donatur))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()

def del_donatur(id_donatur):
    connection = conn.cursor()
    try:
        connection.execute('DELETE FROM donatur WHERE id_donatur = %s', (id_donatur,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()