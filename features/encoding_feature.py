# -*- coding: utf-8 -*-
"""
Created on Mon May 18 16:20:07 2020

@author: zmddzf
"""

from keras.models import load_model
import numpy as np

# 自动编码器读取
encoder = load_model("./utils/encoder.h5")

def encode_feature(feature_list):
    """
    对特征进行编码
    """
    vector = np.array(feature_list).reshape(1,109)
    codes = encoder.predict(vector)
    codes = (codes >= 0.5).astype(int)
    codes = ''.join([str(i) for i in codes[0].tolist()])
    return codes
    
    
    
    