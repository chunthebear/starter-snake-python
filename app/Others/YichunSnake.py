from flask import Flask, request, jsonify
#import bottle
import os
import random


app = Flask(__name__)

def snakeMove(data, move):
    myCoor = data['you']['body']['data']
    myLen = data['you']['length']

    if (move == 'up'):
        nextMove = [myCoor[0]['x'], myCoor[0]['y'] + 1]
    elif (move == 'down'):
        nextMove = [myCoor[0]['x'], myCoor[0]['y'] - 1]
    elif (move == 'left'):
        nextMove = [myCoor[0]['x'] - 1, myCoor[0]['y']]
    else:
        nextMove = [myCoor[0]['x'] + 1, myCoor[0]['y']]

    #snake won't run into itself
    for i in range(1, myLen):
        if (nextMove[0] == myCoor[i]['x'] and nextMove[1] == myCoor[i]['y']):
            return False

    #snake won't run into walls
    if ((nextMove[0] == data['width']) or (nextMove[0] == -1) or (nextMove[1] == data['height']) or (nextMove[1] == -1)):
        return False

    #snake won't run into other snakes
    for i in range(len(data['snakes']['data'])):
        for j in range(len(data['snakes']['data'][i]['body']['data'])):
            enemyX = data['snakes']['data'][i]['body']['data'][j]['x']
            enemyY = data['snakes']['data'][i]['body']['data'][j]['y']
            if (nextMove[0] == enemyX and nextMove[1] == enemyY):
                return False

    return True


'''
@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')
'''

@app.route("/start", methods=["GET","HEAD","POST","PUT"])
def start():
	print(request.data)
	snake = {
		"color": "#ccff00",
		"name": "Yichun"
	}
	return jsonify(snake)


@app.route("/move", methods=["GET","HEAD","POST","PUT"])
def move():
    global goX, goY, myX, myY

    data = request.json


    #x and y coordinates of snake's head
    myX = data['you']['body']['data'][0]['x']
    myY = data['you']['body']['data'][0]['y']

    #set go to location to closest food

    
    #health = data['you']['health']
    #if (health > 0):
    closestDist = 1000
        
    for i in range(len(data['food']['data'])):
        foodX = data['food']['data'][i]['x']
        foodY = data['food']['data'][i]['y']
        distX = abs(myX - foodX)
        distY = abs(myY - foodY)
        dist = distX + distY

        if (dist < closestDist):
            closestDist = dist
            goX = foodX
            goY = foodY

    #else:
    #    myLen = data['you']['length']
    #    
    #    goX = [myCoor[myLen]['x'] - 2]
    #    goY = [myCoor[myLen]['y'] - 2]


    moveX = myX - goX
    moveY = goY - myY
    
    #call def snakeMove to check if it is safe to move
    if (moveY > 0 and snakeMove(data, 'up')):
        return {'move': 'down'}
    elif (moveY < 0 and snakeMove(data, 'down')):
        return {'move': 'up'}
    elif (moveX > 0 and snakeMove(data, 'left')):
        return {'move': 'left'}
    elif (moveX < 0 and snakeMove(data, 'right')):
        return {'move': 'right'}
    elif (snakeMove(data, 'up')):
        return {'move': 'down'}
    elif (snakeMove(data, 'down')):
        return {'move': 'up'}
    elif (snakeMove(data, 'left')):
        return {'move': 'left'}
    else:
        return {'move': 'right'}




if __name__ == "__main__":
    # Don't forget to change the IP address before you try to run it locally
    app.run(host='192.168.7.39', port=8086, debug=False)