from db import conn

def login_model(email, password):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
        item = cur.fetchone()
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