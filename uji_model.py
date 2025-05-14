from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model = load_model("model.h5")

img = image.load_img("ti.jpg", target_size=(100, 100))
img_array = image.img_to_array(img) / 255.
img_array = np.expand_dims(img_array, axis=0)

pred = model.predict(img_array)
kelas = ['ngantuk', 'fokus', 'terdistraksi']
print("Prediksi:", kelas[np.argmax(pred)])
