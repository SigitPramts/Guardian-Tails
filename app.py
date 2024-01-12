from flask import Flask, request, render_template, jsonify
import os, time, db
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
 
    get_jwt_identity,
)
import logging
import pets
from validator import validate_register, ValidateError
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "secret key boleh random"
jwt = JWTManager(app)

#Login Done
@app.post("/login")
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if pets.auth(email, password) is None:
        return {"msg":"Email atau password tidak benar"}
    
    access_token = create_access_token(identity=email)
    return{"access_token":access_token}, 200

#Register Done
@app.post("/register")
def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        nama_lengkap = request.form.get('nama_lengkap')
        email = request.form.get('email')

        validate_register(username, password, nama_lengkap, email)
        pets.register(username, password, nama_lengkap, email)
        return "", 202
    except ValidateError as e:
        return str(e), 401


@app.get("/pets")
def get_pets():
    return pets.get_pets()

@app.get('/pets/<int:id>')
def get_pet_id(id):
    pet = pets.get_pet_id(id)
    if pet is None:
        return "", 404
    return pet

@app.post("/")
def new_pet():
    if "file" not in request.files:
        return "No file part"
    
    file = request.files["file"]

    if file.filename == "":
        return "No selected file"
    
    if file.content_type not in [
        "image/jpeg",
        "image/jpg",
        "image/webp",
        "image/png"
    ]:
        return "File type not allowed"
    
    image = "static/images/" + str(time.time()) + "_" + file.filename
    file.save(image)

    conn = db.conn.cursor()
    conn.execute("INSERT INTO images (image) VALUES (%s)", (image,))
    db.conn.commit()
    conn.close()
    return {"msg": "Hewan baru berhasil ditambah"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=True)