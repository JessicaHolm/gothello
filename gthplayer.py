#!/usr/bin/python3

import sys
import gthclient
import board
import table

class Player(object):

    def __init__(self, depth, client):
        self.board = board.Board()
        self.table = table.Table()
        self.depth = depth
        self.client = client
        self.count = 0

    def letter_range(self, letter):
        for i in range(5):
            yield chr(ord(letter) + i)

    def convert_move_to_str(self, move):
        if move == (-1,-1):
            return "pass"
        for i, letter in zip(range(5), self.letter_range('a')):
            for j in range(5):
                if move[0] == i and move[1] == j:
                    move_str = letter + str(j+1)
        return move_str

    def convert_move_to_tuple(self, move):
        if move == "pass":
            return (-1,-1)
        for i, letter in zip(range(5), self.letter_range('a')):
            for digit in self.letter_range('1'):
                if move[0] == letter and move[1] == digit:
                    move_tup = (i, int(digit)-1)
        return move_tup

    def make_player_move(self):
        board = self.board
        board.find_best_move(self, self.depth)
        board.try_move(board.best_move)
        best_move = self.convert_move_to_str(board.best_move)
        print("me:", best_move)
        return self.client.make_move(best_move)

    def get_opp_move(self):
        cont, move = self.client.get_move()
        if not cont:
            return False
        print("opp:", move)
        move = self.convert_move_to_tuple(move)
        self.board.try_move(move)
        return True
        
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
    print("usage: python3 gthplayer.py color depth")
    exit(0)

if len(sys.argv) != 3: usage()
me = sys.argv[1]
depth = int(sys.argv[2])
client = gthclient.GthClient(me, "localhost", 0)
p = Player(depth, client)
p.play()
