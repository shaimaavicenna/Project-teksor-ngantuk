import cv2
import numpy as np
from tensorflow.keras.models import load_model
import threading
import playsound

# Ganti dengan IP ESP32-CAM kamu
ESP32_URL = "http://192.168.1.50:81/stream"

model = load_model("model.h5")

def play_alarm():
    threading.Thread(target=playsound.playsound, args=("alarm.mp3",), daemon=True).start()

cap = cv2.VideoCapture(ESP32_URL)

label_map = ["Fokus", "Mengantuk", "Terdistraksi"]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal ambil stream")
        break

    img = cv2.resize(frame, (100, 100))  # Sesuaikan dengan input model kamu
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)[0]
    idx = np.argmax(pred)
    status = label_map[idx]

    if status == "Mengantuk":
        play_alarm()

    cv2.putText(frame, f"Status: {status}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0) if status == "Fokus" else (0, 0, 255), 2)

    cv2.imshow("Deteksi Fokus", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
