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
        placeholder = "_"
        won = word == input
        input = list(input)
        word = list(word)

        for k, char in enumerate(input):
            if char == word[k]:
                out[k] = "🟩"
                input[k] = placeholder
                word[k] = placeholder

        for k, char in enumerate(input):
            if char == placeholder:
                continue

            if char in word:
                word[word.index(char)] = placeholder
                out[k] = "🟨"

        return won, "".join(out)

    def getMaxTries(self):
        return self.maxTries
