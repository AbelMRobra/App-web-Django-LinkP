import requests

## Bot para enviar mensajes por Telegram

def bot_telegram(send, id, token):
    
    url = "https://api.telegram.org/bot" + token + "/sendMessage"

    params = {
        'chat_id' : id,
        'text' : send
    }

    requests.post(url, params=params)
