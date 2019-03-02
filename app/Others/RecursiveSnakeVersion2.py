# Imported a bunch of stuff even though this snake is not using AStar or random yet
from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

@app.route("/start", methods=["GET","HEAD","POST","PUT"])
def start():
	print(request.data)
	snake = {
		"color": "#ccff00",
		"name": "InDevelopment"
	}
	return jsonify(snake)

@app.route("/move", methods=["GET","HEAD","POST","PUT"])
def move():
	dataStr = request.data
	global jsonData
	jsonData = json.loads(dataStr.decode('utf-8'))
	#print(jsonData)

	x = jsonData['you']['body']['data'][0]['x']
	y = jsonData['you']['body']['data'][0]['y']
	#print("head: ", "(", x, ",", y, ")")
	xlast = jsonData['you']['body']['data'][1]['x']
	ylast = jsonData['you']['body']['data'][1]['y']
	width = jsonData["width"]
	height = jsonData["height"]
	point = closestFood(jsonData)
	foodX0 = jsonData['food']['data'][point]['x']
	foodY0 = jsonData['food']['data'][point]['y']
	#print("food: (", foodX0, ",", foodY0, ")")
	
	#Direction = toFood(foodX0, foodY0, x, y)
	
	Direction = toFoodSmart(foodX0, foodY0, x, y, jsonData)
	
	global usedXY
	usedXY = []
	
	if lastMove(x, y, xlast, ylast) == "up":
		for point in jsonData['you']['body']['data']:
			if (x == point['x'] and y-1 == point['y']) or y == 0 or ( (not x==0 or not x==width-1) and ((x-1 == point['x'] and y-1 == point['y']) or (x+1 == point['x'] and y-1 == point['y']))):
				countLeft = checkSpaces(x-1, y)
				countRight = checkSpaces(x+1, y)
				if countLeft>countRight:
					Direction = "left"
				elif countLeft<countRight: Direction = "right"
			elif ((x-1 == point['x'] and x==width-1) and y-1 == point['y']) or ((x==0 and x+1==point['x']) and y-1 == point['y']):
				Direction = "up"
	elif lastMove(x, y, xlast, ylast) == "down":
		for point in jsonData['you']['body']['data']:
			if (x == point['x'] and y+1 == point['y']) or y == height-1 or ( (not x==0 or not x==width-1) and((x-1 == point['x'] and y+1 == point['y']) or (x+1 == point['x'] and y+1 == point['y']))):
				countLeft = checkSpaces(x-1, y)
				countRight = checkSpaces(x+1, y)
				if countLeft>countRight:
					Direction = "left"
				elif countLeft<countRight: Direction = "right"
			elif ((x-1 == point['x'] and x==width-1) and y+1 == point['y']) or ((x==0 and x+1==point['x']) and y+1 == point['y']):
				Direction = "down"
	elif lastMove(x, y, xlast, ylast) == "left":
		for point in jsonData['you']['body']['data']:
			if (x-1 == point['x'] and y == point['y']) or x == 0 or ( (not y==0 or not y==height-1) and((x-1 == point['x'] and y+1 == point['y']) or (x-1 == point['x'] and y-1 == point['y']))):
				countUp = checkSpaces(x, y-1)
				countDown = checkSpaces(x, y+1)
				if countUp>countDown:
					Direction = "up"
				elif countUp<countDown: Direction = "down"
			elif ((x-1 == point['x'] and y==height-1) and y-1 == point['y']) or ((y==0 and x-1==point['x']) and y+1 == point['y']):
				Direction = "left"
	else: 
		for point in jsonData['you']['body']['data']:
			if (x+1 == point['x'] and y == point['y']) or x == width-1 or ( (not y==0 or not y==height-1) and((x+1 == point['x'] and y+1 == point['y']) or (x+1 == point['x'] and y-1 == point['y']))):
				countUp = checkSpaces(x, y-1)
				countDown = checkSpaces(x, y+1)
				if countUp>countDown:
					Direction = "up"
				elif countUp<countDown: Direction = "down"
			elif ((x+1 == point['x'] and y==height-1) and y-1 == point['y']) or ((y==0 and x+1==point['x']) and y+1 == point['y']):
				Direction = "right"
    
    
    
	#Direction = dontDieNextTurn(jsonData, x, y, Direction)
    
	print(Direction)
	response = {
		"move": Direction
	}
	return jsonify(response)


def checkSpaces(x, y):
	if not isSafe(x, y, jsonData):
		return 0
	for point in usedXY:
		if [x, y] == point:
			return 0
	usedXY.append([x, y])
	return 1 + checkSpaces(x, y+1) + checkSpaces(x, y-1) + checkSpaces(x-1, y) + checkSpaces(x+1, y)


	

def isSafe(x, y, jsonData):
	width = jsonData["width"]
	height = jsonData["height"]
	
	if x == width:
		return False 
	if x == -1:
		return False 
	if y == height:
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

def futureVision(x, y, jsonData):
	count = 0
	if isSafe(x+1, y, jsonData):
		count = count + 1
	if isSafe(x-1, y, jsonData):
		count = count + 1
	if isSafe(x, y+1, jsonData):
		count = count + 1
	if isSafe(x, y-1, jsonData):
		count = count + 1
	return count

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

def toFoodSmart(fx, fy, sx, sy, jsonData):
	if fx > sx and isSafe(sx+1, sy, jsonData) and futureVision(sx+1, sy, jsonData)>0:
		return "right"
	if fx < sx and isSafe(sx-1, sy, jsonData) and futureVision(sx-1, sy, jsonData)>0:
		return "left"
	if fy > sy and isSafe(sx, sy+1, jsonData) and futureVision(sx, sy+1, jsonData)>0:
		return "down"
	if fy < sy and isSafe(sx, sy-1, jsonData) and futureVision(sx, sy-1, jsonData)>0:
		return "up"
	return dontDieNextTurn(jsonData, sx, sy, "right")

def closestFood(jsonData):
	count = 0
	closest = 0
	width = jsonData["width"]
	height = jsonData["height"]
	default = width + height + 1
	youX = jsonData['you']['body']['data'][0]['x']
	youY = jsonData['you']['body']['data'][0]['y']
	
	for food in jsonData['food']['data']:
		count = count + 1
		pathX = abs(youX - food['x'])
   		pathY = abs(youY - food['y'])
   		pathTotal = pathX + pathY
   		if pathTotal<default:
   			default = pathTotal
   			closest = count - 1
   	
   	return closest		

def dontDieNextTurn(jsonData, x, y, Direction):		
	if Direction == "right":
		if not isSafe(x+1, y, jsonData) or futureVision(x+1, y, jsonData)<1:
			Direction = "left"
	if Direction == "left":
		if not isSafe(x-1, y, jsonData) or futureVision(x-1, y, jsonData)<1:
			Direction = "down"
	if Direction == "down":
		if not isSafe(x, y+1, jsonData) or futureVision(x, y+1, jsonData)<1:
			Direction = "up"
	if Direction == "up":
		if not isSafe(x, y-1, jsonData) or futureVision(x, y-1, jsonData)<1:
			Direction = "right"
	if Direction == "right":
		if not isSafe(x+1, y, jsonData) or futureVision(x+1, y, jsonData)<1:
			Direction = "left"
	if Direction == "left":
		if not isSafe(x-1, y, jsonData) or futureVision(x-1, y, jsonData)<1:
			Direction = "down"
	if Direction == "down":
		if not isSafe(x, y+1, jsonData) or futureVision(x, y+1, jsonData)<1:
			Direction = "up"
	if Direction == "up":
		if not isSafe(x, y-1, jsonData) or futureVision(x, y-1, jsonData)<1:
			Direction = "right"
    
	return dontDieThisTurn(jsonData, x, y, Direction)

def dontDieThisTurn(jsonData, x, y, Direction):
	if Direction == "right":
		if not isSafe(x+1, y, jsonData):
			Direction = "left"
	if Direction == "left":
		if not isSafe(x-1, y, jsonData):
			Direction = "down"
	if Direction == "down":
		if not isSafe(x, y+1, jsonData):
			Direction = "up"
	if Direction == "up":
		if not isSafe(x, y-1, jsonData):
			Direction = "right"
	if Direction == "right":
		if not isSafe(x+1, y, jsonData):
			Direction = "left"
	if Direction == "left":
		if not isSafe(x-1, y, jsonData):
			Direction = "down"
	if Direction == "down":
		if not isSafe(x, y+1, jsonData):
			Direction = "up"
	if Direction == "up":
		if not isSafe(x, y-1, jsonData):
			Direction = "right"
    
	return Direction
   
if __name__ == "__main__":
    # Don't forget to change the IP address before you try to run it locally
    app.run(host='192.168.7.39', port=8089, debug=True)
    