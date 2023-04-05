import moviepy.editor as mp
import speech_recognition as sr
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import sent_tokenize, word_tokenize


# Load the video file
video_path = r"C:\Users\Ridma Premaratne\Desktop\SDGP\timestampOCR\video\imaginecupvideo.mp4"
video = mp.VideoFileClip(video_path)

import requests

API_KEY = 'YOUR_API_KEY'
VIDEO_PATH = '/path/to/your/video.mp4'

url = 'https://api.assemblyai.com/v2/transcript'
headers = {
    'authorization': API_KEY,
}
files = {
    'audio': open(VIDEO_PATH, 'rb'),
}
response = requests.post(url, headers=headers, files=files)

response_data = response.json()
media_id = response_data['id']



# Extract audio from the video
audio = video.audio

# Convert audio to audio file format (WAV)
audio_file = 'audio.wav'
audio.write_audiofile(audio_file)

# Load the audio file
r = sr.Recognizer()
with sr.AudioFile(audio_file) as source:
    audio = r.record(source)

# Extract transcript from audio using SpeechRecognition
transcript = r.recognize_google(audio)

sentences = sent_tokenize(transcript)

formatted_transcript = ". ".join(sentences)

#

# Print the transcript
print(formatted_transcript)
        
  