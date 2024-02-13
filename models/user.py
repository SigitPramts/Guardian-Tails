from db import conn  # Import koneksi database
from flask_bcrypt import Bcrypt  # Import modul Flask-Bcrypt untuk enkripsi dan dekripsi password

# Fungsi untuk melakukan login
def login_model(email, password):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi query SQL untuk mendapatkan informasi pengguna berdasarkan email
        connection.execute('SELECT email, password, id_admin FROM admin WHERE email = %s', (email,))
        user = connection.fetchone()  # Ambil satu baris hasil
        
        if user:  # Jika pengguna ditemukan
            hash_password = user[1]  # Ambil password terenkripsi dari hasil query
            bcrypt = Bcrypt()  # Buat objek Bcrypt
            if bcrypt.check_password_hash(hash_password, password):  # Periksa apakah password yang dimasukkan sesuai dengan yang terenkripsi
                return {
                    'email': user[0],
                    'id_admin': user[2]
                }  # Kembalikan informasi pengguna jika autentikasi berhasil

    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk mencari pengguna berdasarkan ID
def find_id_user(id_admin: int):
    with conn.cursor() as cursor:  # Membuka kursor database
        cursor.execute("SELECT id_admin, username, password, nama_lengkap, email FROM admin WHERE id_admin=%s",(id_admin,))  # Eksekusi query SQL dengan parameter
        item = cursor.fetchone()  # Ambil satu baris hasil
        
        if item is None:
            return None  # Kembalikan None jika tidak ditemukan
        
        # Buat kamus dari baris hasil
        return {
            "id_admin": item[0],
            "username": item[1],
            "password": item[2],
            "nama_lengkap": item[3],
            "email": item[4],
        }

# Fungsi untuk mendaftarkan pengguna baru
def register(username: str, password: str, nama_lengkap: str, email: str):
    connection = conn.cursor()  # Membuat kursor database
    try:
        bcrypt = Bcrypt()  # Buat objek Bcrypt
        hash_pass = bcrypt.generate_password_hash(password).decode('utf-8')  # Enkripsi password
        # Eksekusi pernyataan SQL untuk menambahkan pengguna baru
        connection.execute('INSERT INTO admin (username, password, nama_lengkap, email) VALUES (%(username)s, %(password)s, %(nama_lengkap)s, %(email)s)',
                    {
                        "username":username,
                        "password":hash_pass,
                        "nama_lengkap":nama_lengkap,
                        "email":email,
                    },)
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk mengedit informasi pengguna
def edit_user(id_admin, username: str, password: str, nama_lengkap: str, email: str):
    connection = conn.cursor()  # Membuat kursor database
    try:
        bcrypt = Bcrypt()  # Buat objek Bcrypt
        hash_pass = bcrypt.generate_password_hash(password).decode('utf-8')  # Enkripsi password
        # Eksekusi pernyataan SQL untuk mengedit informasi pengguna
        connection.execute("UPDATE admin SET username=%s, password=%s, nama_lengkap=%s, email=%s WHERE id_admin=%s", (username, hash_pass, nama_lengkap, email, id_admin))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk menghapus pengguna
def del_user(id_admin: int):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk menghapus pengguna
        connection.execute('DELETE FROM admin WHERE id_admin = %s', (id_admin,))
        conn.commit()  # Commit transaksi jika berhasil
    except Exception as e:
        conn.rollback()  # Lakukan rollback jika terjadi kesalahan
        raise e  # Angkat kembali kesalahan
    finally:
        connection.close()  # Tutup koneksi database setelah selesai

# Fungsi untuk memeriksa apakah username dan email unik
def is_username_email_unique(username, email):
    connection = conn.cursor()  # Membuat kursor database
    try:
        # Eksekusi pernyataan SQL untuk memeriksa apakah username atau email sudah digunakan
        connection.execute('SELECT COUNT(*) FROM admin WHERE username = %(username)s OR email = %(email)s', {"username": username, "email": email})
        result = connection.fetchone()  # Ambil satu baris hasil
        return result[0] == 0  # Kembalikan True jika username dan email unik
    finally:
        connection.close()  # Tutup koneksi database setelah selesai
