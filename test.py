import os
import whisper
import numpy as np
from pydub import AudioSegment

def transcribe_audio_from_folder(filename):
    # Define the folder path and full audio file path
    folder_path = "audio"
    audio_path = os.path.join(folder_path, filename)

    # Check if the audio file exists
    if not os.path.isfile(audio_path):
        print(f"Audio file not found: {audio_path}")
        return

    # Load Whisper model
    model = whisper.load_model("base")

    # Load the audio file using pydub
    audio = AudioSegment.from_file(audio_path)
    audio_length = len(audio)  # Length in milliseconds

    # Function to convert pydub audio segment to numpy array
    def audio_segment_to_numpy(audio_segment):
        samples = np.array(audio_segment.get_array_of_samples())
        # Convert to float32
        return samples.astype(np.float32) / 32768.0

    # Function to process a chunk of audio
    def process_chunk(start_time, end_time):
        chunk = audio[start_time:end_time]
        chunk_np = audio_segment_to_numpy(chunk)
        chunk_np = whisper.pad_or_trim(chunk_np)
        mel = whisper.log_mel_spectrogram(chunk_np).to(model.device)
        _, probs = model.detect_language(mel)
        result = whisper.decode(model, mel, whisper.DecodingOptions())
        return result.text

    # Process the audio in 30-second chunks
    chunk_duration_ms = 30 * 1000  # 30 seconds in milliseconds
    transcriptions = []
    for start in range(0, audio_length, chunk_duration_ms):
        end = min(start + chunk_duration_ms, audio_length)
        print(f"Processing chunk: {start // 1000}s to {end // 1000}s")
        try:
            transcription = process_chunk(start, end)
            transcriptions.append(transcription)
        except Exception as e:
            print(f"An error occurred during processing chunk {start // 1000}s to {end // 1000}s: {e}")

    # Combine all transcriptions into a single result
    full_transcription = "\n".join(transcriptions)
    
    # Save the transcription to a text file
    output_text_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_transcription.txt")
    with open(output_text_path, "w") as text_file:
        text_file.write(full_transcription)
    
    print(f"Transcription saved to {output_text_path}")

if __name__ == "__main__":
    # Get the filename from the user
    filename = input("Enter the audio file name (including extension): ")
    transcribe_audio_from_folder(filename)
