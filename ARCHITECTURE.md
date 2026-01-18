# 🏗️ System Architecture - Animal Sound Classifier

## 📊 Complete System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ANIMAL SOUND CLASSIFICATION SYSTEM                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 1: DATA PREPARATION (1_generate_spectrograms.py)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Input: sounds.csv + Audio Files (.wav)                             │
│     │                                                                 │
│     ├─► Read CSV metadata (100 samples)                             │
│     │                                                                 │
│     ├─► For each audio file:                                        │
│     │   ├─► Load audio (librosa)                                    │
│     │   ├─► Resample to 22050 Hz                                    │
│     │   ├─► Trim/Pad to 3 seconds                                   │
│     │   ├─► Generate Mel-Spectrogram (128 mel bands)               │
│     │   ├─► Convert to dB scale                                     │
│     │   └─► Save as 128x128 PNG image                              │
│     │                                                                 │
│     └─► Output: spectrograms_dataset/                               │
│         ├─► Lion/ (50 images)                                       │
│         ├─► Bear/ (50 images)                                       │
│         └─► ... (other animals)                                     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 2: MODEL TRAINING (2_train_model.py)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Input: spectrograms_dataset/                                        │
│     │                                                                 │
│     ├─► Load images with ImageDataGenerator                         │
│     │   ├─► Training set (80%) with augmentation                   │
│     │   │   ├─► Rotation (±10°)                                     │
│     │   │   ├─► Shift (±10%)                                        │
│     │   │   ├─► Zoom (±10%)                                         │
│     │   │   └─► Horizontal flip                                     │
│     │   │                                                             │
│     │   └─► Validation set (20%) without augmentation              │
│     │                                                                 │
│     ├─► Build CNN Model                                             │
│     │   │                                                             │
│     │   │   INPUT: 128x128x3 RGB Image                             │
│     │   │      │                                                     │
│     │   │      ├─► BLOCK 1: Conv2D(32) → BN → Conv2D(32) → BN     │
│     │   │      │              → MaxPool(2x2) → Dropout(0.25)       │
│     │   │      │                                                     │
│     │   │      ├─► BLOCK 2: Conv2D(64) → BN → Conv2D(64) → BN     │
│     │   │      │              → MaxPool(2x2) → Dropout(0.25)       │
│     │   │      │                                                     │
│     │   │      ├─► BLOCK 3: Conv2D(128) → BN → Conv2D(128) → BN   │
│     │   │      │              → MaxPool(2x2) → Dropout(0.25)       │
│     │   │      │                                                     │
│     │   │      ├─► BLOCK 4: Conv2D(256) → BN → Conv2D(256) → BN   │
│     │   │      │              → MaxPool(2x2) → Dropout(0.25)       │
│     │   │      │                                                     │
│     │   │      ├─► Flatten                                          │
│     │   │      │                                                     │
│     │   │      ├─► Dense(512) → BN → Dropout(0.5)                  │
│     │   │      │                                                     │
│     │   │      ├─► Dense(256) → BN → Dropout(0.5)                  │
│     │   │      │                                                     │
│     │   │      └─► Dense(num_classes) → Softmax                    │
│     │   │                                                             │
│     │   │   OUTPUT: Probability distribution over animal classes    │
│     │   │                                                             │
│     │   └─► Compile with Adam optimizer                             │
│     │                                                                 │
│     ├─► Train Model                                                 │
│     │   ├─► Batch size: 32                                          │
│     │   ├─► Epochs: up to 50                                        │
│     │   ├─► Callbacks:                                              │
│     │   │   ├─► ModelCheckpoint (save best)                        │
│     │   │   ├─► EarlyStopping (patience=10)                        │
│     │   │   └─► ReduceLROnPlateau (patience=5)                     │
│     │   │                                                             │
│     │   └─► Monitor validation accuracy                             │
│     │                                                                 │
│     └─► Output: trained_model/                                      │
│         ├─► animal_sound_classifier.h5 (model)                     │
│         ├─► class_labels.json (label mapping)                      │
│         ├─► training_history.json (metrics)                        │
│         └─► training_history.png (plots)                           │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 3: INFERENCE (3_predict.py)                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Input: New audio file (any_animal.wav)                             │
│     │                                                                 │
│     ├─► Load trained model (.h5)                                    │
│     ├─► Load class labels (.json)                                   │
│     │                                                                 │
│     ├─► Preprocess audio                                            │
│     │   ├─► Load with librosa                                       │
│     │   ├─► Resample to 22050 Hz                                    │
│     │   └─► Trim/Pad to 3 seconds                                   │
│     │                                                                 │
│     ├─► Generate spectrogram                                        │
│     │   ├─► Mel-spectrogram (128 bands)                            │
│     │   ├─► Convert to dB                                           │
│     │   └─► Save as temp image                                      │
│     │                                                                 │
│     ├─► Load and normalize image                                    │
│     │   ├─► Resize to 128x128                                       │
│     │   ├─► Normalize to [0, 1]                                     │
│     │   └─► Add batch dimension                                     │
│     │                                                                 │
│     ├─► Model prediction                                            │
│     │   └─► Forward pass through CNN                                │
│     │                                                                 │
│     └─► Output results                                              │
│         ├─► Predicted animal name                                   │
│         ├─► Confidence score (%)                                    │
│         └─► All class probabilities                                 │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Detailed Component Breakdown

### 1. Audio Preprocessing Pipeline

```
Raw Audio File
     │
     ├─► librosa.load(sr=22050)
     │   └─► Converts any sample rate to 22050 Hz
     │
     ├─► Duration normalization
     │   ├─► If < 3s: Pad with zeros
     │   └─► If > 3s: Trim to 3s
     │
     └─► Output: numpy array [66150 samples]
```

### 2. Spectrogram Generation

```
Audio Signal [66150 samples]
     │
     ├─► librosa.feature.melspectrogram()
     │   ├─► n_mels = 128 (frequency bins)
     │   ├─► hop_length = 512 (time steps)
     │   ├─► n_fft = 2048 (FFT window)
     │   └─► fmax = 11025 Hz (Nyquist frequency)
     │
     ├─► librosa.power_to_db()
     │   └─► Convert power to decibel scale
     │
     ├─► Normalize to [0, 1]
     │
     └─► Output: 128x128 image (mel-frequency vs time)
```

### 3. CNN Architecture Details

```
Layer Type          Output Shape        Parameters    Activation
─────────────────────────────────────────────────────────────────
Input               (128, 128, 3)       0             -
─────────────────────────────────────────────────────────────────
Conv2D              (128, 128, 32)      896           ReLU
BatchNorm           (128, 128, 32)      128           -
Conv2D              (128, 128, 32)      9,248         ReLU
BatchNorm           (128, 128, 32)      128           -
MaxPooling2D        (64, 64, 32)        0             -
Dropout             (64, 64, 32)        0             -
─────────────────────────────────────────────────────────────────
Conv2D              (64, 64, 64)        18,496        ReLU
BatchNorm           (64, 64, 64)        256           -
Conv2D              (64, 64, 64)        36,928        ReLU
BatchNorm           (64, 64, 64)        256           -
MaxPooling2D        (32, 32, 64)        0             -
Dropout             (32, 32, 64)        0             -
─────────────────────────────────────────────────────────────────
Conv2D              (32, 32, 128)       73,856        ReLU
BatchNorm           (32, 32, 128)       512           -
Conv2D              (32, 32, 128)       147,584       ReLU
BatchNorm           (32, 32, 128)       512           -
MaxPooling2D        (16, 16, 128)       0             -
Dropout             (16, 16, 128)       0             -
─────────────────────────────────────────────────────────────────
Conv2D              (16, 16, 256)       295,168       ReLU
BatchNorm           (16, 16, 256)       1,024         -
Conv2D              (16, 16, 256)       590,080       ReLU
BatchNorm           (16, 16, 256)       1,024         -
MaxPooling2D        (8, 8, 256)         0             -
Dropout             (8, 8, 256)         0             -
─────────────────────────────────────────────────────────────────
Flatten             (16384)             0             -
─────────────────────────────────────────────────────────────────
Dense               (512)               8,389,120     ReLU
BatchNorm           (512)               2,048         -
Dropout             (512)               0             -
─────────────────────────────────────────────────────────────────
Dense               (256)               131,328       ReLU
BatchNorm           (256)               1,024         -
Dropout             (256)               0             -
─────────────────────────────────────────────────────────────────
Dense               (num_classes)       varies        Softmax
─────────────────────────────────────────────────────────────────
Total Parameters: ~9,700,000 (depends on num_classes)
Trainable Parameters: ~9,700,000
Non-trainable Parameters: 0
```

### 4. Training Process Flow

```
Epoch Loop (1 to 50)
     │
     ├─► For each batch (32 images):
     │   │
     │   ├─► Forward pass
     │   │   ├─► Input: batch of spectrograms
     │   │   ├─► CNN processing
     │   │   └─► Output: predictions
     │   │
     │   ├─► Calculate loss
     │   │   └─► Categorical cross-entropy
     │   │
     │   ├─► Backward pass
     │   │   ├─► Compute gradients
     │   │   └─► Update weights (Adam optimizer)
     │   │
     │   └─► Update metrics
     │       ├─► Training accuracy
     │       └─► Training loss
     │
     ├─► Validation phase
     │   ├─► Evaluate on validation set
     │   ├─► Calculate validation loss
     │   └─► Calculate validation accuracy
     │
     ├─► Callbacks
     │   ├─► Save model if val_acc improved
     │   ├─► Check early stopping condition
     │   └─► Reduce LR if plateau detected
     │
     └─► Next epoch or stop
```

### 5. Prediction Pipeline

```
New Audio File
     │
     ├─► Preprocess (same as training)
     │   ├─► Load audio
     │   ├─► Normalize duration
     │   └─► Generate spectrogram
     │
     ├─► Load trained model
     │   └─► Restore weights from .h5 file
     │
     ├─► Forward pass
     │   ├─► Input: single spectrogram
     │   ├─► CNN processing
     │   └─► Output: probability vector
     │
     ├─► Post-processing
     │   ├─► argmax(probabilities) → predicted class
     │   ├─► max(probabilities) → confidence
     │   └─► Map class index to animal name
     │
     └─► Display results
         ├─► Animal name
         ├─► Confidence %
         └─► All class probabilities
```

---

## 📐 Mathematical Operations

### Mel-Spectrogram Calculation

```
1. Short-Time Fourier Transform (STFT):
   X[m,k] = Σ x[n] * w[n-m] * e^(-j2πkn/N)
   where:
   - x[n] = audio signal
   - w[n] = window function
   - m = time frame
   - k = frequency bin

2. Power Spectrogram:
   P[m,k] = |X[m,k]|²

3. Mel Filterbank:
   M[i,k] = triangular filters on mel scale
   mel(f) = 2595 * log₁₀(1 + f/700)

4. Mel-Spectrogram:
   S[m,i] = Σ P[m,k] * M[i,k]

5. dB Conversion:
   S_dB[m,i] = 10 * log₁₀(S[m,i] / ref)
```

### CNN Convolution Operation

```
Output[i,j,k] = Σ Σ Σ Input[i+m, j+n, c] * Kernel[m,n,c,k] + Bias[k]
                m n c

where:
- (i,j) = spatial position
- k = output channel
- (m,n) = kernel position
- c = input channel
```

### Softmax Activation

```
P(class_i) = e^(z_i) / Σ e^(z_j)
             j

where:
- z_i = logit for class i
- P(class_i) = probability of class i
- Σ P(class_i) = 1 (probabilities sum to 1)
```

---

## 🎯 Data Flow Summary

```
Audio File → Preprocessing → Spectrogram → CNN → Prediction
   (.wav)      (librosa)      (128x128)    (TF)   (Animal)
     │              │              │          │        │
     └──────────────┴──────────────┴──────────┴────────┘
              All steps automated in pipeline
```

---

## 💾 Memory Requirements

### Training Phase
- **Spectrograms on disk**: ~5-10 MB per 100 images
- **Model in memory**: ~40 MB
- **Training batch**: ~50 MB (32 images)
- **Total RAM needed**: ~2-4 GB

### Inference Phase
- **Model in memory**: ~40 MB
- **Single image**: ~0.2 MB
- **Total RAM needed**: ~100 MB

---

## ⚡ Performance Characteristics

### Time Complexity
- **Spectrogram generation**: O(n log n) per audio file
- **CNN forward pass**: O(k × h × w × c) per image
- **Training epoch**: O(N × k × h × w × c) for N samples

### Space Complexity
- **Model parameters**: O(P) where P ≈ 2M parameters
- **Activation maps**: O(B × H × W × C) per batch
- **Gradients**: O(P) during training

---

This architecture provides a robust, scalable system for animal sound classification with clear separation of concerns and efficient data flow.
