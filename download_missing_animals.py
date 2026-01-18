"""
Download Missing Animals: Elephant, Goat, Lion, Tiger, Bear
Downloads 100 audio files for each animal to mini_project/data folder
"""

import os
import requests
from pathlib import Path
import time
from tqdm import tqdm
import json

# Configuration
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
DATA_PATH = PROJECT_PATH / "mini_project" / "data"

# Missing animals
ANIMALS = ['Elephant', 'Goat', 'Lion', 'Tiger', 'Bear']

TARGET_COUNT = 100

# Freesound API
FREESOUND_API_KEY = "YOUR_API_KEY_HERE"  # Get from https://freesound.org/apiv2/apply/
FREESOUND_BASE_URL = "https://freesound.org/apiv2"

def download_from_freesound(animal, target_count=100):
    """Download sounds from Freesound API"""
    
    if FREESOUND_API_KEY == "YOUR_API_KEY_HERE":
        print(f"\n⚠ Freesound API key not set!")
        return 0
    
    print(f"\n{'='*60}")
    print(f"Downloading {animal} sounds from Freesound...")
    print(f"{'='*60}")
    
    # Multiple search queries for better coverage
    queries = [
        f"{animal.lower()} sound",
        f"{animal.lower()} call",
        f"{animal.lower()} roar" if animal in ['Lion', 'Tiger', 'Bear'] else f"{animal.lower()} noise",
        f"{animal.lower()} vocalization"
    ]
    
    all_results = []
    
    # Collect results from multiple queries
    for query in queries:
        print(f"Searching: '{query}'...")
        
        url = f"{FREESOUND_BASE_URL}/search/text/"
        params = {
            'query': query,
            'token': FREESOUND_API_KEY,
            'fields': 'id,name,previews,duration,license',
            'page_size': 50,
            'filter': 'duration:[1 TO 15]'  # 1-15 seconds
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            results = response.json()
            
            if 'results' in results:
                all_results.extend(results['results'])
                print(f"  Found: {len(results['results'])} sounds")
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    # Remove duplicates
    unique_results = {item['id']: item for item in all_results}.values()
    print(f"\nTotal unique sounds found: {len(list(unique_results))}")
    
    # Download files
    downloaded = 0
    
    for idx, sound in enumerate(tqdm(list(unique_results)[:target_count], desc=f"{animal}")):
        if downloaded >= target_count:
            break
        
        try:
            # Use high-quality preview
            preview_url = sound['previews']['preview-hq-mp3']
            filename = f"{animal}_{downloaded + 1}.mp3"
            filepath = DATA_PATH / filename
            
            # Skip if exists
            if filepath.exists():
                downloaded += 1
                continue
            
            # Download
            audio_response = requests.get(preview_url, timeout=30)
            audio_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(audio_response.content)
            
            downloaded += 1
            time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            continue
    
    print(f"✓ Downloaded {downloaded}/{target_count} {animal} sounds")
    return downloaded

def show_manual_download_instructions():
    """Show instructions for manual download"""
    print("\n" + "="*80)
    print("MANUAL DOWNLOAD INSTRUCTIONS")
    print("="*80)
    
    print("\n🌐 OPTION 1: BBC Sound Effects (FREE, NO REGISTRATION)")
    print("-" * 80)
    print("URL: https://sound-effects.bbcrewind.co.uk/")
    print("\nSteps:")
    print("1. Go to the website")
    print("2. Search for each animal: elephant, goat, lion, tiger, bear")
    print("3. Click on sounds and download WAV files")
    print("4. Save to: C:\\Users\\sasik\\OneDrive\\Documents\\AnimalVoicedetection\\mini_project\\data")
    print("5. Rename files as: Elephant_1.wav, Elephant_2.wav, etc.")
    
    print("\n\n🌐 OPTION 2: Freesound.org (FREE, REQUIRES REGISTRATION)")
    print("-" * 80)
    print("URL: https://freesound.org/")
    print("\nSteps:")
    print("1. Create free account at https://freesound.org/")
    print("2. Get API key at https://freesound.org/apiv2/apply/")
    print("3. Edit this script (line 18) and add your API key")
    print("4. Run this script again")
    
    print("\n\n🌐 OPTION 3: Direct Download Links (Curated Sources)")
    print("-" * 80)
    
    sources = {
        "Elephant": [
            "https://freesound.org/ (search 'elephant trumpet')",
            "https://sound-effects.bbcrewind.co.uk/ (search 'elephant')",
            "YouTube Audio Library (search 'elephant sound')"
        ],
        "Goat": [
            "https://freesound.org/ (search 'goat bleat')",
            "https://sound-effects.bbcrewind.co.uk/ (search 'goat')",
        ],
        "Lion": [
            "https://freesound.org/ (search 'lion roar')",
            "https://sound-effects.bbcrewind.co.uk/ (search 'lion')",
        ],
        "Tiger": [
            "https://freesound.org/ (search 'tiger roar')",
            "https://sound-effects.bbcrewind.co.uk/ (search 'tiger')",
        ],
        "Bear": [
            "https://freesound.org/ (search 'bear growl')",
            "https://sound-effects.bbcrewind.co.uk/ (search 'bear')",
        ]
    }
    
    for animal, links in sources.items():
        print(f"\n{animal}:")
        for link in links:
            print(f"  • {link}")
    
    print("\n\n📝 FILE NAMING CONVENTION")
    print("-" * 80)
    print("Save files as:")
    print("  Elephant_1.wav, Elephant_2.wav, ..., Elephant_100.wav")
    print("  Goat_1.wav, Goat_2.wav, ..., Goat_100.wav")
    print("  Lion_1.wav, Lion_2.wav, ..., Lion_100.wav")
    print("  Tiger_1.wav, Tiger_2.wav, ..., Tiger_100.wav")
    print("  Bear_1.wav, Bear_2.wav, ..., Bear_100.wav")
    
    print(f"\n📁 Save location: {DATA_PATH}")
    
    print("\n\n💡 QUICK TIP")
    print("-" * 80)
    print("You don't need exactly 100 files for each animal.")
    print("Even 30-50 files per animal will work well.")
    print("You can use the expand_dataset.py script to augment them to 100.")

def count_existing_files():
    """Count existing files for missing animals"""
    print("\n" + "="*80)
    print("CURRENT STATUS")
    print("="*80)
    
    counts = {}
    for animal in ANIMALS:
        count = len(list(DATA_PATH.glob(f"{animal}_*.wav"))) + len(list(DATA_PATH.glob(f"{animal}_*.mp3")))
        counts[animal] = count
        
        status = "✓" if count >= TARGET_COUNT else "⚠" if count > 0 else "✗"
        percentage = (count / TARGET_COUNT) * 100 if count > 0 else 0
        print(f"{status} {animal:12} : {count:3}/{TARGET_COUNT} ({percentage:5.1f}%)")
    
    return counts

def create_download_script_for_kaggle():
    """Create a script to download from Kaggle datasets"""
    script_content = """# Kaggle Download Script for Animal Sounds
# Install: pip install kaggle

# Setup Kaggle API:
# 1. Go to https://www.kaggle.com/settings
# 2. Click "Create New API Token"
# 3. Save kaggle.json to: C:\\Users\\sasik\\.kaggle\\kaggle.json

# Download datasets
kaggle datasets download -d maulanaakbardwijaya/animal-sounds-dataset
kaggle datasets download -d mmoreaux/audio-cats-and-dogs

# Extract and organize files manually
"""
    
    script_file = DATA_PATH.parent / "kaggle_download.txt"
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    print(f"\n✓ Kaggle download instructions saved to: {script_file}")

def main():
    print("="*80)
    print("Missing Animals Downloader")
    print("Elephant, Goat, Lion, Tiger, Bear")
    print("="*80)
    
    # Check current status
    counts = count_existing_files()
    
    # Check if API key is set
    if FREESOUND_API_KEY == "YOUR_API_KEY_HERE":
        print("\n" + "="*80)
        print("⚠ FREESOUND API KEY NOT SET")
        print("="*80)
        print("\nAutomatic download requires a Freesound API key.")
        print("You have two options:")
        print("\n1. Get a FREE API key (recommended):")
        print("   - Visit: https://freesound.org/apiv2/apply/")
        print("   - Create account and get API key")
        print("   - Edit this script line 18 and add your key")
        print("   - Run this script again")
        print("\n2. Download manually (see instructions below)")
        
        show_manual_download_instructions()
        create_download_script_for_kaggle()
        
    else:
        # Download using Freesound API
        print("\n" + "="*80)
        print("DOWNLOADING FROM FREESOUND")
        print("="*80)
        
        results = {}
        for animal in ANIMALS:
            current_count = counts.get(animal, 0)
            
            if current_count >= TARGET_COUNT:
                print(f"\n✓ {animal}: Already has {current_count} files")
                results[animal] = current_count
                continue
            
            needed = TARGET_COUNT - current_count
            downloaded = download_from_freesound(animal, needed)
            results[animal] = current_count + downloaded
        
        # Final summary
        print("\n" + "="*80)
        print("DOWNLOAD SUMMARY")
        print("="*80)
        
        for animal, count in results.items():
            status = "✓" if count >= TARGET_COUNT else "⚠"
            print(f"{status} {animal}: {count}/{TARGET_COUNT}")
        
        # Show manual instructions for incomplete downloads
        incomplete = [a for a, c in results.items() if c < TARGET_COUNT]
        if incomplete:
            print(f"\n⚠ Incomplete: {', '.join(incomplete)}")
            print("\nFor remaining files, use manual download (see instructions below)")
            show_manual_download_instructions()
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Check the data folder:")
    print(f"   {DATA_PATH}")
    
    print("\n2. If you have < 100 files per animal:")
    print("   - Download more manually from BBC Sound Effects or Freesound")
    print("   - OR use expand_dataset.py to augment existing files")
    
    print("\n3. Once you have audio files, generate spectrograms:")
    print("   python new_animal_sound_pipeline.py")

if __name__ == "__main__":
    main()
