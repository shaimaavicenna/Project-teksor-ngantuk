import cv2
import numpy as np
from tensorflow.keras.models import load_model
import threading
import playsound

# Load model (input: 64x64x3, output: 3 kelas)
model = load_model("model.h5")

class_names = ["fokus", "ngantuk", "terdistraksi"]

def play_alarm():
    threading.Thread(target=playsound.playsound, args=("alarm.mp3",), daemon=True).start()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize sesuai input model
    img = cv2.resize(frame, (64, 64))  # <- disesuaikan ke model
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    # Prediksi
    preds = model.predict(img)[0]
    class_idx = np.argmax(preds)
    status = class_names[class_idx]

    if status == "ngantuk":
        play_alarm()

    color = (0, 255, 0) if status == "fokus" else (0, 255, 255) if status == "terdistraksi" else (0, 0, 255)
    cv2.putText(frame, f"Status: {status}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Deteksi fokus", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
