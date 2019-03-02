import bottle
import os
import random

from api import *


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    snake = {
        "color": "#FF0000",
            "name": "SlipperyFrogSnake",
            "head_type": "tongue"
        }
    
    return jsonify(snake)


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '10.0.1.25'),
        port=os.getenv('PORT', '8080'),
        debug=True)
