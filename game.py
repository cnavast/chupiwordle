from datetime import date, timedelta
import random
from sessions import Sessions
from word import Word
from wordRepository import WordRepository

class Game:
    wordRepository = WordRepository()
    sessions = Sessions()
    maxTries = 6

    def getWordById(self, id):
        return self.wordRepository.getWordById(id)
        
    def checkValidWord(self, word):
        return self.wordRepository.checkValidWord(word)

    def writeWords(self, words):
        return self.wordRepository.writeWords(words)

    def getRandomWord(self):
        return self.wordRepository.getRandomWord()

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
