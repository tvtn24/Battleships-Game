import random
import json

# initialize an empty game board 
def initialise_board(size=10) -> list[list]:
    board = [[None]*size for i in range(size)] 
    return board

# create a dictionary of battleships from battleships.txt file.
def create_battleships(filename="battleships.txt") -> dict[str, int]:
    battleships = {}
    with open(filename, 'r') as file:
        for line in file:
            name, size = line.split(':')
            battleships[name] = int(size)
    return battleships

# check if the position is valid for placing ships or not
def is_valid_position(board: list[list], row: int, col: int, orientation: str, size: int) -> bool:
    if orientation == 'h':
        for i in range(size):
            if col+i>=0 and col+i< len(board[row]) and  board[row][col + i] is None:
                continue
            else:
                return False
        return True
    elif orientation == 'v':
        for i in range(size):
            if row+i>=0 and row+i< len(board) and  board[row+i][col] is None:
                continue
            else:
                return False
        return True

# place battleships on the game board and return a placed board
def place_battleships(board: list[list], ships: dict[str,int], algorithm='simple') -> list[list]:
    battleships = create_battleships()
    if algorithm == 'simple':
        row = 0
        col = 0 
        for name, size in ships.items():
            for col in range(size):
                board[row][col] = name
            row += 1
    
    elif algorithm == 'random':
        for name, size in ships.items():
            orientation = random.choice(['h', 'v'])
            placed = False
            while not placed:
                if orientation == 'h':
                    row = random.randint(0, len(board[0]) - size) 
                    col = random.randint(0, len(board) - 1)
                    if is_valid_position(board, row, col, orientation, size):
                        for i in range(size):
                            board[row + i][col] = name
                        placed = True
                else:
                    row = random.randint(0, len(board[0]) - 1)
                    col = random.randint(0, len(board) - size)
                    if is_valid_position(board, row, col, orientation, size):
                        for i in range(size):
                            board[row + i][col] = name
                        placed = True

    elif algorithm == 'custom':
        with open('placement.json', 'r') as file:
            placement = json.load(file)
            for name, coords in placement.items():
                if name in battleships:
                    size = battleships[name]
                    row, col, orientation = int(coords[1]), int(coords[0]), coords[2]
                    if orientation == 'h':
                        if is_valid_position(board, row, col, orientation, size):
                            for i in range(size):
                                board[row][col + i] = name
                    elif orientation == 'v':
                        if is_valid_position(board, row, col, orientation, size):
                            for i in range(size):
                                board[row + i][col] = name
    return board