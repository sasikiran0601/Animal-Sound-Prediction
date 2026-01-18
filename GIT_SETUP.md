# 🚀 Git Setup Guide

This guide will help you prepare and upload your Animal Voice Detection project to GitHub.

## 📋 What Will Be Uploaded to Git

### ✅ Files Included in Git:
- **Source Code**: All Python scripts (`app.py`, `1_generate_spectrograms.py`, etc.)
- **Web Frontend**: HTML, CSS, JavaScript files in `static/` folder
- **Documentation**: README, guides, architecture docs
- **Model Files**: `trained_model/` folder (including `best_model.h5` and `class_labels.json`)
- **Configuration**: `requirements.txt`, `.gitignore`

### ❌ Files Excluded from Git (via `.gitignore`):
- **Large Datasets**: 
  - `animal_audio_dataset/` - Raw audio dataset
  - `mini_project/` - Original audio files (46,162 files!)
  - `spectrograms_dataset/` - Generated spectrograms
  - `temp_downloads/` - Temporary downloads
  - `datasets_csv/` - CSV files
- **Large ZIP Files**: 
  - `ChotuKaOutput.zip` (105 MB)
  - `spectrograms_dataset.zip` (18 MB)
- **Temporary Files**:
  - `uploads/` - Temporary upload folder
  - `*.pyc`, `__pycache__/` - Python cache
  - `temp_spectrogram.png` - Temporary files
- **System Files**: `.DS_Store`, `Thumbs.db`, etc.

---

## 🔧 Step-by-Step Git Setup

### 1. Initialize Git Repository

Open terminal in your project folder:

```bash
cd c:\Users\sasik\OneDrive\Documents\AnimalVoicedetection
```

Initialize Git:

```bash
git init
```

### 2. Add Files to Git

Add all files (`.gitignore` will automatically exclude large datasets):

```bash
git add .
```

Check what will be committed:

```bash
git status
```

You should see:
- ✅ Source code files
- ✅ `static/` folder
- ✅ `trained_model/` folder
- ✅ Documentation files
- ❌ NOT seeing: `mini_project/`, `animal_audio_dataset/`, large ZIP files

### 3. Create First Commit

```bash
git commit -m "Initial commit: Animal Voice Detection with Web Frontend"
```

### 4. Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click **"New Repository"** (green button)
3. Repository name: `animal-voice-detection` (or your choice)
4. Description: "AI-powered animal sound classification with CNN and web interface"
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README (we already have one)
7. Click **"Create Repository"**

### 5. Connect to GitHub

Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/animal-voice-detection.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 6. Push to GitHub

```bash
git push -u origin main
```

Enter your GitHub credentials when prompted.

---

## 📊 Repository Size Estimate

**With `.gitignore`** (what will be uploaded):
- Source code: ~200 KB
- Web frontend: ~50 KB
- Trained model: ~25 MB (best_model.h5)
- Documentation: ~100 KB
- **Total: ~25-30 MB** ✅ (Acceptable for GitHub)

**Without `.gitignore`** (if you uploaded everything):
- All datasets: ~500+ MB
- ZIP files: ~124 MB
- **Total: ~650+ MB** ❌ (Too large for GitHub!)

---

## 🎯 Important Notes

### Model File Size
The trained model (`best_model.h5`) is about 25 MB. GitHub allows files up to 100 MB, so this is fine. If you want to exclude it:

1. Edit `.gitignore` and uncomment this line:
   ```
   # trained_model/best_model.h5
   ```

2. Users can then train their own model using the scripts.

### Datasets
The datasets are **intentionally excluded** because:
- They're too large for GitHub (500+ MB)
- Users can download their own datasets
- The scripts include instructions for dataset preparation

### Sharing Datasets Separately
If you want to share datasets:
- Upload to **Google Drive** or **Dropbox**
- Add download link to README
- Or use **Git LFS** (Large File Storage) - requires setup

---

## 📝 Adding a Dataset Download Link

Edit `README.md` and add:

```markdown
## 📦 Dataset

Due to size constraints, the dataset is not included in this repository.

**Download Options:**
1. **Pre-trained Model**: Included in `trained_model/` - ready to use!
2. **Train Your Own**: Follow instructions in `DATASET_DOWNLOAD_GUIDE.md`
3. **Download Dataset**: [Google Drive Link](YOUR_LINK_HERE) (if you upload it)
```

---

## 🔄 Future Updates

After making changes to your code:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

---

## 🌟 Making Your Repository Stand Out

### Add a Nice README Badge

Add to top of `README.md`:

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

### Add Screenshots

1. Take screenshots of your web interface
2. Create `screenshots/` folder
3. Add images to README:
   ```markdown
   ## 🖼️ Screenshots
   ![Web Interface](screenshots/interface.png)
   ```

### Add Demo GIF

Record a quick demo of uploading and predicting, then add:
```markdown
## 🎬 Demo
![Demo](screenshots/demo.gif)
```

---

## ✅ Checklist Before Pushing

- [ ] `.gitignore` file created
- [ ] Large datasets excluded
- [ ] README updated with web frontend info
- [ ] `requirements.txt` includes all dependencies
- [ ] Tested that code runs after fresh clone
- [ ] Removed any sensitive information (API keys, passwords)
- [ ] Commit messages are clear and descriptive

---

## 🆘 Troubleshooting

### "File too large" error
- Check if `.gitignore` is working: `git status`
- Remove large files from staging: `git rm --cached filename`
- Verify `.gitignore` patterns

### "Permission denied"
- Check GitHub credentials
- Use personal access token instead of password
- Or set up SSH keys

### Want to remove already committed large files
```bash
git rm --cached -r mini_project/
git commit -m "Remove large dataset files"
git push
```

---

## 🎓 Git Best Practices

1. **Commit Often**: Small, focused commits
2. **Clear Messages**: Describe what and why
3. **Branch for Features**: Use branches for new features
4. **Pull Before Push**: Always pull latest changes first
5. **Review Before Commit**: Check `git status` and `git diff`

---

**Ready to upload! 🚀**

Your project is now configured to be uploaded to GitHub with only the essential files, keeping the repository size manageable while preserving all functionality.
