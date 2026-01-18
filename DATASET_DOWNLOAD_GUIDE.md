# Animal Sound Dataset Download Guide

This guide helps you download 100 audio files for each of the 14 animals:
**Cat, Dog, Elephant, Cow, Frog, Sheep, Bird, Goat, Lion, Tiger, Hen, Pig, Rooster, Bear**

## Quick Start

### Option 1: Multi-Source Downloader (Recommended)
```bash
# Install dependencies
pip install -r dataset_requirements.txt

# Run the multi-source downloader
python download_animal_sounds_multi_source.py
```

This will automatically download from:
- **ESC-50**: Dog, Rooster, Pig, Cow, Frog, Cat, Hen, Sheep (~40 files each)
- **GitHub Animal Dataset**: Cat, Dog, Bird, Cow, Lion, Sheep, Frog, Hen (200+ files for some)

### Option 2: Freesound API (Best Quality & Coverage)
```bash
# 1. Get API key from https://freesound.org/apiv2/apply/
# 2. Edit download_animal_sounds.py and add your API key
# 3. Run:
python download_animal_sounds.py
```

## Dataset Sources

### Automatic Downloads

| Source | Animals Covered | Files per Animal | Quality |
|--------|----------------|------------------|---------|
| **ESC-50** | Dog, Rooster, Pig, Cow, Frog, Cat, Hen, Sheep | ~40 | High |
| **GitHub Animal Dataset** | Cat, Dog, Bird, Cow, Lion, Sheep, Frog, Hen | 25-200 | Medium |
| **Freesound API** | All 14 animals | Up to 100 | High |

### Manual Downloads (For Missing Animals)

#### 1. BBC Sound Effects (Free, No Registration)
- **URL**: https://sound-effects.bbcrewind.co.uk/
- **Coverage**: All animals including elephant, tiger, bear, goat
- **How to**:
  1. Search for animal name (e.g., "elephant")
  2. Download WAV files
  3. Save to `animal_audio_dataset/elephant/`

#### 2. Xeno-Canto (Birds)
- **URL**: https://www.xeno-canto.org/
- **Coverage**: 700,000+ bird recordings
- **Kaggle**: https://www.kaggle.com/imoore/xenocanto-bird-recordings-dataset

#### 3. Kaggle Datasets

**Animal Sounds Dataset**
```bash
kaggle datasets download -d maulanaakbardwijaya/animal-sounds-dataset
```

**Audio Cats and Dogs**
```bash
kaggle datasets download -d mmoreaux/audio-cats-and-dogs
```

**Animal Sounds Classification**
```bash
kaggle datasets download -d haithammoh/sounds-of-animals
```

## Data Augmentation

If you have fewer than 100 files per animal, use augmentation:

```python
# The multi-source script includes augmentation
# It will ask if you want to augment at the end

# Or run augmentation separately:
python download_animal_sounds_multi_source.py
# Select 'y' when prompted for augmentation
```

**Augmentation techniques used:**
- Time stretching (0.9x - 1.1x speed)
- Pitch shifting (-2 to +2 semitones)
- Adding background noise

## Expected Dataset Structure

```
animal_audio_dataset/
├── cat/
│   ├── cat_001.wav
│   ├── cat_002.wav
│   └── ... (100 files)
├── dog/
│   ├── dog_001.wav
│   └── ... (100 files)
├── elephant/
├── cow/
├── frog/
├── sheep/
├── bird/
├── goat/
├── lion/
├── tiger/
├── hen/
├── pig/
├── rooster/
├── bear/
└── dataset_summary.json
```

## Step-by-Step Instructions

### Step 1: Install Dependencies
```bash
pip install requests tqdm librosa soundfile numpy
```

### Step 2: Run Multi-Source Downloader
```bash
python download_animal_sounds_multi_source.py
```

This will:
1. Create folder structure
2. Download ESC-50 dataset (~600MB)
3. Download GitHub animal dataset
4. Show summary of downloaded files
5. Offer to augment dataset

### Step 3: Check Coverage
```bash
# Check dataset_summary.json
cat animal_audio_dataset/dataset_summary.json
```

### Step 4: Fill Missing Animals

**Animals likely missing**: Elephant, Tiger, Bear, Goat

**Option A: Use Freesound API**
1. Get API key: https://freesound.org/apiv2/apply/
2. Edit `download_animal_sounds.py` line 23
3. Run: `python download_animal_sounds.py`

**Option B: Manual Download from BBC**
1. Visit: https://sound-effects.bbcrewind.co.uk/
2. Search for each missing animal
3. Download WAV files
4. Save to respective folders

### Step 5: Augment if Needed
```bash
# Run the multi-source script again and select augmentation
python download_animal_sounds_multi_source.py
# Type 'y' when asked about augmentation
```

## Troubleshooting

### Issue: "Not enough files for some animals"
**Solution**: 
- Use Freesound API for those animals
- Download manually from BBC Sound Effects
- Use augmentation to generate more files

### Issue: "Download fails"
**Solution**:
- Check internet connection
- Try again (script resumes from where it stopped)
- Use manual download methods

### Issue: "Freesound API key error"
**Solution**:
- Register at https://freesound.org/
- Apply for API key at https://freesound.org/apiv2/apply/
- Replace key in script

## Quality Recommendations

For best model performance:
1. **Minimum**: 50 files per animal (use augmentation)
2. **Good**: 100 files per animal (target)
3. **Best**: 200+ files per animal (download more from Freesound)

Audio specifications:
- **Format**: WAV or MP3
- **Duration**: 1-10 seconds
- **Sample Rate**: 22050 Hz or higher
- **Quality**: Clear animal sounds, minimal background noise

## Next Steps

After downloading the dataset:

1. **Verify dataset**:
   ```bash
   python -c "import json; print(json.dumps(json.load(open('animal_audio_dataset/dataset_summary.json')), indent=2))"
   ```

2. **Generate spectrograms**:
   ```bash
   python new_animal_sound_pipeline.py
   ```

3. **Train model** using the generated spectrograms

## Additional Resources

- **ESC-50**: https://github.com/karolpiczak/ESC-50
- **Freesound**: https://freesound.org/
- **BBC Sound Effects**: https://sound-effects.bbcrewind.co.uk/
- **Xeno-Canto**: https://www.xeno-canto.org/
- **AudioSet**: https://research.google.com/audioset/

## License Notes

- ESC-50: Creative Commons
- Freesound: Various (check individual files)
- BBC Sound Effects: RemArc License (free for research/education)
- Always check license before commercial use
