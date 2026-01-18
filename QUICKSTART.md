# 🚀 Quick Start Guide - Animal Sound Classifier

## ⚡ Fast Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install tensorflow librosa numpy pandas matplotlib soundfile tqdm Pillow
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 2. Run Complete Pipeline
```bash
python run_complete_pipeline.py
```

This will automatically:
- ✅ Generate spectrograms from 100 audio files
- ✅ Train CNN model (30-45 minutes)
- ✅ Save trained model

### 3. Classify New Audio
```bash
python 3_predict.py path/to/your/audio.wav
```

---

## 📝 Manual Step-by-Step

If you prefer to run each step manually:

### Step 1: Generate Spectrograms
```bash
python 1_generate_spectrograms.py
```
**Output**: `spectrograms_dataset/` folder with organized images

### Step 2: Train Model
```bash
python 2_train_model.py
```
**Output**: `trained_model/animal_sound_classifier.h5`

### Step 3: Predict
```bash
python 3_predict.py your_audio.wav
```
**Output**: Animal classification with confidence score

---

## 🎯 Example Usage

```bash
# Classify a dog bark
python 3_predict.py mini_project/data/sample_dog.wav

# Expected output:
# 🐾 Predicted Animal: Dog
# 🎯 Confidence: 92.45%
```

---

## 📊 What You Get

After training, you'll have:

1. **Trained Model** (`animal_sound_classifier.h5`)
   - Ready to classify animal sounds
   - ~2M parameters
   - 75-90% accuracy

2. **Training History** (`training_history.png`)
   - Accuracy and loss curves
   - Shows model performance over time

3. **Class Labels** (`class_labels.json`)
   - Maps model outputs to animal names

4. **Spectrograms** (`spectrograms_dataset/`)
   - Visual representations of audio
   - Organized by animal class

---

## 🔧 Troubleshooting

### "No module named tensorflow"
```bash
pip install tensorflow
```

### "Audio file not found"
- Check that audio files are in `mini_project/` directory
- Verify the CSV file paths

### "Not enough spectrograms"
- Ensure at least 10 audio files are available
- Check that files are in .wav format

### Low GPU memory
Edit `2_train_model.py`:
```python
BATCH_SIZE = 16  # Reduce from 32
```

---

## 💡 Tips

1. **More Data = Better Accuracy**
   - Aim for 50+ samples per animal class
   - Use diverse audio recordings

2. **GPU Acceleration**
   - Install `tensorflow-gpu` for faster training
   - Training time: 10-15 min (GPU) vs 30-45 min (CPU)

3. **Custom Animals**
   - Add new audio files: `NewAnimal_1.wav`, `NewAnimal_2.wav`, etc.
   - Rerun the pipeline

4. **Improve Accuracy**
   - Increase `EPOCHS` in `2_train_model.py`
   - Add more training data
   - Adjust learning rate

---

## 📞 Need Help?

Check the full documentation in `README.md` for:
- Detailed architecture explanation
- Customization options
- Advanced features
- Troubleshooting guide

---

**Ready to classify animal sounds? Run `python run_complete_pipeline.py` now! 🐾**
