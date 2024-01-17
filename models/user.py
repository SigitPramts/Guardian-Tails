from db import conn

def register(username: str, password: str, nama_lengkap: str, email: str):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO admin (username, password, nama_lengkap, email) VALUES (%(username)s, %(password)s, %(nama_lengkap)s, %(email)s)',
                    {
                        "username":username,
                        "password":password,
                        "nama_lengkap":nama_lengkap,
                        "email":email,
                    },)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def edit_user(id_admin, username: str, password: str, nama_lengkap: str, email: str):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE admin SET username=%s, password=%s, nama_lengkap=%s, email=%s WHERE id_admin=%s", (username, password, nama_lengkap, email, id_admin))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def del_user(id_admin: int):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM admin WHERE id_admin = %s', (id_admin,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()