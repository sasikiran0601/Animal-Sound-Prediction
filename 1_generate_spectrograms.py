"""
Step 1: Generate Spectrograms from Audio Files
This script processes 100 animal sound files and generates spectrograms for CNN training
"""

import pandas as pd
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

# ========== CONFIGURATION ==========
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
MINI_PROJECT_PATH = PROJECT_PATH / "mini_project"
CSV_PATH = MINI_PROJECT_PATH / "sounds.csv"
SPECTROGRAM_OUTPUT = PROJECT_PATH / "spectrograms_dataset"
IMG_SIZE = (128, 128)  # Standard size for CNN input
SAMPLE_LIMIT = 100  # Process first 100 samples

# Audio processing parameters
SAMPLE_RATE = 22050  # Standard sample rate
DURATION = 3  # Fixed duration in seconds
N_MELS = 128  # Number of mel bands
HOP_LENGTH = 512

# Create output directory
SPECTROGRAM_OUTPUT.mkdir(parents=True, exist_ok=True)

def extract_label(filename):
    """Extract animal label from filename (e.g., 'Lion_1.wav' -> 'Lion')"""
    return filename.split('_')[0]

def load_and_preprocess_audio(audio_path, target_sr=SAMPLE_RATE, duration=DURATION):
    """Load audio file and preprocess to fixed length"""
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=target_sr, duration=duration)
        
        # Pad or trim to fixed length
        target_length = target_sr * duration
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
        
        # Create figure without axes for clean image
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
        
        # Save figure
        plt.savefig(save_path, dpi=72, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        return True
    except Exception as e:
        print(f"Error generating spectrogram: {e}")
        plt.close()
        return False

def main():
    print("=" * 60)
    print("STEP 1: GENERATING SPECTROGRAMS FOR CNN TRAINING")
    print("=" * 60)
    
    # Check if CSV exists
    if not CSV_PATH.exists():
        print(f"❌ CSV file not found: {CSV_PATH}")
        return
    
    # Read CSV
    df = pd.read_csv(CSV_PATH)
    print(f"✅ Loaded CSV with {len(df)} entries")
    
    # Limit to first 100 samples
    df = df.head(SAMPLE_LIMIT)
    print(f"📊 Processing first {len(df)} samples")
    
    # Get unique animal classes
    df['label'] = df['name'].apply(extract_label)
    animals = df['label'].unique()
    print(f"🐾 Found {len(animals)} animal classes: {', '.join(animals)}")
    
    # Create directories for each animal class
    for animal in animals:
        (SPECTROGRAM_OUTPUT / animal).mkdir(parents=True, exist_ok=True)
    
    # Process each audio file
    success_count = 0
    fail_count = 0
    
    print("\n🎵 Processing audio files...")
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Generating spectrograms"):
        filename = row['name']
        label = row['label']
        
        # Try to find the audio file in mini_project directory
        audio_path = MINI_PROJECT_PATH / filename
        
        # If not found, try in data subdirectory
        if not audio_path.exists():
            audio_path = MINI_PROJECT_PATH / "data" / filename
        
        # If still not found, skip
        if not audio_path.exists():
            fail_count += 1
            continue
        
        # Load and preprocess audio
        y, sr = load_and_preprocess_audio(audio_path)
        if y is None:
            fail_count += 1
            continue
        
        # Generate spectrogram filename
        spec_filename = f"{Path(filename).stem}_spec.png"
        save_path = SPECTROGRAM_OUTPUT / label / spec_filename
        
        # Generate and save spectrogram
        if generate_mel_spectrogram(y, sr, save_path):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully generated: {success_count} spectrograms")
    print(f"❌ Failed: {fail_count} files")
    print(f"📁 Output directory: {SPECTROGRAM_OUTPUT}")
    
    # Print class distribution
    print("\n📊 Class Distribution:")
    for animal in animals:
        count = len(list((SPECTROGRAM_OUTPUT / animal).glob("*.png")))
        print(f"  {animal}: {count} spectrograms")
    
    print("\n✅ Spectrogram generation complete!")
    print("Next step: Run '2_train_model.py' to train the CNN")

if __name__ == "__main__":
    main()
