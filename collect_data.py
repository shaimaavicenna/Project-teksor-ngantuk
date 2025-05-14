# collect_data.py
import cv2
import os

label = "ngantuk"  # GANTI ke "fokus" atau "terdistraksi" sesuai sesi
save_dir = f"dataset/{label}"
os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0
max_images = 50

print("[INFO] Tekan 's' untuk simpan gambar, 'q' untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and count < max_images:
        filename = os.path.join(save_dir, f"{label}_{count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"[INFO] Disimpan: {filename}")
        count += 1

    elif key == ord('q') or count >= max_images:
        break

cap.release()
cv2.destroyAllWindows()
