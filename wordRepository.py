from word import Word
from random import randrange

class WordRepository:
    gameWordsFile = "words/game.txt"
    validWordsFile = "words/valid.txt"
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u")
    )

    gameWords = list()
    validWords = list()

    def __init__(self):
        self.loadWords()

    def normalize(self, s):
        s = s.lower()
        for a, b in self.replacements:
            s = s.replace(a, b)
        return s

    def loadWords(self):
        self.gameWords = list(map(lambda w: w.strip().upper(), open(self.gameWordsFile, "r").readlines()))
        self.validWords = list(map(lambda w: w.strip().upper(), open(self.validWordsFile, "r").readlines()))

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

        k = len(self.gameWords)
        self.loadWords()
        listWords = list()
        for word in words:
            listWords.append(Word(word, k))
            k = k + 1
        return listWords

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
