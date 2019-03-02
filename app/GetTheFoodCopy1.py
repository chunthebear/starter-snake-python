# Imported a bunch of stuff even though this snake is not using AStar or random yet
from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

@app.route("/start", methods=["GET","HEAD","POST","PUT"])
def start():
    print(request.data)
    snake = {
        "color": "#dc3527",
        "name": "GetTheFood"
    }
    return jsonify(snake)

@app.route("/move", methods=["GET","HEAD","POST","PUT"])
def move():
    dataStr = request.data
    jsonData = json.loads(dataStr.decode('utf-8'))
    
    print(jsonData)

    x = jsonData['you']['body']['data'][0]['x']
    y = jsonData['you']['body']['data'][0]['y']
    print("x: ", x)
    print("y: ", y)
    xlast = jsonData['you']['body']['data'][1]['x']
    ylast = jsonData['you']['body']['data'][1]['y']
    width = jsonData["width"]
    height = jsonData["height"]
    print("width: ", width)
    print("height: ", height)
    foodX0 = jsonData['food']['data'][0]['x']
    foodY0 = jsonData['food']['data'][0]['y']
    print("food: (", foodX0, ",", foodY0, ")")
    
    Direction = toFood(foodX0, foodY0, x, y)
    
    if Direction == "right":
    	if not isSafe(x+1, y, width, height, jsonData):
    		Direction = "left"
    if Direction == "left":
    	if not isSafe(x-1, y, width, height, jsonData):
    		Direction = "down"
    if Direction == "down":
    	if not isSafe(x, y+1, width, height, jsonData):
    		Direction = "up"
    if Direction == "up":
    	if not isSafe(x, y-1, width, height, jsonData):
    		Direction = "right"
    if Direction == "right":
    	if not isSafe(x+1, y, width, height, jsonData):
    		Direction = "left"
    if Direction == "left":
    	if not isSafe(x-1, y, width, height, jsonData):
    		Direction = "down"
    if Direction == "down":
    	if not isSafe(x, y+1, width, height, jsonData):
    		Direction = "up"
    if Direction == "up":
    	if not isSafe(x, y-1, width, height, jsonData):
    		Direction = "right"
    
    response = {
        "move": Direction
    }
    return jsonify(response)


def isSafe(x, y, maxX, maxY, jsonData):
	if x == maxX:
		return False 
	if x == -1:
		return False 
	if y == maxY:
		return False 
	if y == -1:
		return False 
	for point in jsonData['you']['body']['data']:
		if x == point['x'] and y == point['y']:
			return False
	for snake in jsonData['snakes']['data']:
		for point in snake['body']['data']:
			if x == point['x'] and y == point['y']:
				return False
	return True

def lastMove(headX, headY, lastX, lastY):
	if headX > lastX:
		return "right"
	if headX < lastX:
		return "left"
	if headY > lastY:
		return "down"
	if headY < lastY:
		return "up"
	return "right"

def toFood(fx, fy, sx, sy):
	if fx > sx:
		return "right"
	if fx < sx:
		return "left"
	if fy > sy:
		return "down"
	if fy < sy:
		return "up"
	return "right"
   
if __name__ == "__main__":
    # Don't forget to change the IP address before you try to run it locally
    app.run(host='192.168.7.39', port=8087, debug=True)
    