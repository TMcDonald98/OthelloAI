#The main chunck of this project.
# This board objects handles board orientation, checking for valid moves, displaying the board, taking turns, 
# and all the functions for the min/max ai.
class Board(object):
    _human_dict = dict(enumerate('ABCDEFGH')) #self._human_dict[i]
    _computer_dict = dict([(v, k) for k, v in enumerate('ABCDEFGH')])
    def __init__(self):
        self.board = [['.' for i in range(8)] for j in range(8)]
        self.w_score = 2 #'w' on board
        self.b_score = 2 #'b' on board
        self.current_player = 'b'
        self.game_over = False
        self.board[3][3], self.board[4][4] = 'b','b'#places the 4 initial game tokens
        self.board[4][3], self.board[3][4] = 'w','w'
        self.valid_moves = []
        self.update_valid_moves()
        self.depth = 0
        self.checkers_flipped = []
        self.last_move = (-1,-1)
        self.parent_move = (-1,-1)

    # these functions track the depth of moves used for the ai
    def increase_depth(self):
        self.depth+=1

    def reset_depth(self):
        self.depth=0

    def get_depth(self):
        return self.depth

    def get_current_player(self):
        return self.current_player

    def get_board(self):
        return self.board

    def get_last_move_score(self):
        return len(self.checkers_flipped)

    def get_last_move(self):
        return self.last_move
    #player has opthion to rotate board
    def rotate_board(self):
        self.board[3][3], self.board[4][4] = 'w','w' 
        self.board[4][3], self.board[3][4] = 'b','b'
        self.update_valid_moves()

    def display_score_board(self):
        print("\nCurrent Players Turn:", self.current_player)
        print("w's Score:", self.w_score, " b's Score:", self.b_score)
    #checks moves to see if valid
    def no_valid_moves(self):
        if(self.last_move == (-1,-1)):
            return True
        if self.current_player == 'w':
                self.current_player = 'b'
        else: 
            self.current_player = 'w'
        self.checkers_flipped = []
        self.last_move = (-1,-1)
        self.update_valid_moves()
    #Neatly prints the board 
    def display(self):
        print("  _________________")
        for x in range(8):
            print(x+1, end ="| ")
            for y in range(8):
                if (y,x) in self.valid_moves:
                    print ("~", end = " ")
                elif (y,x) in self.checkers_flipped or (y,x) == self.last_move:
                    print (self.board[y][x].upper(), end =" ")
                else:
                    print (self.board[y][x], end =" ")
            print("|")
        print("  —————————————————")
        print("   A B C D E F G H")
        
    #Checks to see if given move is valid and if so flips the relevant pieces 
    def take_turn(self, x, y):
        if self.current_player == 'w':
            opponent = 'b'
        else:
            opponent = 'w'
        if (x, y) in self.valid_moves:
            self.checkers_flipped = []
            self.board[x][y] = self.current_player
            if x - 1 >= 0 and self.board[x - 1][y] == opponent:
                potential = []
                i = 1
                while x - i >= 0 and self.board[x - i][y] != '.':
                    if self.board[x - i][y] == self.current_player:
                        self.checkers_flipped.extend(potential)
                        break
                    potential.append((x - i, y))
                    i += 1
            if x + 1 < 8 and self.board[x + 1][y] == opponent:
                potential = []
                i = 1
                while x + i < 8 and self.board[x + i][y] != '.':
                    if self.board[x + i][y] == self.current_player:
                        self.checkers_flipped.extend(potential)
                        break
                    potential.append((x + i, y))
                    i += 1
            if y - 1 >= 0 and self.board[x][y - 1] == opponent:
                potential = []
                i = 1
                while y - i >= 0 and self.board[x][y - i] != '.':
                    if self.board[x][y - i] == self.current_player:
                        self.checkers_flipped.extend(potential)
                        break
                    potential.append((x, y - i))
                    i += 1
            if y + 1 < 8 and self.board[x][y + 1] == opponent:
                potential = []
                i = 1
                while y + i < 8 and self.board[x][y + i] != '.':
                    if self.board[x][y + i] == self.current_player:
                        self.checkers_flipped.extend(potential)
                        break
                    potential.append((x, y + i))
                    i += 1
            if y - 1 >= 0 and x - 1 >= 0 and self.board[x - 1][y - 1] == opponent:
                potential = []
                i = 1
                while y - i >= 0 and x - i >= 0 and self.board[x - i][y - i] != '.':
                    if self.board[x - i][y - i] == self.current_player:
                        self.checkers_flipped.extend(potential)
                        break
                    potential.append((x - i, y - i))
                    i += 1
            if y + 1 < 8 and x + 1 < 8 and self.board[x + 1][y + 1] == opponent:
                potential = []
                i = 1
                while y + i < 8 and x + i < 8 and self.board[x + i][y + i] != '.':
                    if self.board[x + i][y + i] == self.current_player:
                        self.checkers_flipped.extend(potential)
                        break
                    potential.append((x + i, y + i))
                    i += 1
            if y - 1 >= 0 and x + 1 < 8 and self.board[x + 1][y - 1] == opponent:
                potential = []
                i = 1
                while y - i >= 0 and x + i < 8 and self.board[x + i][y - i] != '.':
                    if self.board[x + i][y - i] == self.current_player:
                        self.checkers_flipped.extend(potential)
                        break
                    potential.append((x + i, y - i))
                    i += 1
            if y + 1 < 8 and x - 1 >= 0 and self.board[x - 1][y + 1] == opponent:
                potential = []
                i = 1
                while y + i < 8 and x - i >= 0 and self.board[x - i][y + i] != '.':
                    if self.board[x - i][y + i] == self.current_player:
                        self.checkers_flipped.extend(potential)
                        break
                    potential.append((x - i, y + i))
                    i += 1
            for (x,y) in self.checkers_flipped:
                self.board[x][y] = self.current_player
            if self.current_player == 'w':
                self.w_score+= (1 + len(self.checkers_flipped))
                self.b_score-= len(self.checkers_flipped)
                self.current_player = 'b'
            else:
                self.b_score+= (1 + len(self.checkers_flipped))
                self.w_score-= len(self.checkers_flipped)
                self.current_player = 'w'
        else:
            print("invalid move")
            return False

    def get_valid_moves(self):
        return self.valid_moves

    # This method looks messy, but does alot for how compact it is
    # It essentially checks for an oponents piece then searches for a open slot around it and if it finds one 
    # it searches in the opposit direction of the empty slot till it find a token of the current players color
    # if it finds a blank or goes past the size of the board before this occurs, then it is not a valid move and
    # it continues checking all spaces. This could perhaps be made more efficient by searching for empty space in
    # the later sections of the game since it would not have to check as many pieces.  
    def update_valid_moves(self):
        if self.current_player == 'w':
            opponent = 'b'
        else:
            opponent = 'w'
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == opponent:
                    for x_dir,y_dir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                        if x + x_dir in range(8) and y + y_dir in range(8):
                            if self.board[x+x_dir][y+y_dir] == '.' and self.board[x+x_dir][y+y_dir] not in self.valid_moves:
                                i = 1
                                while x - i*x_dir in range(8) and y - i*y_dir in range(8) and self.board[x - i*x_dir][y - i*y_dir] != '.':
                                    if self.board[x - i*x_dir][y - i*y_dir] == self.current_player:
                                        valid_moves.append((x+x_dir,y+y_dir))
                                        break
                                    i += 1
        self.valid_moves = valid_moves
        