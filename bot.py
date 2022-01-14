from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from game import Game

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='5064935067:AAHL2b0R4NUUFX4YDL7APlAqcQY6q2EflpY', use_context=True)
dispatcher = updater.dispatcher

game = Game()

def start(update: Update, context: CallbackContext):
    text = "¡Bienvenido al Chupiwordle!\nDía: " + game.day.strftime("%Y-%m-%d") + "\n\n⬛⬛⬛⬛⬛"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def tryWord(update: Update, context: CallbackContext):
    uuid = update.effective_chat.id
    word = game.getWord()
    input = update.message.text.upper()

    if game.sessions.hasWon(uuid) or game.sessions.getTries(uuid) >= game.maxTries:
        context.bot.send_message(chat_id=uuid, text="Ya has jugado hoy.")
        return

    if len(input) != 5:
        context.bot.send_message(chat_id=uuid, text="Palabras de cinco (5) letras.")
        return

    if game.checkValidWord(input) is False:
        context.bot.send_message(chat_id=uuid, text="Esta palabra no es válida.")
        return

    won, out = game.checkWord(word, input)
    game.sessions.register(uuid, won, "".join(out))

    tries = game.sessions.getTries(uuid)
    if won or tries >= game.maxTries:
        if not won:
            context.bot.send_message(chat_id=uuid, text="La palabra era: " + word)
        out_text = "¡Ganaste!" if won else "¡Perdiste!"
        out_text += " " + str(game.sessions.getTries(uuid)) + "/" + str(game.maxTries)
        out_text += "\n" + "\n".join(game.sessions.getHistory(uuid))
        out_text += "\n\nJuega en @ChupiLeBot"
    else:
        out_text = "".join(out)
        out_text += "\nIntento " + str(game.sessions.getTries(uuid)) + " de " + str(game.maxTries)
    context.bot.send_message(chat_id=uuid, text=out_text)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

try_handler = MessageHandler(Filters.text & (~Filters.command), tryWord)
dispatcher.add_handler(try_handler)

updater.start_polling()
