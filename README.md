# 🐾 Animal Sound Classification System

A complete deep learning pipeline for classifying animal sounds using Convolutional Neural Networks (CNN) and spectrograms.

## 📋 Overview

This project converts audio files (.wav, .mp3) into mel-spectrograms and uses a CNN model to classify which animal the sound belongs to. The system includes both a command-line interface and a modern web frontend for easy audio classification.

**NEW**: 🌐 **Web Frontend** - Upload audio files through a beautiful web interface and get instant predictions!

## 🎯 Features

- **🌐 Web Frontend**: Modern, responsive web interface with drag-and-drop upload
- **Audio to Spectrogram Conversion**: Converts audio files to mel-spectrograms
- **CNN Model Training**: Deep learning model with 8+ layers
- **Multi-class Classification**: Supports 15 animal species
- **High Accuracy**: Achieves good accuracy with data augmentation
- **Easy Prediction**: Simple interface to classify new audio files
- **Real-time Results**: Instant predictions with confidence scores

## 🏗️ Architecture

```
Audio File (.wav/.mp3)
    ↓
Preprocessing (3 seconds, 22050 Hz)
    ↓
Mel-Spectrogram Generation (128 mel bands)
    ↓
CNN Model (VGG-inspired architecture)
    ↓
Animal Classification Output
```

## � Supported Animal Classes

The model can detect **15 different animal sounds**:

1. 🐻 Bear
2. 🐦 Bird
3. 🐱 Cat
4. 🐮 Cow
5. 🦅 Crow
6. 🐕 Dog
7. 🐸 Frog
8. 🐔 Hen
9. 🦗 Insects
10. 🦁 Lion
11. 🐷 Pig
12. 🐓 Rooster
13. 🐑 Sheep
14. 🐦 Humming-bird
15. 📊 Sample

## 📦 Dataset

### Download from Kaggle

The complete dataset is hosted on Kaggle for easy access:

**🎵 [Animal Sound Dataset on Kaggle](https://www.kaggle.com/datasets/sasikiran0601/animaldataset)**

This includes:
- 46,162+ audio files (.wav format)
- 15 animal classes
- Pre-processed spectrograms
- Trained CNN model (best_model.h5)

### Quick Download

**Option 1: Download via Kaggle Website**
1. Visit: https://www.kaggle.com/datasets/sasikiran0601/animaldataset
2. Click "Download" button
3. Extract to your project folder

**Option 2: Download via Kaggle CLI**
```bash
# Install Kaggle CLI
pip install kaggle

# Download dataset
kaggle datasets download -d sasikiran0601/animaldataset

# Extract
unzip animaldataset.zip
```

> **Note**: The trained model is included in this repository, so you can start using the web app immediately without downloading the full dataset!

---

## 📦 Installation

1. **Install Python 3.8+**

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

Required packages:
- `tensorflow` - Deep learning framework
- `librosa` - Audio processing
- `numpy` - Numerical computing
- `matplotlib` - Plotting
- `flask` - Web server
- `flask-cors` - CORS support

## 🚀 Usage

### 🌐 Quick Start: Web Interface (Recommended)

The easiest way to use the animal sound classifier:

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

- Drag and drop an audio file (MP3, WAV, FLAC, OGG, M4A)
- Click "Predict Animal"
- See results with confidence scores for all 15 animal classes!

---

### 📚 Advanced: Command Line Interface

### Step 1: Generate Spectrograms

Process audio files and generate spectrograms for training:

```bash
python 1_generate_spectrograms.py
```

This will:
- Read 100 audio samples from `mini_project/sounds.csv`
- Generate mel-spectrograms (128x128 images)
- Save organized by animal class in `spectrograms_dataset/`

### Step 2: Train the Model

Train the CNN model on generated spectrograms:

```bash
python 2_train_model.py
```

This will:
- Load spectrograms from `spectrograms_dataset/`
- Build a CNN model with ~2M parameters
- Train for up to 50 epochs with early stopping
- Save the best model to `trained_model/animal_sound_classifier.h5`
- Generate training history plots

### Step 3: Predict New Audio

Classify a new audio file:

```bash
python 3_predict.py path/to/your/audio.wav
```

Or run interactively:
```bash
python 3_predict.py
```

## 📊 Model Architecture

```
Input: 128x128x3 RGB Spectrogram Image

Block 1: Conv2D(32) → BatchNorm → Conv2D(32) → BatchNorm → MaxPool → Dropout(0.25)
Block 2: Conv2D(64) → BatchNorm → Conv2D(64) → BatchNorm → MaxPool → Dropout(0.25)
Block 3: Conv2D(128) → BatchNorm → Conv2D(128) → BatchNorm → MaxPool → Dropout(0.25)
Block 4: Conv2D(256) → BatchNorm → Conv2D(256) → BatchNorm → MaxPool → Dropout(0.25)

Flatten
Dense(512) → BatchNorm → Dropout(0.5)
Dense(256) → BatchNorm → Dropout(0.5)
Dense(num_classes, softmax)

Total Parameters: ~2,000,000
```

## 🎵 Audio Processing Parameters

- **Sample Rate**: 22,050 Hz
- **Duration**: 3 seconds (fixed)
- **Mel Bands**: 128
- **Hop Length**: 512
- **FFT Window**: 2048
- **Frequency Range**: 0 - 11,025 Hz

## 📁 Project Structure

```
AnimalVoicedetection/
├── static/                    # Web frontend files
│   ├── index.html            # Main web page
│   ├── style.css             # Premium styling
│   └── script.js             # Interactive functionality
├── mini_project/              # Original audio files and CSV
│   ├── sounds.csv            # Audio metadata
│   └── *.wav                 # Audio files
├── spectrograms_dataset/      # Generated spectrograms
│   ├── Lion/
│   ├── Bear/
│   ├── Cat/
│   └── ...
├── trained_model/             # Trained model and artifacts
│   ├── best_model.h5         # Trained CNN model
│   ├── class_labels.json     # Animal class labels
│   ├── training_history.json
│   └── training_history.png
├── uploads/                   # Temporary upload folder (auto-created)
├── app.py                     # Flask web server
├── 1_generate_spectrograms.py # Step 1: Generate spectrograms
├── 2_train_model.py           # Step 2: Train CNN model
├── 3_predict.py               # Step 3: Predict new audio (CLI)
├── 4_batch_predict.py         # Batch prediction script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🎓 Training Details

- **Optimizer**: Adam (learning rate: 0.001)
- **Loss Function**: Categorical Cross-Entropy
- **Batch Size**: 32
- **Epochs**: 50 (with early stopping)
- **Validation Split**: 20%
- **Data Augmentation**: 
  - Rotation (±10°)
  - Width/Height shift (±10%)
  - Horizontal flip
  - Zoom (±10%)

## 📈 Expected Results

- **Training Accuracy**: 85-95%
- **Validation Accuracy**: 75-90%
- **Inference Time**: ~0.5 seconds per audio file

## 🐛 Troubleshooting

### Issue: "Audio file not found"
- Ensure audio files are in `mini_project/` directory
- Check CSV file paths match actual file locations

### Issue: "Model not found"
- Run `2_train_model.py` before `3_predict.py`

### Issue: Low accuracy
- Increase training samples per class (aim for 50+ per class)
- Increase training epochs
- Adjust learning rate

## 🔧 Customization

### Change Audio Duration
Edit in all three scripts:
```python
DURATION = 5  # Change from 3 to 5 seconds
```

### Change Image Size
Edit in all three scripts:
```python
IMG_SIZE = (256, 256)  # Change from (128, 128)
```

### Add More Animals
Simply add more audio files with naming pattern: `AnimalName_X.wav`

## 📝 Example Output

```
PREDICTION RESULTS
============================================================
🐾 Predicted Animal: Lion
🎯 Confidence: 94.32%

📊 All Class Probabilities:
  Lion            94.32% ███████████████████████████████████████████████
  Bear             3.21% █
  Dog              1.45% 
  Cat              0.67% 
  Cow              0.35% 
============================================================
```

## 🤝 Contributing

Feel free to:
- Add more animal classes
- Improve model architecture
- Add more audio preprocessing techniques
- Implement real-time audio classification

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Librosa for audio processing
- TensorFlow/Keras for deep learning
- Animal sound datasets from various sources

---

**Made with ❤️ for Animal Sound Classification**
