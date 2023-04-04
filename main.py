from flask import Flask
from apis.api_getvideo import api_getVideo
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.register_blueprint(api_getVideo)

if __name__ == '__main__':
   
    app.run(host = 'localhost', port = 8088,debug=True)