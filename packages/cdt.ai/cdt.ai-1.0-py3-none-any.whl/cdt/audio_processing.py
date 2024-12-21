import whisper
import librosa
import magic  # To detect MIME type
import os

# Load pre-trained Whisper model
whisper_model = whisper.load_model("base")

def get_mimetype(file_path):
    """
    Detects the MIME type of a file (e.g., audio file) using python-magic.
    """
    mime = magic.Magic(mime=True)
    mimetype = mime.from_file(file_path)
    return mimetype

def transcribe_audio(audio_path):
    """
    Transcribes audio using Whisper.
    """
    try:
        # Check MIME type of the input audio file
        mimetype = get_mimetype(audio_path)
        print(f"Detected MIME type: {mimetype}")

        # Ensure the file is a valid audio format
        if not mimetype.startswith('audio'):
            raise ValueError(f"Provided file is not an audio file. MIME type: {mimetype}")

        # Transcribe audio using Whisper
        result = whisper_model.transcribe(audio_path)
        return result['text']
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def extract_audio_features(audio_path):
    """
    Extracts audio features (MFCC) using Librosa.
    """
    try:
        # Check MIME type of the input audio file
        mimetype = get_mimetype(audio_path)
        print(f"Detected MIME type: {mimetype}")

        # Ensure the file is a valid audio format
        if not mimetype.startswith('audio'):
            raise ValueError(f"Provided file is not an audio file. MIME type: {mimetype}")

        # Extract features using Librosa (MFCC, etc.)
        y, sr = librosa.load(audio_path)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        return mfcc
    except Exception as e:
        return f"Error extracting audio features: {str(e)}"

def process_audio_file(audio_path):
    """
    Processes the audio file: transcribe and extract features.
    """
    mimetype = get_mimetype(audio_path)
    print(f"Detected MIME type: {mimetype}")

    # Transcribe the audio
    transcription = transcribe_audio(audio_path)

    # Extract features from the audio
    audio_features = extract_audio_features(audio_path)

    return {
        "mimetype": mimetype,
        "transcription": transcription,
        "audio_features": audio_features.shape if isinstance(audio_features, np.ndarray) else audio_features
    }

# Example usage
audio_path = "path_to_your_audio_file.wav"
result = process_audio_file(audio_path)
print(result)
