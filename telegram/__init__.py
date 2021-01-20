#!/usr/bin/env python 
import os 
import sys 
from os import path 

# set path manually 
app_path = path.dirname( path.dirname( path.abspath(__file__) ) )
sys.path.append(app_path)