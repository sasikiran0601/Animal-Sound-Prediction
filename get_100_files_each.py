"""
Get 100 Audio Files for Each Missing Animal
Elephant, Goat, Lion, Tiger, Bear
Combines: Freesound API + Manual Download Guide + Auto-Augmentation
"""

import os
import requests
from pathlib import Path
import time
from tqdm import tqdm
import json
import librosa
import soundfile as sf
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configuration
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
DATA_PATH = PROJECT_PATH / "mini_project" / "data"

ANIMALS = ['Elephant', 'Goat', 'Lion', 'Tiger', 'Bear']
TARGET_COUNT = 100

# Freesound API (get from https://freesound.org/apiv2/apply/)
FREESOUND_API_KEY = "YOUR_API_KEY_HERE"
FREESOUND_BASE_URL = "https://freesound.org/apiv2"

def count_files(animal):
    """Count existing audio files for an animal"""
    wav_files = list(DATA_PATH.glob(f"{animal}_*.wav"))
    mp3_files = list(DATA_PATH.glob(f"{animal}_*.mp3"))
    return len(wav_files) + len(mp3_files)

def get_next_file_number(animal):
    """Get the next file number for an animal"""
    existing = count_files(animal)
    return existing + 1

def download_from_freesound(animal, needed):
    """Download from Freesound API"""
    if FREESOUND_API_KEY == "YOUR_API_KEY_HERE":
        return 0
    
    print(f"\n📥 Downloading {animal} from Freesound (need {needed} files)...")
    
    # Search queries
    search_terms = {
        'Elephant': ['elephant trumpet', 'elephant sound', 'elephant call'],
        'Goat': ['goat bleat', 'goat sound', 'goat call'],
        'Lion': ['lion roar', 'lion growl', 'lion sound'],
        'Tiger': ['tiger roar', 'tiger growl', 'tiger sound'],
        'Bear': ['bear growl', 'bear roar', 'bear sound']
    }
    
    all_results = []
    
    for query in search_terms.get(animal, [animal.lower()]):
        url = f"{FREESOUND_BASE_URL}/search/text/"
        params = {
            'query': query,
            'token': FREESOUND_API_KEY,
            'fields': 'id,name,previews,duration',
            'page_size': 50,
            'filter': 'duration:[1 TO 15]'
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'results' in data:
                all_results.extend(data['results'])
            
            time.sleep(0.5)
        except:
            continue
    
    # Remove duplicates
    unique = {r['id']: r for r in all_results}.values()
    
    # Download
    downloaded = 0
    start_num = get_next_file_number(animal)
    
    for sound in list(unique)[:needed]:
        try:
            preview_url = sound['previews']['preview-hq-mp3']
            filepath = DATA_PATH / f"{animal}_{start_num + downloaded}.mp3"
            
            if filepath.exists():
                downloaded += 1
                continue
            
            response = requests.get(preview_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            downloaded += 1
            time.sleep(0.3)
            
        except:
            continue
    
    print(f"  ✓ Downloaded: {downloaded} files")
    return downloaded

def augment_to_100(animal, current_count):
    """Augment existing files to reach 100"""
    if current_count == 0:
        print(f"  ⚠ No files to augment for {animal}")
        return 0
    
    needed = TARGET_COUNT - current_count
    
    if needed <= 0:
        return 0
    
    print(f"\n🔄 Augmenting {animal}: {current_count} → {TARGET_COUNT}")
    
    # Get existing files
    existing = list(DATA_PATH.glob(f"{animal}_*.wav")) + list(DATA_PATH.glob(f"{animal}_*.mp3"))
    
    if not existing:
        return 0
    
    augmented = 0
    start_num = current_count + 1
    
    for i in tqdm(range(needed), desc=f"  Augmenting {animal}"):
        source = existing[i % len(existing)]
        
        try:
            # Load audio
            y, sr = librosa.load(source, sr=22050)
            
            # Apply augmentation
            aug_type = i % 5
            
            if aug_type == 0:
                # Time stretch
                y_aug = librosa.effects.time_stretch(y, rate=np.random.uniform(0.85, 1.15))
            elif aug_type == 1:
                # Pitch shift
                y_aug = librosa.effects.pitch_shift(y, sr=sr, n_steps=np.random.randint(-3, 4))
            elif aug_type == 2:
                # Add noise
                noise = np.random.normal(0, 0.005, y.shape)
                y_aug = y + noise
            elif aug_type == 3:
                # Time stretch + pitch
                y_aug = librosa.effects.time_stretch(y, rate=np.random.uniform(0.9, 1.1))
                y_aug = librosa.effects.pitch_shift(y_aug, sr=sr, n_steps=np.random.randint(-2, 3))
            else:
                # Reverse + effects
                y_aug = y[::-1]
                y_aug = librosa.effects.pitch_shift(y_aug, sr=sr, n_steps=np.random.randint(-1, 2))
            
            # Normalize
            y_aug = librosa.util.normalize(y_aug)
            
            # Save
            output = DATA_PATH / f"{animal}_{start_num + augmented}.wav"
            sf.write(output, y_aug, sr)
            
            augmented += 1
            
        except Exception as e:
            continue
    
    print(f"  ✓ Augmented: {augmented} files")
    return augmented

def show_manual_instructions(animal, needed):
    """Show manual download instructions"""
    print(f"\n{'='*60}")
    print(f"📥 MANUAL DOWNLOAD: {animal} ({needed} files needed)")
    print(f"{'='*60}")
    
    sources = {
        'Elephant': {
            'BBC': 'https://sound-effects.bbcrewind.co.uk/search?q=elephant',
            'Freesound': 'https://freesound.org/search/?q=elephant+trumpet',
            'Pixabay': 'https://pixabay.com/sound-effects/search/elephant/',
        },
        'Goat': {
            'BBC': 'https://sound-effects.bbcrewind.co.uk/search?q=goat',
            'Freesound': 'https://freesound.org/search/?q=goat+bleat',
            'Pixabay': 'https://pixabay.com/sound-effects/search/goat/',
        },
        'Lion': {
            'BBC': 'https://sound-effects.bbcrewind.co.uk/search?q=lion',
            'Freesound': 'https://freesound.org/search/?q=lion+roar',
            'Pixabay': 'https://pixabay.com/sound-effects/search/lion/',
        },
        'Tiger': {
            'BBC': 'https://sound-effects.bbcrewind.co.uk/search?q=tiger',
            'Freesound': 'https://freesound.org/search/?q=tiger+roar',
            'Pixabay': 'https://pixabay.com/sound-effects/search/tiger/',
        },
        'Bear': {
            'BBC': 'https://sound-effects.bbcrewind.co.uk/search?q=bear',
            'Freesound': 'https://freesound.org/search/?q=bear+growl',
            'Pixabay': 'https://pixabay.com/sound-effects/search/bear/',
        }
    }
    
    print(f"\n🌐 Download from these sources:")
    for source, url in sources.get(animal, {}).items():
        print(f"   {source}: {url}")
    
    next_num = get_next_file_number(animal)
    print(f"\n📝 Save files as:")
    print(f"   {DATA_PATH}\\{animal}_{next_num}.wav")
    print(f"   {DATA_PATH}\\{animal}_{next_num+1}.wav")
    print(f"   ... (continue numbering)")
    
    print(f"\n💡 Tip: Download at least 30-40 files, then run this script again")
    print(f"        It will augment them to reach 100!")

def process_animal(animal):
    """Process one animal to get 100 files"""
    print(f"\n{'='*70}")
    print(f"🐾 PROCESSING: {animal.upper()}")
    print(f"{'='*70}")
    
    current = count_files(animal)
    print(f"Current files: {current}/{TARGET_COUNT}")
    
    if current >= TARGET_COUNT:
        print(f"✓ Already has {current} files!")
        return current
    
    needed = TARGET_COUNT - current
    
    # Strategy 1: Try Freesound API
    if FREESOUND_API_KEY != "YOUR_API_KEY_HERE":
        downloaded = download_from_freesound(animal, needed)
        current += downloaded
        needed = TARGET_COUNT - current
    
    # Strategy 2: If we have some files (30+), augment to 100
    if current >= 30:
        augmented = augment_to_100(animal, current)
        current += augmented
    
    # Strategy 3: If still not enough, show manual instructions
    if current < TARGET_COUNT:
        needed = TARGET_COUNT - current
        
        if current < 30:
            print(f"\n⚠ Need at least 30 files to augment effectively")
            print(f"   Current: {current}, Need: {30 - current} more for augmentation")
            show_manual_instructions(animal, 30 - current)
        else:
            show_manual_instructions(animal, needed)
    
    final_count = count_files(animal)
    print(f"\n{'='*70}")
    print(f"✓ {animal}: {final_count}/{TARGET_COUNT} files")
    print(f"{'='*70}")
    
    return final_count

def create_summary():
    """Create final summary"""
    print("\n" + "="*80)
    print("FINAL SUMMARY - ALL ANIMALS")
    print("="*80)
    
    summary = {}
    total = 0
    
    for animal in ANIMALS:
        count = count_files(animal)
        summary[animal] = count
        total += count
        
        status = "✓" if count >= TARGET_COUNT else "⚠" if count >= 30 else "✗"
        percentage = (count / TARGET_COUNT) * 100
        bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
        
        print(f"{status} {animal:12} : {count:3}/{TARGET_COUNT} [{bar}] {percentage:5.1f}%")
    
    print(f"\nTotal files: {total}/{len(ANIMALS) * TARGET_COUNT}")
    
    # Save to JSON
    summary_data = {
        "animals": summary,
        "total_files": total,
        "target_per_animal": TARGET_COUNT,
        "total_target": len(ANIMALS) * TARGET_COUNT,
        "completion_percentage": (total / (len(ANIMALS) * TARGET_COUNT)) * 100
    }
    
    with open(DATA_PATH / "missing_animals_summary.json", 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    return summary

def main():
    print("="*80)
    print("GET 100 AUDIO FILES FOR EACH ANIMAL")
    print("Elephant, Goat, Lion, Tiger, Bear")
    print("="*80)
    
    print(f"\n📁 Data folder: {DATA_PATH}")
    
    # Check if librosa is installed
    try:
        import librosa
        import soundfile
    except ImportError:
        print("\n⚠ Required packages not installed!")
        print("Run: pip install librosa soundfile")
        return
    
    # Process each animal
    results = {}
    for animal in ANIMALS:
        results[animal] = process_animal(animal)
        time.sleep(1)  # Brief pause between animals
    
    # Final summary
    create_summary()
    
    # Next steps
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    
    incomplete = [a for a, c in results.items() if c < TARGET_COUNT]
    
    if not incomplete:
        print("\n🎉 SUCCESS! All animals have 100 files!")
        print("\nYou can now:")
        print("1. Run: python new_animal_sound_pipeline.py")
        print("   (This will generate spectrograms and train the model)")
    else:
        print(f"\n⚠ Incomplete animals: {', '.join(incomplete)}")
        print("\nOptions:")
        print("\n1. Get Freesound API key (recommended):")
        print("   - Visit: https://freesound.org/apiv2/apply/")
        print("   - Edit this script line 21 with your key")
        print("   - Run this script again")
        
        print("\n2. Download manually:")
        print("   - Use the URLs shown above for each animal")
        print("   - Download 30-40 files per animal")
        print("   - Save with correct naming")
        print("   - Run this script again (it will augment to 100)")
        
        print("\n3. Use what you have:")
        print("   - If you have 30+ files per animal, run this script again")
        print("   - It will augment them to 100")

if __name__ == "__main__":
    main()
