import os
import re
from flask import Blueprint,request, jsonify
from functions.generateTimeStamps import TimeStamp
from functions.generateSummery import generateSummery


api_getVideo = Blueprint('api_getVideo', __name__)

@api_getVideo.route('/api/getVideo', methods=['POST'])
def post_data():
    #data = request.get_json() # get the JSON data from the request
    # process the data here (e.g. save it to a database)

      # Get the uploaded video file
    video_file = request.files['video']

    # Save the video file to disk
    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)

    
    #videoPath = data['videopath']
    deleteData()
    responses = TimeStamp.generateTimeStamp(video_path)

    unique_topics = []
    unique_objects = []

    for obj in responses:
        topic = obj['topic']
        if topic not in unique_topics:
            unique_topics.append(topic)
            unique_objects.append(obj)

    summeries = generateSummery(video_path,len(unique_objects))
    #AudioExtract.extract_audio(videoPath)
    unique_objects.insert(0,{"topic":"Introduction","timestamp":"00:00:00" , "image":" " , "summary":" " , "timeInSeconds":0})
    for index,obj in enumerate(unique_objects):
        time_string = obj['timestamp']
        hours, minutes, seconds = map(int, time_string.split(":"))
        total_seconds = (hours * 60 + minutes) * 60 + seconds
        if index < len(unique_objects)-1:
            obj['summary']  = re.sub(r'<.*?>', '', summeries[index])
        obj['timeInSeconds'] = total_seconds
    
    return jsonify({"data" : unique_objects })

def deleteData() :
    folder_path = "data"

    # iterate over all files and folders in the folder
    for filename in os.listdir(folder_path):

        # create the full path of the file or folder
        file_path = os.path.join(folder_path, filename)

        # if the item is a file, delete it
        if os.path.isfile(file_path):
            os.remove(file_path)

        # if the item is a folder, delete its contents recursively
        elif os.path.isdir(file_path):
            for sub_filename in os.listdir(file_path):
                sub_file_path = os.path.join(file_path, sub_filename)
                os.remove(sub_file_path)

            os.rmdir(file_path)