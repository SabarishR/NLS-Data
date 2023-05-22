#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:41:03 2021

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]:
from flask import Flask,request
import json
import pyfiles.model_train_predictions as ML

app = Flask(__name__)

# In[Functions Start]:
@app.route('/train_model', methods=['GET', 'POST'])
def train_model():
    data = json.loads(request.get_data())
    
    result = ML.Model_Training(data)
    
    return result

@app.route('/get_model_predictions',methods=['GET','POST'])
def get_model_predictions():
    data = json.loads(request.get_data())
    
    result = ML.Model_Prediction(data)
    
    return result

if __name__ == '__main__':
    app.config.from_object('pyfiles.config.baseconfig')
    app.run(host='0.0.0.0',port=5001, debug=False, threaded=True)