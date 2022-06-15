#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def pizza(update, context):
    print(update.message.text.upper())
    message = update.message.text.upper()
    if message == 'OKEY VAMOS PROGRESANDO':
        update.message.reply_text("Gracias")

    if '/BOT:REPORTE_LC_' in message and  message != '/BOT:REPORTE_LC_GENERAL':
        user = message.split("_")[-1]
        api_url = f'http://www.linkp.online/api/v1/api_linkcoins/{user}/reporte/'
        response = requests.request('GET', api_url)
        if response.status_code == 200:
            user_data = response.json()
            update.message.reply_text(f"{user} genero {user_data['monedas_generadas']} monedas, recibio {user_data['monedas_recibidas']} monedas y canjeo {user_data['monedas_canjeadas']} monedas. Tiene pendiente {user_data['canjes_pendientes']} canjes y el ultimo realizado fue {user_data['ultimo_canje']}")
        else:
            update.message.reply_text(f"Problemas con la Api")

    if '/BOT:REPORTE_LCENTREGAS_' in message:
        try:
            user = message.split("_")[-2]
            number = int(message.split("_")[-1])
            api_url = f'http://www.linkp.online/api/v1/api_linkcoins/{user}/reporte_entrega/'
            response = requests.request('GET', api_url)
            if response.status_code == 200:
                entregas = response.json()
                for n in range(number):
                    update.message.reply_text(f"Entrego {entregas['entrega'][n]['cantidad']} monedas a {entregas['entrega'][n]['destino']} el {entregas['entrega'][n]['fecha']}")
            else:
                update.message.reply_text(f"Problemas con la Api")
        except:
            update.message.reply_text(f"Tu pedido tiene un error")

    if message == '/BOT:REPORTE_LC_GENERAL':
        update.message.reply_text("Listo para consultar")
    
    if message == '/BOT:REPORTE':
        update.message.reply_text(
"""
Okey:
- /bot:reporte_lc_{user} para reporte de un usuario
- /bot:reporte_lcentregas_{user}_{n} para reporte de las ultimas n entregas que hizo un usuario
- /bot:reporte_lc_general para datos generales
""")

def saldo(update,context):
    try:
        update.message.reply_text("Proximamente")

    except (ValueError):
        update.message.reply_text("No puedo encontrar el saldo de este proyecto")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("saldo", saldo))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, pizza))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()