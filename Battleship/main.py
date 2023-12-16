import json
from flask import Flask, request, render_template, jsonify
import components
import game_engine
import mp_game_engine

app = Flask(__name__)

ai_board = []
ai_ships = {}
player_board = []
player_ships = {}

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    """
    Accept a post request contianing the player board in the form of config.json
    also accepts a get request which returns the placement.html template with a ship dictionary
    :return:
    """

    global player_board, player_ships, ai_board, ai_ships
    if request.method == 'GET':
        #initialise player and AI board and ships
        player_board = components.initialise_board()
        player_ships = components.create_battleships()
        ai_board = components.initialise_board()
        ai_ships = components.create_battleships()
        return render_template('placement.html', board_size= 10,ships=player_ships)
        
    if request.method == "POST":
        data =  request.get_json()
        if data:
            with open('placement.json', 'w') as f:
                f.write(json.dumps(data))

            #place ships on player and AI board
            components.place_battleships(player_board, player_ships, algorithm='custom')
            components.place_battleships(ai_board, ai_ships, algorithm='random')
    
            return jsonify({'message': 'Placement received'}), 200
        else:
            return jsonify({'message': 'No placement data received'}), 400

@app.route('/attack', methods = ['GET'])
def process_attack():
    """
    Accept get request contains two parameters x and y 
    if game finished respond with jsonify {hit: True/False, AI Turn: (x,y), finished:'SOME MESSAGE'}
    :return:
    """

    global player_board, player_ships, ai_board, ai_ships
    
    if request.method == 'GET':

        x = request.args.get('x')
        y = request.args.get('y')
        ai_turn = mp_game_engine.generate_attack()
        coordinates = [x, y]

        #process player and AI attack on each other board
        hit = game_engine.attack(coordinates, ai_board, ai_ships)
        ai_hit = game_engine.attack(ai_turn, player_board, player_ships)

        #track ship sunk for both player and AI
        player_game_finished = game_engine.is_all_ships_sunk(ai_ships)
        ai_game_finished = game_engine.is_all_ships_sunk(player_ships)

        if player_game_finished: 
            return jsonify({'hit': hit, 
                            'AI_Turn': (ai_turn[0], ai_turn[1]), 
                            'finished': "Game Over Player wins"})
        elif ai_game_finished: 
            return jsonify({'hit': ai_hit, 
                            'AI_Turn': (ai_turn[0], ai_turn[1]), 
                            'finished': "Game Over AI wins"})
        else: 
            return jsonify({'hit': hit,
                             'AI_Turn': (ai_turn[0], ai_turn[1])})

@app.route('/', methods=['GET'])
def root():
    """
    Renders the main interface.
    """

    global player_board
    return render_template('main.html', player_board=player_board)

if __name__ == '__main__':
    app.run(port = 5000)