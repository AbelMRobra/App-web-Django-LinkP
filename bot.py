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

    if(update.message.text.upper().find("HOLA") > 0):
        update.message.reply_text("Hola!, necesitas ayuda?")

    if(update.message.text.upper().find("AYUDA") > 0):
        update.message.reply_text('''
        Puedo ayudar!, escribe "Saber sobre .." y elige un tema
        
        Linkcoins:
        *LINKCOINS-EXPLICACIÓN
        *LINKCOINS-SISTEMA

        Indice Link:
        *INDICE-LINK-IVA

        Área compras:
        *SOLICITUDES-COMPRA
        
        
        ''')

    if(update.message.text.upper().find("INDICE-LINK-IVA") > 0):
        update.message.reply_text("El cálculo del IVA se realiza al actualizar un presupuesto, el mismo se cálcula de la siguiente manera: Imprevisto + Saldos MO y MAT + credito + fdr por 0.07875")

    if(update.message.text.upper().find("LINKCOINS-EXPLICACIÓN") > 0):
        update.message.reply_text("Linkcoins es un sistema de premios de Link Inversiones!, funciona de la siguiente manera: Todos los meses que trabajes para Link, recibiras 10 monedas que puedes entregar a tus compañeros reconociendo su apoyo. Las monedas que recibas podras canjearlas por premios. Si quieres saber mas escribe 'Quiero saber sobre LINKCOINS-SISTEMA'")

    if(update.message.text.upper().find("SOLICITUDES-COMPRA") > 0):
        update.message.reply_text(" Las solicitudes de compra es el medio por el cual la dirección aprueba una OC previamente realizada en Tango gestión. Debes tener los permisos correspondientes")


    if(update.message.text.upper().find("LINKCOINS-SISTEMA") > 0):
        update.message.reply_text("Todos los meses siendo un empleado ACTIVO recibiras 10 monedas que puedes entregar ingresando a www.linkp.online")

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