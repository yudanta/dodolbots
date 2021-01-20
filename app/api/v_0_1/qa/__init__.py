#!/usr/bin/env python 
from datetime import datetime
import json 
import time

import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import request
from flask_restplus import Namespace, Resource, fields, marshal, marshal_with
from app.question_answering import approximate_answers

api = Namespace('QAEngine', description='Question Answering API Engine')

answer_model = api.model('QuestionAnswerModel', {
    'query': fields.String(description='User query string'),
    'answer': fields.String(description="Bot's aswers"),
    'confidence_score': fields.Float(description='confidence score for the returned answer'),
    'profiling_time': fields.Float(description='time elapsed for generating answer')
})

question_query = api.model('QuestionQueryModel', {
    'query': fields.String(description='User question', required=True)
})


@api.route('/getAnswer')
class VideoPresets(Resource):
    @api.doc('Get answers from question string')
    @api.marshal_with(answer_model)
    @api.expect(question_query, validate=True)
    @api.response(200, 'Success', answer_model)
    @api.response(412, 'Parameter required')
    def post(self):
        st = time.time()

        answers = {
            'query': '',
            'answer': '',
            'confidence': 0.0,
            'profiling_time': 0.0
        }

        # json payload 
        json_data = request.json 

        answer, max_score, prediction = approximate_answers(json_data['query'])
        answers['query'] = json_data['query']
        answers['answer'] = answer 
        answers['confidence'] = max_score
        
        elapsed = float(time.time() - st)
        answers['profiling_time'] = elapsed

        return answers 