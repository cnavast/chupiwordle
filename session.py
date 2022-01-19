from word import Word
from datetime import datetime
import math

class Session:
    def __init__(self, key, word):
        self.key = key
        self.word = word
        self.start = datetime.now()
        self.inputs = []
        self.outputs = []
        self.won = False
        self.lost = False
        self.allTries = 0

    def isActive(self):
        return self.won == False and self.lost == False

    def register(self, input, output, won, lost):
        self.won = won
        self.lost = lost
        self.inputs.append(input)
        self.outputs.append(output)

    def addTry(self):
        self.allTries = self.allTries + 1

    def getTries(self):
        return len(self.inputs)

    def getInvalidTries(self):
        return self.allTries - self.getTries()

    def getWord(self):
        return self.word

    def getOutputs(self):
        return self.outputs

    def getVerbose(self):
        verbose = ''
        for input, output in zip(self.inputs, self.outputs):
            for letter, box in zip(list(input), list(output)):
                verbose += letter + box + ' '
            verbose += '\n'
        return verbose

    def getTime(self):
        total_seconds = math.floor(10 * (datetime.now() - self.start).total_seconds()) / 10
        minutes = math.floor(total_seconds / 60)
        seconds = math.floor(total_seconds - 60 * minutes)
        decimal = math.floor(10 * (total_seconds - 60 * minutes - seconds))
        return str(minutes) + 'm' + str(seconds) + '.' + str(decimal) + 's'
