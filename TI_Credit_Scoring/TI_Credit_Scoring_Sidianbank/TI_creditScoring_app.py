#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  24 10:41:03 2021

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]:
from flask import Flask,request
import json
import pyfiles.model_train_predictions as MTP
import yaml

# In[Flask initialization]
app = Flask(__name__)
app.config.from_object('pyfiles.config.dev_mysqlConfig')
# In[Model Train]:
"""
Method for training RF Model
"""
@app.route('/TI_creditScoring_rfRegressor_modelTraining',methods=['GET','POST'])
def train_model():
    
    result = MTP.to_TI_creditScoring_rfRegressor_modelTraining()
    
    return result

# In[Model Prediction]
"""
Method for Prediction - RF Model
"""
@app.route('/TI_creditScoring_rfRegressor_modelPredictions',methods=['GET','POST'])
def get_model_predictions():
    
    data = json.loads(request.get_data())
    
    result = MTP.to_TI_creditScoring_rfRegressor_modelPredictions(data)
    
    return result

# In[flask app run]

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2014, debug=False, threaded=True,use_reloader=False)
else :
    with open('config/logging.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    
