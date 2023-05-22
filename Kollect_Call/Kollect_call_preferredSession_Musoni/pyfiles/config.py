#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:05:56 2022

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
    VAR_TIME_STAMP = 'TIME_STAMP'
    VAR_DATETIME_SESSION_SPLIT = [0,3,5,9,12,14,16,18,20,23]
    VAR_SESSIONS =['Late_Night','Early_Morning','Morning','Late_Morning','Afteroon','Late_Afternoon','Evening','Late_Evening','Night']
    VAR_TRAINTESTSPLIT_RANDOMSTATE = 4  
    VAR_XGB_CLASSIFIER_CLEANSED_CSV = 'data/xgb_callsession_classifier.csv'
    VAR_XGB_CLASSIFIER_SCALAR_NAME = 'Models/xgb_callsession_scalar'
    VAR_XGB_CLASSIFIER_MODEL = 'xgb_callsession_classifier'
    VAR_XGB_CLASSIFIER_MODEL_NAME = 'Models/xgb_callsession_classifier'
    VAR_MODEL_FILE_FORMAT = '.pkl'
    VAR_ML_USERNAME = environ.get('DEV_ML_USERNAME')
    VAR_XGB_CLASSIFIER_ONEHOT_LIST = ["PROMISE_SUCCESS","LOAN_STATUS","STAGE"]
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
    VAR_LOAN_TYPE = 'LOAN_TYPE'
    VAR_BRANCH = 'BRANCH'
    VAR_PROMISE_SUCCESS = 'PROMISE_SUCCESS'
    VAR_LOAN_STATUS = 'LOAN_STATUS'
    VAR_CUSTOMER_STATUS = 'CUSTOMER_STATUS'
    
    VAR_XGB_CLASSIFIER_OPTIMAL_PARAM = {
                                            "n_estimators" : 50,
                                            "max_depth" : 10,
                                            "eta" : 0.1,
                                            "eval_metric" : "error",
                                            "objective" : "multi:softmax"
                                        }
                             
# In[MYSQL QUERIES]
class mysqlQueries(common_config):
    MYSQL_SELECT_CUSTOMERINFORMATION = "select ID,BRANCH,CUSTOMER_STATUS,PROMISE_SUCCESS,TIME_STAMP,LOAN_STATUS,LOAN_TYPE,STAGE from customer$information"
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