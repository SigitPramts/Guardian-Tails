from flask import Flask, request, render_template, jsonify
import os, time
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

import controllers.donatur as donatur
import controllers.kegiatan as kegiatan
import controllers.penyelamatan as penyelamatan

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
    

#----------------------------------------------------------------------------

@app.get("/pets")
def get_binatang():
    return pets.get_binatang()

@app.get('/pets/<int:id>')
def get_pet_id(id):
    pet = pets.get_pet_id(id)
    if pet is None:
        return "", 404
    return pet

#Upload Gambar Done
@app.route("/gambar/<int:id_binatang>", methods=["POST"])
def upload_gambar(id_binatang: int):
    try:
        # Check if the 'file' key exists in request.files
        if "file" not in request.files:
            return "No file part"

        files = request.files.getlist("file")

        # Check if files list is empty
        if not files:
            return "No selected file"

        locations = []

        for file in files:
            # Check file type
            if file.content_type not in ["image/jpeg", "image/jpg", "image/webp", "image/png"]:
                return "File type not allowed"

            location = "static/images/" + str(time.time()) + "_" + file.filename
            file.save(location)
            locations.append(location)

            # Assume you have a function named 'upload_gambar' that takes a list of locations
            pets.upload_gambar(id_binatang,lokasi_gambar=location)

        return {"message": "Upload gambar berhasil"}, 200
    except Exception as e:
        # If an exception occurs, delete the uploaded files
        for location in locations:
            if os.path.exists(location):
                os.remove(location)
        raise e
        
#Edit Gambar Done
@app.route("/gambar/<int:id_gambar>", methods=["PUT"])
def edit_gambar(id_gambar):
    if "file" not in request.files:
        return "no file part"

    files = request.files.getlist("file")

    # Check if the file is selected
    if not files:
        return "No selected files"
    
    pets = {"id_gambar": pets[0], "lokasi_gambar": pets[1]}

    allowed_files = ["image/jpeg", "image/jpg", "image/webp", "image/png"]
    # Check if the file type is allowed
    for file in files:
        if file.content_type not in allowed_files:
            return "File type not allowed"

    # Save the uploaded file to a specific folder
    locations = []
    for file in files:
        location = "static/images/" + str(time.time()) + "_" + file.filename
        file.save(location)
        locations.append(location)
    
    id_gambar = request.form.get("id_gambar")

    try:
        pets.edit_gambar(id_gambar, lokasi_gambar=locations)
    except Exception as e:
        for file in files:
            if os.path.exists(location):
                os.remove(location)
        raise e
    return {"message": "Edit gambar berhasil"}, 200

#Delete Gambar
@app.delete("/gambar/<int:binatang>")
def del_gambar(id_binatang: int):
    if pets is None:
        return "Image not found"

    data = {"id_gambar": pets[0], "lokasi_gambar": pets[1]}
    os.remove(data["lokasi_gambar"])
    pets.upload_gambar(id_binatang)
    return {"message": "Edit gambar berhasil"}, 200
        
#----------------------------------------------------------------------------
#Donatur Done
@app.get("/donatur")
def get_all_donatur():
    return donatur.get_all_donatur()

@app.get("/donatur/<int:id_donatur>")
def find_id_donatur(id_donatur: int):
    return donatur.find_id_donatur(id_donatur)

@app.post("/donatur")
def new_donatur():
    return donatur.new_donatur()

@app.put("/donatur/<int:id_donatur>")
def edit_donatur(id_donatur: int):
    return donatur.edit_donatur(id_donatur)

@app.delete("/donatur/<int:id_donatur>")
def del_donatur(id_donatur):
    return donatur.del_donatur(id_donatur)


#----------------------------------------------------------------------------
#Kegiatan Done
@app.get("/kegiatan")
def get_all_kegiatan():
    return kegiatan.get_all_kegiatan()

@app.get("/kegiatan/<int:id_kegiatan>")
def find_by_id(id_kegiatan: int):
    return kegiatan.find_by_id(id_kegiatan)

@app.post("/kegiatan")
def new_kegiatan():
    return kegiatan.new_kegiatan()

@app.put("/kegiatan/<int:id_kegiatan>")
def edit_kegiatan(id_kegiatan):
    return kegiatan.edit_kegiatan(id_kegiatan)

@app.delete("/kegiatan/<int:id_kegiatan>")
def del_kegiatan(id_kegiatan):
    return kegiatan.del_kegiatan(id_kegiatan)


#----------------------------------------------------------------------------
#Penyelamatan Done
@app.get("/penyelamatan")
def get_all_penyelamatan():
    return penyelamatan.get_all_penyelamatan()

@app.get("/penyelamatan/<int:id_penyelamatan>")
def find_id_penyelamatan(id_penyelamatan: int):
    return penyelamatan.find_id_penyelamatan(id_penyelamatan)
    
@app.post("/penyelamatan")
def new_penyelamatan():
    return penyelamatan.new_penyelamatan()

@app.put("/penyelamatan/<int:id_penyelamatan>")
def edit_penyelamatan(id_penyelamatan):
    return penyelamatan.edit_penyelamatan(id_penyelamatan)

@app.delete("/penyelamatan/<int:id_penyelamatan>")
def del_penyelamatan(id_penyelamatan):
    return penyelamatan.del_penyelamatan(id_penyelamatan)

    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=True)