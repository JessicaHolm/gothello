import random

class Table(object):
    
    def __init__(self):
        bit_table = [[0] * 2 for _ in range(25)]
        for i in range(25):
            for j in range(2):
                bit_table[i][j] = random.getrandbits(32)
        self.bit_table = bit_table
        self.table = []

    def get_hash(self, grid):
        h = 0
        count = 0
        for i in range(5):
            for j in range(5):
                if grid[i][j] != 0:
                    k = grid[i][j] - 1
                    h = h ^ self.bit_table[count][k]
                count += 1
        return h

    def ttLookup(self, grid):
        key = self.get_hash(grid)
        for entry in self.table:
            if entry.key == key:
                # print("value", entry.value)
                return entry
        return Entry(key)

    def ttStore(self, grid, ttEntry):
        key = self.get_hash(grid)
        for entry in self.table:
            if entry.key == key:
                entry = ttEntry
                return
        
        self.table.append(ttEntry)

class Entry(object):

    def __init__(self, key = 0, move = (0,0), value = 0, flag = 0, depth = -1):
        self.key = key
        self.move = move
        self.value = value
        self.flag = flag
        self.depth = depth
