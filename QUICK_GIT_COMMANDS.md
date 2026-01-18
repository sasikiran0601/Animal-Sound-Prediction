# 🚀 Quick Git Upload Commands

## Step 1: Initialize Git
```bash
cd c:\Users\sasik\OneDrive\Documents\AnimalVoicedetection
git init
```

## Step 2: Add All Files
```bash
git add .
```

## Step 3: Check Status (Verify .gitignore is working)
```bash
git status
```

**You should see:**
- ✅ Python scripts (app.py, 1_generate_spectrograms.py, etc.)
- ✅ static/ folder
- ✅ trained_model/ folder
- ✅ Documentation files
- ❌ NOT mini_project/ (excluded by .gitignore)
- ❌ NOT animal_audio_dataset/ (excluded by .gitignore)
- ❌ NOT *.zip files (excluded by .gitignore)

## Step 4: Create First Commit
```bash
git commit -m "Initial commit: Animal Voice Detection with Web Frontend"
```

## Step 5: Create GitHub Repository
1. Go to https://github.com
2. Click "New Repository"
3. Name: `animal-voice-detection`
4. Description: "AI-powered animal sound classification with CNN and web interface"
5. Choose Public or Private
6. Click "Create Repository"

## Step 6: Connect to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/animal-voice-detection.git
git branch -M main
```

## Step 7: Push to GitHub
```bash
git push -u origin main
```

---

## 📊 What Will Be Uploaded

**Size: ~30-35 MB** (well within GitHub limits)

**Included:**
- All source code
- Web frontend (HTML, CSS, JS)
- Trained model (25 MB)
- Documentation
- Configuration files

**Excluded (via .gitignore):**
- Large datasets (~650 MB)
- ZIP files (~124 MB)
- Temporary files
- System files

---

## ✅ Verification Checklist

Before pushing:
- [ ] `.gitignore` file exists
- [ ] `git status` shows ~40 files (not 46,000+)
- [ ] Large datasets are NOT listed in `git status`
- [ ] README.md includes web frontend info
- [ ] requirements.txt includes Flask

---

**Need help?** See `GIT_SETUP.md` for detailed instructions!
