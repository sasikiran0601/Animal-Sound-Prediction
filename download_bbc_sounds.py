"""
BBC Sound Effects Downloader
Downloads animal sounds from BBC Sound Effects Library (Free, No API Key Required)
"""

import requests
from pathlib import Path
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

# Configuration
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
DATA_PATH = PROJECT_PATH / "mini_project" / "data"

# Animals to download
ANIMALS = {
    'Elephant': ['elephant', 'elephant trumpet', 'elephant call'],
    'Goat': ['goat', 'goat bleat', 'goat call'],
    'Lion': ['lion', 'lion roar', 'lion growl'],
    'Tiger': ['tiger', 'tiger roar', 'tiger growl'],
    'Bear': ['bear', 'bear growl', 'bear roar']
}

TARGET_PER_ANIMAL = 100

def search_bbc_sounds(query):
    """
    Search BBC Sound Effects
    Note: This is a simplified version. BBC website may require manual download.
    """
    print(f"\nSearching BBC Sound Effects for: '{query}'")
    
    # BBC Sound Effects search URL
    base_url = "https://sound-effects.bbcrewind.co.uk/search"
    
    params = {
        'q': query
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        # Note: BBC website may require JavaScript, so this might not work directly
        # This is a placeholder for the structure
        
        print(f"  Response received (manual download may be required)")
        return response.text
        
    except Exception as e:
        print(f"  Error: {e}")
        return None

def show_download_guide():
    """
    Show step-by-step guide for downloading from BBC Sound Effects
    """
    print("\n" + "="*80)
    print("BBC SOUND EFFECTS - MANUAL DOWNLOAD GUIDE")
    print("="*80)
    
    print("\n📌 BBC Sound Effects is FREE but requires manual download")
    print("   (No registration or API key needed!)")
    
    print("\n" + "="*80)
    print("STEP-BY-STEP INSTRUCTIONS")
    print("="*80)
    
    for animal, search_terms in ANIMALS.items():
        print(f"\n{'='*60}")
        print(f"🐾 {animal.upper()}")
        print(f"{'='*60}")
        
        print(f"\n1. Open browser and go to:")
        print(f"   https://sound-effects.bbcrewind.co.uk/")
        
        print(f"\n2. Search for: '{search_terms[0]}'")
        
        print(f"\n3. Browse results and click on sounds you want")
        
        print(f"\n4. Click 'Download' button (WAV format)")
        
        print(f"\n5. Save files to:")
        print(f"   {DATA_PATH}")
        
        print(f"\n6. Rename files as:")
        print(f"   {animal}_1.wav")
        print(f"   {animal}_2.wav")
        print(f"   {animal}_3.wav")
        print(f"   ... (continue numbering)")
        
        print(f"\n💡 Alternative search terms:")
        for term in search_terms[1:]:
            print(f"   - {term}")
        
        print(f"\n🎯 Target: {TARGET_PER_ANIMAL} files")
        print(f"   Minimum: 30-50 files (can augment later)")

def show_alternative_sources():
    """Show alternative download sources"""
    print("\n\n" + "="*80)
    print("ALTERNATIVE DOWNLOAD SOURCES")
    print("="*80)
    
    print("\n🌐 SOURCE 1: Freesound.org (Requires free account)")
    print("-" * 80)
    print("1. Create account: https://freesound.org/")
    print("2. Search for animal sounds")
    print("3. Download directly (no API needed for manual download)")
    print("4. Save to data folder with correct naming")
    
    print("\n🌐 SOURCE 2: YouTube Audio Library")
    print("-" * 80)
    print("1. Go to: https://www.youtube.com/audiolibrary")
    print("2. Search for animal sounds")
    print("3. Download MP3 files")
    print("4. Convert to WAV if needed")
    
    print("\n🌐 SOURCE 3: Zapsplat (Free with attribution)")
    print("-" * 80)
    print("1. Go to: https://www.zapsplat.com/")
    print("2. Create free account")
    print("3. Search: elephant, goat, lion, tiger, bear")
    print("4. Download WAV files")
    
    print("\n🌐 SOURCE 4: Pixabay Sound Effects")
    print("-" * 80)
    print("1. Go to: https://pixabay.com/sound-effects/")
    print("2. Search for each animal")
    print("3. Download MP3 files (free, no account needed)")
    
    print("\n🌐 SOURCE 5: FreeSound Library")
    print("-" * 80)
    print("1. Go to: https://freesound.org/")
    print("2. No API key needed for manual download")
    print("3. Just create free account")
    print("4. Search and download")

def create_quick_links():
    """Create HTML file with quick links"""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Animal Sound Download Links</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        h1 { color: #2c3e50; }
        h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .animal { margin: 20px 0; padding: 15px; background: #ecf0f1; border-radius: 5px; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .instructions { background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐾 Animal Sound Download Links</h1>
        
        <div class="instructions">
            <strong>Instructions:</strong>
            <ol>
                <li>Click on the links below for each animal</li>
                <li>Download WAV or MP3 files</li>
                <li>Save to: <code>C:\\Users\\sasik\\OneDrive\\Documents\\AnimalVoicedetection\\mini_project\\data</code></li>
                <li>Rename as: Animal_1.wav, Animal_2.wav, etc.</li>
            </ol>
        </div>
        
        <h2>🐘 Elephant</h2>
        <div class="animal">
            <a href="https://sound-effects.bbcrewind.co.uk/search?q=elephant" target="_blank">BBC: Elephant Sounds</a><br>
            <a href="https://freesound.org/search/?q=elephant+trumpet" target="_blank">Freesound: Elephant Trumpet</a><br>
            <a href="https://pixabay.com/sound-effects/search/elephant/" target="_blank">Pixabay: Elephant</a><br>
            <a href="https://www.zapsplat.com/sound-effect-category/elephants/" target="_blank">Zapsplat: Elephants</a>
        </div>
        
        <h2>🐐 Goat</h2>
        <div class="animal">
            <a href="https://sound-effects.bbcrewind.co.uk/search?q=goat" target="_blank">BBC: Goat Sounds</a><br>
            <a href="https://freesound.org/search/?q=goat+bleat" target="_blank">Freesound: Goat Bleat</a><br>
            <a href="https://pixabay.com/sound-effects/search/goat/" target="_blank">Pixabay: Goat</a><br>
            <a href="https://www.zapsplat.com/sound-effect-category/goats/" target="_blank">Zapsplat: Goats</a>
        </div>
        
        <h2>🦁 Lion</h2>
        <div class="animal">
            <a href="https://sound-effects.bbcrewind.co.uk/search?q=lion" target="_blank">BBC: Lion Sounds</a><br>
            <a href="https://freesound.org/search/?q=lion+roar" target="_blank">Freesound: Lion Roar</a><br>
            <a href="https://pixabay.com/sound-effects/search/lion/" target="_blank">Pixabay: Lion</a><br>
            <a href="https://www.zapsplat.com/sound-effect-category/lions/" target="_blank">Zapsplat: Lions</a>
        </div>
        
        <h2>🐯 Tiger</h2>
        <div class="animal">
            <a href="https://sound-effects.bbcrewind.co.uk/search?q=tiger" target="_blank">BBC: Tiger Sounds</a><br>
            <a href="https://freesound.org/search/?q=tiger+roar" target="_blank">Freesound: Tiger Roar</a><br>
            <a href="https://pixabay.com/sound-effects/search/tiger/" target="_blank">Pixabay: Tiger</a><br>
            <a href="https://www.zapsplat.com/sound-effect-category/tigers/" target="_blank">Zapsplat: Tigers</a>
        </div>
        
        <h2>🐻 Bear</h2>
        <div class="animal">
            <a href="https://sound-effects.bbcrewind.co.uk/search?q=bear" target="_blank">BBC: Bear Sounds</a><br>
            <a href="https://freesound.org/search/?q=bear+growl" target="_blank">Freesound: Bear Growl</a><br>
            <a href="https://pixabay.com/sound-effects/search/bear/" target="_blank">Pixabay: Bear</a><br>
            <a href="https://www.zapsplat.com/sound-effect-category/bears/" target="_blank">Zapsplat: Bears</a>
        </div>
        
        <div class="instructions" style="background: #d4edda; border-color: #28a745;">
            <strong>💡 Quick Tips:</strong>
            <ul>
                <li>You don't need exactly 100 files - even 30-50 per animal works!</li>
                <li>Use expand_dataset.py to augment files to reach 100</li>
                <li>WAV format is preferred, but MP3 works too</li>
                <li>Keep files between 1-10 seconds for best results</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
    
    html_file = PROJECT_PATH / "animal_download_links.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ Quick links saved to: {html_file}")
    print(f"  Open this file in your browser for easy access to download links!")
    
    return html_file

def main():
    print("="*80)
    print("BBC Sound Effects & Multi-Source Downloader")
    print("="*80)
    
    # Show download guide
    show_download_guide()
    
    # Show alternative sources
    show_alternative_sources()
    
    # Create HTML quick links
    html_file = create_quick_links()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    print("\n✅ EASIEST METHOD:")
    print(f"   1. Open: {html_file}")
    print("   2. Click links to download sounds")
    print("   3. Save files to data folder")
    print("   4. Rename as: Animal_1.wav, Animal_2.wav, etc.")
    
    print("\n📁 Save location:")
    print(f"   {DATA_PATH}")
    
    print("\n🎯 Target: 100 files per animal")
    print("   Minimum: 30-50 files (can augment to 100 later)")
    
    print("\n📝 File naming:")
    print("   Elephant_1.wav, Elephant_2.wav, ..., Elephant_100.wav")
    print("   Goat_1.wav, Goat_2.wav, ..., Goat_100.wav")
    print("   Lion_1.wav, Lion_2.wav, ..., Lion_100.wav")
    print("   Tiger_1.wav, Tiger_2.wav, ..., Tiger_100.wav")
    print("   Bear_1.wav, Bear_2.wav, ..., Bear_100.wav")
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Open the HTML file in your browser")
    print("2. Download audio files from the links")
    print("3. Save and rename files correctly")
    print("4. Run: python expand_dataset.py (to augment if needed)")
    print("5. Run: python new_animal_sound_pipeline.py (to generate spectrograms)")

if __name__ == "__main__":
    # Install BeautifulSoup if needed
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("\n⚠ Installing required package: beautifulsoup4")
        print("Run: pip install beautifulsoup4")
        print("\nContinuing without web scraping functionality...")
    
    main()
