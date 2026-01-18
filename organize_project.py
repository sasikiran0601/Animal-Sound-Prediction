"""
Organize Essential Project Files into ChotuKaOutput folder
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
import shutil

# Paths
PROJECT_PATH = Path(r"C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection")
OUTPUT_FOLDER = PROJECT_PATH / "ChotuKaOutput"

# Create output folder
OUTPUT_FOLDER.mkdir(exist_ok=True)
print("=" * 70)
print("ORGANIZING PROJECT FILES INTO 'ChotuKaOutput'")
print("=" * 70)

# Essential files to copy
essential_files = [
    # Main scripts
    "prepare_esc50_dataset.py",
    "new_animal_sound_pipeline.py",
    "3_predict.py",
    
    # Configuration
    "requirements.txt",
    
    # Documentation
    "README.md",
    "QUICKSTART.md",
]

# Copy essential files
print("\n📁 Copying essential files...")
copied_count = 0

for file_name in essential_files:
    src = PROJECT_PATH / file_name
    dst = OUTPUT_FOLDER / file_name
    
    if src.exists():
        shutil.copy2(src, dst)
        print(f"  ✅ {file_name}")
        copied_count += 1
    else:
        print(f"  ⚠️  {file_name} (not found, skipping)")

# Copy trained model folder
print("\n📦 Copying trained model...")
model_src = PROJECT_PATH / "trained_model"
model_dst = OUTPUT_FOLDER / "trained_model"

if model_src.exists():
    if model_dst.exists():
        shutil.rmtree(model_dst)
    shutil.copytree(model_src, model_dst)
    model_files = len(list(model_dst.glob("*")))
    print(f"  ✅ trained_model/ ({model_files} files)")
else:
    print(f"  ⚠️  trained_model/ (not found)")

# Copy sample audio files (5 per animal for testing)
print("\n🎵 Copying sample audio files...")
data_src = PROJECT_PATH / "mini_project" / "data"
data_dst = OUTPUT_FOLDER / "sample_audio"
data_dst.mkdir(exist_ok=True)

if data_src.exists():
    animals = ['Dog', 'Rooster', 'Frog']
    sample_count = 0
    
    for animal in animals:
        # Copy first 5 files of each animal
        for i in range(1, 6):
            src_file = data_src / f"{animal}_{i}.wav"
            if src_file.exists():
                dst_file = data_dst / f"{animal}_{i}.wav"
                shutil.copy2(src_file, dst_file)
                sample_count += 1
    
    print(f"  ✅ sample_audio/ ({sample_count} files)")
else:
    print(f"  ⚠️  sample_audio/ (source not found)")

# Create a usage guide
usage_guide = """# ChotuKaOutput - Animal Sound Classifier

## 📁 Files Included

### Main Scripts:
1. **prepare_esc50_dataset.py** - Extract animal sounds from ESC-50 dataset
2. **new_animal_sound_pipeline.py** - Train the model (generates spectrograms + trains CNN)
3. **3_predict.py** - Make predictions on new audio files

### Model:
- **trained_model/** - Pre-trained model ready to use
  - `best_model.h5` - Trained neural network
  - `class_labels.json` - Animal class mappings

### Sample Audio:
- **sample_audio/** - 15 sample files (5 per animal) for testing

---

## 🚀 Quick Start

### Test the Model (No training needed):
```bash
python 3_predict.py sample_audio/Dog_1.wav
python 3_predict.py sample_audio/Rooster_1.wav
python 3_predict.py sample_audio/Frog_1.wav
```

### Retrain with Different Animals:
1. Edit `new_animal_sound_pipeline.py` line 29:
   ```python
   SELECTED_ANIMALS = ['Dog', 'Cat', 'Rooster', 'Cow', 'Frog']
   ```

2. Run training:
   ```bash
   python new_animal_sound_pipeline.py
   ```

### Add New Animals:
1. Add audio files to `sample_audio/` folder:
   - Name format: `AnimalName_1.wav`, `AnimalName_2.wav`, etc.
   - Need 30-50 files per animal

2. Update `SELECTED_ANIMALS` in `new_animal_sound_pipeline.py`

3. Retrain the model

---

## 📊 Current Model

**Trained on:** Dog, Rooster, Frog  
**Accuracy:** ~58% validation  
**Status:** ✅ Working

---

## 🔧 Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- tensorflow
- librosa
- numpy
- matplotlib
- pandas
- tqdm

---

## 💡 Tips

- **3 animals** = Best accuracy (60-70%)
- **5 animals** = Good balance (50-65%)
- **7+ animals** = Lower accuracy (40-55%)

Keep audio files:
- Format: `.wav` (recommended)
- Duration: Any (model uses first 3 seconds)
- Quality: Clear audio, minimal background noise

---

## 📝 Workflow

```
1. Test existing model
   python 3_predict.py sample_audio/Dog_1.wav

2. (Optional) Retrain with more animals
   python new_animal_sound_pipeline.py

3. Use your own audio files
   python 3_predict.py path/to/your/audio.wav
```

---

## ✅ You're Ready!

The model is already trained. Just run `3_predict.py` to test it!
"""

with open(OUTPUT_FOLDER / "README.md", 'w', encoding='utf-8') as f:
    f.write(usage_guide)
print("\nCreated README.md")

# Summary
print("\n" + "=" * 70)
print("✅ PROJECT ORGANIZED SUCCESSFULLY!")
print("=" * 70)
print(f"\n📁 Output folder: {OUTPUT_FOLDER}")
print(f"\n📊 Summary:")
print(f"  - Python scripts: {copied_count}")
print(f"  - Trained model: {'✅ Included' if model_src.exists() else '❌ Not found'}")
print(f"  - Sample audio: {sample_count if data_src.exists() else 0} files")
print(f"  - Documentation: README.md")

print(f"\n🎯 Next steps:")
print(f"  1. cd ChotuKaOutput")
print(f"  2. python 3_predict.py sample_audio/Dog_1.wav")
print(f"\n🎉 All essential files are in 'ChotuKaOutput' folder!")
