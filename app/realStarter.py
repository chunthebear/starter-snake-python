# Imported a bunch of stuff even though this snake is not using AStar or random yet
from AStar import *
from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

@app.route("/start", methods=["GET","HEAD","POST","PUT"])
def start():
    print(request.data)
    snake = {
        "color": "#C0C0C0",
        "name": "BareBones"
    }
    return jsonify(snake)

@app.route("/move", methods=["GET","HEAD","POST","PUT"])
def move():
    dataStr = str(request.data)
    jsonData = json.loads(dataStr)
    
    Direction = "right"
    response = {
        "move": Direction
    }
    return jsonify(response)
    
if __name__ == "__main__":
    # Don't forget to change the IP address before you try to run it locally
    app.run(host='134.87.162.112', port=8085, debug=True)
    
