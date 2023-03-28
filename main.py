from flask import Flask
from apis.api_getvideo import api_getVideo

app = Flask(__name__)

app.register_blueprint(api_getVideo)

if __name__ == '__main__':
    app.run(host = 'localhost', port = 8088,debug=True)