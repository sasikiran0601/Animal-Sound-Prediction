"""
Automatic Animal Sound Downloader
Downloads audio files from Pixabay and other free sources
Saves to mini_project/data with correct naming
"""

import requests
from pathlib import Path
import time
from tqdm import tqdm
import json

# Configuration
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
DATA_PATH = PROJECT_PATH / "mini_project" / "data"

ANIMALS = ['Elephant', 'Goat', 'Lion', 'Tiger', 'Bear']
TARGET_PER_ANIMAL = 40  # Download 40, then augment to 100

# Pixabay API (Free - get from https://pixabay.com/api/docs/)
PIXABAY_API_KEY = "YOUR_PIXABAY_API_KEY"  # Get free key from https://pixabay.com/accounts/register/

# Freesound API
FREESOUND_API_KEY = "alFVPTkJhq1daTAhnohv0CjwGjSmWmlPoCHRQxCx"  # Get from https://freesound.org/apiv2/apply/

def download_from_pixabay(animal, count=40):
    """Download from Pixabay Sound Effects"""
    if PIXABAY_API_KEY == "YOUR_PIXABAY_API_KEY":
        print(f"⚠ Pixabay API key not set")
        return 0
    
    print(f"\n📥 Downloading {animal} from Pixabay...")
    
    url = "https://pixabay.com/api/"
    params = {
        'key': PIXABAY_API_KEY,
        'q': animal.lower(),
        'audio_type': 'sound_effect',
        'per_page': min(count, 200)
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        downloaded = 0
        start_num = get_next_number(animal)
        
        for idx, sound in enumerate(data.get('hits', [])[:count]):
            try:
                # Get download URL
                download_url = sound.get('previewURL') or sound.get('url')
                
                if not download_url:
                    continue
                
                # Download file
                filepath = DATA_PATH / f"{animal}_{start_num + downloaded}.mp3"
                
                if filepath.exists():
                    downloaded += 1
                    continue
                
                audio_response = requests.get(download_url, timeout=30)
                audio_response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(audio_response.content)
                
                downloaded += 1
                time.sleep(0.5)
                
            except Exception as e:
                continue
        
        print(f"✓ Downloaded {downloaded} files from Pixabay")
        return downloaded
        
    except Exception as e:
        print(f"Error: {e}")
        return 0

def download_from_freesound(animal, count=40):
    """Download from Freesound API"""
    if FREESOUND_API_KEY == "YOUR_FREESOUND_API_KEY":
        print(f"⚠ Freesound API key not set")
        return 0
    
    print(f"\n📥 Downloading {animal} from Freesound...")
    
    search_terms = {
        'Elephant': 'elephant trumpet',
        'Goat': 'goat bleat',
        'Lion': 'lion roar',
        'Tiger': 'tiger roar',
        'Bear': 'bear growl'
    }
    
    query = search_terms.get(animal, animal.lower())
    
    url = "https://freesound.org/apiv2/search/text/"
    params = {
        'query': query,
        'token': FREESOUND_API_KEY,
        'fields': 'id,name,previews,duration',
        'page_size': min(count, 150),
        'filter': 'duration:[1 TO 10]'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        downloaded = 0
        start_num = get_next_number(animal)
        
        for sound in tqdm(data.get('results', [])[:count], desc=f"{animal}"):
            try:
                preview_url = sound['previews']['preview-hq-mp3']
                filepath = DATA_PATH / f"{animal}_{start_num + downloaded}.mp3"
                
                if filepath.exists():
                    downloaded += 1
                    continue
                
                audio_response = requests.get(preview_url, timeout=30)
                audio_response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(audio_response.content)
                
                downloaded += 1
                time.sleep(0.3)
                
            except Exception as e:
                continue
        
        print(f"✓ Downloaded {downloaded} files from Freesound")
        return downloaded
        
    except Exception as e:
        print(f"Error: {e}")
        return 0

def download_from_free_sources(animal, count=40):
    """
    Download from completely free sources (no API key needed)
    Uses direct download links from public repositories
    """
    print(f"\n📥 Attempting free downloads for {animal}...")
    
    # ESC-50 dataset direct links (if available)
    # Note: This is a placeholder - actual implementation would need specific URLs
    
    print(f"⚠ Free direct downloads not available without API keys")
    print(f"   Please use one of these options:")
    print(f"   1. Get free Freesound API key: https://freesound.org/apiv2/apply/")
    print(f"   2. Get free Pixabay API key: https://pixabay.com/accounts/register/")
    print(f"   3. Download manually from the HTML page")
    
    return 0

def get_next_number(animal):
    """Get next file number for an animal"""
    existing = list(DATA_PATH.glob(f"{animal}_*.wav")) + list(DATA_PATH.glob(f"{animal}_*.mp3"))
    return len(existing) + 1

def count_files(animal):
    """Count existing files"""
    return len(list(DATA_PATH.glob(f"{animal}_*.wav"))) + len(list(DATA_PATH.glob(f"{animal}_*.mp3")))

def show_api_setup_instructions():
    """Show how to get API keys"""
    print("\n" + "="*80)
    print("API KEY SETUP INSTRUCTIONS")
    print("="*80)
    
    print("\n🔑 OPTION 1: Freesound API (Recommended)")
    print("-" * 80)
    print("1. Go to: https://freesound.org/")
    print("2. Click 'Sign up' (top right)")
    print("3. Create free account")
    print("4. Go to: https://freesound.org/apiv2/apply/")
    print("5. Fill in application (instant approval)")
    print("6. Copy your API key")
    print("7. Edit this script line 19: FREESOUND_API_KEY = 'your_key_here'")
    print("8. Run this script again")
    
    print("\n🔑 OPTION 2: Pixabay API")
    print("-" * 80)
    print("1. Go to: https://pixabay.com/accounts/register/")
    print("2. Create free account")
    print("3. Go to: https://pixabay.com/api/docs/")
    print("4. Click 'Get Started' and copy your API key")
    print("5. Edit this script line 16: PIXABAY_API_KEY = 'your_key_here'")
    print("6. Run this script again")
    
    print("\n💡 Both are FREE and take only 2-3 minutes to set up!")

def main():
    print("="*80)
    print("AUTOMATIC ANIMAL SOUND DOWNLOADER")
    print("="*80)
    
    # Create data directory if not exists
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    
    # Check API keys
    has_freesound = FREESOUND_API_KEY != "YOUR_FREESOUND_API_KEY"
    has_pixabay = PIXABAY_API_KEY != "YOUR_PIXABAY_API_KEY"
    
    if not has_freesound and not has_pixabay:
        print("\n⚠ NO API KEYS CONFIGURED")
        print("\nThis script needs at least one API key to download automatically.")
        show_api_setup_instructions()
        
        print("\n" + "="*80)
        print("ALTERNATIVE: Manual Download")
        print("="*80)
        print("\nIf you don't want to set up API keys:")
        print("1. Open: download_links.html (in your browser)")
        print("2. Click the download links")
        print("3. Save files manually")
        print("4. Run: python get_100_files_each.py")
        
        return
    
    # Download for each animal
    print(f"\n📁 Save location: {DATA_PATH}")
    print(f"🎯 Target: {TARGET_PER_ANIMAL} files per animal\n")
    
    results = {}
    
    for animal in ANIMALS:
        print(f"\n{'='*70}")
        print(f"Processing: {animal}")
        print(f"{'='*70}")
        
        current = count_files(animal)
        print(f"Current files: {current}")
        
        if current >= TARGET_PER_ANIMAL:
            print(f"✓ Already has enough files!")
            results[animal] = current
            continue
        
        needed = TARGET_PER_ANIMAL - current
        downloaded = 0
        
        # Try Freesound first
        if has_freesound:
            downloaded += download_from_freesound(animal, needed - downloaded)
        
        # Try Pixabay if still need more
        if has_pixabay and downloaded < needed:
            downloaded += download_from_pixabay(animal, needed - downloaded)
        
        results[animal] = current + downloaded
        
        print(f"\n✓ {animal}: {results[animal]}/{TARGET_PER_ANIMAL} files")
    
    # Summary
    print("\n" + "="*80)
    print("DOWNLOAD SUMMARY")
    print("="*80)
    
    for animal, count in results.items():
        status = "✓" if count >= TARGET_PER_ANIMAL else "⚠"
        percentage = (count / TARGET_PER_ANIMAL) * 100
        print(f"{status} {animal:12} : {count:3}/{TARGET_PER_ANIMAL} ({percentage:5.1f}%)")
    
    # Next steps
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    
    total = sum(results.values())
    target_total = len(ANIMALS) * TARGET_PER_ANIMAL
    
    if total >= target_total * 0.8:  # If we have 80% or more
        print("\n✅ Good progress! Now augment to 100 files per animal:")
        print("   python get_100_files_each.py")
    else:
        incomplete = [a for a, c in results.items() if c < TARGET_PER_ANIMAL]
        print(f"\n⚠ Need more files for: {', '.join(incomplete)}")
        print("\nOptions:")
        print("1. Set up API keys (see instructions above)")
        print("2. Download manually from: download_links.html")
        print("3. Run this script again after setting up API keys")

if __name__ == "__main__":
    main()
