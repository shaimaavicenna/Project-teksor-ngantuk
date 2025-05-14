import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Dataset loader dengan augmentasi dan rescaling
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Load data dengan 3 kelas: fokus, ngantuk, dan terdistraksi
train_gen = datagen.flow_from_directory(
    "dataset",  # Pastikan path ini benar
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',  # Menggunakan 'categorical' untuk 3 kelas
    subset='training'
)

val_gen = datagen.flow_from_directory(
    "dataset",  # Pastikan path ini benar
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',  # Menggunakan 'categorical' untuk 3 kelas
    subset='validation'
)

# Model CNN untuk klasifikasi 3 kelas
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')  # 3 kelas, softmax untuk multi-kelas
])

# Compile model dengan loss categorical_crossentropy
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Training model
model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=10
)

# Simpan model setelah training
model.save("model.h5")  # Simpan dengan nama 'model.h5'
print("✅ Model disimpan ke model.h5")
