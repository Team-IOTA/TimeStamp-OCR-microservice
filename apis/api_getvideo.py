from flask import Blueprint,request, jsonify
from functions.generateTimeStamps import TimeStamp
from functions.extractAudiio import AudioExtract

api_getVideo = Blueprint('api_getVideo', __name__)

@api_getVideo.route('/api/getVideo', methods=['POST'])

def post_data():
    data = request.get_json() # get the JSON data from the request
    # process the data here (e.g. save it to a database)

    videoPath = data['videopath']
    responses = TimeStamp.generateTimeStamp(videoPath)
    AudioExtract.extract_audio(videoPath)
   
    response = {'message': "Time stamp generated"}
    
    return jsonify( responses)