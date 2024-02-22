#error
from flask import request
from flask_jwt_extended import get_jwt_identity, create_access_token
from flask_jwt_extended import jwt_required
from models import user 
from models.user import find_id_user 

from validator.auth import ValidateError, validate_register, validate_edit

#----------------------------------------------------------------------------

def ambil_data_user_controller():
    try:
        #Mengambil identitas pengguna dari token JWT yang sedang digunakan
        admin_saat_ini = get_jwt_identity()['id_admin']
        return find_id_user(admin_saat_ini)
    except Exception as e:
        raise e

def protected_controller():
    #Mengambil identitas pengguna dari token JWT yang sedang digunakan
    admin_saat_ini = get_jwt_identity()
    return {'login as': admin_saat_ini["username"]},200

#Login
def login_controller():
    #Mengambil inputan user
    email = request.form.get("email")
    password = request.form.get("password")
    
    login_controller = user.login_model(email=email,password=password)

    #Jika valid maka akan membuat token akses bagi pengguna
    if login_controller:
        access_token = create_access_token(identity={'id_admin':login_controller['id_admin'],'email':login_controller['email']})
        return{"token": access_token}
    return{"message":"Email atau password salah"}, 400


#----------------------------------------------------------------------------
#Untuk menambah user baru
def register_controller():
    try:
        #Mengambil inputan user
        username = request.form.get('username')
        password = request.form.get('password')
        nama_lengkap = request.form.get('nama_lengkap')
        email = request.form.get('email')

        #Validasi jika memiliki kesalahan
        validate = validate_register(username, password, nama_lengkap, email, )
        if validate is not None:
            return validate, 404

        #Menambahkan kedalam database
        user.register(username, password, nama_lengkap, email)
        return {"msg": "Admin berhasil ditambah"}, 200
    except ValidateError as e:
        return str(e), 400

#Untuk mengubah data user
@jwt_required() # Memerlukan token JWT untuk mengakses fitur
def edit_user():
    try:
        #Mengambil inputan user
        admin_saat_ini = get_jwt_identity().get('id_admin') #Mengambil user ID dari JWT token
        username = request.form.get('username')
        password = request.form.get('password')
        nama_lengkap = request.form.get('nama_lengkap')
        email = request.form.get('email')

        #Validasi jika memiliki kesalahan
        validate = validate_edit(username, password, nama_lengkap, email, )
        if validate is not None:
            return validate, 404

        #Menambahkan kedalam database
        user.edit_user(admin_saat_ini, username, password, nama_lengkap, email)
        return {"msg": "Admin berhasil diubah"}, 200
    except ValidateError as e:
        return str(e), 400

#Untuk menghapus data user
@jwt_required() # Memerlukan token JWT untuk mengakses fitur
def del_user():
    try:
        admin_saat_ini = get_jwt_identity()['id_admin'] #Mengambil user ID dari JWT token
        user.del_user(admin_saat_ini)
        return {"msg": "Berhasil dihapus"}, 200
    except Exception as e:
        raise e