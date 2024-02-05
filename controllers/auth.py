#error
from flask import request
from flask_jwt_extended import get_jwt_identity, create_access_token
from flask_jwt_extended import jwt_required
from models import user 
from models.user import find_id_user 

from validator.auth import ValidateError, validate_register

#----------------------------------------------------------------------------

def ambil_data_user_controller():
    try:
        admin_saat_ini = get_jwt_identity()['id_admin']
        return find_id_user(admin_saat_ini)
    except Exception as e:
        raise e

def protected_controller():
    admin_saat_ini = get_jwt_identity()
    return {'login as': admin_saat_ini["username"]},200

#Login
def login_controller():
    email = request.form.get("email")
    password = request.form.get("password")
    
    login_controller = user.login_model(email=email,password=password)
    if login_controller:
        access_token = create_access_token(identity={'id_admin':login_controller['id_admin'],'email':login_controller['email']})
        return{"token": access_token}
    return("Email atau password salah"), 404


#----------------------------------------------------------------------------
#User
def register_controller():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        nama_lengkap = request.form.get('nama_lengkap')
        email = request.form.get('email')

        validate = validate_register (username, password, nama_lengkap, email)
        if validate is not None:
            return validate, 404

        user.register(username, password, nama_lengkap, email)
        return {"msg":"Admin berhasil ditambah"}, 200
    except ValidateError as e:
        return str(e), 400

@jwt_required()
def edit_user():
    try:
        admin_saat_ini = get_jwt_identity().get('id_admin')
        username = request.form.get('username')
        password = request.form.get('password')
        nama_lengkap = request.form.get('nama_lengkap')
        email = request.form.get('email')

        user.edit_user(admin_saat_ini, username, password, nama_lengkap, email)
        return {"msg": "Admin berhasil diubah"}, 200
    except ValidateError as e:
        return str(e), 400

@jwt_required()
def del_user():
    try:
        admin_saat_ini = get_jwt_identity()['id_admin']
        user.del_user(admin_saat_ini)
        return {"msg": "Berhasil dihapus"}, 404
    except Exception as e:
        raise e