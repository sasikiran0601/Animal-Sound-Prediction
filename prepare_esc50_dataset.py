"""
Prepare ESC-50 Dataset for Animal Sound Classification
Extracts animal sounds from ESC-50 and organizes them for training
"""

import pandas as pd
from pathlib import Path
import shutil

# Paths
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
ESC50_PATH = PROJECT_PATH / "datasets_csv" / "ESC-50-master"
ESC50_AUDIO = ESC50_PATH / "audio"
ESC50_META = ESC50_PATH / "meta" / "esc50.csv"
OUTPUT_PATH = PROJECT_PATH / "mini_project" / "data"

# Create output directory
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("PREPARE ESC-50 DATASET FOR ANIMAL SOUND CLASSIFICATION")
print("=" * 70)

# Check if ESC-50 exists
if not ESC50_META.exists():
    print(f"\n❌ ESC-50 metadata not found: {ESC50_META}")
    print("Please download ESC-50 dataset first!")
    exit(1)

# Read metadata
print(f"\n📊 Reading ESC-50 metadata...")
df = pd.read_csv(ESC50_META)
print(f"✅ Found {len(df)} audio files in ESC-50")

# Define animal categories we want
# ESC-50 has these animal-related categories:
animal_mapping = {
    'dog': 'Dog',
    'rooster': 'Rooster',
    'pig': 'Pig',
    'cow': 'Cow',
    'frog': 'Frog',
    'cat': 'Cat',
    'hen': 'Hen',
    'insects': 'Insects',
    'sheep': 'Sheep',
    'crow': 'Crow',
    'chirping_birds': 'Bird'
}

print(f"\n🐾 Animal categories in ESC-50:")
for esc_name, our_name in animal_mapping.items():
    count = len(df[df['category'] == esc_name])
    print(f"  {our_name:15s}: {count} files")

# Filter for animal sounds
animal_df = df[df['category'].isin(animal_mapping.keys())]
print(f"\n📁 Total animal sound files: {len(animal_df)}")

# Copy and rename files
print(f"\n🔄 Copying files to {OUTPUT_PATH}...")
copied_count = 0
counters = {}  # Track numbering for each animal

for idx, row in animal_df.iterrows():
    filename = row['filename']
    esc_category = row['category']
    our_category = animal_mapping[esc_category]
    
    # Initialize counter for this animal
    if our_category not in counters:
        counters[our_category] = 1
    
    # Source and destination paths
    src_path = ESC50_AUDIO / filename
    new_filename = f"{our_category}_{counters[our_category]}.wav"
    dst_path = OUTPUT_PATH / new_filename
    
    # Copy file
    try:
        shutil.copy2(src_path, dst_path)
        copied_count += 1
        counters[our_category] += 1
        
        if copied_count % 10 == 0:
            print(f"  Copied {copied_count}/{len(animal_df)} files...")
    except Exception as e:
        print(f"  ❌ Error copying {filename}: {e}")

print(f"\n✅ Successfully copied {copied_count} files!")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"📁 Output directory: {OUTPUT_PATH}")
print(f"\n📊 Files per animal:")

total_files = 0
for animal in sorted(counters.keys()):
    count = counters[animal] - 1  # Subtract 1 because we incremented after copying
    total_files += count
    print(f"  {animal:15s}: {count} files")

print(f"\n📈 Total files: {total_files}")

print("\n" + "=" * 70)
print("✅ DATASET READY!")
print("=" * 70)
print("\nNext steps:")
print("  1. Run: python run_complete_pipeline.py")
print("  2. Wait for training to complete (30-45 minutes)")
print("  3. Test with: python 3_predict.py your_audio.wav")
print("\n🎉 You now have a proper animal sound dataset!")
