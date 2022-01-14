from datetime import date, timedelta
import random
import logging

class Sessions:
    session = {}

    def register(self, key, won, out):
        if key not in self.session:
            self.session[key] = {'won': False, 'history': []}
            logging.info("New user " + str(key))
        self.session[key]['history'].append(out)
        self.session[key]['won'] = won
        logging.info("User " + str(key) + " got " + out)

    def hasWon(self, key):
        if key not in self.session:
            return False
        return self.session[key]['won']

    def getTries(self, key):
        if key not in self.session:
            return 0
        else:
            return len(self.session[key]['history'])

    def getHistory(self, key):
        return self.session[key]['history']
