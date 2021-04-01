# -*- coding: utf-8 -*-
"""
Created on Mon May 18 01:31:10 2020

@author: zmddzf
"""
from flask import Blueprint
from flask_restful import Api
from resources import *

api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

api.add_resource(recommend.RecommendResource, '/recommend')

