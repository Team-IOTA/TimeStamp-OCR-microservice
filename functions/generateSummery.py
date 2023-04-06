from transformers import T5Tokenizer, T5ForConditionalGeneration
import subprocess
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from transformers import pipeline
import moviepy.editor
from tkinter.filedialog import *
import requests
import time


import nltk
# Load the saved T5 model

model_path = r"C:\Users\Ridma Premaratne\Desktop\SDGP\my_t5_model"
model = T5ForConditionalGeneration.from_pretrained(model_path)
tokenizer = T5Tokenizer.from_pretrained('t5-small')

API_KEY_ASSEMBLYAI = "5741f5d475f7408392d2451df2cf67de"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

headers_auth_only = {'authorization': API_KEY_ASSEMBLYAI}

headers = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

CHUNK_SIZE = 5_242_880  # 5MB

def generateSummery(video_path,num) :
    nltk.download('punkt')
    # Extracting audio out of video
    
    video = video_path
    video = moviepy.editor.VideoFileClip(video)

    audio = video.audio

    audio.write_audiofile("audio.wav")
    print("Completed")

    # Using API keys
    #apikey = 'O_Z3Ib3vGgzGFvwV_l4ztFjptvN5nLnb3JaDuD7lajho'
    #url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/ce01a695-b6c4-4bef-ac76-8a252c64057a'

    # Setup Speech to text service
    #authenticator = IAMAuthenticator(apikey)
    #stt = SpeechToTextV1(authenticator=authenticator)
    #stt.set_service_url(url)

    # Extracting text out of audio
    #with open('audio.wav', 'rb') as f:
    #    res = stt.recognize(audio=f, content_type='audio/wav', model='en-US_NarrowbandModel').get_result()

    #text = [result['alternatives'][0]['transcript'].rstrip() + '.\n' for result in res['results']]

    # Formatting text and output to a text file
    #text = [para[0].title() + para[1:] for para in text]
    #transcript = ''.join(text)
    #with open('lecture_transcript.txt', 'w') as out:
    #    out.writelines(transcript)

    audio_url = upload(video_path)

    trans = save_transcript(audio_url)

  
    # Split the transcript into sentences using NLTK
    sentences = nltk.sent_tokenize(trans)

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
        tokenized_result = model.generate(**tokenized, max_length=100)
        tokenized_result = tokenized_result.to('cpu')
        predicted_summary = tokenizer.decode(tokenized_result[0])
        return predicted_summary

def upload(filename):
   
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers_auth_only, data=read_file(filename))
    return upload_response.json()['upload_url']


def transcribe(audio_url):
    transcript_request = {
        'audio_url': audio_url
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    return transcript_response.json()['id']

        
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(url):
    transcribe_id = transcribe(url)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
            
        print("waiting for 30 seconds")
        time.sleep(30)
        
        
def save_transcript(url):
    data, error = get_transcription_result_url(url)
    
    if data:
        #filename = title + '.txt'
        #with open(filename, 'w') as f:
        #    f.write(data['text'])
        #print('Transcript saved')
        return data['text']
    elif error:
        return "Error!!!", error
