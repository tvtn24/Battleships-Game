import random
from components import initialise_board, create_battleships, place_battleships
from game_engine import attack, cli_coordinates_input, is_all_ships_sunk


players = {}

#list to track attacked positions
attacked_pos = []

def generate_attack() -> tuple[int,int]:
    global attacked_pos
    while True:
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        coor = (row, col)
        
        #get a new attack position if the coordinate is already attacked
        if coor not in attacked_pos:
            #add the new attack position to the list
            attacked_pos.append(coor)
            return coor

def ai_opponent_game_loop():
    print('Welcome to the Battleship Game!')

    player_board = initialise_board()
    player_battleships = create_battleships()
    place_battleships(player_board,player_battleships, algorithm='custom')

    ai_board = initialise_board()
    ai_battleships = create_battleships()
    place_battleships(ai_board, ai_battleships, algorithm='random')

    while not is_all_ships_sunk(ai_battleships): 
        #player's turn 
        print('\nPlayer\'s Turn:')
        player_coordinates = cli_coordinates_input()

        #process player's attack on AI board
        hit = attack(player_coordinates, ai_board, ai_battleships)
        if hit:
            print('It\'s a Hit!')
        else:
            print('It\'s a Miss!')

        #check if AI battleships are all sunk
        if is_all_ships_sunk(ai_battleships):
            print('\nGame Over! You have sunk all their ship!')
            break

        #AI turn
        print('\n Opponent\'s Turn:')
        ai_coordinates = generate_attack()
        print(f' Opponent attacks at coordinates: {ai_coordinates}')

        #process AI attack on player's board 
        hit = attack(ai_coordinates, player_board, player_battleships)
        if hit:
            print('Your ship got Hit!')
        else:
            print('The Opponent misses!')

        #show player's board after AI turn
        print('\nYour Board after Opponent\'s turn:')
        for row in player_board:
            print(' '.join(str(cell) if cell else '-' for cell in row))

        #check if player's battleships are all sunk
        if  is_all_ships_sunk(player_battleships):
            print('\nGame Over! All your ships have been sunk!')
            break

if __name__ == '__main__':
    ai_opponent_game_loop()