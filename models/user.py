from db import conn

def login_model(email, password):
    connection = conn.cursor()
    try:
        connection.execute('SELECT email, password, id_admin from admin WHERE email = %s AND password = %s',(email,password))
        item = connection.fetchone()
        conn.commit()
        if item is None:
            return None
        return{
            'email':item[0],
            'id_admin':item[2]
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()

def find_id_user(id_admin: int):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_admin, username, password, nama_lengkap, email FROM admin WHERE id_admin=%s",(id_admin,))
        item = cursor.fetchone()
        
        if item is None:
            return None

        return {
            "id_admin": item[0],
            "username": item[1],
            "password": item[2],
            "nama_lengkap": item[3],
            "email": item[4],
        }

def register(username: str, password: str, nama_lengkap: str, email: str):
    connection = conn.cursor()
    try:
        connection.execute('INSERT INTO admin (username, password, nama_lengkap, email) VALUES (%(username)s, %(password)s, %(nama_lengkap)s, %(email)s)',
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
        connection.close()

def edit_user(id_admin, username: str, password: str, nama_lengkap: str, email: str):
    connection = conn.cursor()
    try:
        connection.execute("UPDATE admin SET username=%s, password=%s, nama_lengkap=%s, email=%s WHERE id_admin=%s", (username, password, nama_lengkap, email, id_admin))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()
        
def del_user(id_admin: int):
    connection = conn.cursor()
    try:
        connection.execute('DELETE FROM admin WHERE id_admin = %s', (id_admin,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection.close()