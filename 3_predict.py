"""
Step 3: Predict Animal Sound from Audio File
This script takes a new audio file and predicts which animal it belongs to
"""

import tensorflow as tf
from tensorflow import keras
import librosa
import librosa.display
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
import json
import sys

# ========== CONFIGURATION ==========
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
MODEL_PATH = PROJECT_PATH / "trained_model" / "best_model.h5"  # Updated to match pipeline output
CLASS_LABELS_PATH = PROJECT_PATH / "trained_model" / "class_labels.json"
TEMP_SPEC_PATH = PROJECT_PATH / "temp_spectrogram.png"

# Audio parameters (must match training)
SAMPLE_RATE = 22050
DURATION = 3
N_MELS = 128
HOP_LENGTH = 512
IMG_SIZE = (128, 128)

def load_model_and_labels():
    """Load trained model and class labels"""
    if not MODEL_PATH.exists():
        print(f"❌ Model not found: {MODEL_PATH}")
        print("Please run '2_train_model.py' first!")
        return None, None
    
    if not CLASS_LABELS_PATH.exists():
        print(f"❌ Class labels not found: {CLASS_LABELS_PATH}")
        return None, None
    
    # Load model
    model = keras.models.load_model(MODEL_PATH)
    print(f"✅ Model loaded: {MODEL_PATH}")
    
    # Load class labels
    with open(CLASS_LABELS_PATH, 'r') as f:
        class_labels = json.load(f)
    print(f"✅ Class labels loaded: {list(class_labels.values())}")
    
    return model, class_labels

def load_and_preprocess_audio(audio_path, target_sr=SAMPLE_RATE, duration=DURATION):
    """Load and preprocess audio file"""
    try:
        print(f"🎵 Loading audio: {audio_path}")
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=target_sr, duration=duration)
        
        # Pad or trim to fixed length
        target_length = target_sr * duration
        if len(y) < target_length:
            y = np.pad(y, (0, target_length - len(y)), mode='constant')
        else:
            y = y[:target_length]
        
        print(f"✅ Audio loaded: {len(y)} samples, {sr} Hz")
        return y, sr
    except Exception as e:
        print(f"❌ Error loading audio: {e}")
        return None, None

def generate_spectrogram_image(y, sr, save_path):
    """Generate spectrogram and save as image"""
    try:
        # Generate mel-spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=y, 
            sr=sr, 
            n_mels=N_MELS,
            hop_length=HOP_LENGTH,
            fmax=sr//2
        )
        
        # Convert to dB scale
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Create figure without axes
        fig = plt.figure(figsize=(4, 4))
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Plot spectrogram
        librosa.display.specshow(
            mel_spec_db,
            sr=sr,
            hop_length=HOP_LENGTH,
            x_axis='time',
            y_axis='mel',
            cmap='inferno',
            ax=ax
        )
        
        # Save
        plt.savefig(save_path, dpi=72, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        print(f"✅ Spectrogram generated: {save_path}")
        return True
    except Exception as e:
        print(f"❌ Error generating spectrogram: {e}")
        plt.close()
        return False

def load_and_preprocess_image(image_path, target_size=IMG_SIZE):
    """Load and preprocess spectrogram image for model"""
    try:
        # Load image
        img = keras.preprocessing.image.load_img(image_path, target_size=target_size)
        
        # Convert to array
        img_array = keras.preprocessing.image.img_to_array(img)
        
        # Normalize
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return None

def predict_animal(audio_path, model, class_labels, show_probabilities=True):
    """Predict animal from audio file"""
    # Load and preprocess audio
    y, sr = load_and_preprocess_audio(audio_path)
    if y is None:
        return None
    
    # Generate spectrogram
    if not generate_spectrogram_image(y, sr, TEMP_SPEC_PATH):
        return None
    
    # Load spectrogram image
    img_array = load_and_preprocess_image(TEMP_SPEC_PATH)
    if img_array is None:
        return None
    
    # Make prediction
    print("\n🔮 Making prediction...")
    predictions = model.predict(img_array, verbose=0)
    predicted_class_idx = np.argmax(predictions[0])
    predicted_class = class_labels[str(predicted_class_idx)]
    confidence = predictions[0][predicted_class_idx] * 100
    
    # Clean up temp file
    if TEMP_SPEC_PATH.exists():
        TEMP_SPEC_PATH.unlink()
    
    # Display results
    print("\n" + "=" * 60)
    print("PREDICTION RESULTS")
    print("=" * 60)
    print(f"🐾 Predicted Animal: {predicted_class}")
    print(f"🎯 Confidence: {confidence:.2f}%")
    
    if show_probabilities:
        print("\n📊 All Class Probabilities:")
        # Sort by probability
        sorted_indices = np.argsort(predictions[0])[::-1]
        for idx in sorted_indices:
            animal = class_labels[str(idx)]
            prob = predictions[0][idx] * 100
            bar = "█" * int(prob / 2)
            print(f"  {animal:15s} {prob:6.2f}% {bar}")
    
    print("=" * 60)
    
    return {
        'predicted_animal': predicted_class,
        'confidence': confidence,
        'all_probabilities': {class_labels[str(i)]: float(predictions[0][i]) * 100 
                             for i in range(len(class_labels))}
    }

def main():
    print("=" * 60)
    print("ANIMAL SOUND CLASSIFIER - PREDICTION")
    print("=" * 60)
    
    # Load model and labels
    model, class_labels = load_model_and_labels()
    if model is None or class_labels is None:
        return
    
    # Get audio file path from command line or user input
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        print("\nEnter the path to the audio file (.wav or .mp3):")
        audio_file = input("> ").strip().strip('"')
    
    audio_path = Path(audio_file)
    
    # Check if file exists
    if not audio_path.exists():
        print(f"❌ Audio file not found: {audio_path}")
        return
    
    # Check file extension
    if audio_path.suffix.lower() not in ['.wav', '.mp3', '.flac', '.ogg']:
        print(f"⚠️ Warning: Unsupported file format. Supported: .wav, .mp3, .flac, .ogg")
    
    # Make prediction
    result = predict_animal(audio_path, model, class_labels)
    
    if result:
        print(f"\n✅ Prediction complete!")
        print(f"The audio file contains: {result['predicted_animal']} sound")

if __name__ == "__main__":
    main()
