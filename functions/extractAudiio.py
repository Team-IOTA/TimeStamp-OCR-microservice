import moviepy.editor as mp
import speech_recognition as sr


class AudioExtract:

    def extract_audio(filepath):

        # Load the video file
        video_path = filepath
        video = mp.VideoFileClip(video_path)

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

        # Print the transcript
        return transcript
        
  