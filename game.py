from datetime import date, timedelta
import random
from sessions import Sessions
from word import Word
from random import randrange

class Game:
    gameWordsFile = "words/game.txt"
    validWordsFile = "words/valid.txt"
    gameWords = list()
    validWords = list()
    sessions = Sessions()
    maxTries = 6
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "$")
    )

    def __init__(self):
        self.loadWords()

    def loadWords(self):
        self.gameWords = list(map(lambda w: w.strip().upper(), open(self.gameWordsFile, "r").readlines()))
        self.validWords = list(map(lambda w: w.strip().upper(), open(self.validWordsFile, "r").readlines()))

    def getGameWords(self):
        return self.gameWords

    def normalize(self, s):
        s = s.lower()
        for a, b in self.replacements:
            s = s.replace(a, b)
        return s

    def writeWords(self, words):
        words = map(lambda w: w.strip().upper(), words)
        words = filter(lambda w: len(w) == 5, words)
        words = filter(lambda w: w not in self.validWords, words)
        words = map(lambda w: self.normalize(w), words)
        words = list(words)

        if len(words) == 0:
            return words

        possible = open(self.gameWordsFile, 'a')
        accepted = open(self.validWordsFile, 'a')

        possible.write("\n".join(words) + "\n")
        accepted.write("\n".join(words) + "\n")

        possible.close()
        accepted.close()
        return words

    def getRandomWord(self):
        id = randrange(len(self.gameWords))
        word = self.gameWords[id]
        return Word(word, id)

    def getWordById(self, id):
        if not id.isnumeric():
            raise Exception('Invalid id')
        word = self.gameWords[int(id)]
        return Word(word, id)

    def checkValidWord(self, word):
        return word in self.validWords

    # Returns a flag indicating if the word is correct & the positions.
    @staticmethod
    def checkWord(word, input):
        out = ["⬛", "⬛", "⬛", "⬛", "⬛"]
        k = 0
        for c in input:
            if c == word[k]:
                out[k] = "🟩"
                input = input[:k] + "_" + input[k + 1:]
                word = word[:k] + "_" + word[k + 1:]
            k = k + 1

        k = 0
        for c in input:
            if c == "_":
                k = k + 1
                continue
            l = 0
            for d in word:
                if c == d:
                    word = word[:l] + "_" + word[l + 1:]
                    out[k] = "🟨"
                    break
                l = l + 1
            k = k + 1

        return word == input, "".join(out)

    def getMaxTries(self):
        return self.maxTries
