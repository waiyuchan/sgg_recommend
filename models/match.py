# -*- coding: utf-8 -*-
"""
Created on Mon May 18 01:53:47 2020

@author: zmddzf
"""

from . import db

class ApplicantsModel(db.Model):
    """
    申请人表格映射
    """
    __tablename__ = 'match_applicants_t'
    index = db.Column(db.INTEGER)
    aid = db.Column(db.INTEGER, primary_key = True)
    codes = db.Column(db.TEXT)
    location = db.Column(db.TEXT)
    
class OfferModel(db.Model):
    """
    录取信息表格映射
    """
    __tablename__ = 'offer_t'
    index = db.Column(db.INTEGER, primary_key = True)
    aid = db.Column(db.INTEGER)
    major = db.Column(db.INTEGER)
    result = db.Column(db.INTEGER)
    tschool = db.Column(db.INTEGER)