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
# In[basic app config]:
class common_config(object):
    VAR_ACCOUNT_TURNOVER_RANGE = 'data/ACC_TURNOVER_RANGE.csv'
    VAR_AGE_RANGE = 'data/AGE_RANGE.csv'
    VAR_CRB_CHECK_RANGE = 'data/CRB_SCORE_RANGE.csv'
    VAR_PROPOSED_LOAN_RANGE = 'data/PROPOSED_LOAN_RANGE.csv'
    VAR_DF_BINNING_COL = 'BAND'
    VAR_DF_WEIGHT_COL = 'WEIGHT'
    VAR_DF_MIN_COL = 'MIN'
    VAR_DF_MAX_COL = 'MAX'
    VAR_GENDER = {
                    "M" : 0,
                    "F" : 1
                 }
    VAR_GENDER_TO_REPLACE = {
                                0:1, 
                                1:1.3
                            }
    VAR_AVG_TRUNOVER_MIN = 2500
    VAR_AVG_TRUNOVER_MAX = 170000
    VAR_DATAFRAME_COLUMNS = ['ACCOUNT_TURNOVER','CRB_CHECK','GENDER','AGE','AVG_TURNOVER']
    VAR_ACCOUNT_TURNOVER_COL = 'ACCOUNT_TURNOVER'
    VAR_CRB_CHECK_COL = 'CRB_CHECK'
    VAR_GENDER_COL = 'GENDER'
    VAR_AGE_COL = 'AGE'
    VAR_AVG_TURNOVER = 'AVG_TURNOVER'
    VAR_ACCOUNT_TURNOVER_WEIGHT_COL = 'ACCOUNT_TURNOVER_WEIGHT'
    VAR_CRB_CHECK_WEIGHT_COL = 'CRB_CHECK_WEIGHT'
    VAR_GENDER_WEIGHT_COL = 'GENDER_WEIGHT'
    VAR_AGE_WEIGHT_COL = 'AGE_WEIGHT'
    VAR_CUSTOMER_WEIGHT_COL = 'CUSTOMER_WEIGHT'
    VAR_CUSTOMER_SCORE_COL = 'CUSTOMER_SCORE'
    VAR_LOAN_AMOUNT = 'LOAN_AMOUNT'
    VAR_COL_FOR_CUSTOMER_WEIGHT_SUM = ['ACCOUNT_TURNOVER_WEIGHT','CRB_CHECK_WEIGHT','GENDER_WEIGHT','AGE_WEIGHT']
    VAR_TOTAL_WEIGHT = 23.2
    VAR_LOAN_AMT_LESSTHEN_MINLOANAMT = 0
    VAR_LOAN_AMT_LESSTHEN_MINTURNOVER = 0
    VAR_MIN_LOAN_APPROVED_AMT = 1000
    VAR_MAX_LOAN_APPROVED_AMT = 50000
    VAR_MAX_LOAN_AMOUNT_FORMODEL = 52500
    VAR_RF_REGRESSPR_COLUMNS_LIST = ['ACCOUNT_TURNOVER','CRB_CHECK','GENDER','AGE','AVG_TURNOVER','CUSTOMER_WEIGHT','LOAN_AMOUNT']
    VAR_TRAINTESTSPLIT_RANDOMSTATE = 4  
    VAR_PREDICTOR_COLUMNS = ['CUSTOMER_WEIGHT','LOAN_AMOUNT']
    VAR_RF_REGRESSOR_CLEANSED_CSV = 'data/RF_creditscoring_regressor.csv'
    VAR_RF_REGRESSOR_SCALAR_NAME = 'Models/rf_creditscoring_scalar'
    VAR_RF_REGRESSOR_MODEL = 'rf_creditscoring_regressor'
    VAR_RF_REGRESSOR_MODEL_NAME = 'Models/rf_creditscoring_regressor'
    VAR_MODEL_FILE_FORMAT = '.gz'
    VAR_RF_REGRESSOR_OPTIMAL_PARAM = {
                                        "n_estimators" : 1,
                                        "max_depth" : 20,
                                        "min_samples_split" : 2,
                                        "min_samples_leaf" : 1,
                                        "bootstrap" : False,
                                        "random_state" : 4,
                                        "warm_start" : True
                                    }                            
    VAR_ML_USERNAME = environ.get('DEV_ML_USERNAME')
    VAR_MIN_CRB_SCORE = 600
    VAR_PHONE_NUMBER_PREFIX_REMOVE = 3
    VAR_PHONE_NUMBER_PREFIX_ADD = 'M0'
    VAR_AML_BLOCKLIST_REJECT = "Dear customer. Your account is blocked.please contact the bank"
    VAR_AML_PAR_REJECT = "Dear customer. Your account is blocked.please contact the bank"
    VAR_AGE_REJECT = "Dear customer. Your age is below 18.please contact the bank"
    VAR_AMOUNT_REJECT = "Dear customer. Your loan request has been declined due to poor credit score"
    
# In[MYSQL QUERIES]
class mysqlQueries(common_config):
    
    MYSQL_SELECT_RF_REGRESSOR_MODELINFORMATION = "SELECT * FROM regression$model$information WHERE ID = ( SELECT MAX(ID) FROM regression$model$information where MODEL_NAME = '"+common_config.VAR_RF_REGRESSOR_MODEL+"')"
    MYSQL_SELECT_RF_REGRESSOR_CUSTOMERDETAILS = "select CRB_SCORE,AGE,GENDER from crb$iprs$data where ID_NUMBER = %(ID_NUMBER)s"
    MYSQL_SELECT_RF_REGRESSOR_MOBILEBLOCKEDACCOUNTS = "select ACCOUNT_NUMBER from mobile$blocked$accounts where ACCOUNT_NUMBER = %(ACCOUNT_NUMBER)s"
    MYSQL_SELECT_RF_REGRESSOR_PARREPORTSLOG = "select TELEPHONE from slk$par$report$log where TELEPHONE = %(TELEPHONE)s"
    MYSQL_INSERT_MODELINFORMATION = ("INSERT INTO regression$model$information"
                                     "(MODEL_NAME,FILE_NAME,SCALAR_NAME,R2SCORE,EXPLAINEDVARIANCE,MAE,MSE,RMSE,CREATED_BY,CREATED_ON)"
                                     "VALUES (%(MODEL_NAME)s, %(FILE_NAME)s,%(SCALAR_NAME)s, %(R2SCORE)s, %(EXPLAINEDVARIANCE)s,%(MAE)s, %(MSE)s, %(RMSE)s,%(CREATED_BY)s, %(CREATED_ON)s)")
    MYSQL_INSERT_MODELPREDICTION = ("INSERT INTO regression$model$prediction"
                                    "(MODEL_ID,INPUT,OUTPUT,CREATED_BY,CREATED_ON)"
                                    "VALUES (%(MODEL_ID)s, %(INPUT)s,%(OUTPUT)s,%(CREATED_BY)s, %(CREATED_ON)s)")
# In[MYSQL CONNECTION]    
class dev_mysqlConfig(mysqlQueries):
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('DEV_MYSQL_USER'),
                                  'password': environ.get('DEV_MYSQL_PASSWORD'),
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
                                  'password': environ.get('CLOUDTESTING_MYSQL_PASSWORD'),
                                  'host': environ.get('CLOUDTESTING_MYSQL_HOST'),
                                  'port': environ.get('CLOUDTESTING_MYSQL_PORT'),
                                  'database': environ.get('CLOUDTESTING_MYSQL_DB'),
                                  'auth_plugin' : environ.get('CLOUDTESTING_MYSQL_AUTH_PLUGIN'),
                                  'raise_on_warnings': json.loads(environ.get('CLOUDTESTING_MYSQL_RAISE_WARNING').lower())
                              }