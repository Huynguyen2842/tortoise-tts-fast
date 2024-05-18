# customize voice - python add_new_voice.py 



import librosa
import soundfile as sf
import os
import yt_dlp as youtube_dl
# Parameters
output_directory = "/home/ubuntu/capstone/tortoise-tts-fast/tortoise/voices/thoisuvoice"
clip_length = 10  # seconds for each clip
total_duration = 64  # total seconds to load from the audio file
sample_rate = 22050  # target sample rate

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',
        'noplaylist': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "downloaded_audio.wav"

def segment_audio(file_path, target_dir, total_duration, clip_length, sr):
    print("Loading audio...")
    # Load the specified duration of audio at the desired sample rate
    audio, _ = librosa.load(file_path, sr=sr, duration=total_duration)
    print("Audio loaded.")
    total_length = audio.shape[0] / sr
    print(f"Total audio length: {total_length}s")

    # Ensure the directory exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    print(f"Directory '{target_dir}' prepared.")

    # Calculate the number of full clips we can extract within the loaded audio
    num_segments = int(total_length // clip_length)
    print(f"Preparing to write {num_segments} segments.")

    for i in range(num_segments):
        start_sample = i * clip_length * sr
        end_sample = start_sample + clip_length * sr
        segment = audio[start_sample:end_sample]
        sf.write(f"{target_dir}/{i+1}.wav", segment, sr, format='WAV', subtype='FLOAT')
        print(f"Wrote segment {i+1} to {target_dir}.")

# Pre-downloaded audio file path
audio_file_path = "/home/ubuntu/capstone/tortoise-tts-fast/data_clone.wav"
# audio_file_path = download_audio("https://www.youtube.com/watch?v=rZnygcVV3vI&list=PL2HJubrp1ilgaJgML9KeC6KJtLdfaggpR")

print("Starting segmentation...")
segment_audio(audio_file_path, output_directory, total_duration, clip_length, sample_rate)
print("Segmentation completed. Audio clips have been saved to", output_directory)

# Optionally, clean up the original download
os.remove(audio_file_path)
print("Original audio file removed.")

# audio_file_path = download_audio("https://www.youtube.com/watch?v=9FXNn0p7L_I")
