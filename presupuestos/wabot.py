import json
import requests
import datetime

class WABot():
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['messages']
        self.APIUrl = 'https://api.chat-api.com/instance304624/'
        self.token = 'cat0hd37m7imu8cz'

    def send_message(self, chatId, text):
        data = {"chatId" : chatId,
                "body" : text}
        answer = self.send_requests('sendMessage', data)
        return answer
        

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

