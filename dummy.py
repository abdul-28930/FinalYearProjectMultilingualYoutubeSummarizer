# import re
# import os
# import yt_dlp as youtube_dl
# import whisper

# def is_valid_url(url):
#     # Simple regex to validate YouTube URL
#     youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
#     return youtube_regex.match(url)

# def download_youtube_audio(url, output_filename="output.mp3"):
#     try:
#         # Check if the "audio" folder exists; if not, create it
#         folder_path = "audio"
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)

#         # Set the full output path
#         output_path = os.path.join(folder_path, output_filename)
#         print(f"Output path: {output_path}")  # Debugging output

#         # Define options for yt-dlp
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'outtmpl': output_path,
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#         }

#         # Download the audio using yt-dlp
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])

#         # Check if the file exists after downloading
#         if os.path.isfile(output_path):
#             print(f"Audio successfully downloaded and saved to {output_path}")
#             return output_path
#         else:
#             print("Failed to find the downloaded audio file.")
#             return None
        
#     except youtube_dl.utils.DownloadError:
#         print("Failed to download the video. The URL might be invalid or the video is unavailable.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# def transcribe_audio(audio_path):
#     # Check if the audio file exists
#     if not os.path.isfile(audio_path):
#         print(f"Audio file not found: {audio_path}")
#         return

#     # Load Whisper model
#     model = whisper.load_model("base")

#     try:
#         # Load audio and pad/trim it
#         audio = whisper.load_audio(audio_path)
#         audio = whisper.pad_or_trim(audio)

#         # Make log-Mel spectrogram and move to the same device as the model
#         mel = whisper.log_mel_spectrogram(audio).to(model.device)

#         # Detect the spoken language
#         _, probs = model.detect_language(mel)
#         print(f"Detected language: {max(probs, key=probs.get)}")

#         # Decode the audio
#         options = whisper.DecodingOptions()
#         result = whisper.decode(model, mel, options)

#         # Print the recognized text
#         print("Transcription:")
#         print(result.text)

#     except Exception as e:
#         print(f"An error occurred during transcription: {e}")

# if __name__ == "__main__":
#     video_url = input("Enter the YouTube video URL: ")

#     if not is_valid_url(video_url):
#         print("Invalid YouTube URL. Please enter a valid URL.")
#     else:
#         output_filename = input("Enter the output filename (including .mp3 extension): ")
#         audio_path = download_youtube_audio(video_url, output_filename)
        
#         if audio_path:
#             transcribe_audio(audio_path)