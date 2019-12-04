#!/usr/bin/python3

import sys
import random
import copy

import gthclient

class Board(object):
    
    def __init__(self):
        self.best_move = None
        self.to_move = 2
        self.previous_move = None
        self.grid = [[0] * 5 for _ in range(5)]

    def opponent(self, player):
        if player == 1:
            return 2
        if player == 2:
            return 1

    def scratch_board(self):
        return [[False] * 5 for _ in range(5)]

    def flood(self, scratch, color, x, y):
        if not (x >= 0 and x <= 4 and y >= 0 and y <= 4):
            return
        if scratch[x][y]:
            return
        if self.grid[x][y] != color:
            return
        scratch[x][y] = True
        self.flood(scratch, color, x - 1, y)
        self.flood(scratch, color, x + 1, y)
        self.flood(scratch, color, x, y - 1)
        self.flood(scratch, color, x, y + 1)

    def group_border(self, scratch, x, y):
        if scratch[x][y]:
            return False
        if x > 0 and scratch[x - 1][y]:
            return True
        if x < 4 and scratch[x + 1][y]:
            return True
        if y > 0 and scratch[x][y - 1]:
            return True
        if y < 4 and scratch[x][y + 1]:
            return True
        return False

    def liberties(self, x, y):
        scratch = self.scratch_board()
        self.flood(scratch, self.grid[x][y], x, y)
        n = 0
        for i in range(5):
            for j in range(5):
                if self.grid[i][j] == 0 and self.group_border(scratch, i, j):
                    n += 1
        return n

    def move_ok(self, move):
        if move == (-1, -1):
            return True
        if self.grid[move[0]][move[1]] != 0:
            return False
        self.grid[move[0]][move[1]] = self.to_move;
        n = self.liberties(move[0], move[1])
        self.grid[move[0]][move[1]] = 0;
        if n == 0:
            return False
        return True

    def genMoves(self):
        result = []
        for i in range(5):
            for j in range(5):
                if self.grid[i][j] == 0:
                    move = (i, j)
                    if self.move_ok(move):
                        result.append(move)
        return result

    def capture(self, x, y):
        if self.liberties(x, y) > 0:
          return
        scratch = self.scratch_board()
        self.flood(scratch, self.grid[x][y], x, y)
        for i in range(5):
            for j in range(5):
                if scratch[i][j]:
                    self.grid[i][j] = self.to_move

    def do_captures(self, move):
        to_move = self.to_move
        if move[0] > 0 and self.grid[move[0] - 1][move[1]] == self.opponent(to_move):
            self.capture(move[0] - 1, move[1])
        if move[0] < 4 and self.grid[move[0] + 1][move[1]] == self.opponent(to_move):
            self.capture(move[0] + 1, move[1])
        if move[1] > 0 and self.grid[move[0]][move[1] - 1] == self.opponent(to_move):
            self.capture(move[0], move[1] - 1)
        if move[1] < 4 and self.grid[move[0]][move[1] + 1] == self.opponent(to_move):
            self.capture(move[0], move[1] + 1)
        
    def make_move(self, move):
        self.previous_move = move
        if move == (-1, -1):
            return
        self.grid[move[0]][move[1]] = self.to_move
        self.do_captures(move)

    def try_move(self, move):
        if move == (-1,-1) and self.previous_move != None and self.previous_move == (-1,-1):
            return 1
        self.make_move(move)
        self.to_move = self.opponent(self.to_move)
        return 0

    def heval(self):
        mstones = 0
        ostones = 0
        for i in range(5):
            for j in range(5):
                if self.grid[i][j] == self.to_move:
                    mstones += 1
                elif self.grid[i][j] == self.opponent(self.to_move):
                    ostones += 1
        return mstones - ostones

    def optimal_move(self, depth):
        v = self.negamax(depth, True)

    def negamax(self, depth, find_move):
        moves = self.genMoves()
        nmoves = len(moves)
        if nmoves == 0:
            self.best_move = (-1,-1)
            scratch = copy.deepcopy(self)
            status = scratch.try_move(self.best_move)
            if status != 1:
                return -scratch.negamax(25, False)
            return 0
        if depth <= 0:
            return self.heval()
        values = []
        if find_move:
            values = [0] * nmoves
        maxv = -26
        for i in range(nmoves):
            move = moves[i]
            scratch = copy.deepcopy(self)
            status = scratch.try_move(move)
            v = -scratch.negamax(depth - 1, False)
            if find_move:
                values[i] = v
            if v >= maxv:
                maxv = v
        if not find_move:
            return maxv
        nbest = 0
        for i in range(nmoves):
            if values[i] == maxv:
                nbest += 1
        randmove = random.randint(0, nbest-1)
        for i in range(nmoves):
            if values[i] == maxv:
                if randmove == 0:
                    self.best_move = moves[i]
                randmove -= 1
        return maxv

class Player(object):

    def __init__(self, depth, client):
        self.board = Board()
        self.depth = depth
        self.client = client

    def letter_range(self, letter):
        for i in range(5):
            yield chr(ord(letter) + i)

    def convert_move_str(self, move):
        if move == (-1,-1):
            return "pass"
        for i, letter in zip(range(5), self.letter_range('a')):
            for j in range(5):
                if move[0] == i and move[1] == j:
                    move_str = letter + str(j+1)
        return move_str

    def convert_move_tuple(self, move):
        if move == "pass":
            return (-1,-1)
        for i, letter in zip(range(5), self.letter_range('a')):
            for digit in self.letter_range('1'):
                if move[0] == letter and move[1] == digit:
                    move_tup = (i, int(digit)-1)
        return move_tup

    def make_player_move(self):
        self.board.optimal_move(self.depth)
        result = self.board.try_move(self.board.best_move)
        best_move = self.convert_move_str(self.board.best_move)
        print("me:", best_move)
        # print(self.board.grid)
        return self.client.make_move(best_move)

    def get_opp_move(self):
        cont, move = self.client.get_move()
        if not cont:
            return False
        print("opp:", move)
        move = self.convert_move_tuple(move)
        result = self.board.try_move(move)
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

me = sys.argv[1]
depth = int(sys.argv[2])
client = gthclient.GthClient(me, "localhost", 0)
p = Player(depth, client)
p.play()
