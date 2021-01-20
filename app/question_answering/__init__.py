#!/usr/bin/env python 
import re 
import pandas as pd 
from Levenshtein import ratio

from app import qa_datasets

def approximate_answers(q):
    max_score = 0
    answers = ""
    prediction = ""
    
    for idx, row in qa_datasets.iterrows():
        score = ratio(row['Question'], q)
        if score >= 0.8:
            return row['Answer'], score, row['Question']
        
        elif score > max_score:
            max_score = score
            answer = row["Answer"]
            prediction = row["Question"]

    if max_score > 0.51:
        return answer, max_score, prediction

    else:
        return "Maap aku gak ngerti kamu ngomong apa... :(", max_score, prediction
            