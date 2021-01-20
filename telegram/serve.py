#!/usr/bin/env python 
import os 
import sys 
from os import path 
import time 
import json 
import requests

# set path manually 
app_path = path.dirname( path.dirname( path.abspath(__file__) ) )
sys.path.append(app_path)
print(app_path)

from telegram.bot import telegram_bot
from app.question_answering import approximate_answers

update_id = 1
try:
    with open('telegram/log/log_id.txt', 'r') as f:
        update_id = f.readline() 
        update_id = int(update_id)
except Exception as e:
    print(e)

t_bot = telegram_bot()

while True:
    print('...check message... latest update id is: {}'.format(update_id))
    updates = t_bot.get_updates(offset=update_id)
    print(updates)
    updates = updates['result']
    print(updates)
    if updates:
        for item in updates:
            update_id = item['update_id']
            print(update_id)
            try:
                message = item['message']['text']
                print(message)
            except Exception as e:
                print(e)
                message = None

            from_id = item['message']['from']['id']
            print(from_id)
            
            if message:
                # if start 
                if message == '/start':
                    t_bot.send_message("Halo, aku Kinara, malu bertanya sesat di mana? nah boleh nanya siapa tau kita jodoh ye kan?, \nkalau keliatan maksa ya namanya juga usaha *love", from_id)

                else:
                    # make reply from approx message 
                    # answer, max_score, prediction = approximate_answers(message)
                    
                    # get from api service instead of direct module 
                    resp_json = None 
                    payload = {
                        'query': message
                    }
                    resp = requests.post(os.getenv('QA_API_URL', 'http://localhost:8080') + '/api/v.0.1/dodolbots/getAnswer', json=payload)
                    if resp.status_code == 200:
                        resp_json = resp.json()

                    if resp_json:
                        t_bot.send_message(resp_json['answer'], from_id)
                        time.sleep(2)

                    else:
                        t_bot.send_message('API QA System unavailable...')

    # update latest update id 
    with open('telegram/log/log_id.txt', 'w') as f:
        f.write(str(update_id))
    # sleep 
    time.sleep(8)
