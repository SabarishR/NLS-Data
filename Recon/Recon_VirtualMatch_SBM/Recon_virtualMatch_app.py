#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  22 13:08:03 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]:
from flask import Flask,abort,request,Response
import json
import pyfiles.pattern_handler as PH
import yaml
import logging
from logging.handlers import RotatingFileHandler
from multiprocessing import Process

# In[Flask initialization]
app = Flask(__name__)
app.config.from_object('pyfiles.config.live_mysqlConfig')

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
    response = json.dumps({'STATUS': app.config['VAR_STATUS_ERROR']})
    return response

# In[Virtual recon match]
"""
Method for Virtual match
"""
@app.route('/recon_virtualMatch_customModel',methods=['GET','POST'])
def get_model_predictions():
   
    with app.app_context():
        try:
            data = json.loads(request.get_data())
            # result = PH.to_loop_available_accounts(data)
            process = Process(target = recon_background_function,daemon=True,args=(str(data['ID'])))
            process.start()
            return Response(response = '{"Process": "Asynchronous", "Status": "Started"}', mimetype='application/json',status=200)
        except:
            abort(400)      
        
# In[Asynchronous function]       
"""
Backgrpound function
"""
def recon_background_function(ID):
    
    with app.app_context():    
        result = PH.to_loop_available_accounts(ID)
    
        return result

# In[flask app run]
"""
Flask app run with automatic background scheduler
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2018, debug=False, threaded=True,use_reloader=False)
else :
    with open('config/logging.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
        
        
    