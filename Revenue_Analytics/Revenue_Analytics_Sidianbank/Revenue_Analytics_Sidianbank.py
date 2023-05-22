#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 03 12:12:20 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]:
from flask import Flask,request,abort
import json
import pyfiles.analytics as AY
import logging
from logging.handlers import RotatingFileHandler
# In[Flask initialization]
app = Flask(__name__)
app.config.from_object('pyfiles.config.dev_mysqlConfig')

# In[Error Handling]:
if app.debug is not True:   
    
    file_handler = RotatingFileHandler(app.config['VAR_ERROR_LOG'], maxBytes=1024 * 1024 * 100, backupCount=app.config['VAR_ERROR_BK_COUNT'])
    logging.getLogger(app.config['VAR_LOGGER_TYPE']).setLevel(logging.DEBUG)
    formatter = logging.Formatter(app.config['VAR_ERROR_FORMAT'])
    file_handler.setFormatter(formatter)
    logging.getLogger(app.config['VAR_LOGGER_TYPE']).addHandler(file_handler)
    app.logger.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

# In[Error handler]
@app.errorhandler(400)
def err_handler(error):
    
    app.logger.exception(error)
    response = json.dumps({'STATUS': app.config['VAR_STATUS_ERROR']})
    return response

# In[Revenue Analytcics]
"""
Method for Revenue Analytics
"""
@app.route('/get_revenue_analysis',methods=['GET','POST'])
def get_revenue_analysis():
   
    try:
        data = json.loads(request.get_data())
        result = AY.to_get_revenue_analysis(data)
        return result
    except:
        abort(400)
# In[flask app run]

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2011, debug=False, threaded=True,use_reloader=False)
    