from flask import Flask
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
)
from flask_cors import CORS

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Mengaktifkan CORS untuk mengizinkan akses lintas domain
CORS(app)

# Mengatur kunci rahasia untuk JWT
app.config["JWT_SECRET_KEY"] = "rahasia"

# Menginisialisasi JWTManager dengan aplikasi Flask
jwt = JWTManager(app)

# Mengimpor modul-modul yang diperlukan
import controllers.donatur as donatur
import controllers.kegiatan as kegiatan
import controllers.penyelamatan as penyelamatan
import controllers.auth as user
from controllers.auth import ambil_data_user_controller
import controllers.binatang as binatang


#----------------------------------------------------------------------------
# Fungsi untuk mendapatkan data pengguna (user)
@app.get("/users")
@jwt_required()
def ambil_data_user():
    return ambil_data_user_controller()

# Endpoint terlindungi untuk validasi token JWT
@app.get("/protected")
@jwt_required()
def validation():
    return ambil_data_user_controller()

# Endpoint untuk proses login pengguna
@app.post("/login")
def login():
    return user.login_controller()

# Endpoint untuk proses registrasi pengguna
@app.post("/register")
def register():
    return user.register_controller()

# Endpoint untuk mengubah profil pengguna
@app.put('/user/profile')
def edit_user():
    return user.edit_user()

# Endpoint untuk menghapus profil pengguna
@app.delete("/user/profile")
def del_user():
    return user.del_user()
    
    
#----------------------------------------------------------------------------
# Endpoint untuk mengambil informasi binatang
@app.get("/pets")
def get_all_binatang():
    return binatang.get_all_binatang()

# Endpoint untuk mencari informasi binatang
@app.get("/pets/search")
def search():
    return binatang.search()

# Endpoint untuk mencari informasi binatang
@app.get("/pets/multi_search")
def multi_search():
    return binatang.multi_search()

# Endpoint untuk mencari informasi binatang
@app.get("/pets/<int:id_binatang>")
def find_id_binatang(id_binatang: int):
    return binatang.find_id_binatang(id_binatang)

# Endpoint untuk menambah binatang
@app.post("/pets")
def new_binatang():
    return binatang.new_binatang()

# Endpoint untuk mengubah binatang
@app.put("/pets/<int:id_binatang>")
def edit_binatang(id_binatang: int):
    return binatang.edit_binatang(id_binatang)

# Endpoint untuk menghapus binatang
@app.delete("/pets/<int:id_binatang>")
def del_binatang(id_binatang: int):
    return binatang.del_binatang(id_binatang)


#----------------------------------------------------------------------------
# Endpoint untuk mencari gambar binatang
@app.get("/gambar")
def get_all_gambar():
    return binatang.get_all_gambar()

# Endpoint untuk mencari gambar binatang
@app.get("/gambar/<int:id_gambar>")
def find_id_gambar(id_gambar: int):
    return binatang.find_id_gambar(id_gambar)

# Endpoint untuk menambah gambar binatang
@app.post("/gambar/<int:id_binatang>")
def upload_gambar(id_binatang: int):
    return binatang.upload_gambar(id_binatang)

# Endpoint untuk menghapus gambar binatang
@app.delete("/gambar/<int:id_gambar>")
def delete_gambar(id_gambar: int):
    return binatang.del_gambar(id_gambar)

        
#----------------------------------------------------------------------------
# Endpoint untuk mencari donatur
@app.get("/donatur")
def get_all_donatur():
    return donatur.get_all_donatur()

# Endpoint untuk mencari donatur
@app.get("/donatur/<int:id_donatur>")
def find_id_donatur(id_donatur: int):
    return donatur.find_id_donatur(id_donatur)

# Endpoint untuk menambah donatur
@app.post("/donatur")
def new_donatur():
    return donatur.new_donatur()

# Endpoint untuk mengubah donatur
@app.put("/donatur/<int:id_donatur>")
def edit_donatur(id_donatur: int):
    return donatur.edit_donatur(id_donatur)

# Endpoint untuk menghapus donatur
@app.delete("/donatur/<int:id_donatur>")
def del_donatur(id_donatur):
    return donatur.del_donatur(id_donatur)


#----------------------------------------------------------------------------
# Endpoint untuk mencari kegiatan
@app.get("/kegiatan")
def get_all_kegiatan():
    return kegiatan.get_all_kegiatan()

# Endpoint untuk mencari kegiatan
@app.get("/kegiatan/<int:id_kegiatan>")
def find_by_id(id_kegiatan: int):
    return kegiatan.find_by_id(id_kegiatan)

# Endpoint untuk membuat kegiatan
@app.post("/kegiatan")
def new_kegiatan():
    return kegiatan.new_kegiatan()

# Endpoint untuk mengubah kegiatan
@app.put("/kegiatan/<int:id_kegiatan>")
def edit_kegiatan(id_kegiatan):
    return kegiatan.edit_kegiatan(id_kegiatan)

# Endpoint untuk menghapus kegiatan
@app.delete("/kegiatan/<int:id_kegiatan>")
def del_kegiatan(id_kegiatan):
    return kegiatan.del_kegiatan(id_kegiatan)


#----------------------------------------------------------------------------
# Endpoint untuk mencari penyelamatan
@app.get("/penyelamatan")
def get_all_penyelamatan():
    return penyelamatan.get_all_penyelamatan()

# Endpoint untuk mencari kegiatan
@app.get("/penyelamatan/<int:id_penyelamatan>")
def find_id_penyelamatan(id_penyelamatan: int):
    return penyelamatan.find_id_penyelamatan(id_penyelamatan)
    
# Endpoint untuk menambah penyelamatan
@app.post("/penyelamatan")
def new_penyelamatan():
    return penyelamatan.new_penyelamatan()

# Endpoint untuk mengubah penyelamatan
@app.put("/penyelamatan/<int:id_penyelamatan>")
def edit_penyelamatan(id_penyelamatan):
    return penyelamatan.edit_penyelamatan(id_penyelamatan)

# Endpoint untuk menghapus penyelamatan
@app.delete("/penyelamatan/<int:id_penyelamatan>")
def del_penyelamatan(id_penyelamatan):
    return penyelamatan.del_penyelamatan(id_penyelamatan)
    
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001, use_reloader=True)