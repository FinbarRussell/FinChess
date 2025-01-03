import re




piece_conversion = {
    "N":"Knight",
    "K":"King",
    "Q":"Queen",
    "R":"Rook",
    "B":"Bishop"
}

icons = {
    "Black": {
        "Pawn": "♟",
        "Knight": "♞",
        "Bishop": "♝",
        "Rook": "♜",
        "Queen": "♛",
        "King": "♚"
    },
    "White": {
        "Pawn": "♙",
        "Knight": "♘",
        "Bishop": "♗",
        "Rook": "♖",
        "Queen": "♕",
        "King": "♔"
    }
}

icons2 = {
    "Black": {
        "pawn": "black-pawn",
        "knight": "black-knight",
        "bishop": "black-bishop",
        "rook": "black-rook",
        "queen": "black-queen",
        "king": "black-king"
    },
    "White": {
        "pawn": "white-pawn",
        "knight": "white-knight",
        "bishop": "white-bishop",
        "rook": "white-rook",
        "queen": "white-queen",
        "king": "white-king"
    }
}

icons_from_pieces = {
        "black-pawn": "♟",
        "black-knight": "♞",
        "black-bishop": "♝",
        "black-rook": "♜",
        "black-queen": "♛",
        "black-king": "♚",
        "white-pawn": "♙",
        "white-knight": "♘",
        "white-bishop": "♗",
        "white-rook": "♖",
        "white-queen": "♕",
        "white-king": "♔"
}

col_coordinates = {
    "A":0,
    "B":1,
    "C":2,
    "D":3,
    "E":4,
    "F":5,
    "G":6,
    "H":7,
}

col_notation = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

row_coordinates = {
    "1":7,
    "2":6,
    "3":5,
    "4":4,
    "5":3,
    "6":2,
    "7":1,
    "8":0,
}

row_notation = {7: '1', 6: '2', 5: '3', 4: '4', 3: '5', 2: '6', 1: '7', 0: '8'}

next_colour = {
    "White":"Black",
    "Black":"White"
}

def validate_move(input_value):
    pattern = r"^[nNrRqQkKbB]{0,1}[a-hA-H]{1}[1-8]{1}$"  
    if not re.match(pattern, input_value):
        raise ValueError(f"Invalid move: {input_value}")
    return input_value

def board_only_squares(coordinates):
    # Define the range
    min_value = 0
    max_value = 7

    # Create an empty list to store valid squares
    filtered_squares = []

    # Loop through each square
    for square in coordinates:
        # Check if both values in the square are within the range
        if min_value <= square[0] <= max_value and min_value <= square[1] <= max_value:
            # Add the square to the filtered list
            filtered_squares.append(square)
    return filtered_squares

def get_move(validated_move):

    ##get coordinates and piece type from code
    parts = list(validated_move)

    if parts.__len__() > 2: #if its not a pawn move
        piece = parts[0] 
        col = parts[1].upper()
        row = parts[2].upper()
        piece = piece.upper()
        piece_type = piece_conversion[piece]

    elif parts.__len__() == 2: #no piece specific info so pawn
        piece_type = "Pawn"
        col = parts[0].upper()
        row = parts[1].upper()

    #convert to coordinates
    col = col_coordinates[col]
    row = row_coordinates[row]
    return piece_type, col, row


def coordinates_to_notation(coordinates): #iterable
    col_notations = []
    row_notations = []
    for move in coordinates:
        row_notations += row_notation[move[0]]
        col_notations += col_notation[move[1]]

    return list(zip(col_notations,row_notations))