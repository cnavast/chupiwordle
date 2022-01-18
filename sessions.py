from datetime import date, timedelta
import random
import logging
from word import Word
from session import Session

class Sessions:
    sessions = {}

    def hasActiveSession(self, key):
        if key not in self.sessions:
            return False
        return self.sessions[key].isActive()

    def getSession(self, key):
        if key not in self.sessions:
            raise Exception(str(key) + ' does not exist in memory.')
        return self.sessions[key]

    def newSession(self, key, word):
        newSession = Session(key, word)
        self.sessions[key] = newSession
        return newSession

    def restart(self):
        self.sessions = {}
