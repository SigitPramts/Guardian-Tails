from flask import Flask
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
)
import logging
from controllers.validator import validate_register, ValidateError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "rahasia"
jwt = JWTManager(app)

import controllers.donatur as donatur
import controllers.kegiatan as kegiatan
import controllers.penyelamatan as penyelamatan
import controllers.auth as user
import controllers.binatang as binatang


#----------------------------------------------------------------------------
#Auth done
@app.get("/protected")
@jwt_required()
def validation():
    users = get_jwt_identity()
    return{"Kamu berhasil login sebagai":users}, 200

@app.post("/login")
def login():
    return user.login_controller()

@app.post("/register")
def register():
    return user.register_controller()

@app.put("/user/<int:id_admin>")
def edit_user(id_admin: int):
    return user.edit_user(id_admin)

@app.delete("/user/<int:id_admin>")
def del_user(id_admin: int):
    return user.del_user(id_admin)
    
    
#----------------------------------------------------------------------------
#Binatang Done
@app.get("/pets")
def get_all_binatang():
    return binatang.get_all_binatang()

@app.get("/pets/search")
def search():
    return binatang.search()

@app.get("/pets/multi_search")
def multi_search():
    return binatang.multi_search()

@app.get("/pets/<int:id_binatang>")
def find_id_binatang(id_binatang: int):
    return binatang.find_id_binatang(id_binatang)

@app.post("/pets")
@jwt_required()
def new_binatang():
    return binatang.new_binatang()

@app.put("/pets/<int:id_binatang>")
@jwt_required()
def edit_binatang(id_binatang: int):
    return binatang.edit_binatang(id_binatang)

@app.delete("/pets/<int:id_binatang>")
@jwt_required()
def del_binatang(id_binatang: int):
    return binatang.del_binatang(id_binatang)


#----------------------------------------------------------------------------
@app.get("/gambar")
def get_all_gambar():
    return binatang.get_all_gambar()

@app.get("/gambar/<int:id_gambar>")
def find_id_gambar(id_gambar: int):
    return binatang.find_id_gambar(id_gambar)

#Upload Gambar Done
@app.post("/gambar/<int:id_binatang>")
@jwt_required()
def upload_gambar(id_binatang: int):
    return binatang.upload_gambar(id_binatang)

@app.delete("/gambar/<int:id_gambar>")
@jwt_required()
def delete_gambar(id_gambar: int):
    return binatang.del_gambar(id_gambar)

        
#----------------------------------------------------------------------------
#Donatur Done
@app.get("/donatur")
def get_all_donatur():
    return donatur.get_all_donatur()

@app.get("/donatur/<int:id_donatur>")
def find_id_donatur(id_donatur: int):
    return donatur.find_id_donatur(id_donatur)

@app.post("/donatur")
@jwt_required()
def new_donatur():
    return donatur.new_donatur()

@app.put("/donatur/<int:id_donatur>")
@jwt_required()
def edit_donatur(id_donatur: int):
    return donatur.edit_donatur(id_donatur)

@app.delete("/donatur/<int:id_donatur>")
@jwt_required()
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
@jwt_required()
def new_kegiatan():
    return kegiatan.new_kegiatan()

@app.put("/kegiatan/<int:id_kegiatan>")
@jwt_required()
def edit_kegiatan(id_kegiatan):
    return kegiatan.edit_kegiatan(id_kegiatan)

@app.delete("/kegiatan/<int:id_kegiatan>")
@jwt_required()
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
@jwt_required()
def new_penyelamatan():
    return penyelamatan.new_penyelamatan()

@app.put("/penyelamatan/<int:id_penyelamatan>")
@jwt_required()
def edit_penyelamatan(id_penyelamatan):
    return penyelamatan.edit_penyelamatan(id_penyelamatan)

@app.delete("/penyelamatan/<int:id_penyelamatan>")
@jwt_required()
def del_penyelamatan(id_penyelamatan):
    return penyelamatan.del_penyelamatan(id_penyelamatan)

    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=True)