from PIL import Image

def hide_file_in_image(image_path, file_path, output_path):
    # Baca gambar
    image = Image.open(image_path)
    pixels = image.load()

    # Baca file yang akan disembunyikan
    with open(file_path, 'rb') as f:
        data = f.read()

    # Tentukan ukuran gambar dan file
    image_width, image_height = image.size
    file_size = len(data)

    # Periksa apakah ukuran file melebihi kapasitas gambar
    max_file_size = (image_width * image_height * 3) // 8  # Menggunakan 1 bit dari masing-masing nilai piksel RGB
    if file_size > max_file_size:
        raise ValueError('Ukuran file terlalu besar untuk disembunyikan dalam gambar.')

    # Ubah ukuran file menjadi 4 byte (32-bit integer) dan tambahkan sebagai header pada data
    file_size_header = file_size.to_bytes(4, byteorder='big')
    data = file_size_header + data

    # Mengubah bit terakhir dari setiap nilai piksel menjadi bit dari file yang akan disembunyikan
    data_index = 0
    for y in range(image_height):
        for x in range(image_width):
            r, g, b = pixels[x, y]

            if data_index < len(data):
                # Ubah bit terakhir menjadi bit dari file yang akan disembunyikan
                pixels[x, y] = (r & 0b11111110 | ((data[data_index] & 0b10000000) >> 7),
                                g & 0b11111110 | ((data[data_index] & 0b01000000) >> 6),
                                b & 0b11111110 | ((data[data_index] & 0b00100000) >> 5))
                data_index += 1
            else:
                # Jika semua data telah disisipkan, keluar dari loop
                break

    # Simpan gambar yang telah dimodifikasi
    image.save(output_path)

    print('File berhasil disisipkan dalam gambar.')

def extract_file_from_image(image_path, output_path):
    # Baca gambar
    image = Image.open(image_path)
    pixels = image.load()

    # Ekstraksi ukuran file dari header
    file_size_header = b''
    data_index = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            file_size_header += ((r & 0b00000001) << 7 |
                                 (g & 0b00000001) << 6 |
                                 (b & 0b00000001) << 5).to_bytes(1, byteorder='big')
            data_index += 1
            if data_index >= 32:
                break
        if data_index >= 32:
            break

    file_size = int.from_bytes(file_size_header, byteorder='big')
    if file_size == 0:
        raise ValueError('File tidak ditemukan dalam gambar.')

    # Ekstraksi data dari gambar
    extracted_data = b''
    data_index = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            extracted_data += ((r & 0b00000001) << 7 |
                               (g & 0b00000001) << 6 |
                               (b & 0b00000001) << 5).to_bytes(1, byteorder='big')
            data_index += 1
            if data_index >= file_size * 8:
                break
        if data_index >= file_size * 8:
            break

    # Simpan data yang telah diekstrak ke dalam file
    with open(output_path, 'wb') as f:
        f.write(extracted_data[32:])  # Menghilangkan header

    print('Data berhasil diekstrak dari gambar.')

# Contoh penggunaan
hide_file_in_image('gambar.jpg', 'niko.txt', 'gambar_tersembunyi.jpg')
extract_file_from_image('gambar_tersembunyi.jpg', 'file_extraksi.txt')
