import Board
import pylint
import random
import copy
from threading import Timer, Thread, Event

class Othello(object):
        _human_dict = dict(enumerate('ABCDEFGH')) #self._human_dict[i]
        _computer_dict = dict([(v, k) for k, v in enumerate('ABCDEFGH')])
        #These represent the the weights of how important places on the board are used for heuristic later
        # I found these values online, can be tweaked for different results.
        _scores =       [[4, -3, 2, 2, 2, 2, -3, 4],
                        [-3, -4, -1, -1, -1, -1, -4, -3],
                        [2, -1, 1, 0, 0, 1, -1, 2],
                        [2, -1, 0, 1, 1, 0, -1, 2],
                        [2, -1, 0, 1, 1, 0, -1, 2],
                        [2, -1, 1, 0, 0, 1, -1, 2],
                        [-3, -4, -1, -1, -1, -1, -4, -3],
                        [4, -3, 2, 2, 2, 2, -3, 4]]

        def __init__(self):
                self.board_states = []
                self.board = Board.Board()
                self.human_color = 'b'
                self.ai_color = 'w'
                self.quit_game = False
                self.valid_moves = []

        def setup_game(self):
                print()
                self.board.display_score_board()
                self.board.display()
                print("Rotate Board? (y/n):", end = " ")
                choice = input().lower()
                if choice == 'y':
                        self.board.rotate_board()
                        self.board.display_score_board()
                        self.board.display()
                print("Choose color (b/w):", end = " ")
                choice = input().lower()
                if(choice == 'w'):
                        self.human_color = 'w'
                        self.ai_color = 'b'
                print()

        def start_game(self):
                while not self.quit_game:
                        self.board_states.append(copy.deepcopy(self.board))
                        self.valid_moves = self.board.get_valid_moves()
                        if(len(self.valid_moves) == 0):
                                print("No Available Moves!")
                                if(self.board.no_valid_moves()):
                                        print ("Game Over!")
                                        if(self.board.w_score > self.board.b_score):
                                                print("White Wins!")
                                        else:
                                                print("Black Wins!")    
                                        break
                        elif(self.board.get_current_player() == self.human_color):
                                self.player_move()
                        else:
                                self.robot_move()
                        print("Undo? (y/n)", end = "")
                        choice = input().lower()
                        if choice == 'r':
                                self.board.update_valid_moves()
                        if choice == 'y':
                                self.board = self.board_states.pop(-1)
                                self.board.display_score_board()
                                self.board.display()
                        if choice == 'q':
                                self.quit_game = True

        # This method prompts the user for coordinates, I made this very robust and it can accept coordinates
        # with and without spaces. There were much easier ways to handle this.
        def player_move(self):
                validMoveFound = False
                while(not validMoveFound):
                        print("Enter Move (ex: \"C5\"):", end = " ")
                        userInput = input() 
                        if(userInput != ""):
                                coordinates = userInput.split()
                                letter = coordinates[0][0]
                                if(letter.isalpha()):
                                        letter = letter.upper()
                                        if(letter in self._computer_dict):
                                                x = self._computer_dict[letter] 
                                                validMoveFound = True
                                if(len(coordinates) == 2 and coordinates[1].isnumeric()):    
                                        y = int(coordinates[1]) - 1
                                elif(len(coordinates[0]) == 2 and coordinates[0][1].isnumeric()):
                                        y = int(coordinates[0][1]) - 1
                                else:
                                        validMoveFound = False
                                if(validMoveFound):
                                        if(not (x in range(8) and y in range(8))):
                                                validMoveFound = False     
                self.board.last_move = (x,y)
                self.board.take_turn(x,y)
                self.board.update_valid_moves()
                self.board.display_score_board()
                self.board.display()

        #These next few methods handle the ai
        # by tracking the depth of a possible move tree and scoring the outcomes at a set depth,
        # it will conclude which next available move will be most effective.
        def robot_move(self):
                print("\n***AI Taking Turn***")
                stopFlag = Event()
                seconds_passed=[0]
                thread = Timer(stopFlag, seconds_passed)
                thread.start()
                (x,y)= self.pruning(self.board)
                self.board.last_move = (x,y)
                self.board.take_turn(x,y)
                stopFlag.set()
                print(seconds_passed)
                self.board.update_valid_moves()
                self.board.display_score_board()
                self.board.display()

        #this method begins the recursive calls of the min and max methods feeding
        # in every valid move and making a tree of valid moves from each player
        # it acts as an initial max method
        def pruning(self,curr_board):
                best = -10000
                return_move = curr_board.get_valid_moves()[0]
                for x,y in curr_board.get_valid_moves():
                        board = copy.deepcopy(curr_board)
                        board.take_turn(x,y)

                        weight = self.min(board, 10000, -10000) #10000 replace ment for infinity
                        if weight > best:
                                best = weight
                                return_move = (x,y)
                print("Score:",best)
                return (return_move)

        def max(self, curr_board, alpha, beta):
                if(curr_board.get_depth()==12):
                        return self.get_heuristic(curr_board)
                best = -10000
                curr_board.update_valid_moves()
                for x,y in curr_board.get_valid_moves():
                        child = copy.deepcopy(curr_board)
                        child.increase_depth()
                        child.take_turn(x,y)
                        weight = self.min(child, alpha, beta)
                        if weight > best:
                                best = weight
                        if best >= alpha:
                                return best
                        alpha = max(beta,best)
                return best

        def min(self, curr_board, alpha, beta):
                if(curr_board.get_depth()==12):
                        return self.get_heuristic(curr_board)
                best = 10000
                curr_board.update_valid_moves()
                for x,y in curr_board.get_valid_moves():
                        child = copy.deepcopy(curr_board)
                        child.increase_depth()
                        child.take_turn(x,y)
                        weight = self.max(child, alpha, beta)
                        if weight < best:
                                best = weight
                        if best <= alpha:
                                return best
                        beta = min(beta,best)
                   
                return best

        #returns children in order of best huristic
        #huristic is a score of the game based on difference of each payers color
        # in the robots favor and the depth of moves, and the weights of each players tokens.
        # optionaly, score can be affected by
        # the number of moves made or other aspect. No right answer here
        def get_heuristic(self, curr_board):
                if(self.ai_color == 'w'):
                        score = curr_board.w_score
                        enemy = curr_board.b_score
                else:
                        score = curr_board.b_score
                        enemy = curr_board.b_score
                #num_moves = len(curr_board.get_valid_moves()) - 1
                weight = 0
                enemy_w= 0
                for x in range(8):
                        for y in range(8):
                                if(curr_board.board[x][y]== self.ai_color):
                                        weight += self._scores[x][y]
                                elif(curr_board.board[x][y]== self.human_color):
                                        enemy_w += self._scores[x][y]
                return weight + score - enemy - enemy_w

# this class is used to track how long the ai takes to make its move
class Timer(Thread):
        def __init__(self, event, time_passed):
                 Thread.__init__(self)
                 self.stopped = event
                 self.time_passed = time_passed
        def run(self):
                print("AI turn length:", self.time_passed[0])
                while not self.stopped.wait(1):
                        self.time_passed[0] = self.time_passed[0] + 1
                        print("AI turn length:", self.time_passed[0])
