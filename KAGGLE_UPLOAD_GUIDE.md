# 📊 Upload Datasets to Kaggle - Step-by-Step Guide

This guide will help you upload your animal sound datasets to Kaggle and link them in your GitHub repository.

## 🎯 Why Kaggle?

- ✅ Free hosting for large datasets
- ✅ Easy sharing and downloading
- ✅ Version control for datasets
- ✅ Community visibility
- ✅ No file size limits (unlike GitHub)

---

## 📦 Datasets to Upload

You have several datasets to upload:

### 1. **Audio Dataset** (~500+ MB)
- **Folder**: `mini_project/`
- **Contents**: 46,162 audio files (.wav)
- **Description**: Raw animal sound recordings for 15 animal classes

### 2. **Spectrograms Dataset** (~18 MB)
- **Folder**: `spectrograms_dataset/` or `spectrograms_dataset.zip`
- **Contents**: Generated mel-spectrogram images
- **Description**: Pre-processed spectrograms ready for CNN training

### 3. **Trained Model** (~25 MB)
- **Folder**: `trained_model/`
- **Contents**: `best_model.h5`, `class_labels.json`, training history
- **Description**: Pre-trained CNN model for animal sound classification

---

## 🚀 Step-by-Step Upload Process

### Step 1: Create Kaggle Account

1. Go to https://www.kaggle.com
2. Sign up or log in
3. Verify your email

### Step 2: Create API Token

1. Go to https://www.kaggle.com/settings
2. Scroll to "API" section
3. Click "Create New API Token"
4. Download `kaggle.json` file
5. Place it in: `C:\Users\sasik\.kaggle\kaggle.json`

### Step 3: Install Kaggle CLI

```bash
pip install kaggle
```

### Step 4: Create Dataset Metadata

For each dataset, create a `dataset-metadata.json` file.

**Example for Audio Dataset:**

Create `mini_project/dataset-metadata.json`:
```json
{
  "title": "Animal Sound Audio Dataset - 15 Classes",
  "id": "sasikiran0601/animal-sound-audio-dataset",
  "licenses": [
    {
      "name": "CC0-1.0"
    }
  ],
  "keywords": ["audio", "animals", "sound classification", "deep learning"],
  "description": "Raw audio recordings of 15 different animal species including Lion, Bear, Dog, Cat, Frog, Hen, Cow, Pig, Sheep, Bird, Crow, Rooster, Insects, and Humming-bird. Contains 46,162 WAV files suitable for training audio classification models."
}
```

### Step 5: Upload Using Kaggle CLI

**Upload Audio Dataset:**
```bash
cd c:\Users\sasik\OneDrive\Documents\AnimalVoicedetection\mini_project
kaggle datasets create -p .
```

**Upload Spectrograms Dataset:**
```bash
cd c:\Users\sasik\OneDrive\Documents\AnimalVoicedetection\spectrograms_dataset
kaggle datasets create -p .
```

**Upload Trained Model:**
```bash
cd c:\Users\sasik\OneDrive\Documents\AnimalVoicedetection\trained_model
kaggle datasets create -p .
```

---

## 🌐 Alternative: Upload via Web Interface

If you prefer using the web interface:

### Step 1: Create New Dataset

1. Go to https://www.kaggle.com/datasets
2. Click "New Dataset"
3. Click "Upload" or drag and drop your folder/ZIP file

### Step 2: Fill Dataset Information

**For Audio Dataset:**
- **Title**: Animal Sound Audio Dataset - 15 Classes
- **Subtitle**: Raw audio recordings for animal sound classification
- **Description**: 
  ```
  This dataset contains 46,162 audio files (.wav format) of 15 different animal species.
  
  **Animal Classes:**
  - Bear, Bird, Cat, Cow, Crow, Dog, Frog, Hen, Insects, Lion, Pig, Rooster, Sheep, Humming-bird, Sample
  
  **Audio Specifications:**
  - Format: WAV
  - Sample Rate: 22,050 Hz
  - Duration: Varies (typically 3-5 seconds)
  
  **Use Cases:**
  - Audio classification
  - Deep learning model training
  - Sound recognition research
  
  **Related Project:**
  GitHub: https://github.com/sasikiran0601/Animal-Sound-Prediction
  ```

- **Tags**: audio, animals, sound-classification, deep-learning, cnn
- **License**: CC0: Public Domain

### Step 3: Upload Files

**Option A: Upload ZIP file**
- Compress `mini_project/` folder
- Upload the ZIP file
- Kaggle will automatically extract it

**Option B: Upload folder directly**
- Select the entire `mini_project/` folder
- Drag and drop into Kaggle

### Step 4: Publish Dataset

1. Review your dataset
2. Click "Create"
3. Wait for processing (may take a few minutes for large datasets)
4. Copy the dataset URL

---

## 📝 Update Your GitHub README

Once uploaded to Kaggle, update your README.md:

```markdown
## 📦 Datasets

Due to size constraints, datasets are hosted on Kaggle:

### 🎵 Audio Dataset
**Download**: [Animal Sound Audio Dataset on Kaggle](https://www.kaggle.com/datasets/YOUR_USERNAME/animal-sound-audio-dataset)
- 46,162 audio files (.wav)
- 15 animal classes
- Ready for training

### 🖼️ Spectrograms Dataset
**Download**: [Animal Sound Spectrograms on Kaggle](https://www.kaggle.com/datasets/YOUR_USERNAME/animal-sound-spectrograms)
- Pre-processed mel-spectrograms
- 128x128 images
- Ready for CNN training

### 🤖 Pre-trained Model
**Download**: [Trained CNN Model on Kaggle](https://www.kaggle.com/datasets/YOUR_USERNAME/animal-sound-model)
- best_model.h5 (25 MB)
- 85-95% accuracy
- Ready to use

## 🔧 Quick Setup with Kaggle Datasets

```bash
# Install Kaggle CLI
pip install kaggle

# Download datasets
kaggle datasets download -d YOUR_USERNAME/animal-sound-audio-dataset
kaggle datasets download -d YOUR_USERNAME/animal-sound-spectrograms
kaggle datasets download -d YOUR_USERNAME/animal-sound-model

# Extract
unzip animal-sound-audio-dataset.zip -d mini_project/
unzip animal-sound-spectrograms.zip -d spectrograms_dataset/
unzip animal-sound-model.zip -d trained_model/
```
```

---

## 🎯 Recommended Upload Strategy

**Upload in this order:**

1. **First**: Trained Model (~25 MB) - Quick and easy
2. **Second**: Spectrograms Dataset (~18 MB) - Medium size
3. **Third**: Audio Dataset (~500 MB) - Largest, may take time

This way, users can start using your project immediately with the pre-trained model!

---

## ✅ After Upload Checklist

- [ ] All datasets uploaded to Kaggle
- [ ] Dataset URLs copied
- [ ] README.md updated with Kaggle links
- [ ] Tested download links work
- [ ] GitHub repository pushed with updated README
- [ ] .gitignore still excludes local dataset folders

---

## 🔗 Example Dataset URLs

After upload, your URLs will look like:
- `https://www.kaggle.com/datasets/sasikiran0601/animal-sound-audio-dataset`
- `https://www.kaggle.com/datasets/sasikiran0601/animal-sound-spectrograms`
- `https://www.kaggle.com/datasets/sasikiran0601/animal-sound-model`

---

## 💡 Pro Tips

1. **Use descriptive titles** - Makes datasets easier to find
2. **Add good descriptions** - Explain what's in the dataset
3. **Include usage examples** - Show how to download and use
4. **Add tags** - Improves discoverability
5. **Link to GitHub** - Cross-reference your code repository
6. **Version your datasets** - Kaggle supports versioning

---

**Ready to upload! 🚀**

Choose either CLI or Web Interface method and start uploading your datasets to Kaggle!
