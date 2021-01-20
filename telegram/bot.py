#!/usr/bin/env python 
import os 
import sys 
from os import path 

# set path manually 
app_path = path.dirname( path.dirname( path.abspath(__file__) ) )
sys.path.append(app_path)

import requests
import json 
import time 
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_URL

class telegram_bot:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.url = TELEGRAM_BOT_URL

    def get_updates(self, offset=None):
        url = self.url + "/getUpdates?timeout=100"
        if offset:
            url = url + f"&offset={offset+1}"
        
        url_info = requests.get(url)
        return json.loads(url_info.content)

    def send_message(self, msg, chat_id):
        url = self.url + f"/sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url)

    def grab_token(self):
        return self.token