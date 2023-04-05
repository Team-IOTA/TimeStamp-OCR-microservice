from transformers import T5Tokenizer, T5ForConditionalGeneration
import subprocess
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from transformers import pipeline
import moviepy.editor
from tkinter.filedialog import *
import nltk
# Load the saved T5 model

model_path = r"C:\Users\Ridma Premaratne\Desktop\SDGP\my_t5_model"
model = T5ForConditionalGeneration.from_pretrained(model_path)
tokenizer = T5Tokenizer.from_pretrained('t5-small')

def generateSummery(video_path,num) :
    nltk.download('punkt')
    # Extracting audio out of video
    video = video_path
    video = moviepy.editor.VideoFileClip(video)

    audio = video.audio

    audio.write_audiofile("audio.wav")
    print("Completed")

    # Using API keys
    apikey = 'O_Z3Ib3vGgzGFvwV_l4ztFjptvN5nLnb3JaDuD7lajho'
    url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/ce01a695-b6c4-4bef-ac76-8a252c64057a'

    # Setup Speech to text service
    authenticator = IAMAuthenticator(apikey)
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(url)

    # Extracting text out of audio
    with open('audio.wav', 'rb') as f:
        res = stt.recognize(audio=f, content_type='audio/wav', model='en-AU_NarrowbandModel').get_result()

    text = [result['alternatives'][0]['transcript'].rstrip() + '.\n' for result in res['results']]

    # Formatting text and output to a text file
    text = [para[0].title() + para[1:] for para in text]
    transcript = ''.join(text)
    with open('lecture_transcript.txt', 'w') as out:
        out.writelines(transcript)

    

  
    # Split the transcript into sentences using NLTK
    sentences = nltk.sent_tokenize(transcript)

    # Split the sentences into n segments of roughly equal length
    n = num
    segment_size = len(sentences) // n
    segments = []
    start = 0
    for i in range(n):
        end = start + segment_size
        if i == n - 1:
            end = len(sentences)
        segments.append(' '.join(sentences[start:end]))
        start = end

   

    # Generate summaries for each segment
    summaries = []
    for segment in segments:
        doc = ''.join(segment)
        summary = predict_summary(doc)
        summaries.append(summary)

    # Print the summaries
    for i, summary in enumerate(summaries):
        print(f'Summary {i+1}: {summary}')

    return summaries

   

def predict_summary(document):
        device = model.device
        tokenized = tokenizer([document], truncation=True, padding='longest', return_tensors='pt')
        tokenized = {k: v.to(device) for k, v in tokenized.items()}
        tokenized_result = model.generate(**tokenized, max_length=128)
        tokenized_result = tokenized_result.to('cpu')
        predicted_summary = tokenizer.decode(tokenized_result[0])
        return predicted_summary