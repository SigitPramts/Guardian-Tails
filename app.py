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

@app.route("/upload_gambar", methods=["POST"])
def upload_gambar():
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
        pets.upload_gambar(lokasi_gambar=locations)

        return {"message": "Upload gambar berhasil"}, 200
    except Exception as e:
        # If an exception occurs, delete the uploaded files
        for location in locations:
            if os.path.exists(location):
                os.remove(location)
        raise e



        
#----------------------------------------------------------------------------
#New Donatur Done
@app.post("/donatur")
def new_donatur():
    try:
        nama_donatur = request.form.get('nama_donatur')
        email_donatur = request.form.get('email_donatur')
        jumlah_donasi = request.form.get('jumlah_donasi')

        pets.new_donatur(nama_donatur, email_donatur, jumlah_donasi)
        return "", 202
    except ValidateError as e:
        return str(e), 401
    
#Edit Donatur Done
@app.put("/donatur/<int:id_donatur>")
def edit_donatur(id_donatur):
    
        nama_donatur = request.form.get('nama_donatur')
        email_donatur = request.form.get('email_donatur')
        jumlah_donasi = request.form.get('jumlah_donasi')

        pets.edit_donatur(id_donatur, nama_donatur, email_donatur, jumlah_donasi)
        return "", 202

#Delete Donatur Done
@app.delete("/donatur/<int:id_donatur>")
def del_donatur(id_donatur):
    pets.del_donatur(id_donatur)
    return "Sudah di Hapus", 404


#----------------------------------------------------------------------------
#New Kegiatan Done
@app.post("/kegiatan")
def new_kegiatan():
    try:
        jenis_kegiatan = request.form.get('jenis_kegiatan')
        lokasi_kegiatan = request.form.get('lokasi_kegiatan')

        pets.new_kegiatan(jenis_kegiatan, lokasi_kegiatan)
        return "", 202
    except ValidateError as e:
        return str(e), 401
    
#Edit Kegiatan Done
@app.put("/kegiatan/<int:id_kegiatan>")
def edit_kegiatan(id_kegiatan):
    try:
        jenis_kegiatan = request.form.get('jenis_kegiatan')
        lokasi_kegiatan = request.form.get('lokasi_kegiatan')

        pets.edit_kegiatan(id_kegiatan, jenis_kegiatan, lokasi_kegiatan)
        return "", 202
    except ValidateError as e:
        return str(e), 401

#Delete Kegiatan Done
@app.delete("/kegiatan/<int:id_kegiatan>")
def del_kegiatan(id_kegiatan):
    pets.del_kegiatan(id_kegiatan)
    return "Sudah di Hapus", 404

#----------------------------------------------------------------------------
#New penyelamatan Done
@app.post("/penyelamatan")
def new_penyelamatan():
    try:
        lokasi_penyelamatan = request.form.get('lokasi_penyelamatan')
        nama_penyelamatan = request.form.get('nama_penyelamatan')

        pets.new_penyelamatan(lokasi_penyelamatan, nama_penyelamatan)
        return "", 202
    except ValidateError as e:
        return str(e), 401
    
#Edit penyelamatan Done
@app.put("/penyelamatan/<int:id_penyelataman>")
def edit_penyelamatan(id_penyelataman):
    try:
        lokasi_penyelamatan = request.form.get('lokasi_penyelamatan')
        nama_penyelamatan = request.form.get('nama_penyelamatan')

        pets.edit_penyelamatan(id_penyelataman, lokasi_penyelamatan, nama_penyelamatan)
        return "", 202
    except ValidateError as e:
        return str(e), 401

#Delete penyelamatan Done
@app.delete("/penyelamatan/<int:id_penyelataman>")
def del_penyelamatan(id_penyelataman):
    pets.del_penyelamatan(id_penyelataman)
    return "Sudah di Hapus", 404
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=True)