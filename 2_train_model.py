"""
Step 2: Train CNN Model for Animal Sound Classification
This script trains a deep learning model using the generated spectrograms
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

# ========== CONFIGURATION ==========
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
SPECTROGRAM_PATH = PROJECT_PATH / "spectrograms_dataset"
MODEL_OUTPUT_PATH = PROJECT_PATH / "trained_model"
MODEL_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Training parameters
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 50
VALIDATION_SPLIT = 0.2
LEARNING_RATE = 0.001

# Model save paths
MODEL_FILE = MODEL_OUTPUT_PATH / "animal_sound_classifier.h5"
HISTORY_FILE = MODEL_OUTPUT_PATH / "training_history.json"
CLASS_LABELS_FILE = MODEL_OUTPUT_PATH / "class_labels.json"

def build_cnn_model(input_shape, num_classes):
    """
    Build CNN architecture for audio classification
    Architecture inspired by VGGNet with batch normalization
    """
    model = models.Sequential([
        # Input layer
        layers.Input(shape=input_shape),
        
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 4
        layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Flatten and Dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        
        # Output layer
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def plot_training_history(history, save_path):
    """Plot and save training history"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    axes[0].plot(history['accuracy'], label='Train Accuracy')
    axes[0].plot(history['val_accuracy'], label='Validation Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True)
    
    # Plot loss
    axes[1].plot(history['loss'], label='Train Loss')
    axes[1].plot(history['val_loss'], label='Validation Loss')
    axes[1].set_title('Model Loss')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Training history plot saved: {save_path}")

def main():
    print("=" * 60)
    print("STEP 2: TRAINING CNN MODEL")
    print("=" * 60)
    
    # Check if spectrogram directory exists
    if not SPECTROGRAM_PATH.exists():
        print(f"❌ Spectrogram directory not found: {SPECTROGRAM_PATH}")
        print("Please run '1_generate_spectrograms.py' first!")
        return
    
    # Count classes and samples
    classes = [d.name for d in SPECTROGRAM_PATH.iterdir() if d.is_dir()]
    num_classes = len(classes)
    
    if num_classes == 0:
        print("❌ No animal classes found in spectrogram directory!")
        return
    
    print(f"🐾 Found {num_classes} animal classes: {', '.join(classes)}")
    
    # Count total spectrograms
    total_spectrograms = sum(len(list((SPECTROGRAM_PATH / cls).glob("*.png"))) for cls in classes)
    print(f"📊 Total spectrograms: {total_spectrograms}")
    
    if total_spectrograms < 10:
        print("❌ Not enough spectrograms for training!")
        return
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=VALIDATION_SPLIT,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1,
        fill_mode='nearest'
    )
    
    # Validation data (no augmentation)
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=VALIDATION_SPLIT
    )
    
    # Create training generator
    print("\n📁 Loading training data...")
    train_generator = train_datagen.flow_from_directory(
        SPECTROGRAM_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True,
        seed=42
    )
    
    # Create validation generator
    print("📁 Loading validation data...")
    validation_generator = val_datagen.flow_from_directory(
        SPECTROGRAM_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False,
        seed=42
    )
    
    # Save class labels
    class_labels = {v: k for k, v in train_generator.class_indices.items()}
    with open(CLASS_LABELS_FILE, 'w') as f:
        json.dump(class_labels, f, indent=4)
    print(f"✅ Class labels saved: {CLASS_LABELS_FILE}")
    
    # Build model
    print("\n🏗️ Building CNN model...")
    input_shape = (*IMG_SIZE, 3)
    model = build_cnn_model(input_shape, num_classes)
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Print model summary
    print("\n📋 Model Architecture:")
    model.summary()
    
    # Calculate total parameters
    total_params = model.count_params()
    print(f"\n📊 Total parameters: {total_params:,}")
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            MODEL_FILE,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train model
    print("\n🚀 Starting training...")
    print(f"Epochs: {EPOCHS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {validation_generator.samples}")
    print("-" * 60)
    
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save training history
    history_dict = {
        'accuracy': [float(x) for x in history.history['accuracy']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']],
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history['val_loss']]
    }
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history_dict, f, indent=4)
    print(f"\n✅ Training history saved: {HISTORY_FILE}")
    
    # Plot training history
    plot_path = MODEL_OUTPUT_PATH / "training_history.png"
    plot_training_history(history_dict, plot_path)
    
    # Evaluate on validation set
    print("\n📊 Evaluating model on validation set...")
    val_loss, val_accuracy = model.evaluate(validation_generator, verbose=0)
    print(f"Validation Loss: {val_loss:.4f}")
    print(f"Validation Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
    
    # Summary
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"✅ Model saved: {MODEL_FILE}")
    print(f"✅ Class labels: {CLASS_LABELS_FILE}")
    print(f"✅ Training history: {HISTORY_FILE}")
    print(f"✅ Training plot: {plot_path}")
    print(f"\n🎯 Final Validation Accuracy: {val_accuracy*100:.2f}%")
    print("\nNext step: Run '3_predict.py' to classify new audio files!")

if __name__ == "__main__":
    main()
