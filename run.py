#!/usr/bin/env python 
from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=8080, debug=True)