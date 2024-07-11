from imutils.video import VideoStream
from imutils.video import FPS
from ultralytics import YOLO
import cv2
import math
import time
import serial

# Inisialisasi koneksi serial dengan Arduino
# port_usb_ttl = 'COM6'  # Ganti dengan port USB-TTL yang sesuai
# baud_rate = 9600
# ser = serial.Serial(port_usb_ttl, baud_rate, timeout=1)
# time.sleep(2)

# Inisialisasi video stream
vs = VideoStream(src=1).start()
time.sleep(2.0)
fps = FPS().start()

# Inisialisasi model YOLO
model = YOLO("yolo-Weights/yolov8n.pt")

# Inisialisasi posisi objek pada frame sebelumnya
prev_obj_position = None


classNames = ["Jeruk Hijau Kecil", "Jeruk Hijau Besar", "Jeruk Hijau Orange Besar", "Jeruk Hijau Orange Kecil",
              "Jeruk Orange Besar", "Jeruk Orange Kecil"]


while True:
    # Baca frame dari video stream
    frame = vs.read()
    frame = cv2.resize(frame, (1080, 720))  # Resize frame jika diperlukan

    # Deteksi objek menggunakan YOLO
    results = model(frame, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Koordinat bounding box objek
            obj_position = (x1 + x2) / 2, (y1 + y2) / 2  # Posisi objek pada frame ini

            # Hitung perubahan posisi objek dari frame sebelumnya
            if prev_obj_position:
                dx = obj_position[0] - prev_obj_position[0]
                dy = obj_position[1] - prev_obj_position[1]

                # Tentukan arah pergerakan objek (naik, turun, kanan, kiri)
                if abs(dx) > abs(dy):
                    if dx > 0:
                        direction = "right"
                    else:
                        direction = "left"
                else:
                    if dy > 0:
                        direction = "down"
                    else:
                        direction = "up"

                # Kirim instruksi ke Arduino berdasarkan arah pergerakan objek
                # ser.write(direction.encode())
                # ser.write(b'\n')  # Karakter newline sebagai penanda akhir instruksi

            # Simpan posisi objek untuk frame berikutnya
            prev_obj_position = obj_position

    # Tampilkan frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # Keluar dari loop jika tombol 'q' ditekan
    if key == ord("q"):
        break

    fps.update()

# Stop video stream dan tutup jendela
fps.stop()
cv2.destroyAllWindows()
vs.stop()