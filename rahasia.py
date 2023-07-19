import base64
from PIL import Image

# Membaca gambar
gambar = Image.open("gambar.jpg")

# Mengkodekan data sebagai Base64
pesan = "Niko S1 Informatika."
pesan_encoded = base64.b64encode(pesan.encode())
pesan_encoded_str = pesan_encoded.decode()

# Menyimpan pesan dalam metadata gambar
gambar.info["pesan_rahasia"] = pesan_encoded_str
gambar.save("gambar_rahasia.jpg")

print("Pesan berhasil disembunyikan dalam gambar.")

# Membaca kembali pesan dari metadata gambar
gambar_rahasia = Image.open("gambar_rahasia.jpg")
pesan_encoded_str = gambar_rahasia.info["pesan_rahasia"]
pesan_encoded = pesan_encoded_str.encode()
pesan = base64.b64decode(pesan_encoded).decode()
print("Pesan yang tersembunyi:", pesan)
