#!/usr/bin/env python 
import time 
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, Namespace, emit, disconnect, join_room, rooms, leave_room, close_room

async_mode = None

# APP Config
app = Flask(__name__, instance_relative_config=True)

# load config 
app.config.from_object('config')
app.config.from_pyfile('application.cfg', silent=True)

# load qa datasets 
qa_datasets = pd.read_excel(app.config['BASEDIR'] + '/app/datasets/simple_qa_datasets.xlsx') #load with path 

socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')

# global vars
clients = []
users = {}
room_lists = {}
all_chat = {}
thread = None 

# private funcs 
def background_thread():
    count = 0
    while True:
        for key in all_chat:
            if (int(datetime.now().strftime('%s')) - all_chat[key]['last_activity']) >= (60 * 3) and all_chat[key]['exit_msg'] == False:
                print(int(datetime.now().strftime('%s')), all_chat[key]['last_activity'], key)
                socketio.emit('message_response', {
                        'type': 'conversation',
                        'query': '',
                        'response': {
                            'responded_by': 'Kinara',
                            'response_txt': 'Udah bosen chat sama aku ya? yaudah deh kamu exit aja...',
                            'systime': 'Current systime: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        }
                }, room=key, namespace='/dodolbot')

                all_chat[key]['exit_msg'] = True                

        socketio.sleep(60)
        count += 1


def get_username(sid):
    for user in users:
        if users[user] == sid:
            return user

    return None 


@app.route('/', methods=['GET', 'POST'])
def index():
    data = {
        'key': 'value'
    }
    return render_template('index.html', data=data)


# import api + register as blueprint
from app.api.v_0_1 import api_v_0_1
from app.api.v_0_1 import api

app.register_blueprint(api_v_0_1)

# from app.question_answering import approximate_answers

# namespace for web sockets 
class ConversationalChatBot(Namespace):
    def on_connect(self):
        global thread 
        clients.append(request.sid)
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

    def on_register(self, message):
        # register user to list of users 
        # users[message['user']] = request.sid 

        if request.sid not in all_chat:
            all_chat[request.sid] = {
                'last_activity': int(datetime.now().strftime('%s')),
                'exit_msg': False
            }

        # broadcast notif user is connected and send a greeting message 
        emit('chat_response', {
            'type': 'connect',
            'message': 'Halo, aku Kinara, malu bertanya sesat di mana? nah boleh nanya siapa tau kita jodoh ye kan?, \nkalau keliatan maksa ya namanya juga usaha *love',
            'data': {
                'response_from': 'Kinara',
                # 'users': message['user'],
                'sid': request.sid
            }
        }, room=request.sid)

    def on_user_send(self, message):
        print(message['query'])
        all_chat[request.sid]['last_activity'] = int(datetime.now().strftime('%s'))
        all_chat[request.sid]['exit_msg'] = False

        # answer, max_score, prediction = approximate_answers(message['query'])
        resp_json = None 

        # get froma API endpoint instead from direct model
        with app.test_client() as c:
            payload = {
                'query': message['query']
            }
            
            resp = c.post('/api/v.0.1/dodolbots/getAnswer', json=payload)
            
            if resp.status_code == 200:
                # print(answer)
                resp_json = resp.json

        emit('message_response', {
                    'type': 'conversation',
                    'query': message['query'],
                    'response': {
                        'responded_by': 'Kinara',
                        'response_txt': resp_json['answer'] if resp_json else 'API QA System down...',
                        'systime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }, room=request.sid)

    # on disconnect from client 
    def on_disconnect(self):
        print('Client disconnected: {}'.format(request.sid))
        all_chat.pop(request.sid, None)


# register namespace
socketio.on_namespace(ConversationalChatBot('/dodolbot'))
