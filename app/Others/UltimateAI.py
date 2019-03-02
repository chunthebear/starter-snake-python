from AStar import *
from flask import Flask, request, jsonify
import json
import random
import time

app = Flask(__name__)

SNEK_BUFFER = 3
ID = 'de508402-17c8-4ac7-ab0b-f96cb53fbee8'
SNAKE = 1
WALL = 2
FOOD = 3
GOLD = 4
KILLZONE = 5

def isValidPoint(x, y, width, height):
    if x < 0 or x > (width - 1):
        return False
    elif y < 0 or y > (height - 1):
        return False
    else:
        return True

def DeadEnd(Hedx, Hedy, x, y, grid, width, height):
    DangerMarker = 0

    #Need to return false if the point is next to the head
    if x == Hedx+1 or x == Hedx-1 or y == Hedy+1 or y == Hedy-1:
        return False

    if not isValidPoint(x+1,y,width,height) or grid[x+1][y] == SNAKE:
        DangerMarker = DangerMarker + 1
    if not isValidPoint(x-1,y,width,height) or grid[x-1][y] == SNAKE:
        DangerMarker = DangerMarker + 1
    if not isValidPoint(x,y+1,width,height) or grid[x][y+1] == SNAKE:
        DangerMarker = DangerMarker + 1
    if not isValidPoint(x,y-1,width,height) or grid[x][y-1] == SNAKE:
        DangerMarker = DangerMarker + 1
    if DangerMarker >= 3:
        return True
    return False

def DeadlyFood(x, y, grid, width, height):
    DangerMarker = 0
    if not isValidPoint(x+1,y,width,height) or grid[x+1][y] == SNAKE:
        DangerMarker = DangerMarker + 1
    if not isValidPoint(x-1,y,width,height) or grid[x-1][y] == SNAKE:
        DangerMarker = DangerMarker + 1
    if not isValidPoint(x,y+1,width,height) or grid[x][y+1] == SNAKE:
        DangerMarker = DangerMarker + 1
    if not isValidPoint(x,y-1,width,height) or grid[x][y-1] == SNAKE:
        DangerMarker = DangerMarker + 1
    if DangerMarker >= 2:
        return True
    return False



def init(data):
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
    mysnake = data['you']
    #we want to know length in order to judge whether going near other snakes is safe
    myLength = len(data["you"]["body"]["data"])
    myID = data["you"]["id"]


    #The following loop marks food in grid
    for f in data['food']['data']:
        if f['x'] > 0 and f['y'] > 0 and f['x'] < data['width']-1 and f['y'] < data['height']-1:
            grid[f['x']][f['y']] = FOOD


    #The following loop marks the squares around longer snake's heads as dangerous.
    for snek in data['snakes']['data']:
        EnemyLength = len(snek["body"]["data"])

        if EnemyLength >= myLength:
            #We have a threat!
            EvilHeadX = snek['body']['data'][0]['x']
            EvilHeadY = snek['body']['data'][0]['y']

            #Mark all possible moves of the enemy snake as dangerous
            if snek["id"] == myID:
                continue

            if isValidPoint(EvilHeadX - 1, EvilHeadY, data['width'], data['height']):
                grid[EvilHeadX - 1][EvilHeadY] = SNAKE
            if isValidPoint(EvilHeadX + 1, EvilHeadY, data['width'], data['height']):
                grid[EvilHeadX + 1][EvilHeadY] = SNAKE
            if isValidPoint(EvilHeadX, EvilHeadY - 1, data['width'], data['height']):
                grid[EvilHeadX][EvilHeadY - 1] = SNAKE
            if isValidPoint(EvilHeadX, EvilHeadY + 1, data['width'], data['height']):
                grid[EvilHeadX][EvilHeadY + 1] = SNAKE

        if EnemyLength < myLength:
            #We have a target :)
            EvilHeadX = snek['body']['data'][0]['x']
            EvilHeadY = snek['body']['data'][0]['y']
            if isValidPoint(EvilHeadX - 1, EvilHeadY, data['width'], data['height']):
                grid[EvilHeadX - 1][EvilHeadY] = FOOD
            if isValidPoint(EvilHeadX + 1, EvilHeadY, data['width'], data['height']):
                grid[EvilHeadX + 1][EvilHeadY] = FOOD
            if isValidPoint(EvilHeadX, EvilHeadY - 1, data['width'], data['height']):
                grid[EvilHeadX][EvilHeadY - 1] = FOOD
            if isValidPoint(EvilHeadX, EvilHeadY + 1, data['width'], data['height']):
                grid[EvilHeadX][EvilHeadY + 1] = FOOD

    #The following loop marks other snakes as dangerous

    for snek in data['snakes']['data']:
        points = snek["body"]["data"]
        for pnt in points :
            grid[pnt["x"]][pnt["y"]] = SNAKE


#        print "Is he gonna eat?"
#        EvilTailX = snek['body']['data'][-1]['x']
#        EvilTailY = snek['body']['data'][-1]['y']
#        print("Tail ", EvilTailX, EvilTailY)
#        if NotGonnaEat(points[0]["x"], points[0]["y"], grid, data['width'], data['height']):
#            print "Not gonna eat"
#            grid[points[-1]["x"]][points[-1]["y"]] = 0

    """
    for k in range (0, myLength):
        for i in range (0, data['width']):
            for j in range (0, data['height']):
                if DeadEnd (i, j, grid, data['width'], data['height']):
                    grid[i][j] = 1
    """
    return mysnake, grid

    #don't go into corners!

    #Take tails off of grid unless head is next to food*****Danger, this does not account for food yet!!!!
    #Dangerous tails: only if you are one move away.

    #don't trap self in corner just to get a food!! (if food is surrounded stay away)********
    #Aim for tails
    #Don't go for food if other snakes are closer
    #Mark edges of grid as dangerous

def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]

    if dx == 1:
        return 'right'
    elif dx == -1:
        return 'left'
    elif dy == -1:
        return 'up'
    elif dy == 1:
        return 'down'

@app.route("/start", methods=["GET","HEAD","POST","PUT"])
def start():

    snake = {
        "color": "#FF0000",
        "name": "SlipperyFrogSnake",
        "head_type": "tongue"
    }

    return jsonify(snake)

@app.route("/move", methods=["GET","HEAD","POST","PUT"])
def move():
    startTime = time.time()
    dataStr = str(request.data)
    jsonData = json.loads(dataStr)
    snek,grid = init(jsonData)
    HeadX = snek['body']['data'][0]['x']
    HeadY = snek['body']['data'][0]['y']
    width = jsonData["width"]
    height = jsonData["height"]
    myLength = len(jsonData["you"]["body"]["data"])
    Direction = "up"

    #Print the co-ords of the head of the snake


    #If not on the edge, mark edge traps as dangerous
    if (HeadX > 0 and HeadY > 0 and HeadX < width-1 and HeadY < height-1):
        for k in range (0, 2):
            for i in range (0, width):
                for j in range (0, height):
                    if DeadEnd (HeadX, HeadY, i, j, grid, width, height):
                        grid[i][j] = 1
    ###

    start = [HeadX,HeadY]
    goal = [width / 2, height /2]

    shortestPath = None
    for fud in jsonData['food']['data']:
        if DeadlyFood(fud['x'], fud['y'], grid, width, height):
            continue
        if fud['x'] > 0 and fud['y'] > 0 and fud['x'] < width-1 and fud['y'] < height-1:
            goal = [fud['x'],fud['y']]
            path = a_star(start, goal, grid, snek["body"]["data"])
            if shortestPath == None:
                shortestPath = path
            if (path != None) and (shortestPath != None):
                if len(path) < len(shortestPath):
                    shortestPath = path


    #if len(jsonData['food']['data']) > 0:
    #    goal = [jsonData['food']['data'][0]['x'],jsonData['food']['data'][0]['y']]
    #find the path from 'start' to 'goal'
    #path = a_star(start, goal, grid, snek["body"]["data"])

    if HeadX == 0 or HeadY == 0 or HeadX == width-1 or HeadY == height-1:
        goal = [width / 2, height /2]
        shortestPath = a_star(start, goal, grid, snek["body"]["data"])

    if shortestPath:
        Direction = direction(shortestPath[0], shortestPath[1])
    else:
        #crap! no path, what to do?! choose a safe emergency move
        Direction = FindSafeMoveDirection(HeadX,HeadY,grid,width,height)


    moves = ["up", "down", "left", "right"]
    response = {
        "move": Direction
    }


    endTime = time.time()
    timeDelta = (endTime-startTime) * 1000000
    print timeDelta
    return jsonify(response)

def FindSafeMoveDirection(HeadX, HeadY, grid, width, height):
    Direction = "up";
    if IsSafe(HeadX - 1, HeadY, grid, width, height):
        Direction = "left"
    if IsSafe(HeadX + 1, HeadY, grid, width, height):
        Direction = "right"
    if IsSafe(HeadX, HeadY - 1, grid, width, height):
        Direction = "up"
    if IsSafe(HeadX, HeadY + 1, grid, width, height):
        Direction = "down"
    return Direction

def IsSafe(x, y, grid, width, height):
    if x < 0:
        return False
    if x >= width:
        return False
    if y < 0:
        return False
    if y >= height:
        return False
    if grid[x][y] == 0:
        return True
    elif grid[x][y] == 3:
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(host='192.168.1.64', port=8088, debug=True)
