from telegram.ext import Updater
import logging
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from game import Game
from word import Word

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='TELEGRAM_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

game = Game()

def start(update: Update, context: CallbackContext):
    uuid = update.effective_chat.id
    input = update.message.text[7:]

    if input.isnumeric():
        try:
            word = game.getWordById(input)
            game.sessions.newSession(uuid, word)
            logging.info("LOAD " + str(uuid) + " word: " + word.word + " id: " + str(word.id))
            text = "¡La palabra de tu amig@ se ha cargado, suerte!\n\n⬛⬛⬛⬛⬛"
        except:
            text = "Identificador inválido o no encontrado."
    else:
        text = "¡Bienvenido al Chupiwordle!\n\n⬛⬛⬛⬛⬛"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def tryWord(update: Update, context: CallbackContext):
    uuid = update.effective_chat.id
    input = update.message.text.upper()

    if not game.sessions.hasActiveSession(uuid):
        word = game.getRandomWord()
        session = game.sessions.newSession(uuid, word)
        logging.info("NEW " + str(uuid) + " " + word.word + " id: " + str(word.id))

    try:
        session = game.sessions.getSession(uuid)
    except e:
        logging.error("ERROR LOADING USER " + str(uuid) + " " +e)
        context.bot.send_message(chat_id=uuid, text="There was an error " + e)

    if len(input) != 5:
        context.bot.send_message(chat_id=uuid, text="Palabras de cinco (5) letras.")
        return

    session.addTry()

    if game.checkValidWord(input) is False:
        context.bot.send_message(chat_id=uuid, text="Esta palabra no es válida.")
        return

    word = session.getWord().word
    wordId = session.getWord().id

    won, out = game.checkWord(word, input)
    lost = (session.getTries() + 1) == game.getMaxTries()
    session.register(input, out, won, lost)
    logging.info("TRY " + str(uuid) + " " + word + " " + input + " " + out)

    if won or lost:
        if lost:
            context.bot.send_message(chat_id=uuid, text="La palabra era: " + word)
        out_text = "¡Ganaste!" if won else "¡Perdiste!"
        out_text += " " + str(session.getTries()) + "/" + str(game.maxTries)
        out_text += "\n" + "\n".join(session.getOutputs())
        out_text += "\n❌: " + str(session.getInvalidTries()) + " palabras"
        out_text += "\n⌛: " + str(session.getTime())
        out_text += "\n\n🕹️🎮: @ChupiLeBot"
        out_text += "\nJuega la misma palabra con <a href='http://telegram.me/chupiLeBot?start=" + str(wordId) + "'>/start " + str(wordId) + "</a>"
        context.bot.send_message(chat_id=uuid, text=out_text, parse_mode=ParseMode.HTML)
        context.bot.send_message(chat_id=uuid, text="Se ha cargado una nueva palabra, ¡puedes seguir jugando!")
    else:
        out_text = "<code>" + session.getVerbose() + "</code>"
        out_text += "\nIntento " + str(session.getTries()) + " de " + str(game.maxTries)
        context.bot.send_message(chat_id=uuid, text=out_text, parse_mode=ParseMode.HTML)


def add(update: Update, context: CallbackContext):
    uuid = update.effective_chat.id
    words = update.message.text[5:].split(',')
    writtenWords = game.writeWords(words)
    k = len(game.getGameWords())
    game.loadWords()
    out = "Palabras añadidas:\n"
    for word in writtenWords:
        out += word + " ID: " + str(k) + "\n"
        k = k + 1
    context.bot.send_message(chat_id=update.effective_chat.id, text=out, parse_mode=ParseMode.HTML)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

add_handler = CommandHandler('add', add)
dispatcher.add_handler(add_handler)

try_handler = MessageHandler(Filters.text & (~Filters.command), tryWord)
dispatcher.add_handler(try_handler)

updater.start_polling()
