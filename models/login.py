from db import conn

def login_model(email, password):
    connection = conn.cursor()
    try:
        connection.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
        item = connection.fetchone()
        conn.commit()
        if item is None:
            return None
        return{
            'email':item[0],
            'password':item[1]
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()