"""
Flask Backend for Animal Voice Detection
Provides web interface for uploading audio files and getting predictions
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
from tensorflow import keras
import librosa
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
import json
import os
from werkzeug.utils import secure_filename
import traceback

app = Flask(__name__, static_folder='static')
CORS(app)

# ========== CONFIGURATION ==========
PROJECT_PATH = Path(__file__).parent
MODEL_PATH = PROJECT_PATH / "trained_model" / "best_model.h5"
CLASS_LABELS_PATH = PROJECT_PATH / "trained_model" / "class_labels.json"
UPLOAD_FOLDER = PROJECT_PATH / "uploads"
TEMP_SPEC_PATH = PROJECT_PATH / "temp_spectrogram.png"

# Create upload folder if it doesn't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Audio parameters (must match training)
SAMPLE_RATE = 22050
DURATION = 3
N_MELS = 128
HOP_LENGTH = 512
IMG_SIZE = (128, 128)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}

# Global variables for model and labels
model = None
class_labels = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model_and_labels():
    """Load trained model and class labels"""
    global model, class_labels
    
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    
    if not CLASS_LABELS_PATH.exists():
        raise FileNotFoundError(f"Class labels not found: {CLASS_LABELS_PATH}")
    
    # Load model
    model = keras.models.load_model(MODEL_PATH)
    print(f"✅ Model loaded: {MODEL_PATH}")
    
    # Load class labels
    with open(CLASS_LABELS_PATH, 'r') as f:
        class_labels = json.load(f)
    print(f"✅ Class labels loaded: {list(class_labels.values())}")

def load_and_preprocess_audio(audio_path, target_sr=SAMPLE_RATE, duration=DURATION):
    """Load and preprocess audio file"""
    # Load audio
    y, sr = librosa.load(audio_path, sr=target_sr, duration=duration)
    
    # Pad or trim to fixed length
    target_length = target_sr * duration
    if len(y) < target_length:
        y = np.pad(y, (0, target_length - len(y)), mode='constant')
    else:
        y = y[:target_length]
    
    return y, sr

def generate_spectrogram_image(y, sr, save_path):
    """Generate spectrogram and save as image"""
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

def load_and_preprocess_image(image_path, target_size=IMG_SIZE):
    """Load and preprocess spectrogram image for model"""
    # Load image
    img = keras.preprocessing.image.load_img(image_path, target_size=target_size)
    
    # Convert to array
    img_array = keras.preprocessing.image.img_to_array(img)
    
    # Normalize
    img_array = img_array / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_animal(audio_path):
    """Predict animal from audio file"""
    try:
        # Load and preprocess audio
        y, sr = load_and_preprocess_audio(audio_path)
        
        # Generate spectrogram
        generate_spectrogram_image(y, sr, TEMP_SPEC_PATH)
        
        # Load spectrogram image
        img_array = load_and_preprocess_image(TEMP_SPEC_PATH)
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = class_labels[str(predicted_class_idx)]
        confidence = float(predictions[0][predicted_class_idx]) * 100
        
        # Clean up temp file
        if TEMP_SPEC_PATH.exists():
            TEMP_SPEC_PATH.unlink()
        
        # Get all probabilities
        all_probabilities = {
            class_labels[str(i)]: float(predictions[0][i]) * 100 
            for i in range(len(class_labels))
        }
        
        # Sort by probability
        sorted_probs = dict(sorted(all_probabilities.items(), key=lambda x: x[1], reverse=True))
        
        return {
            'success': True,
            'predicted_animal': predicted_class,
            'confidence': confidence,
            'all_probabilities': sorted_probs
        }
    
    except Exception as e:
        print(f"Error in prediction: {e}")
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle audio file upload and prediction"""
    try:
        # Check if file is present
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['audio']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False, 
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = UPLOAD_FOLDER / filename
        file.save(filepath)
        
        # Make prediction
        result = predict_animal(filepath)
        
        # Clean up uploaded file
        if filepath.exists():
            filepath.unlink()
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in /predict endpoint: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("ANIMAL VOICE DETECTION - WEB SERVER")
    print("=" * 60)
    
    # Load model and labels
    try:
        load_model_and_labels()
        print("\n✅ Server ready!")
        print(f"📂 Upload folder: {UPLOAD_FOLDER}")
        print(f"🌐 Open browser to: http://localhost:5000")
        print("=" * 60)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        traceback.print_exc()
