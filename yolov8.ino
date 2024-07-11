void setup() {
  Serial1.begin(9600); // Baud rate harus sama dengan yang diatur di Python
  Serial.begin(9600);
}

void loop() {
  if (Serial1.available() > 0) {
    String data = Serial1.readStringUntil('\n'); // Membaca string sampai karakter '\n' ditemukan
    data.trim(); // Menghapus spasi tambahan di sekitar string
    if (data.length() > 0) { // Pastikan data tidak kosong
      bool validData = true;
      for (int i = 0; i < data.length(); i++) {
        if (!isdigit(data[i])) { // Periksa apakah semua karakter adalah angka
          validData = false;
          break;
        }
      }
      if (validData) {
        int nilai = data.toInt(); // Konversi string menjadi integer
        Serial.print("Nilai yang diterima: ");
        Serial.println(nilai);
        // Lakukan sesuatu dengan nilai integer yang diterima di sini
      } else {
        Serial.println("Data tidak valid");
      }
    }
  }
}
