from flask import Flask, jsonify
import quandl as q
from flask_cors import CORS

#Key to connect to the Quandl API
q.ApiConfig.api_key = "xaFxr9SP6Wd5sKFHdEax"

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World'


if __name__ == "__main__":
	app.run(debug=True, port=8080)