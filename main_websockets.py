from regexs import *
import json
#col coordinate starting attribute

class Sprite():
    def __init__(self, row, col, colour, availble_squares=None,availble_squares_notation=None, piece=None):
        self.row = row
        self.col = col
        self.colour = colour
        self.move_counter = 0 #Used for pawns and castling
        ## Create a hastable adding/subtracting possible squares, and removing those that are not possible, then look up move in table to see if legal
        self.availble_squares = availble_squares
        self.availble_squares_notation = availble_squares_notation

    def move_left_right(self, pieces):

        for i in range(1,8):
            if any(piece.row == self.row+i and piece.col == self.col for piece in pieces):
                self.availble_squares.append([self.row+i,self.col])
                break
            else:
                self.availble_squares.append([self.row+i,self.col])

        for i in range(1,8):
            if any(piece.row == self.row-i and piece.col == self.col for piece in pieces):
                self.availble_squares.append([self.row-i,self.col])
                break
            else:
                self.availble_squares.append([self.row-i,self.col])
            

        for i in range(1,8):          
            if any(piece.row == self.row and piece.col == self.col+i for piece in pieces):
                self.availble_squares.append([self.row,self.col+i])        
                break
            else:
                self.availble_squares.append([self.row,self.col+i])

        for i in range(1,8):          
            if any(piece.row == self.row and piece.col == self.col-i for piece in pieces):
                self.availble_squares.append([self.row,self.col-i])
                break
            else:
                self.availble_squares.append([self.row,self.col-i])
        

    def move_diagonally(self, pieces):

        for i in range(1,8):        
            if any(piece.row == self.row+i and piece.col == self.col+i for piece in pieces):
                self.availble_squares.append([self.row+i,self.col+i]) 
                break
            else:
                self.availble_squares.append([self.row+i,self.col+i])


        for i in range(1,8):         
            if any(piece.row == self.row-i and piece.col == self.col+i for piece in pieces):
                self.availble_squares.append([self.row-i,self.col+i])
                break
            else:
                self.availble_squares.append([self.row-i,self.col+i])


        for i in range(1,8):         
            if any(piece.row == self.row+i and piece.col == self.col-i for piece in pieces):
                self.availble_squares.append([self.row+i,self.col-i])
                break
            else:
                self.availble_squares.append([self.row+i,self.col-i])
                
        for i in range(1,8):    
            if any(piece.row == self.row-i and piece.col == self.col-i for piece in pieces):
                self.availble_squares.append([self.row-i,self.col-i])
                break
            else:
                self.availble_squares.append([self.row-i,self.col-i])


    def movement(self, row, col):
        if (row , col) in self.availble_squares:
            self.row == row 
            self.col == col
        else:
            return "Illegal Move"


class Pawn(Sprite):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.piece = "pawn"
        self.icon = icons2[self.colour][self.piece]

    def movement(self, pieces):
        if self.colour == "White":
            self.availble_squares = [
                ]
            if self.move_counter == 0 and not any(piece.row == self.row-2 and piece.col == self.col for piece in pieces):  
                self.availble_squares.append([self.row-2,self.col])

            if not any(piece.row == self.row-1 and piece.col == self.col for piece in pieces):
                self.availble_squares.append([self.row-1,self.col])

            if any(piece.row == self.row-1 and piece.col == self.col+1 for piece in pieces):
                self.availble_squares.append([self.row-1,self.col+1])

            if any(piece.row == self.row-1 and piece.col == self.col-1 for piece in pieces):
                self.availble_squares.append([self.row-1,self.col-1])

        elif self.colour == "Black":
            self.availble_squares = [
                
                ]
            if self.move_counter == 0 and not any(piece.row == self.row+2 and piece.col == self.col for piece in pieces):
                self.availble_squares.append([self.row+2,self.col])

            if not any(piece.row == self.row+1 and piece.col == self.col for piece in pieces):
                self.availble_squares.append([self.row+1,self.col])

            if any(piece.row == self.row+1 and piece.col == self.col+1 for piece in pieces):
                self.availble_squares.append([self.row+1,self.col+1])
                
            if any(piece.row == self.row+1 and piece.col == self.col-1 for piece in pieces):
                self.availble_squares.append([self.row+1,self.col-1])
        

    def promote(self, pieces):
        if self.row == 0 or self.row ==7:
            print("pawn at back rank")
            #get userinput
            user_input = ""

            while user_input != "queen" and user_input != "rook" and user_input != "bishop" and user_input != "knight":
                user_input = input("Enter Piece ('Queen' or 'Rook' or 'Bishop' or 'Knight')")
                print(user_input)

            if user_input == "queen":
                pieces.append(Queen(row=self.row,col=self.col,colour=self.colour))
            if user_input == "rook":
                pieces.append(Rook(row=self.row,col=self.col,colour=self.colour))
            if user_input == "bishop":
                pieces.append(Bishop(row=self.row,col=self.col,colour=self.colour))
            if user_input == "knight":
                pieces.append(Knight(row=self.row,col=self.col,colour=self.colour))

            pieces.remove(self)


class Knight(Sprite):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.piece = "knight"
        self.icon = icons2[self.colour][self.piece]

    def movement(self, pieces):
        self.availble_squares = [
                [self.row-2,self.col-1],
                [self.row-2,self.col+1],
                [self.row+2,self.col-1],
                [self.row+2,self.col+1],
                [self.row-1,self.col-2],
                [self.row-1,self.col+2],
                [self.row+1,self.col-2],
                [self.row+1,self.col+2],
                ]
        

class Bishop(Sprite):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.piece = "bishop"
        self.icon = icons2[self.colour][self.piece]

    def movement(self, pieces):
        self.availble_squares = []
        self.move_diagonally(pieces)


class Rook(Sprite):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.piece = "rook"
        self.icon = icons2[self.colour][self.piece]

    def movement(self, pieces):
        self.availble_squares = []
        self.move_left_right(pieces)


class Queen(Sprite):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.piece = "queen"
        self.icon = icons2[self.colour][self.piece]

    def movement(self, pieces):
        self.availble_squares = []
        self.move_diagonally(pieces)
        self.move_left_right(pieces)


class King(Sprite):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.piece = "king"
        self.icon = icons2[self.colour][self.piece]

    def movement(self, pieces):
        self.availble_squares= []
        self.availble_squares = [
            [self.row+1,self.col],#up
            [self.row+1,self.col+1],#upright
            [self.row+1,self.col-1],#upleft
            [self.row,self.col+1],#right
            [self.row-1,self.col+1],#rightdown
            [self.row-1,self.col],#down
            [self.row-1,self.col-1],#leftdown
            [self.row,self.col-1],#left
            ]


class Main():
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.current_turn = "White"
        self.captured_pieces = []
        self.checkmate = False
        self.initialize_board()


    def initialize_board(self):
        for row in range(8):
            for col in range(8):
                self.board[row][col] = None  # Black square
        #Place Each piece on it's square
        for piece in self.pieces:
            self.board[piece.row][piece.col] = piece.icon

    def check_checkmate(self):
        #call at the start of each round, check everymove, if after everymove, the player is still in check, call checkmate and break 

        #if all moves lead to check

        valid_move = False
        for piece in self.pieces:
            if piece.colour == self.current_turn:
                for move in piece.availble_squares:
                    invalid_move = self.in_check_after_move(piece, move)
                    if invalid_move == False:
                        return False
        self.checkmate = True
        return True

    
    def find_piece_colour(self, coordinate):

        col, row = coordinate
        for piece in self.pieces:
            if piece.col == col and piece.row==row:
                return piece.colour

    def set_board(self):
        
        ## Add objects to a dictionary for quick lookup i.e. black king, white king etc. etc. 

        #Pawns
        for col in range(8):
            self.pieces.append(Pawn(row=1,col=col,colour="Black"))
            self.pieces.append(Pawn(row=6,col=col,colour="White"))

        #Knights
        self.pieces.append(Knight(row=0,col=1,colour="Black"))
        self.pieces.append(Knight(row=7,col=1,colour="White"))

        self.pieces.append(Knight(row=0,col=6,colour="Black"))
        self.pieces.append(Knight(row=7,col=6,colour="White"))

        #Bishops
        self.pieces.append(Bishop(row=0,col=2,colour="Black"))
        self.pieces.append(Bishop(row=7,col=2,colour="White"))

        self.pieces.append(Bishop(row=0,col=5,colour="Black"))
        self.pieces.append(Bishop(row=7,col=5,colour="White"))

        #Rooks
        self.pieces.append(Rook(row=0,col=0,colour="Black"))
        self.pieces.append(Rook(row=7,col=0,colour="White"))

        self.pieces.append(Rook(row=0,col=7,colour="Black"))
        self.pieces.append(Rook(row=7,col=7,colour="White"))

        #Queens
        self.pieces.append(Queen(row=0,col=3,colour="Black"))
        self.pieces.append(Queen(row=7,col=3,colour="White"))

        #Kings
        self.pieces.append(King(row=0,col=4,colour="Black"))
        self.pieces.append(King(row=7,col=4,colour="White"))

        #Place Each piece on it's starting square
        for piece in self.pieces:
            self.board[piece.row][piece.col] = piece.icon

    def print_board(self):
        for col in self.board:
            print(col)
        json_string = json.dumps(self.board, ensure_ascii=False)    
        return json_string

    def select_piece(self, recieved_piece): # Redundancy in the removal of illegal moves (moves into check) may refactor at some point
        try:
            found = False
            while found == False:
                illegal = False
                selected_piece = recieved_piece
                print(selected_piece)
                piece_type, row, col = selected_piece.split(", ")
                row = int(row)
                col = int(col)
                piece_type = piece_type.split("-")
                piece_type = piece_type[1]
                print(piece_type, col, row)
                #print(f"piece: {piece_type} col: {col} row: {row}") ## Logging

                #if selected move is found on a square print true
                for piece in self.pieces:
                    #print(piece.piece,piece.col, piece.row,  piece.colour)
                    if piece.piece == piece_type and piece.col == col and piece.row == row and piece.colour == self.current_turn:
                        self.initialise_moves(piece)
                        active_piece = piece
                        print("selected correct piece")
                        illegal_squares = []
                        for move in active_piece.availble_squares[:]:
                            if self.in_check_after_move(piece, move):
                                illegal_squares.append(move)
                                print(f"move that puts in check: {move}")

                        for move in illegal_squares:
                            print(illegal_squares)
                            active_piece.availble_squares.remove(move)
                            print(f"after removale here are active squares: {active_piece.availble_squares}")
                        active_piece.availble_squares = board_only_squares(active_piece.availble_squares) 
                        piece.availble_squares_notation = coordinates_to_notation(piece.availble_squares)

                        if active_piece.availble_squares == []:
                            print("No Legal Moves")
                            illegal = True
                            return "No Legal Moves"

                        else:
                            return active_piece

                if illegal != True:
                    print("Piece not found")
                    return "Piece not found"
            return active_piece
            
        except ValueError or UnboundLocalError:
            print(f"Invalid notation: {selected_piece}")
            return f"Invalid notation: {selected_piece}"

    def select_move(self, piece,move):
        made_move = False
        while made_move == False:
            try:
                found = False
                while found == False:
                    selected_move = move  # I.e. e5
                    validated_move = validate_move(selected_move)  #Validates that it is correct notation
                    _, col, row = get_move(validated_move)
                    current_square = [piece.row, piece.col]
                    old_row, old_col = current_square 
                    move_to = [row,col]
                    print(f"Selected pieces availble squares: {piece.availble_squares}")
                    print(f"Selected pieces move: {move_to}")

                    if move_to in piece.availble_squares:
                        piece.col = col
                        piece.row = row
                        for chessman in self.pieces:
                            if piece.col == chessman.col and piece.row == chessman.row and chessman.colour == next_colour[self.current_turn]:
                                self.pieces.remove(chessman)
                                self.captured_pieces.append(chessman)
                        self.board[old_row][old_col] = None
                        self.board[piece.row][piece.col] = piece.icon
                        piece.move_counter += 1
                        #print(piece.availble_squares)
                        made_move = True
                        return True
                    else:
                        print("Illegal Move")
                        return "Illegal Move"

                    #check that validated move is in list of pieces availble squares, if true then change col/row, remove from current board square, and append to new
            except ValueError:
                print(f"Invalid notation: {selected_move}")
                return f"Invalid notation: {selected_move}"

    def in_check_after_move(self, piece, move):
        
        current_square = [piece.row, piece.col]
        old_row, old_col = current_square 
        move_to = move
        row, col = move_to
        piece.row = row
        piece.col = col

        piece_to_take = None

        for chessman in self.pieces:
            if piece.col == chessman.col and piece.row == chessman.row and chessman.colour == next_colour[self.current_turn] and chessman != piece:
                piece_to_take = chessman
                self.pieces.remove(piece_to_take)
                

        self.initialise_moves(piece)

        if self.in_check(self.pieces) == True:
            piece.row = old_row
            piece.col = old_col
            if piece_to_take != None:
                self.pieces.append(piece_to_take)
            self.initialise_moves(piece)
            return True

        elif self.in_check(self.pieces) == False:
            piece.row = old_row
            piece.col = old_col
            if piece_to_take != None:
                self.pieces.append(piece_to_take)
            self.initialise_moves(piece)
            return False            

    def initialise_moves(self,active_piece):
        for piece in self.pieces:
            piece.availble_squares = []
            piece.availble_squares_notation = []
            piece.movement(self.pieces)
            piece.availble_squares = board_only_squares(piece.availble_squares) 
           
        self.remove_friendly_squares()
        for piece in self.pieces:
            piece.availble_squares_notation = coordinates_to_notation(piece.availble_squares)

    def in_check(self, pieces):

        for piece in pieces:
            if piece.colour == self.current_turn and piece.piece == "king":
                king = piece
                king_coordinates = [king.row, king.col]

                # Loop through the pieces
        for piece in pieces:
            if piece.colour != self.current_turn:
                # Check if king_coordinates is in piece.available_squares
                if king_coordinates in piece.availble_squares:
                    # If true, return the piece
                    #offending_piece = piece
                    #print(f"the offending piece is {offending_piece.icon}")
                    return True

        return False    

    def remove_friendly_squares(self): # Could move this into the sprite class to make code more consistent

        all_friendly_squares = []
        #for white pieces, loop through pieces and store coordinates in a hasmap, then for each white piece, remove all availble squares in hasmap
        for piece in self.pieces:
            if piece.colour == self.current_turn:
                all_friendly_squares.append([piece.row,piece.col])

        # Remove matching coordinates
        for piece in self.pieces:
            if piece.colour == self.current_turn:
                new_coordinates = []  # Temporary list to hold non-matching coordinates
                for coord in piece.availble_squares:
                    if coord not in all_friendly_squares:
                        new_coordinates.append(coord)
                piece.availble_squares = new_coordinates  # Update the object's coordinates

    def run(self):

        self.set_board()
        self.print_board()
        self.initialise_moves(None)

        while self.checkmate == False:
            in_check = self.in_check(self.pieces)
            print(f"It's {self.current_turn}'s Turn")

            if in_check:
                print("in Check")
            no_moves = self.check_checkmate() #check for any legal moves, if none then check if in check, if in check return checkmate, if not in check return stalemate -
            
            if no_moves:
                if in_check:
                    print(f"# {next_colour[self.current_turn]} wins!")
                    continue
                elif not in_check:
                    print(f"1/2 Stalemate!")
                    continue
            
            selected_piece = self.select_piece()
            print(selected_piece.icon, col_notation[selected_piece.col], row_notation[selected_piece.row], f"Possible Moves : {selected_piece.availble_squares_notation}")
            self.select_move(selected_piece)

            if selected_piece.piece == "pawn":
                selected_piece.promote(self.pieces) #Must go here to prevent promoting during illegal moves, i.e. once it's passed "select_move"
                
            self.initialise_moves(selected_piece)
            self.initialize_board()
            self.print_board()
            self.current_turn = next_colour[self.current_turn]
            result = f"Captutured pieces: {', '.join(str(x.icon) for x in self.captured_pieces)}"
            print(result)
        