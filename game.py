from datetime import date, timedelta
import random
from sessions import Sessions

class Game:
    v = 1
    day = date.today() - timedelta(days=1)
    word = "PATIO"
    gameWords = list(map(lambda w: w.strip().upper(), open("palabras/list-unique-chars.txt", "r").readlines()))
    validWords = list(map(lambda w: w.strip().upper(), open("palabras/list.txt", "r").readlines()))
    sessions = Sessions()
    maxTries = 6

    def newWord(self):
        self.word = random.choice(self.gameWords)
        print(self.word)

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

        return word == input, out

    def getWord(self):
        self.refresh()
        return self.word

    def refresh(self):
        if self.day < date.today():
            self.newWord()
            self.day = date.today()
            self.v = self.v + 1
            self.sessions = Sessions()
