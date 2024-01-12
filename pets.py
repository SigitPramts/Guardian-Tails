from db import conn
from flask import request
from psycopg2.errors import DatabaseError


def get_pets():
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, image, name, bio, status, date_discovered, image FROM pets")
        pets = cur.fetchall()

        # Convert tuple to dictionary
        # Karena python mereturn tipe data tuple. Maka kita harus mengubahnya menjadi dictionary
        new_pets = []
        for pet in pets:
            new_todo = {
                "id": pet[0],
                "image": pet[1],
                "name": pet[2],
                "bio": pet[3],
                "status": pet[4],
                "date_discovered": pet[5]
            }
            new_pets.append(new_todo)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    return new_pets

def get_pet_id(id):
    cur = conn.cursor()
    try:
        # %s adalah placeholder. Jika ada 2 placeholder maka harus ada 2 parameter, harus urut dan harus tuple
        cur.execute("SELECT id, image, name, bio, status, date_discovered, image FROM pets WHERE id = %s", (id,))
        pet = cur.fetchone()

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

    if pet is None:
        return None

    # Convert tuple to dictionary
    return {
        "id": pet[0],
        "image": pet[1],
        "name": pet[2],
        "bio": pet[3],
        "status": pet[4],
        "date_discovered": pet[5]
    }

def new_pet(nama: str, bio: str, status: str):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO test (nama, bio, status) VALUES (%(nama)s, %(bio)s, %(status)s)',
            {
                "nama": nama,
                "bio": bio,
                "status": status,
            },
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def auth(email, password):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
        pets = cur.fetchone()
        conn.commit()
        if pets is None:
            return None
        return{
            'email':pets[0],
            'password':pets[1]
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

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