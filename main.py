import Othello

#Simple method to create the board and setup & run game.
def main():
    game = Othello.Othello()
    game.setup_game()
    game.start_game()

main()