// ========== DOM ELEMENTS ==========
const uploadArea = document.getElementById('uploadArea');
const audioFileInput = document.getElementById('audioFile');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFile');
const predictBtn = document.getElementById('predictBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const predictedAnimal = document.getElementById('predictedAnimal');
const confidenceValue = document.getElementById('confidenceValue');
const confidenceFill = document.getElementById('confidenceFill');
const probabilitiesList = document.getElementById('probabilitiesList');
const newPredictionBtn = document.getElementById('newPredictionBtn');
const retryBtn = document.getElementById('retryBtn');

// ========== STATE ==========
let selectedFile = null;

// ========== UTILITY FUNCTIONS ==========
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function getConfidenceClass(confidence) {
    if (confidence >= 70) return 'high';
    if (confidence >= 40) return 'medium';
    return 'low';
}

// ========== FILE UPLOAD HANDLERS ==========
uploadArea.addEventListener('click', () => {
    audioFileInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

audioFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    // Validate file type
    const allowedTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/flac', 'audio/ogg', 'audio/x-m4a'];
    const allowedExtensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a'];
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
        showError('Invalid file type. Please upload an audio file (MP3, WAV, FLAC, OGG, M4A).');
        return;
    }
    
    selectedFile = file;
    
    // Update UI
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    uploadArea.style.display = 'none';
    fileInfo.style.display = 'block';
    predictBtn.disabled = false;
    
    // Hide previous results/errors
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    resetUpload();
});

function resetUpload() {
    selectedFile = null;
    audioFileInput.value = '';
    uploadArea.style.display = 'block';
    fileInfo.style.display = 'none';
    predictBtn.disabled = true;
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// ========== PREDICTION ==========
predictBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    // Show loading
    predictBtn.style.display = 'none';
    loading.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Create form data
    const formData = new FormData();
    formData.append('audio', selectedFile);
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Prediction failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        loading.style.display = 'none';
        predictBtn.style.display = 'flex';
    }
});

function displayResults(data) {
    // Update main result
    predictedAnimal.textContent = data.predicted_animal;
    confidenceValue.textContent = data.confidence.toFixed(2) + '%';
    confidenceFill.style.width = data.confidence + '%';
    
    // Update all probabilities
    probabilitiesList.innerHTML = '';
    
    Object.entries(data.all_probabilities).forEach(([animal, probability], index) => {
        const item = document.createElement('div');
        item.className = 'probability-item';
        item.style.animationDelay = `${index * 0.05}s`;
        
        item.innerHTML = `
            <span class="prob-label">${animal}</span>
            <div class="prob-bar-container">
                <div class="prob-bar-fill" style="width: ${probability}%">
                    <span class="prob-value">${probability.toFixed(1)}%</span>
                </div>
            </div>
        `;
        
        probabilitiesList.appendChild(item);
    });
    
    // Show results
    resultsSection.style.display = 'block';
    
    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    // Scroll to error
    setTimeout(() => {
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// ========== NEW PREDICTION / RETRY ==========
newPredictionBtn.addEventListener('click', () => {
    resetUpload();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

retryBtn.addEventListener('click', () => {
    errorSection.style.display = 'none';
    if (selectedFile) {
        predictBtn.click();
    } else {
        resetUpload();
    }
});

// ========== INITIALIZATION ==========
console.log('🐾 Animal Voice Detection - Ready!');
