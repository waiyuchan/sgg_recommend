# -*- coding: utf-8 -*-
"""
Created on Mon May 18 02:31:01 2020

@author: zmddzf
"""

from flask import current_app, abort
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.match import *
from features.extract_feature import *
from features.encoding_feature import *
import pandas as pd

class RecommendResource(Resource):
    """
    示例profile list资源类
    """

    def __init__(self):
        self.parser = RequestParser()
    
    def post(self):
        """
        进行推荐
        """
        # 参数设定
        self.parser.add_argument("gpa", type=float, required=True)
        self.parser.add_argument("gre", type=float, required=True)
        self.parser.add_argument("gmat", type=float, required=True)
        self.parser.add_argument("school", type=str, required=True)
        self.parser.add_argument("ielts", type=float, required=True)
        self.parser.add_argument("toefl", type=int, required=True)
        self.parser.add_argument("marker", type=str, required=True)
        self.parser.add_argument("major", type=str, required=True)
        
        # 解析参数
        # 内部接口不再进行参数校验
        args = self.parser.parse_args()
        
        gpa = args['gpa']
        gre = args['gre']
        gmat = args['gmat']
        school = args['school']
        ielts = args['ielts']
        toefl = args['toefl']
        marker = args['marker']
        major = args['major']
        
        # 进行特征提取
        feature_list = process_feature(gpa, gre, gmat, school, ielts, toefl, marker, major)
        code = encode_feature(feature_list)
        
        # 设定查询参数
        neighbor_size = 500  # 近邻个数
        school_num = 8  # 推荐学校的个数
        
        
        try:
            # 邻近查找sql
            sql1 = "select aid, length(replace( codes & '{}','0','')) as weight from match_applicants_t order by weight limit {};".format(code, neighbor_size)
            neighbors = dict(db.session.execute(sql1).fetchall())
            
            # 查找邻居录取的学校
            sql2 = "select aid, tschool from offer_t where aid in {}".format(str(tuple(neighbors.keys())))
            schools = db.session.execute(sql2).fetchall()
            
            # 查询所有学校录取占比
            sql3 = "select tschool, count(tschool) from offer_t group by tschool;"
            ratio = dict(db.session.execute(sql3).fetchall())
            count = sum(ratio.values())
        except SQLAlchemyError as e:
            print(e)
            return {"status": 500, "msg": "Internal Server Error", "data":{}}
        
        
        # 转为DataFrame
        neighbors = pd.DataFrame(neighbors.items(), columns=['aid', 'weight'])
        schools = pd.DataFrame(schools, columns=['aid', 'tschool'])
        schools_ratio = schools.groupby('tschool').count() / len(schools)
        schools_ratio.columns=['ratio']
        
        # 连接数据表格
        table = pd.merge(schools, neighbors, on='aid', how='left').merge(schools_ratio, on='tschool', how='left')
        
        # 获取最可能的前k个学校
        table['prob'] = 1 / table['weight'] * table['ratio']
        recom_schools = table.groupby('tschool').max()['prob'].sort_values(ascending=False)[:school_num]
        recom_schools = recom_schools / recom_schools.sum()
        recom_schools = recom_schools.to_dict()
        
        # 生成返回结果
        result = {}
        for school in recom_schools:
            result[school] = [recom_schools[school], ratio[school]/count]
        
        return {"status": 200, "msg": "Success", "data": result}

