# Imported a bunch of stuff even though this snake is not using AStar or random yet
from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

@app.route("/start", methods=["GET","HEAD","POST","PUT"])
def start():
	print(request.data)
	snake = {
		"color": "#f00001",
		"name": "InDevelopment"
	}
	return jsonify(snake)

@app.route("/move", methods=["GET","HEAD","POST","PUT"])
def move():
	
	dataStr = request.data
	global jsonData
	jsonData = json.loads(dataStr.decode('utf-8'))
	#print(jsonData)

	x = jsonData['you']['body'][0]['x']
	y = jsonData['you']['body'][0]['y']
	#print("head: ", "(", x, ",", y, ")")
	xlast = jsonData['you']['body'][1]['x']
	ylast = jsonData['you']['body'][1]['y']
	width = jsonData['board']["width"]
	height = jsonData['board']["height"]
	
	point = closestFood(jsonData)
	foodX0 = jsonData['board']['food'][point]['x']
	foodY0 = jsonData['board']['food'][point]['y']
	
	if not isSafe(foodX0, foodY0, jsonData) and futureVision(x, y, jsonData)>1:
		point = nextClosest(jsonData)
		foodX0 = jsonData['board']['food'][point]['x']
		foodY0 = jsonData['board']['food'][point]['y']
	
	#print("food: (", foodX0, ",", foodY0, ")")
	
	#Direction = toFood(foodX0, foodY0, x, y)
	
	#Direction = toFoodSmart(foodX0, foodY0, x, y, jsonData)
	
	global usedXY
	usedXY = []
	
	
	countRight = checkSpaces(x+1, y)
	usedXY = []
	countLeft = checkSpaces(x-1, y)
	usedXY = []
	countUp = checkSpaces(x, y-1)
	usedXY = []
	countDown = checkSpaces(x, y+1)
	
	print(countRight)
	print(countLeft)
	print(countUp)
	print(countDown)
	
	idealDirection = "right"
	
	if jsonData['you']['health']>50:
		idealDirection = attack(x, y)
		if idealDirection=="food":
			idealDirection = toFoodSmart(foodX0, foodY0, x, y, jsonData)
	else: idealDirection = toFoodSmart(foodX0, foodY0, x, y, jsonData)
	
	Direction = biggest(countRight, countLeft, countUp, countDown, idealDirection) 
    
	#Direction = dontDieNextTurn(jsonData, x, y, Direction)
    
	print(Direction)
	response = {
		"move": Direction
	}
	return jsonify(response)

def attack(x, y):
	target = closestSnake()
	if target==-1:
		return "food"
	
	tx = jsonData['board']['snakes'][target]['body'][0]['x']
	ty = jsonData['board']['snakes'][target]['body'][0]['y']
	
	if isSafe(tx+1, ty, jsonData):
		return toFoodSmart(tx+1, ty, x, y, jsonData)
	if isSafe(tx-1, ty, jsonData):
		return toFoodSmart(tx-1, ty, x, y, jsonData)
	if isSafe(tx, ty+1, jsonData):
		return toFoodSmart(tx, ty+1, x, y, jsonData)
	if isSafe(tx, ty-1, jsonData):
		return toFoodSmart(tx, ty-1, x, y, jsonData)
	
	return "food"

def checkSpaces(x, y):
	if not isSafe(x, y, jsonData):
		return 0
	for point in usedXY:
		if [x, y] == point:
			return 0
	usedXY.append([x, y])
	return 1 + checkSpaces(x, y+1) + checkSpaces(x, y-1) + checkSpaces(x-1, y) + checkSpaces(x+1, y)

def biggest(r, l, u, d, Direction):
	big = r
	if big<l:
		big = l
	if big<u:
		big = u
	if big<d:
		big = d
	
	count = 0
	if big==r:
		count = count+1
	if big==l:
		count = count+1
	if big==u:
		count = count+1
	if big==d:
		count = count+1
	
	print(count)
	
	if count==1:
		if big==r:
			return "right"
		if big==l:
			return "left"
		if big==u:
			return "up"
		if big==d:
			return "down"
	
	if count==2:
		if big==r and Direction=="right":
			return "right"
		if big==l and Direction=="left":
			return "left"
		if big==u and Direction=="up":
			return "up"
		if big==d and Direction=="down":
			return "down"
		if big==r:
			return "right"
		if big==l:
			return "left"
		if big==u:
			return "up"
		if big==d:
			return "down"
	
	return Direction

def isSafe(x, y, jsonData):
	width = jsonData['board']["width"]
	height = jsonData['board']["height"]
	
	if x == width:
		return False 
	if x == -1:
		return False 
	if y == height:
		return False 
	if y == -1:
		return False 
	for point in jsonData['you']['body']:
		if x == point['x'] and y == point['y']:
			return False
	for snake in jsonData['board']['snakes']:
		for point in snake['body']:
			if x == point['x'] and y == point['y']:
				return False
	for snake in range(0, len(jsonData['board']['snakes'])):
		if jsonData['board']['snakes'][snake]['id'] != jsonData['you']['id']:
			if (len(jsonData['board']['snakes'][snake]['body']) >= len(jsonData['you']['body'])):
				if x == jsonData['board']['snakes'][snake]['body'][0]['x']+1 and y == jsonData['board']['snakes'][snake]['body'][0]['y']:
					return False
				if x == jsonData['board']['snakes'][snake]['body'][0]['x']-1 and y == jsonData['board']['snakes'][snake]['body'][0]['y']:
					return False
				if x == jsonData['board']['snakes'][snake]['body'][0]['x'] and y == jsonData['board']['snakes'][snake]['body'][0]['y']+1:
					return False
				if x == jsonData['board']['snakes'][snake]['body'][0]['x'] and y == jsonData['board']['snakes'][snake]['body'][0]['y']-1:
					return False
	return True

def isSafeSimple(x, y, jsonData):
	width = jsonData['board']["width"]
	height = jsonData['board']["height"]
	
	if x == width:
		return False 
	if x == -1:
		return False 
	if y == height:
		return False 
	if y == -1:
		return False 
	for point in jsonData['you']['body']:
		if x == point['x'] and y == point['y']:
			return False
	for snake in jsonData['board']['snakes']:
		for point in snake['body']:
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
	width = jsonData['board']["width"]
	height = jsonData['board']["height"]
	default = width + height + 1
	youX = jsonData['you']['body'][0]['x']
	youY = jsonData['you']['body'][0]['y']
	
	for food in jsonData['board']['food']:
		count = count + 1
		pathX = abs(youX - food['x'])
		pathY = abs(youY - food['y'])
		pathTotal = pathX + pathY
		if pathTotal<default:
			default = pathTotal
			closest = count - 1
	return closest	

def closestSnake():
	count = 0
	closest = -1
	width = jsonData['board']["width"]
	height = jsonData['board']["height"]
	default = 5
	youX = jsonData['you']['body'][0]['x']
	youY = jsonData['you']['body'][0]['y']
	
	for snake in jsonData['board']['snakes']:
		count = count + 1
		pathX = abs(youX - snake['body'][0]['x'])
		pathY = abs(youY - snake['body'][0]['y'])
		pathTotal = pathX + pathY
		if pathTotal<default and (len(snake['body']) < int(len(jsonData['you']['body']))-1):
			default = pathTotal
			closest = count - 1
	return closest

def nextClosest(num):
	count = 0
	closest = 0
	width = jsonData['board']["width"]
	height = jsonData['board']["height"]
	default = width + height + 1
	youX = jsonData['you']['body'][0]['x']
	youY = jsonData['you']['body'][0]['y']
	
	for food in jsonData['board']['food']:
		count = count + 1
		pathX = abs(youX - food['x'])
		pathY = abs(youY - food['y'])
		pathTotal = pathX + pathY
		if pathTotal<default and not num==count-1:
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
		if not isSafeSimple(x+1, y, jsonData):
			Direction = "left"
	if Direction == "left":
		if not isSafeSimple(x-1, y, jsonData):
			Direction = "down"
	if Direction == "down":
		if not isSafeSimple(x, y+1, jsonData):
			Direction = "up"
	if Direction == "up":
		if not isSafeSimple(x, y-1, jsonData):
			Direction = "right"
	if Direction == "right":
		if not isSafeSimple(x+1, y, jsonData):
			Direction = "left"
	if Direction == "left":
		if not isSafeSimple(x-1, y, jsonData):
			Direction = "down"
	if Direction == "down":
		if not isSafeSimple(x, y+1, jsonData):
			Direction = "up"
	if Direction == "up":
		if not isSafeSimple(x, y-1, jsonData):
			Direction = "right"

	return Direction

if __name__ == "__main__":
	# Don't forget to change the IP address before you try to run it locally
	app.run(host='192.168.97.167', port=8082, debug=True)
