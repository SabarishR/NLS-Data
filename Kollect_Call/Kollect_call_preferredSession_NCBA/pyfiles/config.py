#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:41:03 2021

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from os import environ
import json
import cryptocode

# In[basic app config]:
class common_config(object):
    VAR_ACTIVITY_TYPE = 'CALL'
    VAR_SESSION_COLUMNNAME = 'SESSION'
    VAR_FREQUENCY_COLUMNNAME ='FREQ'
    VAR_PREFERREDSESSION_COLUMNAME = 'PREF_SESSION'
    VAR_DATETIME_SESSION_SPLIT = [0,3,5,9,12,14,16,18,20,23]
    VAR_SESSIONS =['Late_Night','Early_Morning','Morning','Late_Morning','Afteroon','Late_Afternoon','Evening','Late_Evening','Night']
    VAR_TRAINTESTSPLIT_RANDOMSTATE = 4  
    VAR_XGB_CLASSIFIER_CLEANSED_CSV = 'data/xgb_callsession_classifier.csv'
    VAR_XGB_CLASSIFIER_SCALAR_NAME = 'Models/xgb_callsession_scalar'
    VAR_XGB_CLASSIFIER_MODEL = 'xgb_callsession_classifier'
    VAR_XGB_CLASSIFIER_MODEL_NAME = 'Models/xgb_callsession_classifier'
    VAR_MODEL_FILE_FORMAT = '.pkl'
    VAR_ML_USERNAME = environ.get('DEV_ML_USERNAME')
    VAR_XGB_CLASSIFIER_ONEHOT_LIST = ["RESIDENCE","GENDER","PROMISE_SUCCESS","REPAY_CURRENCY","CUSTOMER_STATUS","STAGE"]
    VAR_SCHEDULER_MODELTRAIN_TIMEZONE = 'UTC'
    VAR_SCHEDULER_MODELTRAIN_INTERVAL = 240
    VAR_STATUS_ERROR = "error"
    VAR_LOGGER_TYPE ="werkzeug"
    VAR_ERROR_LOG ="log/errorlog.log"
    VAR_ERROR_FORMAT = "\n-------------------------------------------------------------------------\n Datetime - %(asctime)s & Filename - %(name)s & Type - %(levelname)s \n-------------------------------------------------------------------------\n %(message)s"
    VAR_ERROR_BK_COUNT = 200000000
    VAR_OUTCOME_LIST = 'data/NCBA_Outcomes.csv'
    VAR_CALL_PICKED = 'PICKED'
    VAR_OUTCOME = 'OUTCOME'
    
    VAR_XGB_CLASSIFIER_OPTIMAL_PARAM = {
                                            "n_estimators" : 50,
                                            "max_depth" : 10,
                                            "eta" : 0.1,
                                            "eval_metric" : "error",
                                            "objective" : "multi:softmax"
                                        }
    
    VAR_CUSTOMER_RISK_STATUS_LABEL = {"CUSTOMER_RISK_STATUS" : {
                                                                    "A1":1,"A2":1,"A3":3,"A4":4,"A5":5,"A6":6,"A7":7,"A8":8,"A9":9,
                                                                    "A10":10,"A11":11,"A12":12,"A13":13,"A14":14,"A15":15,"A16":16,"A17":17,
                                                                    "A18":18,"A19":19,"A20":20,"B1":21,"B2":22,"B3":23,"B4":24,"B5":25,
                                                                    "B6":26,"B7":27,"B8":28,"B9":29,"B10":30,"B11":31,"B12":32,"B13":33,
                                                                    "B14":34,"B15":35,"B16":36,"B17":37,"B18":38,"B19":39,"B20":40 
                                                                }
                                     }
                             
# In[MYSQL QUERIES]
class mysqlQueries(common_config):
    MYSQL_SELECT_CUSTOMERINFORMATION = "select  ID,GENDER,CUSTOMER_RISK_STATUS,INDUSTRY,RESIDENCE,CUSTOMER_STATUS,PROMISE_SUCCESS,TIME_STAMP,REPAY_CURRENCY,STAGE from customer$information where outcome in ("
    MYSQL_SELECT_XGB_CLASSIFIER_MODELINFORMATION = "SELECT * FROM classification$model$information WHERE ID = ( SELECT MAX(ID) FROM classification$model$information where MODEL_NAME = '"+common_config.VAR_XGB_CLASSIFIER_MODEL+"')"
    MYSQL_INSERT_MODELINFORMATION = ("INSERT INTO classification$model$information"
                                     "(MODEL_NAME,FILE_NAME,SCALAR_NAME,ACCURACY,F1_SCORE,SENSITIVITY,SPECIFICITY,FALSE_POSITIVE,FALSE_NEGATIVE,DATASET_COLUMNS,ONEHOT_LIST,CREATED_BY,CREATED_ON)"
                                     "VALUES (%(MODEL_NAME)s, %(FILE_NAME)s,%(SCALAR_NAME)s, %(ACCURACY)s, %(F1_SCORE)s,%(SENSITIVITY)s, %(SPECIFICITY)s, %(FALSE_POSITIVE)s, %(FALSE_NEGATIVE)s,%(DATASET_COLUMNS)s,%(ONEHOT_LIST)s,%(CREATED_BY)s, %(CREATED_ON)s)")
    MYSQL_SELECT_CUSTOMERINFORMATION_USINGID = "select ID,TIME_STAMP from customer$information where ID = %(ID)s AND  PROMISE_SUCCESS = %(PROMISE_SUCCESS)s"
    MYSQL_INSERT_MODELPREDICTION = ("INSERT INTO classification$model$prediction"
                                    "(MODEL_ID,INPUT,OUTPUT,CREATED_BY,CREATED_ON)"
                                    "VALUES (%(MODEL_ID)s, %(INPUT)s,%(OUTPUT)s,%(CREATED_BY)s, %(CREATED_ON)s)")
# In[MYSQL CONNECTION]    
class dev_mysqlConfig(mysqlQueries):
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('DEV_MYSQL_USER'),
                                  'password':cryptocode.decrypt(environ.get('DEV_MYSQL_PASSWORD'), environ.get('DEV_ENCRYPTION_KEY')),
                                  'host': environ.get('DEV_MYSQL_HOST'),
                                  'port': environ.get('DEV_MYSQL_PORT'),
                                  'database': environ.get('DEV_MYSQL_DB'),
                                  'auth_plugin' : environ.get('DEV_MYSQL_AUTH_PLUGIN'),
                                  'raise_on_warnings': json.loads(environ.get('DEV_MYSQL_RAISE_WARNING').lower())
                              }
    
# In[MYSQL CONNECTION]    
class cloudTesting_mysqlConfig(mysqlQueries):
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('CLOUDTESTING_MYSQL_USER'),
                                  'password': cryptocode.decrypt(environ.get('CLOUDTESTING_MYSQL_PASSWORD'), environ.get('CLOUDTESTING_ENCRYPTION_KEY')),
                                  'host': environ.get('CLOUDTESTING_MYSQL_HOST'),
                                  'port': environ.get('CLOUDTESTING_MYSQL_PORT'),
                                  'database': environ.get('CLOUDTESTING_MYSQL_DB'),
                                  'auth_plugin' : environ.get('CLOUDTESTING_MYSQL_AUTH_PLUGIN'),
                                  'raise_on_warnings': json.loads(environ.get('CLOUDTESTING_MYSQL_RAISE_WARNING').lower())
                              }
    
# In[MYSQL CONNECTION]    
class live_mysqlConfig(mysqlQueries):
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('LIVE_MYSQL_USER'),
                                  'password': cryptocode.decrypt(environ.get('LIVE_MYSQL_PASSWORD'), environ.get('LIVE_ENCRYPTION_KEY')),
                                  'host': environ.get('LIVE_MYSQL_HOST'),
                                  'port': environ.get('LIVE_MYSQL_PORT'),
                                  'database': environ.get('LIVE_MYSQL_DB'),
                                  'auth_plugin' : environ.get('LIVE_MYSQL_AUTH_PLUGIN'),
                                  'raise_on_warnings': json.loads(environ.get('LIVE_MYSQL_RAISE_WARNING').lower())
                              }