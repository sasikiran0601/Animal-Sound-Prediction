"""
Complete Animal Sound Classification Pipeline
Runs all steps: Generate Spectrograms → Train Model → Test Prediction
"""

import subprocess
import sys
from pathlib import Path
import time

PROJECT_PATH = Path(__file__).parent

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print_header(description)
    script_path = PROJECT_PATH / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_PATH,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Error running {script_name}: {e}")
        return False

def main():
    print_header("🐾 ANIMAL SOUND CLASSIFICATION - COMPLETE PIPELINE")
    
    print("This script will:")
    print("  1. Generate spectrograms from audio files")
    print("  2. Train a CNN model on the spectrograms")
    print("  3. Test the model with a sample prediction")
    print("\nThis may take 30-60 minutes depending on your hardware.")
    
    response = input("\nDo you want to continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Pipeline cancelled.")
        return
    
    start_time = time.time()
    
    # Step 1: Generate Spectrograms
    success = run_script(
        "1_generate_spectrograms.py",
        "STEP 1/3: GENERATING SPECTROGRAMS"
    )
    if not success:
        print("\n❌ Pipeline stopped due to error in Step 1")
        return
    
    # Step 2: Train Model
    success = run_script(
        "2_train_model.py",
        "STEP 2/3: TRAINING CNN MODEL"
    )
    if not success:
        print("\n❌ Pipeline stopped due to error in Step 2")
        return
    
    # Step 3: Test Prediction (optional)
    print_header("STEP 3/3: TESTING PREDICTION")
    print("Model training complete!")
    print("\nTo test the model, run:")
    print("  python 3_predict.py path/to/audio.wav")
    
    # Calculate total time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    # Final summary
    print_header("🎉 PIPELINE COMPLETE!")
    print(f"Total time: {minutes} minutes {seconds} seconds")
    print("\n📁 Output files:")
    print(f"  • Spectrograms: {PROJECT_PATH / 'spectrograms_dataset'}")
    print(f"  • Trained model: {PROJECT_PATH / 'trained_model' / 'animal_sound_classifier.h5'}")
    print(f"  • Class labels: {PROJECT_PATH / 'trained_model' / 'class_labels.json'}")
    print(f"  • Training history: {PROJECT_PATH / 'trained_model' / 'training_history.png'}")
    
    print("\n🚀 Next steps:")
    print("  1. Test the model: python 3_predict.py your_audio.wav")
    print("  2. Check training history plot in trained_model/")
    print("  3. Experiment with different audio files!")
    
    print("\n✅ All done! Your animal sound classifier is ready to use.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
