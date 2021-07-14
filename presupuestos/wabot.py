import json
import requests
import datetime

class WABot():
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['messages']
        self.APIUrl = 'https://api.chat-api.com/instance304624/'
        self.token = 'cat0hd37m7imu8cz'

    def send_message(self, phone, text):
        data = {"phone" : phone,
                "body" : text}
        answer = self.send_requests('sendMessage', data)
        return answer
        

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    

response_servidor = {
    "sent": True,
    "messages": "Perri",
    "id": "true_543814986359@c.us_3EB02EDBB05B8CDECF8B",
    "queueNumber": 1
    }

mensaje_prueba = WABot(response_servidor)
mensaje_prueba.send_message("543813023087", "River siempre fue mejor que BOCA, aceptalo")