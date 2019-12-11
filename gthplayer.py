#!/usr/bin/python3

import sys
import gthclient
import board
import table

class Player(object):

    # Initalize variables for the game
    def __init__(self, depth, client):
        self.board = board.Board()
        self.table = table.Table()
        self.depth = depth
        self.client = client
        self.count = 0

    # Gets a range of letters and numbers, supplied by Bart Massey
    # https://github.com/pdx-cs-ai/gothello-libclient-python3
    def letter_range(self, letter):
        for i in range(5):
            yield chr(ord(letter) + i)

    # Converts a move from a tuple to a string in order to be
    # read by the game server
    def convert_move_to_str(self, move):
        if move == (-1,-1):
            return "pass"
        for i, letter in zip(range(5), self.letter_range('a')):
            for j in range(5):
                if move[0] == i and move[1] == j:
                    move_str = letter + str(j+1)
        return move_str

    # Converts a move from a string to a tuple in order to be
    # read by the code that makes the moves.
    def convert_move_to_tuple(self, move):
        if move == "pass":
            return (-1,-1)
        for i, letter in zip(range(5), self.letter_range('a')):
            for digit in self.letter_range('1'):
                if move[0] == letter and move[1] == digit:
                    move_tup = (i, int(digit)-1)
        return move_tup

    # Finds the player's best move and sends it to the server.
    def make_player_move(self):
        board = self.board
        board.find_best_move(self, self.depth)
        board.try_move(board.best_move)
        best_move = self.convert_move_to_str(board.best_move)
        print("me:", best_move)
        return self.client.make_move(best_move)

    # Gets the opponents move and updates the game board.
    def get_opp_move(self):
        cont, move = self.client.get_move()
        if not cont:
            return False
        print("opp:", move)
        move = self.convert_move_to_tuple(move)
        self.board.try_move(move)
        return True
        
    # Main game loop. Continues until the game ends.
    def play(self):
        while True:
            if self.client.who == "black":
                if not self.make_player_move():
                    break
            else:
                if not self.get_opp_move():
                    break
            if self.client.who == "white":
                if not self.make_player_move():
                    break
            else:
                if not self.get_opp_move():
                    break
        if self.client.winner == "black":
            print("black win")
        if self.client.winner == "white":
            print("white win")

def usage():
    print("usage: python3 gthplayer.py color server_name server_number depth")
    exit(0)

if len(sys.argv) != 5: usage()
my_color = sys.argv[1]
server_name = sys.argv[2]
server_number = int(sys.argv[3])
depth = int(sys.argv[4])
client = gthclient.GthClient(my_color, server_name, server_number)
p = Player(depth, client)
p.play()
