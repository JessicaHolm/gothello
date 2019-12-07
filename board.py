# Class that manages the board state.

import copy
import random

PLAYER_BLACK = 1
PLAYER_WHITE = 2
GAME_OVER = 1
PASS = (-1,-1)
INF = float('infinity')

class Board(object):
    
    def __init__(self):
        self.best_move = None
        self.to_move = PLAYER_BLACK
        self.previous_move = None
        self.grid = [[0] * 5 for _ in range(5)]

    def find_best_move(self, depth, maximizing_player):
        moves = self.genMoves()
        values = []
        possible_best_moves = []
        maxval = -INF
        for move in moves:
            scratch = copy.deepcopy(self)
            status = scratch.try_move(move)
            value = -scratch.negamax(move, depth, status, -INF, INF)
            values.append(value)
        if values:
            maxval = max(values)

        for value, move in zip(values, moves):
            if value == maxval:
                possible_best_moves.append(move)
        if moves:
            self.best_move = random.choice(possible_best_moves)
        else:
            self.best_move = PASS
    
    def negamax(self, node, depth, status, a, b):
        if depth == 0 or status == GAME_OVER:
            return self.heval()
        moves = self.genMoves()
        maxval = -INF
        for move in moves:
            scratch = copy.deepcopy(self)
            status = scratch.try_move(move)
            maxval = max(maxval, -scratch.negamax(move, depth - 1, status, -b, -a))
            a = max(a, maxval)
            if a >= b:
                return b
        return maxval
        
    def opponent(self, player):
        if player == PLAYER_BLACK:
            return PLAYER_WHITE 
        if player == PLAYER_WHITE:
            return PLAYER_BLACK

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
        if move == PASS:
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
        if move == PASS:
            return
        self.grid[move[0]][move[1]] = self.to_move
        self.do_captures(move)

    def try_move(self, move):
        if move == PASS and self.previous_move == PASS:
            return GAME_OVER
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
        # print("heval", mstones - ostones)
        return mstones - ostones
