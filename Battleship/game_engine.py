from components import initialise_board, create_battleships, place_battleships

#perfrom attack on a coordinate on the board
def attack(coordinates: tuple, board: list, battleships: dict) -> bool:
    row = int(coordinates[0])
    col = int(coordinates[1])
    if board[row][col] in battleships:
        ship = board[row][col]
        battleships[ship] -= 1
        board[row][col] = None
        return True
    else:
        return False

#get attack coordinate from user input
def cli_coordinates_input() -> tuple:
    print('Coordinate format: (Row, Column), (0-9)')
    while True:
        try:
            user_input = input('Enter attack coordinate: ')
            coordinates = user_input.split(',')
            if len(coordinates) != 2:
                raise ValueError
            row = int(coordinates[0])
            col = int(coordinates[1])
    
            if not (0 <= row <= 9 and 0 <= col <= 9):
                raise ValueError
            
            return row, col
        
        except ValueError:
            print('Please enter a valid coordinate with format (Row, Column), (0-9).')

#check if all ship sunk
def is_all_ships_sunk(ships:dict) -> bool:
    for name in ships:
        if ships[name]>0:
            return False
    return True

def simple_game_loop():
    print('Welcome to the Battleship Game!')
    board = initialise_board()
    ships = create_battleships()
    place_battleships(board, ships, algorithm='random')

    while not is_all_ships_sunk(ships):        
        print('\nCurrent Board:')

        #show board in command-line interface
        for row in board:
            print(' '.join(str(cell) if cell else '-' for cell in row))
        print('\n')
                
         #get user input coordinate       
        coordinates = cli_coordinates_input()
        #attack on board
        hit = attack(coordinates, board, ships)
        if hit:
            print('It\'s a Hit!')
        else:
            print('It\'s a Miss!')  
    #print message when game is over
    print('Congratulation! You have sunk all the ship!')

if __name__ == '__main__':
    simple_game_loop()    