from models import user as user_model
from models import binatang as binatang_model

class ValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)

def vcreate_binatang(**kwargs):
    nama_binatang = kwargs.get("nama_binatang")
    jenis_kelamin = kwargs.get("jenis_kelamin")
    jenis_hewan = kwargs.get("jenis_hewan")

    errors = []

    if nama_binatang is None or len(nama_binatang) <= 0:
        errors.append("Nama binatang harus di isi")

    if jenis_kelamin is None or len(jenis_hewan) <= 0 or jenis_kelamin.lower() not in ['jantan','betina']:
        errors.append("Jenis Kelamin harus di isi dan hanya boleh jantan atau betina")

    if jenis_hewan is None or len(jenis_hewan) <= 0:
        errors.append("Jenis hewan harus di isi")

    """if id_admin is None or str(id_admin).strip() == '':
        errors.append("id admin harus di isi")
        return {"errors": errors}

    try:
        id_admin = int(id_admin)
    except ValueError:
        errors.append("id admin harus berupa angka")
        return {"errors": errors}

    user = user_model.find_id_user(id_admin)
    if user is None:
        errors.append("id kegiatan tidak ditemukan")
        return {"errors": errors}"""
    
    if len(errors) > 0:
        return errors
    return None

    

def vedit_binatang(**kwargs):
    nama_binatang = kwargs.get("nama_binatang")
    jenis_kelamin = kwargs.get("jenis_kelamin")
    jenis_hewan = kwargs.get("jenis_hewan")

    errors = []

    if nama_binatang is None or len(nama_binatang) <= 0:
        errors.append("Nama binatang harus di isi")

    if jenis_kelamin is None or len(jenis_hewan) <= 0 or jenis_kelamin.lower() not in ['jantan','betina']:
        errors.append("Jenis Kelamin harus di isi dan hanya boleh jantan atau betina")

    if jenis_hewan is None or len(jenis_hewan) <= 0:
        errors.append("Jenis hewan harus di isi")

    if len(errors) > 0:
        return errors
    return None
    
def vcreate_gambar_binatang(**kwargs):
    images = kwargs.get("images")
    id_binatang = kwargs.get("id_binatang")

    errors = []

    if id_binatang is None or str(id_binatang).strip() == '':
        errors.append("id binatang harus di isi")
        return {"errors": errors}

    try:
        id_binatang = int(id_binatang)
    except ValueError:
        errors.append("id binatang harus berupa angka")
        return {"errors": errors}

    binatang = BufferError.find_id_binatang(id_binatang)
    if binatang is None:
        errors.append("id binatang tidak ditemukan")
        return {"errors": errors}
    
    if not images:
        errors.append("Gambar dibutuhkan")

    for image in images:
        if image.content_type not in ["image/jpeg", "image/jpg", "image/webp", "image/png"]:
            errors.append("Gambar harus berformat jpeg, jpg, webp, atau png")

    gambar = binatang_model.find_id_binatang(id_binatang)
    if not gambar:
        errors.append("id binatang tidak ditemukan")

    if len(errors) > 0:
        return errors
    return None