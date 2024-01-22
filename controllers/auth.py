from flask import request
from flask_jwt_extended import create_access_token

from models import login
from models import user 

from controllers.validator import ValidateError, validate_register

#----------------------------------------------------------------------------
#Login
def login_controller():
    email = request.form.get("email")
    password = request.form.get("password")
    
    login_controller = login.login_model(email,password)
    if login_controller:
        access_token = create_access_token(identity=email)
        return{"Login berhasil": access_token}
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

def edit_user(id_admin: int):
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        nama_lengkap = request.form.get('nama_lengkap')
        email = request.form.get('email')

        validate = validate_register (username, password, nama_lengkap, email)
        if validate is not None:
            return validate, 404

        user.edit_user(id_admin, username, password, nama_lengkap, email)
        return {"msg":"Admin berhasil diubah"}, 200
    except ValidateError as e:
        return str(e), 400

def del_user(id_admin: int):
    user.del_user(id_admin)
    return {"msg": "Berhasil dihapus"}, 404