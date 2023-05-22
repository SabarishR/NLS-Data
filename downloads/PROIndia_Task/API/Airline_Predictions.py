#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 12:50:03 2023

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]:
from flask import Flask,abort,request
import json
import pyfiles.model_Prediction as MP
import yaml
import logging
from logging.handlers import RotatingFileHandler

# In[Flask initialization]
app = Flask(__name__)
app.config.from_object('pyfiles.config.common_config')

# In[Logger]:
"""
Logger instialization and setup
"""
if app.debug is not True:   
    
    # Set format that both loggers will use:
    formatter = logging.Formatter(app.config['VAR_ERROR_FORMAT'])
    
    error_handler = RotatingFileHandler(app.config['VAR_ERROR_LOG'], maxBytes=1024 * 1024 * 100, backupCount=app.config['VAR_ERROR_BK_COUNT'])
    logging.getLogger(app.config['VAR_LOGGER_TYPE']).setLevel(logging.DEBUG)
    error_handler.setFormatter(formatter)
    logging.getLogger(app.config['VAR_LOGGER_TYPE']).addHandler(error_handler)
    # added error handler
    app.logger.setLevel(logging.ERROR)
    app.logger.addHandler(error_handler)
    # added information handler
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(error_handler)

# In[Error handler]
"""
Error handler
"""
@app.errorhandler(400)
def err_handler(error):
    
    app.logger.exception(error)
    response = json.dumps({app.config['VAR_STATUS']: app.config['VAR_STATUS_ERROR']})
    return response

# In[API ANN Model]
"""
Method for Airline Prediction
"""
@app.route('/Airline_Predictions',methods=['GET','POST'])
def get_model_predictions():
   
    try:
        data = json.loads(request.get_data())
        Satisfaction = MP.fn_Model_ANN(data)
        return Satisfaction
    except:
        abort(400)

# In[flask app run]
"""
Flask app run
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2020, debug=False, threaded=True,use_reloader=False)
else :
    with open('config/logging.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
        
        
    