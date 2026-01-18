# 🔧 Installation Guide - Animal Sound Classifier

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, Linux, or macOS
- **Python**: 3.8 or higher (3.9 or 3.10 recommended)
- **RAM**: Minimum 4GB (8GB+ recommended)
- **Storage**: 2GB free space
- **GPU**: Optional (NVIDIA GPU with CUDA for faster training)

### Check Python Version
```bash
python --version
# Should show: Python 3.8.x or higher
```

If Python is not installed, download from: https://www.python.org/downloads/

---

## 🚀 Quick Installation (5 Minutes)

### Step 1: Navigate to Project Directory
```bash
cd C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- TensorFlow (deep learning framework)
- Librosa (audio processing)
- NumPy (numerical computing)
- Pandas (data manipulation)
- Matplotlib (visualization)
- And other required packages

### Step 3: Verify Installation
```bash
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
python -c "import librosa; print('Librosa version:', librosa.__version__)"
```

If no errors appear, you're ready to go! ✅

---

## 📦 Detailed Installation Steps

### Option 1: Using pip (Recommended)

1. **Open Command Prompt/Terminal**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac/Linux: Open Terminal

2. **Navigate to project folder**
   ```bash
   cd C:\Users\sasik\OneDrive\Documents\AnimalVoicedetection
   ```

3. **Install all packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Wait for installation** (5-10 minutes)

### Option 2: Using Conda (Alternative)

If you use Anaconda/Miniconda:

1. **Create new environment**
   ```bash
   conda create -n animal_sound python=3.9
   conda activate animal_sound
   ```

2. **Install TensorFlow**
   ```bash
   conda install tensorflow
   ```

3. **Install other packages**
   ```bash
   pip install librosa pandas matplotlib soundfile tqdm Pillow scikit-learn
   ```

### Option 3: Manual Installation

Install packages one by one:

```bash
pip install tensorflow>=2.10.0
pip install librosa>=0.10.0
pip install numpy>=1.23.0
pip install pandas>=1.5.0
pip install matplotlib>=3.6.0
pip install soundfile>=0.12.0
pip install tqdm>=4.64.0
pip install Pillow>=9.3.0
pip install scikit-learn>=1.2.0
```

---

## 🎮 GPU Setup (Optional - For Faster Training)

### NVIDIA GPU Users

If you have an NVIDIA GPU, you can use GPU acceleration:

1. **Check GPU availability**
   ```bash
   python -c "import tensorflow as tf; print('GPU Available:', tf.config.list_physical_devices('GPU'))"
   ```

2. **Install CUDA Toolkit** (if not already installed)
   - Download from: https://developer.nvidia.com/cuda-downloads
   - Version: CUDA 11.2 or higher

3. **Install cuDNN** (if not already installed)
   - Download from: https://developer.nvidia.com/cudnn
   - Version: cuDNN 8.1 or higher

4. **Install TensorFlow GPU**
   ```bash
   pip install tensorflow-gpu
   ```

5. **Verify GPU setup**
   ```bash
   python -c "import tensorflow as tf; print('Num GPUs:', len(tf.config.list_physical_devices('GPU')))"
   ```

**Note**: GPU setup can be complex. If you encounter issues, CPU training works fine (just slower).

---

## 🐛 Troubleshooting Installation

### Issue: "pip is not recognized"

**Solution**:
```bash
python -m pip install -r requirements.txt
```

### Issue: "Permission denied"

**Windows Solution**:
```bash
pip install --user -r requirements.txt
```

**Linux/Mac Solution**:
```bash
sudo pip install -r requirements.txt
```

### Issue: "Could not find a version that satisfies the requirement"

**Solution**: Update pip first
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: TensorFlow installation fails

**Solution 1**: Install specific version
```bash
pip install tensorflow==2.10.0
```

**Solution 2**: Use CPU-only version
```bash
pip install tensorflow-cpu
```

### Issue: Librosa installation fails

**Solution**: Install dependencies first
```bash
pip install numpy scipy
pip install librosa
```

### Issue: "ImportError: DLL load failed"

**Windows Solution**: Install Visual C++ Redistributable
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Run installer and restart

### Issue: Out of memory during installation

**Solution**: Install packages one at a time
```bash
pip install tensorflow
pip install librosa
pip install pandas
# ... continue for each package
```

---

## ✅ Verify Installation

Run this test script to verify everything is working:

```python
# Save as test_installation.py
import sys
print("Python version:", sys.version)

try:
    import tensorflow as tf
    print("✅ TensorFlow:", tf.__version__)
except ImportError as e:
    print("❌ TensorFlow not installed:", e)

try:
    import librosa
    print("✅ Librosa:", librosa.__version__)
except ImportError as e:
    print("❌ Librosa not installed:", e)

try:
    import numpy as np
    print("✅ NumPy:", np.__version__)
except ImportError as e:
    print("❌ NumPy not installed:", e)

try:
    import pandas as pd
    print("✅ Pandas:", pd.__version__)
except ImportError as e:
    print("❌ Pandas not installed:", e)

try:
    import matplotlib
    print("✅ Matplotlib:", matplotlib.__version__)
except ImportError as e:
    print("❌ Matplotlib not installed:", e)

print("\n🎉 All packages installed successfully!")
```

Run it:
```bash
python test_installation.py
```

---

## 🔄 Updating Packages

To update all packages to latest versions:

```bash
pip install --upgrade -r requirements.txt
```

To update specific package:
```bash
pip install --upgrade tensorflow
```

---

## 🗑️ Uninstallation

To remove all installed packages:

```bash
pip uninstall -r requirements.txt -y
```

Or if using conda:
```bash
conda remove -n animal_sound --all
```

---

## 📊 Package Sizes (Approximate)

- TensorFlow: ~450 MB
- Librosa: ~50 MB
- NumPy: ~20 MB
- Pandas: ~30 MB
- Matplotlib: ~40 MB
- Other packages: ~50 MB

**Total download**: ~640 MB

---

## 🌐 Alternative Installation Methods

### Using Virtual Environment (Recommended)

1. **Create virtual environment**
   ```bash
   python -m venv animal_env
   ```

2. **Activate environment**
   - Windows:
     ```bash
     animal_env\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source animal_env/bin/activate
     ```

3. **Install packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Deactivate when done**
   ```bash
   deactivate
   ```

### Using Docker (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run_complete_pipeline.py"]
```

Build and run:
```bash
docker build -t animal-sound-classifier .
docker run -v $(pwd):/app animal-sound-classifier
```

---

## 🎯 Post-Installation Steps

After successful installation:

1. **Test the installation**
   ```bash
   python test_installation.py
   ```

2. **Prepare your data**
   - Ensure audio files are in `mini_project/` folder
   - Verify CSV file exists

3. **Run the pipeline**
   ```bash
   python run_complete_pipeline.py
   ```

---

## 📞 Getting Help

If you encounter issues:

1. **Check error messages carefully**
   - Copy the full error message
   - Search online for solutions

2. **Common resources**:
   - TensorFlow docs: https://www.tensorflow.org/install
   - Librosa docs: https://librosa.org/doc/latest/install.html
   - Stack Overflow: https://stackoverflow.com/

3. **System-specific issues**:
   - Windows: Check Visual C++ Redistributable
   - Mac: Check Xcode Command Line Tools
   - Linux: Check build-essential package

---

## ✨ Installation Complete!

You're now ready to:
- ✅ Generate spectrograms from audio
- ✅ Train deep learning models
- ✅ Classify animal sounds

**Next step**: Read `QUICKSTART.md` to start using the system!

---

**Happy classifying! 🐾**
