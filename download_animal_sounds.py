"""
Download Animal Sound Dataset
Downloads 100 audio files for each animal category
"""

import os
import requests
from pathlib import Path
import time
from tqdm import tqdm
import json

# Configuration
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
OUTPUT_PATH = PROJECT_PATH / "animal_audio_dataset"

# Animals to download
ANIMALS = [
    'cat', 'dog', 'elephant', 'cow', 'frog', 
    'sheep', 'bird', 'goat', 'lion', 'tiger',
    'hen', 'pig', 'rooster', 'bear'
]

TARGET_COUNT = 100  # Files per animal

# Freesound API Configuration
# Get your API key from: https://freesound.org/apiv2/apply/
FREESOUND_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your API key
FREESOUND_BASE_URL = "https://freesound.org/apiv2"

def create_directories():
    """Create directory structure for dataset"""
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    
    for animal in ANIMALS:
        animal_dir = OUTPUT_PATH / animal
        animal_dir.mkdir(exist_ok=True)
    
    print(f"✓ Created directories in: {OUTPUT_PATH}")

def search_freesound(query, max_results=100):
    """Search Freesound for audio files"""
    url = f"{FREESOUND_BASE_URL}/search/text/"
    
    params = {
        'query': query,
        'token': FREESOUND_API_KEY,
        'fields': 'id,name,previews,duration,license',
        'page_size': min(max_results, 150),
        'filter': f'duration:[1 TO 10]'  # 1-10 seconds duration
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching Freesound: {e}")
        return None

def download_audio_file(url, filepath):
    """Download a single audio file"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {filepath.name}: {e}")
        return False

def download_animal_sounds_freesound(animal, target_count=100):
    """Download sounds for a specific animal from Freesound"""
    print(f"\n{'='*60}")
    print(f"Downloading {animal} sounds from Freesound...")
    print(f"{'='*60}")
    
    animal_dir = OUTPUT_PATH / animal
    
    # Search queries for better results
    search_queries = [
        f"{animal} sound",
        f"{animal} call",
        f"{animal} voice",
        f"{animal} vocalization"
    ]
    
    downloaded = 0
    all_results = []
    
    # Collect results from multiple queries
    for query in search_queries:
        if downloaded >= target_count:
            break
        
        print(f"Searching: '{query}'...")
        results = search_freesound(query, max_results=50)
        
        if results and 'results' in results:
            all_results.extend(results['results'])
            time.sleep(0.5)  # Rate limiting
    
    # Remove duplicates based on ID
    unique_results = {item['id']: item for item in all_results}.values()
    
    # Download files
    for idx, sound in enumerate(tqdm(list(unique_results)[:target_count], desc=f"{animal}")):
        if downloaded >= target_count:
            break
        
        try:
            # Use high-quality preview
            preview_url = sound['previews']['preview-hq-mp3']
            filename = f"{animal}_{idx+1:03d}_{sound['id']}.mp3"
            filepath = animal_dir / filename
            
            # Skip if already exists
            if filepath.exists():
                downloaded += 1
                continue
            
            # Download
            if download_audio_file(preview_url, filepath):
                downloaded += 1
                time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            print(f"Error processing sound {sound.get('id', 'unknown')}: {e}")
            continue
    
    print(f"✓ Downloaded {downloaded}/{target_count} {animal} sounds")
    return downloaded

def download_from_esc50():
    """
    Alternative: Download ESC-50 dataset which includes animal sounds
    This is a backup method if Freesound API is not available
    """
    print("\n" + "="*60)
    print("Alternative: Download ESC-50 Dataset")
    print("="*60)
    print("\nESC-50 includes these animals:")
    print("- Dog, Rooster, Pig, Cow, Frog, Cat, Hen, Insects, Sheep, Crow")
    print("\nTo download ESC-50:")
    print("1. Visit: https://github.com/karolpiczak/ESC-50")
    print("2. Download: https://github.com/karoldvl/ESC-50/archive/master.zip")
    print("3. Extract and copy animal sound folders to your dataset")

def download_from_kaggle():
    """Instructions for downloading from Kaggle"""
    print("\n" + "="*60)
    print("Alternative: Download from Kaggle")
    print("="*60)
    print("\nRecommended Kaggle datasets:")
    print("\n1. Animal Sounds Dataset:")
    print("   https://www.kaggle.com/datasets/maulanaakbardwijaya/animal-sounds-dataset")
    print("\n2. Audio Cats and Dogs:")
    print("   https://www.kaggle.com/datasets/mmoreaux/audio-cats-and-dogs")
    print("\n3. Animal Sounds Classification:")
    print("   https://www.kaggle.com/datasets/haithammoh/sounds-of-animals")
    print("\nTo download:")
    print("1. Install: pip install kaggle")
    print("2. Setup API key from kaggle.com/account")
    print("3. Run: kaggle datasets download -d <dataset-path>")

def generate_dataset_info():
    """Generate information about the downloaded dataset"""
    info = {
        "animals": ANIMALS,
        "target_count_per_animal": TARGET_COUNT,
        "total_target": len(ANIMALS) * TARGET_COUNT,
        "actual_counts": {}
    }
    
    for animal in ANIMALS:
        animal_dir = OUTPUT_PATH / animal
        if animal_dir.exists():
            count = len(list(animal_dir.glob("*.mp3"))) + len(list(animal_dir.glob("*.wav")))
            info["actual_counts"][animal] = count
    
    info_file = OUTPUT_PATH / "dataset_info.json"
    with open(info_file, 'w') as f:
        json.dump(info, f, indent=2)
    
    print(f"\n✓ Dataset info saved to: {info_file}")
    return info

def main():
    print("="*60)
    print("Animal Sound Dataset Downloader")
    print("="*60)
    
    # Create directories
    create_directories()
    
    # Check if API key is set
    if FREESOUND_API_KEY == "YOUR_API_KEY_HERE":
        print("\n⚠ WARNING: Freesound API key not set!")
        print("\nTo use Freesound API:")
        print("1. Go to: https://freesound.org/apiv2/apply/")
        print("2. Create an account and get your API key")
        print("3. Replace 'YOUR_API_KEY_HERE' in this script with your key")
        print("\nAlternative methods:")
        download_from_esc50()
        download_from_kaggle()
        return
    
    # Download sounds for each animal
    total_downloaded = 0
    results = {}
    
    for animal in ANIMALS:
        count = download_animal_sounds_freesound(animal, TARGET_COUNT)
        results[animal] = count
        total_downloaded += count
    
    # Generate summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    for animal, count in results.items():
        status = "✓" if count >= TARGET_COUNT else "⚠"
        print(f"{status} {animal.capitalize()}: {count}/{TARGET_COUNT}")
    
    print(f"\nTotal downloaded: {total_downloaded}/{len(ANIMALS) * TARGET_COUNT}")
    
    # Save dataset info
    generate_dataset_info()
    
    print(f"\n✓ Dataset saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
