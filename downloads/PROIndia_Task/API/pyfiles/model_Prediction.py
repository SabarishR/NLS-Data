#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:02:28 2023

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from flask import current_app as app
import pyfiles.functions as CF
import pandas as pd
import numpy as np
from jsonmerge import merge
import joblib
from keras.models import load_model
import json
# In[function for ANN MODEL]
def fn_Model_ANN(data):
    
    #Dynamic onehot list
    onehot_json = CF.fn_onehot_encode(app.config['VAR_ONEHOT_LIST'],app.config['VAR_INPUT_ONEHOT'],data)
    # Merging input data and one hot list and converting as dataframe
    ip_json = merge(data, onehot_json)
    df = pd.DataFrame(data=ip_json)
    # Sorting columns for model prediction
    df = df[app.config['VAR_SORTED_COLUMNS']]
    # load the saved scalor to transform the data
    ANN_scalar = joblib.load(app.config['VAR_ANN_SCALAR'])
    modelIP = ANN_scalar.transform(df.values)
    
    #load the saved model and making predictions 
    ANN_model = load_model(app.config['VAR_ANN_MODEL'])
    # predict the data and printind desired results
    y_pred = ANN_model.predict(modelIP)
    y_pred = (y_pred > 0.7)
    np.concatenate((y_pred.reshape(len(y_pred),1)))
    if y_pred == True:
        Satisfaction = app.config['VAR_SATISFACTION_CATEGORIES'][0]
    else:
        Satisfaction = app.config['VAR_SATISFACTION_CATEGORIES'][1]
        
    output = {
                app.config['VAR_SATISFACTION'] : Satisfaction
             }
    return json.dumps(output)