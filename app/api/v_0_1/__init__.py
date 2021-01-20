#!/usr/bin/env python 
from flask import Blueprint, url_for

import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Api

# Fix of returning swagger.json on HTTP
@property
def specs_url(self):
    """
    The Swagger specifications absolute url (ie. `swagger.json`)

    :rtype: str
    """
    return url_for(self.endpoint('specs'), _external=False)


Api.specs_url = specs_url

# api blueprint 
api_v_0_1 = Blueprint('api_v.0.1', __name__, url_prefix='/api/v.0.1')

# config api v.0.1 definition + doc path 
api = Api(
    api_v_0_1,
    title='Simple Conversation Engine API',
    version=0.1,
    description='Conversation REST API version 0.1',
    doc='/doc/'
)

# import namespace from api v1 lists
from app.api.v_0_1.qa import api as api_qna

api.add_namespace(api_qna, path='/dodolbots')