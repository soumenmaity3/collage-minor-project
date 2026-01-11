import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# Load dataset (using CIFAR-10 as example)
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Normalize pixel values
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Convert labels to categorical
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

print(f"Training data shape: {x_train.shape}")
print(f"Training labels shape: {y_train.shape}")

# BUILD MODEL FROM SCRATCH (NO PRE-TRAINED WEIGHTS)
model_no_ft = keras.Sequential([
    # First Convolutional Block
    layers.Conv2D(32, (3, 3), activation='relu', 
                  input_shape=(32, 32, 3), padding='same'),
    layers.BatchNormalization(),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # Second Convolutional Block
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # Third Convolutional Block
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # Dense Layers
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

# Compile the model
model_no_ft.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Display model architecture
model_no_ft.summary()

# Train the model
print("\n=== Training Model from Scratch ===")
history_no_ft = model_no_ft.fit(
    x_train, y_train,
    batch_size=128,
    epochs=20,
    validation_split=0.2,
    verbose=1
)

# Evaluate on test set
test_loss_no_ft, test_acc_no_ft = model_no_ft.evaluate(x_test, y_test, verbose=0)
print(f"\nTest Accuracy (No Fine-Tuning): {test_acc_no_ft:.4f}")
print(f"Test Loss (No Fine-Tuning): {test_loss_no_ft:.4f}")