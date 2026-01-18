"""
Multi-Source Animal Sound Downloader
Downloads from ESC-50, Kaggle, and other open sources
"""

import os
import requests
from pathlib import Path
import zipfile
import shutil
from tqdm import tqdm
import json

# Configuration
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
OUTPUT_PATH = PROJECT_PATH / "animal_audio_dataset"
TEMP_PATH = PROJECT_PATH / "temp_downloads"

ANIMALS = [
    'cat', 'dog', 'elephant', 'cow', 'frog', 
    'sheep', 'bird', 'goat', 'lion', 'tiger',
    'hen', 'pig', 'rooster', 'bear'
]

TARGET_COUNT = 100

def create_directories():
    """Create directory structure"""
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    TEMP_PATH.mkdir(parents=True, exist_ok=True)
    
    for animal in ANIMALS:
        (OUTPUT_PATH / animal).mkdir(exist_ok=True)
    
    print(f"✓ Directories created")

def download_file(url, filepath, desc="Downloading"):
    """Download a file with progress bar"""
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f, tqdm(
            desc=desc,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                size = f.write(chunk)
                pbar.update(size)
        
        return True
    except Exception as e:
        print(f"Error downloading: {e}")
        return False

def download_esc50():
    """Download ESC-50 dataset"""
    print("\n" + "="*60)
    print("Downloading ESC-50 Dataset")
    print("="*60)
    
    url = "https://github.com/karoldvl/ESC-50/archive/master.zip"
    zip_path = TEMP_PATH / "esc50.zip"
    extract_path = TEMP_PATH / "ESC-50-master"
    
    # Download
    if not zip_path.exists():
        print("Downloading ESC-50 (600MB)...")
        if not download_file(url, zip_path, "ESC-50"):
            return False
    
    # Extract
    if not extract_path.exists():
        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TEMP_PATH)
    
    # Map ESC-50 classes to our animals
    esc50_mapping = {
        'dog': '0',      # dog
        'rooster': '14', # rooster
        'pig': '9',      # pig
        'cow': '38',     # cow
        'frog': '8',     # frog
        'cat': '5',      # cat
        'hen': '13',     # hen
        'sheep': '10',   # sheep
    }
    
    # Copy files
    audio_path = extract_path / "audio"
    if audio_path.exists():
        for animal, class_id in esc50_mapping.items():
            animal_dir = OUTPUT_PATH / animal
            
            # Find all files for this class
            for audio_file in audio_path.glob(f"*-{class_id}-*.wav"):
                dest = animal_dir / audio_file.name
                if not dest.exists():
                    shutil.copy2(audio_file, dest)
            
            count = len(list(animal_dir.glob("*.wav")))
            print(f"✓ {animal}: {count} files")
    
    return True

def download_animal_sound_dataset():
    """Download from YashNita Animal Sound Dataset"""
    print("\n" + "="*60)
    print("Downloading Animal Sound Dataset (GitHub)")
    print("="*60)
    
    # This dataset has: cat, dog, bird, cow, lion, sheep, frog, chicken, donkey, monkey
    url = "https://github.com/YashNita/Animal-Sound-Dataset/archive/refs/heads/master.zip"
    zip_path = TEMP_PATH / "animal_sounds.zip"
    
    if not zip_path.exists():
        print("Downloading Animal Sound Dataset...")
        if not download_file(url, zip_path, "Animal Sounds"):
            return False
    
    # Extract
    extract_path = TEMP_PATH / "Animal-Sound-Dataset-master"
    if not extract_path.exists():
        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TEMP_PATH)
    
    # Map folders
    mapping = {
        'Cat': 'cat',
        'Dog': 'dog',
        'Bird': 'bird',
        'Cow': 'cow',
        'Lion': 'lion',
        'Sheep': 'sheep',
        'Frog': 'frog',
        'Chicken': 'hen',
    }
    
    # Copy files
    for source_name, target_name in mapping.items():
        source_dir = extract_path / source_name
        if source_dir.exists():
            target_dir = OUTPUT_PATH / target_name
            
            for audio_file in source_dir.glob("*.wav"):
                dest = target_dir / f"github_{audio_file.name}"
                if not dest.exists():
                    shutil.copy2(audio_file, dest)
            
            count = len(list(target_dir.glob("*.wav")))
            print(f"✓ {target_name}: {count} files")
    
    return True

def download_additional_sources():
    """Download from additional open sources"""
    print("\n" + "="*60)
    print("Additional Sources Information")
    print("="*60)
    
    sources = {
        "BBC Sound Effects (Free)": {
            "url": "https://sound-effects.bbcrewind.co.uk/",
            "animals": "All animals available",
            "note": "Manual download required - search for each animal"
        },
        "FreeSound.org": {
            "url": "https://freesound.org/",
            "animals": "All animals available",
            "note": "Requires API key (see download_animal_sounds.py)"
        },
        "Xeno-Canto (Birds)": {
            "url": "https://www.xeno-canto.org/",
            "animals": "Bird sounds",
            "note": "700,000+ bird recordings"
        },
        "Animal Sound Archive": {
            "url": "https://www.tierstimmenarchiv.de/",
            "animals": "Various animals",
            "note": "Museum für Naturkunde Berlin"
        }
    }
    
    print("\nManual download sources:")
    for name, info in sources.items():
        print(f"\n{name}:")
        print(f"  URL: {info['url']}")
        print(f"  Animals: {info['animals']}")
        print(f"  Note: {info['note']}")

def augment_dataset():
    """
    Augment existing audio files to reach target count
    Uses time-stretching, pitch-shifting, and adding noise
    """
    print("\n" + "="*60)
    print("Dataset Augmentation")
    print("="*60)
    
    try:
        import librosa
        import soundfile as sf
        import numpy as np
    except ImportError:
        print("⚠ librosa not installed. Install with: pip install librosa soundfile")
        return
    
    for animal in ANIMALS:
        animal_dir = OUTPUT_PATH / animal
        existing_files = list(animal_dir.glob("*.wav")) + list(animal_dir.glob("*.mp3"))
        current_count = len(existing_files)
        
        if current_count == 0:
            print(f"⚠ {animal}: No files to augment")
            continue
        
        if current_count >= TARGET_COUNT:
            print(f"✓ {animal}: Already has {current_count} files")
            continue
        
        needed = TARGET_COUNT - current_count
        print(f"\n{animal}: Augmenting {current_count} → {TARGET_COUNT} files")
        
        augmented = 0
        file_idx = 0
        
        while augmented < needed and file_idx < len(existing_files):
            source_file = existing_files[file_idx % len(existing_files)]
            
            try:
                # Load audio
                y, sr = librosa.load(source_file, sr=22050)
                
                # Apply random augmentation
                aug_type = augmented % 3
                
                if aug_type == 0:
                    # Time stretch
                    y_aug = librosa.effects.time_stretch(y, rate=np.random.uniform(0.9, 1.1))
                elif aug_type == 1:
                    # Pitch shift
                    y_aug = librosa.effects.pitch_shift(y, sr=sr, n_steps=np.random.randint(-2, 3))
                else:
                    # Add noise
                    noise = np.random.normal(0, 0.005, y.shape)
                    y_aug = y + noise
                
                # Save augmented file
                output_file = animal_dir / f"{animal}_aug_{augmented+1:03d}.wav"
                sf.write(output_file, y_aug, sr)
                
                augmented += 1
                
            except Exception as e:
                print(f"Error augmenting {source_file.name}: {e}")
            
            file_idx += 1
        
        new_count = len(list(animal_dir.glob("*.wav"))) + len(list(animal_dir.glob("*.mp3")))
        print(f"✓ {animal}: {new_count} files (added {augmented} augmented)")

def generate_summary():
    """Generate dataset summary"""
    print("\n" + "="*60)
    print("DATASET SUMMARY")
    print("="*60)
    
    summary = {
        "animals": {},
        "total_files": 0,
        "target_per_animal": TARGET_COUNT,
        "total_target": len(ANIMALS) * TARGET_COUNT
    }
    
    for animal in ANIMALS:
        animal_dir = OUTPUT_PATH / animal
        count = len(list(animal_dir.glob("*.wav"))) + len(list(animal_dir.glob("*.mp3")))
        summary["animals"][animal] = count
        summary["total_files"] += count
        
        status = "✓" if count >= TARGET_COUNT else "⚠"
        percentage = (count / TARGET_COUNT) * 100
        print(f"{status} {animal.capitalize():12} : {count:3}/{TARGET_COUNT} ({percentage:.0f}%)")
    
    print(f"\nTotal: {summary['total_files']}/{summary['total_target']} files")
    
    # Save summary
    summary_file = OUTPUT_PATH / "dataset_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✓ Summary saved to: {summary_file}")
    
    # Missing animals
    missing = [a for a, c in summary["animals"].items() if c < TARGET_COUNT]
    if missing:
        print(f"\n⚠ Animals needing more files: {', '.join(missing)}")
        print("\nTo get more files:")
        print("1. Use download_animal_sounds.py with Freesound API")
        print("2. Manually download from BBC Sound Effects")
        print("3. Run augmentation to generate synthetic variations")

def main():
    print("="*60)
    print("Multi-Source Animal Sound Dataset Builder")
    print("="*60)
    
    create_directories()
    
    # Download from available sources
    print("\nDownloading from open sources...")
    
    # ESC-50 (covers: dog, rooster, pig, cow, frog, cat, hen, sheep)
    download_esc50()
    
    # GitHub Animal Sound Dataset (covers: cat, dog, bird, cow, lion, sheep, frog, hen)
    download_animal_sound_dataset()
    
    # Show additional sources
    download_additional_sources()
    
    # Generate initial summary
    generate_summary()
    
    # Ask about augmentation
    print("\n" + "="*60)
    print("Would you like to augment the dataset?")
    print("This will create variations of existing files to reach 100 per animal")
    print("="*60)
    response = input("Augment dataset? (y/n): ").lower()
    
    if response == 'y':
        augment_dataset()
        generate_summary()
    
    print(f"\n✓ Dataset location: {OUTPUT_PATH}")
    print("\nNext steps:")
    print("1. Review the dataset_summary.json file")
    print("2. For missing animals, use download_animal_sounds.py with Freesound API")
    print("3. Or manually download from BBC Sound Effects or other sources")

if __name__ == "__main__":
    main()
