"""
Step 4: Batch Prediction - Test model on multiple audio files
Useful for evaluating model performance on test set
"""

import tensorflow as tf
from tensorflow import keras
import librosa
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
import json
import pandas as pd
from tqdm import tqdm

# ========== CONFIGURATION ==========
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
MODEL_PATH = PROJECT_PATH / "trained_model" / "animal_sound_classifier.h5"
CLASS_LABELS_PATH = PROJECT_PATH / "trained_model" / "class_labels.json"
RESULTS_PATH = PROJECT_PATH / "batch_predictions.csv"

# Audio parameters
SAMPLE_RATE = 22050
DURATION = 3
N_MELS = 128
HOP_LENGTH = 512
IMG_SIZE = (128, 128)

def load_model_and_labels():
    """Load trained model and class labels"""
    model = keras.models.load_model(MODEL_PATH)
    with open(CLASS_LABELS_PATH, 'r') as f:
        class_labels = json.load(f)
    return model, class_labels

def load_and_preprocess_audio(audio_path):
    """Load and preprocess audio file"""
    try:
        y, sr = librosa.load(audio_path, sr=SAMPLE_RATE, duration=DURATION)
        target_length = SAMPLE_RATE * DURATION
        if len(y) < target_length:
            y = np.pad(y, (0, target_length - len(y)), mode='constant')
        else:
            y = y[:target_length]
        return y, sr
    except:
        return None, None

def audio_to_spectrogram_array(y, sr):
    """Convert audio to spectrogram array for model input"""
    try:
        # Generate mel-spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=y, sr=sr, n_mels=N_MELS, hop_length=HOP_LENGTH, fmax=sr//2
        )
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Normalize to 0-1
        mel_spec_norm = (mel_spec_db - mel_spec_db.min()) / (mel_spec_db.max() - mel_spec_db.min())
        
        # Resize to target size
        from scipy.ndimage import zoom
        zoom_factors = (IMG_SIZE[0] / mel_spec_norm.shape[0], 
                       IMG_SIZE[1] / mel_spec_norm.shape[1])
        mel_spec_resized = zoom(mel_spec_norm, zoom_factors, order=1)
        
        # Convert to RGB (3 channels)
        mel_spec_rgb = np.stack([mel_spec_resized] * 3, axis=-1)
        
        # Add batch dimension
        return np.expand_dims(mel_spec_rgb, axis=0)
    except:
        return None

def predict_single(audio_path, model, class_labels):
    """Predict single audio file"""
    y, sr = load_and_preprocess_audio(audio_path)
    if y is None:
        return None, None, None
    
    img_array = audio_to_spectrogram_array(y, sr)
    if img_array is None:
        return None, None, None
    
    predictions = model.predict(img_array, verbose=0)
    predicted_idx = np.argmax(predictions[0])
    predicted_class = class_labels[str(predicted_idx)]
    confidence = predictions[0][predicted_idx] * 100
    
    return predicted_class, confidence, predictions[0]

def batch_predict(audio_folder, model, class_labels, output_csv=None):
    """Predict on all audio files in a folder"""
    audio_folder = Path(audio_folder)
    
    # Find all audio files
    audio_files = []
    for ext in ['*.wav', '*.mp3', '*.flac', '*.ogg']:
        audio_files.extend(list(audio_folder.rglob(ext)))
    
    if len(audio_files) == 0:
        print(f"❌ No audio files found in {audio_folder}")
        return None
    
    print(f"📁 Found {len(audio_files)} audio files")
    
    # Process each file
    results = []
    for audio_path in tqdm(audio_files, desc="Processing"):
        # Extract true label from filename if available
        filename = audio_path.name
        true_label = filename.split('_')[0] if '_' in filename else 'Unknown'
        
        # Make prediction
        pred_class, confidence, all_probs = predict_single(audio_path, model, class_labels)
        
        if pred_class is None:
            continue
        
        # Store result
        result = {
            'filename': filename,
            'filepath': str(audio_path),
            'true_label': true_label,
            'predicted_label': pred_class,
            'confidence': confidence,
            'correct': (true_label.lower() == pred_class.lower())
        }
        
        # Add all class probabilities
        for idx, prob in enumerate(all_probs):
            class_name = class_labels[str(idx)]
            result[f'prob_{class_name}'] = prob * 100
        
        results.append(result)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Save to CSV if requested
    if output_csv:
        df.to_csv(output_csv, index=False)
        print(f"✅ Results saved to: {output_csv}")
    
    return df

def print_summary(df):
    """Print summary statistics"""
    print("\n" + "=" * 70)
    print("BATCH PREDICTION SUMMARY")
    print("=" * 70)
    
    total = len(df)
    print(f"\n📊 Total files processed: {total}")
    
    # Overall accuracy (if true labels available)
    if 'correct' in df.columns and df['true_label'].iloc[0] != 'Unknown':
        correct = df['correct'].sum()
        accuracy = (correct / total) * 100
        print(f"✅ Correct predictions: {correct}/{total} ({accuracy:.2f}%)")
        print(f"❌ Incorrect predictions: {total - correct}/{total}")
    
    # Average confidence
    avg_confidence = df['confidence'].mean()
    print(f"\n🎯 Average confidence: {avg_confidence:.2f}%")
    
    # Per-class statistics
    print("\n📈 Per-class predictions:")
    pred_counts = df['predicted_label'].value_counts()
    for animal, count in pred_counts.items():
        percentage = (count / total) * 100
        print(f"  {animal:15s}: {count:3d} ({percentage:5.1f}%)")
    
    # Confusion matrix (if true labels available)
    if 'correct' in df.columns and df['true_label'].iloc[0] != 'Unknown':
        print("\n📊 Confusion Matrix:")
        confusion = pd.crosstab(df['true_label'], df['predicted_label'], 
                               rownames=['True'], colnames=['Predicted'])
        print(confusion)
    
    print("=" * 70)

def main():
    print("=" * 70)
    print("BATCH PREDICTION - TEST MULTIPLE AUDIO FILES")
    print("=" * 70)
    
    # Load model
    print("\n🔧 Loading model...")
    model, class_labels = load_model_and_labels()
    print(f"✅ Model loaded with {len(class_labels)} classes")
    
    # Get folder path
    print("\nEnter the folder path containing audio files:")
    print("(Press Enter to use mini_project folder)")
    folder_input = input("> ").strip().strip('"')
    
    if not folder_input:
        folder_path = PROJECT_PATH / "mini_project"
    else:
        folder_path = Path(folder_input)
    
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # Run batch prediction
    print(f"\n🎵 Processing audio files in: {folder_path}")
    df = batch_predict(folder_path, model, class_labels, output_csv=RESULTS_PATH)
    
    if df is not None and len(df) > 0:
        # Print summary
        print_summary(df)
        
        # Show top predictions
        print("\n🔝 Top 10 Most Confident Predictions:")
        top_10 = df.nlargest(10, 'confidence')[['filename', 'predicted_label', 'confidence']]
        print(top_10.to_string(index=False))
        
        # Show low confidence predictions
        if len(df) >= 10:
            print("\n⚠️ Top 10 Least Confident Predictions:")
            bottom_10 = df.nsmallest(10, 'confidence')[['filename', 'predicted_label', 'confidence']]
            print(bottom_10.to_string(index=False))

if __name__ == "__main__":
    main()
