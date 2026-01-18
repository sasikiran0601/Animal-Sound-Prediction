"""
Expand Existing Animal Sound Dataset
Adds more audio files to mini_project/data folder to reach 100 files per animal
"""

import os
import requests
from pathlib import Path
import shutil
from tqdm import tqdm
import librosa
import soundfile as sf
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configuration
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
DATA_PATH = PROJECT_PATH / "mini_project" / "data"

# Current animals in your dataset
EXISTING_ANIMALS = ['Bird', 'Cat', 'Cow', 'Crow', 'Dog', 'Frog', 'Hen', 'Insects', 'Pig', 'Rooster', 'Sheep']

# New animals to add
NEW_ANIMALS = ['Elephant', 'Goat', 'Lion', 'Tiger', 'Bear']

TARGET_COUNT = 100  # Target files per animal

# Freesound API (optional - set your key if you have one)
FREESOUND_API_KEY = "YOUR_API_KEY_HERE"
FREESOUND_BASE_URL = "https://freesound.org/apiv2"

def count_files(animal):
    """Count existing files for an animal"""
    pattern = f"{animal}_*.wav"
    return len(list(DATA_PATH.glob(pattern)))

def augment_audio_files(animal, current_count, target_count):
    """
    Augment existing audio files to reach target count
    Uses: time-stretching, pitch-shifting, noise addition
    """
    print(f"\n🔄 Augmenting {animal} sounds: {current_count} → {target_count}")
    
    # Get existing files
    existing_files = list(DATA_PATH.glob(f"{animal}_*.wav"))
    
    if not existing_files:
        print(f"⚠ No files found for {animal}")
        return 0
    
    needed = target_count - current_count
    augmented = 0
    
    # Start numbering from current_count + 1
    next_number = current_count + 1
    
    for i in tqdm(range(needed), desc=f"Augmenting {animal}"):
        # Select source file (cycle through existing files)
        source_file = existing_files[i % len(existing_files)]
        
        try:
            # Load audio
            y, sr = librosa.load(source_file, sr=22050)
            
            # Apply different augmentations
            aug_type = i % 4
            
            if aug_type == 0:
                # Time stretch (faster/slower)
                rate = np.random.uniform(0.85, 1.15)
                y_aug = librosa.effects.time_stretch(y, rate=rate)
            
            elif aug_type == 1:
                # Pitch shift
                n_steps = np.random.randint(-3, 4)
                y_aug = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
            
            elif aug_type == 2:
                # Add white noise
                noise_factor = np.random.uniform(0.002, 0.008)
                noise = np.random.normal(0, noise_factor, y.shape)
                y_aug = y + noise
            
            else:
                # Combine: pitch shift + time stretch
                n_steps = np.random.randint(-2, 3)
                rate = np.random.uniform(0.9, 1.1)
                y_aug = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
                y_aug = librosa.effects.time_stretch(y_aug, rate=rate)
            
            # Normalize
            y_aug = librosa.util.normalize(y_aug)
            
            # Save augmented file
            output_file = DATA_PATH / f"{animal}_{next_number}.wav"
            sf.write(output_file, y_aug, sr)
            
            augmented += 1
            next_number += 1
            
        except Exception as e:
            print(f"\nError augmenting {source_file.name}: {e}")
            continue
    
    return augmented

def download_from_freesound(animal, current_count, target_count):
    """Download additional files from Freesound API"""
    if FREESOUND_API_KEY == "YOUR_API_KEY_HERE":
        return 0
    
    needed = target_count - current_count
    print(f"\n📥 Downloading {animal} from Freesound...")
    
    url = f"{FREESOUND_BASE_URL}/search/text/"
    params = {
        'query': f"{animal.lower()} sound",
        'token': FREESOUND_API_KEY,
        'fields': 'id,name,previews,duration',
        'page_size': min(needed, 50),
        'filter': 'duration:[1 TO 10]'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        results = response.json()
        
        downloaded = 0
        next_number = current_count + 1
        
        for sound in results.get('results', [])[:needed]:
            try:
                preview_url = sound['previews']['preview-hq-mp3']
                output_file = DATA_PATH / f"{animal}_{next_number}.mp3"
                
                # Download
                audio_response = requests.get(preview_url, timeout=30)
                audio_response.raise_for_status()
                
                with open(output_file, 'wb') as f:
                    f.write(audio_response.content)
                
                downloaded += 1
                next_number += 1
                
            except Exception as e:
                continue
        
        return downloaded
        
    except Exception as e:
        print(f"Error downloading from Freesound: {e}")
        return 0

def create_new_animal_files(animal, count=100):
    """
    Create placeholder files for new animals
    User needs to manually add real audio files
    """
    print(f"\n📁 Creating placeholder structure for {animal}")
    print(f"⚠ You need to manually add {count} audio files for {animal}")
    print(f"   Save them as: {animal}_1.wav, {animal}_2.wav, ... {animal}_{count}.wav")
    print(f"   Location: {DATA_PATH}")
    
    # Create a README file with instructions
    readme_file = DATA_PATH / f"README_{animal}.txt"
    with open(readme_file, 'w') as f:
        f.write(f"Instructions for {animal} audio files:\n")
        f.write(f"="*50 + "\n\n")
        f.write(f"1. Download {count} {animal.lower()} sound files from:\n")
        f.write(f"   - Freesound.org (search '{animal.lower()} sound')\n")
        f.write(f"   - BBC Sound Effects: https://sound-effects.bbcrewind.co.uk/\n")
        f.write(f"   - Xeno-Canto (for birds): https://www.xeno-canto.org/\n\n")
        f.write(f"2. Save files in this folder as:\n")
        f.write(f"   {animal}_1.wav\n")
        f.write(f"   {animal}_2.wav\n")
        f.write(f"   ...\n")
        f.write(f"   {animal}_{count}.wav\n\n")
        f.write(f"3. Supported formats: .wav or .mp3\n")
        f.write(f"4. Recommended duration: 1-10 seconds\n")
        f.write(f"5. Quality: Clear animal sounds, minimal background noise\n")

def generate_summary():
    """Generate summary of current dataset"""
    print("\n" + "="*80)
    print("DATASET SUMMARY")
    print("="*80)
    
    all_animals = EXISTING_ANIMALS + NEW_ANIMALS
    total_files = 0
    
    summary = {}
    
    for animal in sorted(all_animals):
        count = count_files(animal)
        total_files += count
        summary[animal] = count
        
        status = "✓" if count >= TARGET_COUNT else "⚠" if count > 0 else "✗"
        percentage = (count / TARGET_COUNT) * 100 if count > 0 else 0
        
        print(f"{status} {animal:12} : {count:3}/{TARGET_COUNT} ({percentage:5.1f}%)")
    
    print(f"\nTotal files: {total_files}/{len(all_animals) * TARGET_COUNT}")
    
    # Save summary
    import json
    summary_file = DATA_PATH / "dataset_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "animals": summary,
            "total_files": total_files,
            "target_per_animal": TARGET_COUNT,
            "total_target": len(all_animals) * TARGET_COUNT
        }, f, indent=2)
    
    return summary

def main():
    print("="*80)
    print("Animal Sound Dataset Expander")
    print("="*80)
    print(f"\nWorking directory: {DATA_PATH}")
    
    # Check current status
    print("\n📊 Current Status:")
    current_summary = generate_summary()
    
    # Expand existing animals
    print("\n" + "="*80)
    print("EXPANDING EXISTING ANIMALS")
    print("="*80)
    
    for animal in EXISTING_ANIMALS:
        current_count = current_summary.get(animal, 0)
        
        if current_count >= TARGET_COUNT:
            print(f"\n✓ {animal}: Already has {current_count} files")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing {animal}: {current_count}/{TARGET_COUNT}")
        print(f"{'='*60}")
        
        # Try Freesound first (if API key is set)
        if FREESOUND_API_KEY != "YOUR_API_KEY_HERE":
            downloaded = download_from_freesound(animal, current_count, TARGET_COUNT)
            current_count += downloaded
            print(f"Downloaded: {downloaded} files")
        
        # Use augmentation to fill remaining
        if current_count < TARGET_COUNT:
            augmented = augment_audio_files(animal, current_count, TARGET_COUNT)
            print(f"Augmented: {augmented} files")
    
    # Handle new animals
    print("\n" + "="*80)
    print("NEW ANIMALS (Manual Download Required)")
    print("="*80)
    
    for animal in NEW_ANIMALS:
        create_new_animal_files(animal, TARGET_COUNT)
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    generate_summary()
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. For new animals (Elephant, Goat, Lion, Tiger, Bear):")
    print("   - Check the README_*.txt files in the data folder")
    print("   - Download audio files from suggested sources")
    print("   - Save them with correct naming: Animal_1.wav, Animal_2.wav, etc.")
    
    print("\n2. To get more files via Freesound API:")
    print("   - Get free API key: https://freesound.org/apiv2/apply/")
    print("   - Edit this script and set FREESOUND_API_KEY")
    print("   - Run again")
    
    print("\n3. Manual download sources:")
    print("   - BBC Sound Effects: https://sound-effects.bbcrewind.co.uk/")
    print("   - Freesound: https://freesound.org/")
    print("   - Xeno-Canto (birds): https://www.xeno-canto.org/")
    
    print(f"\n✓ Dataset location: {DATA_PATH}")

if __name__ == "__main__":
    main()
