import os 
import sys 

from os import path 
from datetime import datetime, timedelta

APP_NAME = 'Simple Chat App'

BASEDIR = os.path.abspath(os.path.dirname(__file__))
# DEBUG
DEBUG = True 

SECRET_KEY = 'ca2b84ac72a91a20cbda8be2d1f2c1fb7521'

# telegram configs 
TELEGRAM_BOT_TOKEN = os.getenv(TELEGRAM_BOT_TOKEN, '')
TELEGRAM_BOT_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

