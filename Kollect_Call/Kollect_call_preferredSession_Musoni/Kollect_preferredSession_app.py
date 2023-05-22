#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:03:10 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]:
from flask import Flask,request,abort
import json
import pyfiles.model_train_predictions as MTP
import yaml
import logging
from logging.handlers import RotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# In[Flask initialization]
app = Flask(__name__)
app.config.from_object('pyfiles.config.live_mysqlConfig')

# In[Logger]:
"""
Logger instialization and setup
"""
if app.debug is not True:   
    
    file_handler = RotatingFileHandler(app.config['VAR_ERROR_LOG'], maxBytes=1024 * 1024 * 100, backupCount=app.config['VAR_ERROR_BK_COUNT'])
    logging.getLogger(app.config['VAR_LOGGER_TYPE']).setLevel(logging.DEBUG)
    formatter = logging.Formatter(app.config['VAR_ERROR_FORMAT'])
    file_handler.setFormatter(formatter)
    logging.getLogger(app.config['VAR_LOGGER_TYPE']).addHandler(file_handler)
    app.logger.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

# In[Error handler]
"""
Error handler
"""
@app.errorhandler(400)
def err_handler(error):
    
    app.logger.exception(error)
    response = json.dumps({'STATUS': app.config['VAR_STATUS_ERROR']})
    return response

# In[Model Train]:
"""
Method for training XGB Model
"""
def train_model():
    
    try:
        result = MTP.to_kollectCall_preferredSession_xgbClassifier_modelTraining()
        return result
    except:
        abort(400)

# In[Model Prediction]
"""
Method for Prediction - XGB Model
"""
@app.route('/kollectCall_preferredSession_xgbClassifier_modelPredictions',methods=['GET','POST'])
def get_model_predictions():
   
    try:
        data = json.loads(request.get_data())
        result = MTP.to_kollectCall_preferredSession_xgbClassifier_modelPredictions(data)
        return result
    except:
        abort(400)

# In[flask app run]
"""
Flask app run with automatic background scheduler
"""
if __name__ == '__main__':
    # Background Scheduler initialization
    scheduler = BackgroundScheduler(timezone=app.config['VAR_SCHEDULER_MODELTRAIN_TIMEZONE'])
    # python method with interval [seconds,minutes,hours,days]
    scheduler.add_job(func=train_model, trigger="interval", hours=app.config['VAR_SCHEDULER_MODELTRAIN_INTERVAL'])
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    app.run(host='0.0.0.0',port=2017, debug=False, threaded=True,use_reloader=False)
else :
    with open('config/logging.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
        
        
        
    