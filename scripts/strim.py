import librosa
import numpy as np
import soundfile as sf

def trim_audio(audio, sr, hop_length=512, db_threshold=-0):
    # Compute RMS energy
    audio_rms = librosa.feature.rms(y=audio, frame_length=2048, hop_length=hop_length)[0]
    # Convert RMS energy to dB
    audio_db = librosa.power_to_db(audio_rms**2, ref=np.max)
    
    print("Minimum dB in audio:", np.min(audio_db))
    print("Maximum dB in audio:", np.max(audio_db))

    start_index, end_index = None, None
    for index, frame_db in enumerate(audio_db):
        if frame_db >= db_threshold:
            if start_index is None:
                start_index = index
            end_index = index  # Update end_index whenever valid frame is found
        elif start_index is not None:
            break  # Stop if we have found at least one valid start

    if start_index is None:
        return audio  # Return original if no segment is loud enough
    if end_index is None:
        end_index = len(audio_db) - 1  # Use last index if end isn't found

    # Calculating the actual sample indices for trimming
    sample_start = start_index * hop_length
    sample_end = end_index * hop_length
    return audio[sample_start:sample_end]

# Load the audio file
audio_path = 'results/random_combined.wav'
audio, sr = librosa.load(audio_path, sr=None)  # sr=None ensures original sample rate is used

# Apply the trimming function
trimmed_audio = trim_audio(audio, sr)

# Save the trimmed audio using soundfile
sf.write('results/trimmed_random_combined.wav', trimmed_audio, sr)
