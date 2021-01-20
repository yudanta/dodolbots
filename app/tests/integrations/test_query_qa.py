#!/usr/bin/env python 
import unittest
import json 
from app import app 

API_VERSION = '/api/v.0.1'
QA_ENDPOINT = '/dodolbots/getAnswer'

class TestQueryQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_query_bot(self):
        payload = {
            'query': 'di mana ibu kota indonesia?'
        }

        resp = self.app.post(''.join([API_VERSION, QA_ENDPOINT]), json=payload, content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        resp_data = json.loads(resp.data.decode())
        self.assertTrue('answer' in resp_data)