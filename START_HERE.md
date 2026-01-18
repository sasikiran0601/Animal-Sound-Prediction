# 🎯 START HERE - Your First Steps

## 👋 Welcome to Animal Sound Classifier!

This guide will get you up and running in **10 minutes**.

---

## ⚡ Super Quick Start (3 Commands)

```bash
# 1. Install packages (5 minutes)
pip install -r requirements.txt

# 2. Run the complete pipeline (30-45 minutes)
python run_complete_pipeline.py

# 3. Test with your audio
python 3_predict.py path/to/your/audio.wav
```

**That's it! You're done!** 🎉

---

## 📋 What This System Does

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Audio File │ ───► │ Spectrogram  │ ───► │   Animal    │
│  (.wav/mp3) │      │   (Image)    │      │    Name     │
└─────────────┘      └──────────────┘      └─────────────┘
   Dog bark.wav    →  Visual pattern   →    "Dog (95%)"
```

---

## 🚀 Step-by-Step Guide

### Step 1: Check Python Installation ✅

Open Command Prompt (Windows) or Terminal (Mac/Linux):

```bash
python --version
```

**Expected output**: `Python 3.8.x` or higher

❌ **If not installed**: Download from https://www.python.org/downloads/

---

### Step 2: Install Required Packages 📦

Navigate to project folder:

```bash
cd C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

**Wait 5-10 minutes** for installation to complete.

✅ **Verify installation**:
```bash
python -c "import tensorflow; print('Success!')"
```

---

### Step 3: Run the Pipeline 🎵

#### Option A: Automatic (Recommended)

Run everything in one command:

```bash
python run_complete_pipeline.py
```

This will:
1. ✅ Generate spectrograms from 100 audio files
2. ✅ Train CNN model (30-45 minutes)
3. ✅ Save trained model

**Go grab a coffee! ☕ This takes 30-45 minutes.**

#### Option B: Manual (Step by Step)

If you prefer control:

```bash
# Step 1: Generate spectrograms (5-10 min)
python 1_generate_spectrograms.py

# Step 2: Train model (30-45 min)
python 2_train_model.py

# Step 3: Test prediction
python 3_predict.py mini_project/data/sample_dog.wav
```

---

### Step 4: Classify Your Audio 🎯

Now you can classify any audio file:

```bash
python 3_predict.py your_audio.wav
```

**Example output**:
```
============================================================
PREDICTION RESULTS
============================================================
🐾 Predicted Animal: Dog
🎯 Confidence: 92.45%

📊 All Class Probabilities:
  Dog             92.45% ██████████████████████████████████████████████
  Cat              4.21% ██
  Lion             1.89% 
  Bear             0.98% 
  Cow              0.47% 
============================================================
```

---

## 📁 What Gets Created

After running the pipeline:

```
AnimalVoicedetection/
├── spectrograms_dataset/          ← Generated images
│   ├── Lion/ (50 images)
│   ├── Bear/ (50 images)
│   └── ... (other animals)
│
└── trained_model/                 ← Your trained model
    ├── animal_sound_classifier.h5  ← Main model file
    ├── class_labels.json           ← Animal names
    ├── training_history.json       ← Training metrics
    └── training_history.png        ← Accuracy graph
```

---

## 🎓 Understanding the Files

### Scripts You'll Use:

| File | What It Does | When to Use |
|------|--------------|-------------|
| `run_complete_pipeline.py` | Runs everything automatically | First time setup |
| `1_generate_spectrograms.py` | Creates images from audio | When you add new audio files |
| `2_train_model.py` | Trains the AI model | After generating spectrograms |
| `3_predict.py` | Classifies new audio | Anytime you want to identify an animal sound |
| `4_batch_predict.py` | Tests multiple files | When evaluating model performance |

### Documentation Files:

| File | What's Inside | Read When |
|------|---------------|-----------|
| `QUICKSTART.md` | Fast setup guide | You want quick start |
| `README.md` | Complete documentation | You want full details |
| `INSTALLATION.md` | Setup troubleshooting | Installation problems |
| `ARCHITECTURE.md` | Technical details | You want to understand how it works |
| `PROJECT_SUMMARY.md` | Project overview | You want the big picture |

---

## 🎯 Common Tasks

### Task 1: Classify a Single Audio File

```bash
python 3_predict.py dog_bark.wav
```

### Task 2: Test on Multiple Files

```bash
python 4_batch_predict.py
# Enter folder path when prompted
```

### Task 3: Add New Animal Sounds

1. Add audio files to `mini_project/` folder
   - Name format: `AnimalName_1.wav`, `AnimalName_2.wav`, etc.

2. Regenerate spectrograms:
   ```bash
   python 1_generate_spectrograms.py
   ```

3. Retrain model:
   ```bash
   python 2_train_model.py
   ```

### Task 4: View Training Results

Check the training graph:
- Open: `trained_model/training_history.png`
- Shows accuracy and loss curves

---

## 🐛 Quick Troubleshooting

### Problem: "pip is not recognized"

**Solution**:
```bash
python -m pip install -r requirements.txt
```

### Problem: "No module named tensorflow"

**Solution**:
```bash
pip install tensorflow
```

### Problem: "Audio file not found"

**Solution**:
- Check file path is correct
- Use full path: `C:\path\to\audio.wav`
- Or use quotes: `python 3_predict.py "my audio.wav"`

### Problem: "Model not found"

**Solution**:
- Run training first: `python 2_train_model.py`
- Or run complete pipeline: `python run_complete_pipeline.py`

### Problem: Training is very slow

**Solutions**:
- Normal on CPU (30-45 minutes)
- Use GPU for faster training (10-15 minutes)
- Reduce epochs in `2_train_model.py` (change `EPOCHS = 50` to `EPOCHS = 20`)

---

## 💡 Pro Tips

### Tip 1: Use GPU for Speed
If you have NVIDIA GPU:
```bash
pip install tensorflow-gpu
```
Training will be 3-4x faster!

### Tip 2: Start Small
Test with 10-20 audio files first before processing all 100.

### Tip 3: Check Training Progress
Watch the terminal output during training to see accuracy improving.

### Tip 4: Save Your Best Model
The system automatically saves the best model during training.

### Tip 5: Experiment
Try different audio files, adjust parameters, add new animals!

---

## 📊 Expected Timeline

| Task | Time Required |
|------|---------------|
| Install packages | 5-10 minutes |
| Generate spectrograms (100 files) | 5-10 minutes |
| Train model (CPU) | 30-45 minutes |
| Train model (GPU) | 10-15 minutes |
| Predict single audio | 0.5 seconds |
| **Total (first time)** | **40-65 minutes** |

---

## ✅ Success Checklist

After completing setup, you should be able to:

- [x] Run `python 3_predict.py audio.wav` without errors
- [x] See prediction results with animal name and confidence
- [x] Find trained model in `trained_model/` folder
- [x] See spectrograms in `spectrograms_dataset/` folder
- [x] View training history graph

---

## 🎉 You're Ready!

Congratulations! You now have a working animal sound classifier.

### What You Can Do Now:

1. **Classify sounds**: Use `3_predict.py` on any audio file
2. **Test accuracy**: Use `4_batch_predict.py` on multiple files
3. **Add animals**: Include new species and retrain
4. **Experiment**: Adjust parameters and improve accuracy
5. **Share**: Show off your AI-powered animal identifier!

---

## 📚 Learn More

Want to dive deeper?

- **Quick reference**: Read `QUICKSTART.md`
- **Full documentation**: Read `README.md`
- **Technical details**: Read `ARCHITECTURE.md`
- **Troubleshooting**: Read `INSTALLATION.md`

---

## 🆘 Need Help?

1. Check error messages carefully
2. Read the troubleshooting section above
3. Consult the documentation files
4. Search online for specific errors

---

## 🎯 Your Next Command

Ready to start? Run this:

```bash
python run_complete_pipeline.py
```

Then sit back and watch the magic happen! ✨

---

**Happy classifying! 🐾**

*Remember: The first run takes 40-65 minutes. After that, predictions are instant!*
