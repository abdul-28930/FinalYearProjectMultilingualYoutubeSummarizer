import os
from audioExtractor import download_youtube_audio
from transcriber import transcribe_audio

def main():
    # Step 1: Get YouTube URL and output filename from the user
    video_url = input("Enter the YouTube video URL: ")

    if not video_url:
        print("No URL provided. Exiting.")
        return

    output_filename = input("Enter the output filename for the audio (including .mp3 extension): ")

    # Step 2: Download the audio from YouTube
    print("Downloading audio...")
    audio_path = download_youtube_audio(video_url, output_filename)

    # Step 3: If the download was successful, transcribe the audio
    if audio_path:
        print("Starting transcription...")
        # Extract the filename from the path for transcription
        filename = os.path.basename(audio_path)
        transcribe_audio(filename)
    else:
        print("Audio download failed. Cannot proceed with transcription.")

if __name__ == "__main__":
    main()
