import os
from flask import Blueprint,request, jsonify
from functions.generateTimeStamps import TimeStamp
from functions.generateSummery import generateSummery
from functions.extractAudiio import AudioExtract

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
    responses = TimeStamp.generateTimeStamp(video_path)
    summeries = generateSummery(video_path,len(responses))
    #AudioExtract.extract_audio(videoPath)
    
    return jsonify({"responses" : responses , "Summeries" : summeries})