"""
Complete Animal Sound Classification Pipeline
Works directly with audio files in data folder (no CSV needed)
"""

from pathlib import Path
import librosa
import librosa.display
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import json

# ========== CONFIGURATION ==========
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
DATA_PATH = PROJECT_PATH / "mini_project" / "data"
SPECTROGRAM_OUTPUT = PROJECT_PATH / "spectrograms_dataset"
MODEL_OUTPUT_PATH = PROJECT_PATH / "trained_model"

# Select only 3 animals for best accuracy (most distinct sounds)
SELECTED_ANIMALS = ['Dog', 'Rooster', 'Frog']  # Very different sounds
# Alternative: ['Dog', 'Cat', 'Rooster'] or ['Dog', 'Cow', 'Rooster']

# Audio processing parameters
SAMPLE_RATE = 22050
DURATION = 3
N_MELS = 128
HOP_LENGTH = 512
IMG_SIZE = (128, 128)

# Training parameters
BATCH_SIZE = 8  # Very small batch for better gradient updates
EPOCHS = 100  # More epochs for better convergence
VALIDATION_SPLIT = 0.2

# Create directories
SPECTROGRAM_OUTPUT.mkdir(parents=True, exist_ok=True)
MODEL_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("ANIMAL SOUND CLASSIFICATION - 5 ANIMALS (IMPROVED ACCURACY)")
print("=" * 80)
print(f"Training on: {', '.join(SELECTED_ANIMALS)}")

# ========== STEP 1: GENERATE SPECTROGRAMS ==========
print("\n" + "=" * 80)
print("STEP 1/3: GENERATING SPECTROGRAMS")
print("=" * 80)

def extract_label(filename):
    """Extract animal label from filename (e.g., 'Dog_1.wav' -> 'Dog')"""
    stem = filename.stem
    if '_' in stem:
        return stem.split('_')[0]
    else:
        return stem

def load_and_preprocess_audio(audio_path):
    """Load audio file and preprocess to fixed length"""
    try:
        y, sr = librosa.load(audio_path, sr=SAMPLE_RATE, duration=DURATION)
        target_length = SAMPLE_RATE * DURATION
        if len(y) < target_length:
            y = np.pad(y, (0, target_length - len(y)), mode='constant')
        else:
            y = y[:target_length]
        return y, sr
    except Exception as e:
        print(f"Error loading {audio_path}: {e}")
        return None, None

def generate_mel_spectrogram(y, sr, save_path):
    """Generate and save mel-spectrogram"""
    try:
        mel_spec = librosa.feature.melspectrogram(
            y=y, sr=sr, n_mels=N_MELS, hop_length=HOP_LENGTH, fmax=sr//2
        )
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        fig = plt.figure(figsize=(4, 4))
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        librosa.display.specshow(
            mel_spec_db, sr=sr, hop_length=HOP_LENGTH,
            x_axis='time', y_axis='mel', cmap='inferno', ax=ax
        )
        
        plt.savefig(save_path, dpi=72, bbox_inches='tight', pad_inches=0)
        plt.close()
        return True
    except Exception as e:
        print(f"Error generating spectrogram: {e}")
        plt.close()
        return False

# Find all audio files
all_audio_files = list(DATA_PATH.glob("*.wav"))
print(f"\n✅ Found {len(all_audio_files)} total audio files")

if len(all_audio_files) == 0:
    print(f"❌ No audio files found in {DATA_PATH}")
    print("Please run prepare_esc50_dataset.py first!")
    exit(1)

# Filter for selected animals only
audio_files = [f for f in all_audio_files if extract_label(f) in SELECTED_ANIMALS]
print(f"✅ Filtered to {len(audio_files)} files from selected animals: {', '.join(SELECTED_ANIMALS)}")

# Get unique animal classes (should be 5)
animals = sorted(set(extract_label(f) for f in audio_files))
print(f"✅ Using {len(animals)} animal classes: {', '.join(animals)}")

# Create directories for each animal
for animal in animals:
    (SPECTROGRAM_OUTPUT / animal).mkdir(parents=True, exist_ok=True)

# Generate spectrograms
print(f"\n🎵 Generating spectrograms...")
success_count = 0
fail_count = 0

for audio_file in tqdm(audio_files, desc="Processing"):
    label = extract_label(audio_file)
    
    # Load audio
    y, sr = load_and_preprocess_audio(audio_file)
    if y is None:
        fail_count += 1
        continue
    
    # Generate spectrogram
    spec_filename = f"{audio_file.stem}_spec.png"
    save_path = SPECTROGRAM_OUTPUT / label / spec_filename
    
    if generate_mel_spectrogram(y, sr, save_path):
        success_count += 1
    else:
        fail_count += 1

print(f"\n✅ Successfully generated: {success_count} spectrograms")
print(f"❌ Failed: {fail_count} files")

# Print class distribution
print(f"\n📊 Class Distribution:")
for animal in animals:
    count = len(list((SPECTROGRAM_OUTPUT / animal).glob("*.png")))
    print(f"  {animal}: {count} spectrograms")

if success_count < 20:
    print("\n❌ Not enough spectrograms for training!")
    print("Need at least 20 spectrograms total.")
    exit(1)

print("\n✅ STEP 1/3: GENERATING SPECTROGRAMS completed successfully!")

# ========== STEP 2: TRAIN MODEL ==========
print("\n" + "=" * 80)
print("STEP 2/3: TRAINING CNN MODEL")
print("=" * 80)

# Data generators with strong augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=VALIDATION_SPLIT
)

train_generator = train_datagen.flow_from_directory(
    SPECTROGRAM_OUTPUT,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

validation_generator = train_datagen.flow_from_directory(
    SPECTROGRAM_OUTPUT,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

num_classes = len(train_generator.class_indices)
print(f"\n✅ Found {num_classes} animal classes: {', '.join(train_generator.class_indices.keys())}")
print(f"📊 Total spectrograms: {train_generator.samples + validation_generator.samples}")

if num_classes < 2:
    print("\n❌ Not enough animal classes for training!")
    print("Need at least 2 different animal classes.")
    exit(1)

# Build CNN model (Balanced for 5 classes with limited data)
print(f"\n  Building CNN model...")
model = models.Sequential([
    # Block 1
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.3),
    
    # Block 2
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.3),
    
    # Block 3
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.4),
    
    # Block 4
    layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.4),
    
    # Dense layers
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(f"✅ Model built successfully!")
model.summary()

# Callbacks
callbacks = [
    ModelCheckpoint(
        str(MODEL_OUTPUT_PATH / "best_model.h5"),
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    ),
    EarlyStopping(
        monitor='val_loss',
        patience=15,  # More patience for 5 classes
        restore_best_weights=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=7,  # More patience before reducing LR
        min_lr=1e-7,
        verbose=1
    )
]

# Train model
print(f"\n🚀 Starting training...")
print(f"Epochs: {EPOCHS}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Training samples: {train_generator.samples}")
print(f"Validation samples: {validation_generator.samples}")
print("-" * 80)

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

# Save final model
model.save(MODEL_OUTPUT_PATH / "final_model.h5")
print(f"\n✅ Model saved: {MODEL_OUTPUT_PATH / 'final_model.h5'}")

# Save class labels
class_labels = {v: k for k, v in train_generator.class_indices.items()}
with open(MODEL_OUTPUT_PATH / "class_labels.json", 'w') as f:
    json.dump(class_labels, f, indent=4)
print(f"✅ Class labels saved: {MODEL_OUTPUT_PATH / 'class_labels.json'}")

# Save training history
history_dict = {
    'accuracy': [float(x) for x in history.history['accuracy']],
    'val_accuracy': [float(x) for x in history.history['val_accuracy']],
    'loss': [float(x) for x in history.history['loss']],
    'val_loss': [float(x) for x in history.history['val_loss']]
}

with open(MODEL_OUTPUT_PATH / "training_history.json", 'w') as f:
    json.dump(history_dict, f, indent=4)
print(f"✅ Training history saved: {MODEL_OUTPUT_PATH / 'training_history.json'}")

# Plot training history
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(MODEL_OUTPUT_PATH / "training_history.png", dpi=150)
plt.close()
print(f"✅ Training plot saved: {MODEL_OUTPUT_PATH / 'training_history.png'}")

print("\n✅ STEP 2/3: TRAINING CNN MODEL completed successfully!")

# ========== STEP 3: TESTING ==========
print("\n" + "=" * 80)
print("STEP 3/3: TESTING PREDICTION")
print("=" * 80)

print("\n✅ Model training complete!")
print(f"\n📊 Final Results:")
print(f"  Training Accuracy: {history.history['accuracy'][-1]:.2%}")
print(f"  Validation Accuracy: {history.history['val_accuracy'][-1]:.2%}")

print("\n" + "=" * 80)
print("🎉 PIPELINE COMPLETE!")
print("=" * 80)

print(f"\n📁 Outputs:")
print(f"  Spectrograms: {SPECTROGRAM_OUTPUT}")
print(f"  Model: {MODEL_OUTPUT_PATH / 'best_model.h5'}")
print(f"  Class labels: {MODEL_OUTPUT_PATH / 'class_labels.json'}")

print(f"\n🧪 To test the model, run:")
print(f"  python 3_predict.py path/to/audio.wav")

print("\n✅ STEP 3/3: TESTING PREDICTION completed successfully!")
