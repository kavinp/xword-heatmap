### Crossword Heatmap Generator
import json
import sys
from helpers import *

# read-in .puz file

# initialize crossword grid in here
# get "difficulty rating" as a different grid

# difficulty rating is a ten point scale
# of -5 to +5
# and you just add to get the difficulty of the square

# we can make difficulties more or less than this (-infinity)
# but they get floor/ceiling'd to -5 or +5 in the representation

# do math

# print out letters with color for difficulty


heatDict = {'-5': 22, '-4': 28, '-3': 34, '-2': 40, '-1': 46, '+0': 226,
            '+1': 215, '+2': 214, '+3': 202, '+4': 196, '+5': 160}

class Crossword:

    def __init__(self, data):
        self.author = data["author"]
        self.title = data["title"]
        self.rows = data["size"]["rows"]
        self.cols = data["size"]["cols"]

        # key in with number and then _a_cross or _d_own
        # example: self.words[1]['a'] for 1ACROSS
        # ... this yields a "word" dictionary with:
        #     {'clue': string, 'ans': string, 'diff': int}
        self.words = []


        # init grids
        self.grid = init_grid(data["grid"], self.rows)
        # map of subjective difficulty
        self.diffMap = [[None] + ([0] * self.rows)
                         for _ in range(self.cols + 1)]
        self.words.append({}) # 1-index clues

        # find numbered crossword squares
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                if self.grid[i][j] == '.':
                    continue
                if (i == 1 or j == 1 or self.grid[i-1][j] == '.'
                        or self.grid[i][j-1] == '.'):
                    word = {
                        'xy': (i, j),
                        'a': None,
                        'd': None,
                    }
                    self.words.append(word)

        # intialize words
        for i, wHead in enumerate(self.words[1:], start=1):
            x, y = wHead['xy']
            if y == 1 or self.grid[x][y-1] == '.': # ACROSS
                ans = ""
                while y <= self.cols and self.grid[x][y] != '.':
                    ans += self.grid[x][y]
                    y += 1
                self.words[i]['a'] = {'ans': ans, 'clue': "", 'diff': None}

            x, y = wHead['xy']
            if x == 1 or self.grid[x-1][y] == '.': # DOWN
                ans = ""
                while x <= self.rows and self.grid[x][y] != '.':
                    ans += self.grid[x][y]
                    x += 1
                self.words[i]['d'] = {'ans': ans, 'clue': None, 'diff': None}

        # initialize clues and difficulties
        self.initClues(data["clues"]["across"], 'a')
        self.initClues(data["clues"]["down"], 'd')

        # initialize difficulty heatmap
        for i, wHead in enumerate(self.words[1:], start=1):
            x, y = wHead['xy']
            across = self.words[i]['a']
            if across and across['diff'] != None:
                while y <= self.cols and self.grid[x][y] != '.':
                    self.diffMap[x][y] += across['diff']
                    y += 1

            x, y = wHead['xy']
            down = self.words[i]['d']
            if down and down['diff'] != None:
                while x <= self.rows and self.grid[x][y] != '.':
                    self.diffMap[x][y] += down['diff']
                    x += 1


    def initClues(self, clues, dir):
        """ Put clues from data into the self.words dictionary.
            Dir is 'a' for across or 'd' for down."""
        for clue in clues:
            num = int(clue.split('.')[0])
            diff = int(clue[-3:-1]) if clue[-1] == '}' else None
            clue = clue.partition('. ')[2]
            clue = clue.partition(' {')[2]
            self.words[num][dir]['diff'] = diff
            self.words[num][dir]['clue'] = clue


    def printHeat(self):
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                diff = self.diffMap[i][j] if self.diffMap[i][j] else 0
                diff = to_str_with_sign(normalize_diff(diff))
                to_print = self.grid[i][j]
                sys.stdout.write(u"\u001b[30m\u001b[48;5;" + str(heatDict[diff]) + "m " + to_print.ljust(2))
            print(u"\u001b[0m")

        # for i in range(-5, 6):
        #     i = str(i)
        #     sys.stdout.write(u"\u001b[30m\u001b[48;5;" + str(heatDict[i]) + "m " + str(heatDict[i]).ljust(4))
        # print(u"\u001b[0m")


if __name__ == "__main__":
    file = sys.argv[1]
    with open(file, "r") as read_file:
        data = json.load(read_file)
    x = Crossword(data)
    x.printHeat()
