import serial
import time

# Inisialisasi koneksi serial
ser = serial.Serial('COM7', 9600)  # Ganti 'COM3' dengan port yang sesuai dengan Arduino
time.sleep(0.05)  # Tunggu beberapa detik untuk koneksi serial stabil

# Fungsi untuk membaca dan mengirim data
def kirim_data(nilai):
    data = str(nilai) + '\n'
    ser.write(data.encode())  # Kirim nilai sebagai string
    print("Data terkirim:", nilai)

# Contoh variabel integer yang berubah-ubah
nilai_integer = 0

# Loop untuk membaca dan mengirim data secara terus-menerus
while True:
    # Di sini, Anda dapat mengganti cara nilai_integer diperbarui sesuai kebutuhan aplikasi Anda
    nilai_integer += 1
    kirim_data(nilai_integer)
    time.sleep(0.05)  # Beri jeda satu detik sebelum mengirim data berikutnya
