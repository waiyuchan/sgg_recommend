# -*- coding: utf-8 -*-
"""
Created on Mon May 18 01:13:19 2020

@author: zmddzf
"""
from flask import Flask
from flask_restful import Api
# 导入各资源类
from resources.recommend import *
from routes import api_v1
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///match.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(api_v1, url_prefix='/api/v1')
api = Api(app)


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=False)