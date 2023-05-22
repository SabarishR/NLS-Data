#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 29 15:11:24 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from os import environ

# In[basic app config]:
class common_config(object):
    
    VAR_ID = 'ID'
    VAR_CUSTOMER_ID = 'CUSTOMER_ID'
    VAR_CONTRACT_DATE = 'CONTRACT_DATE'
    VAR_CHARGED_CUSTOMER = 'CHARGED_CUSTOMER'
    VAR_DESCRIPTION = 'DESCRIPTION'
    VAR_DATE_OF_BOOKED = 'DATE_OF_BOOKED'
    VAR_INTEREST_RATE = 'INTEREST_RATE'
    VAR_ARRANGEMENT_ID = 'ARRANGEMENT_ID'
    VAR_STAFF_VAL = 'Staff'
    VAR_ORACLE_DATE_FORMAT = '%Y%m%d'
    VAR_SPLIT = "^"
    VAR_STATUS_SUCCESS = "SUCCESS"
    VAR_STATUS_NO_DATA = "NO DATA"
    VAR_STATUS_ERROR = "ERROR"
    VAR_LOGGER_TYPE ="werkzeug"
    VAR_ERROR_LOG ="log/errorlog.log"
    VAR_ERROR_FORMAT = "\n-------------------------------------------------------------------------\n Datetime - %(asctime)s & Filename - %(name)s & Type - %(levelname)s \n-------------------------------------------------------------------------\n %(message)s"
    VAR_ERROR_BK_COUNT = 200000000
    VAR_ML_USERNAME = "ML_USER"
    
# In[MYSQL QUERIES]
class oracleQueries(common_config):
    
    ORACLE_SELECT_LOAN_DETAILS = """
                                    select ac.id,ac.contract_date,aa.arr_status,ua.customer_id,fth.charged_customer,t.description from ug_aa$account$details ac
                                    inner join ug_aa_arrangement aa on aa.id = ac.id
                                    inner join ugx_account ua on ua.arrangment_id = ac.id
                                    inner join customer c on c.id = ua.customer_id
                                    inner join target t on t.id = c.target
                                    left join ugx_funds$transfer_history fth on ua.customer_id  = fth.charged_customer
                                    where aa.arr_status = 'CURRENT'
                                  """
    ORACLE_SELECT_FD_REPORT_UG = "select ARRANGEMENT_ID,CURRENCY,INTEREST_RATE,DATE_OF_BOOKED from fixed$deposit$report$data$ug where CURRENCY = :CURRENCY"
    ORACLE_INSERT_LOAN_ARRANGEMENTID_DETAILS = "INSERT INTO loan$arrangement_id$details (START_DATE,END_DATE,TOTAL_LOAN,CHARGED_LOAN,NOT_CHARGED_LOAN,STAFF_LOAN,CREATED_BY,CREATED_ON) VALUES (to_date(:START_DATE,'yyyy-mm-dd'),to_date(:END_DATE,'yyyy-mm-dd'),:TOTAL_LOAN,:CHARGED_LOAN,:NOT_CHARGED_LOAN,:STAFF_LOAN,:CREATED_BY,:CREATED_ON)"
    ORACLE_INSERT_FD_ARRANGEMENTID_DETAILS = "INSERT INTO fd$arrangement_id$details (CURRENCY,BAND_LIMIT,START_DATE,END_DATE,TOTAL_FD,FD_NORMAL,FD_REVIEW,CREATED_BY,CREATED_ON) VALUES (:CURRENCY,:BAND_LIMIT,to_date(:START_DATE,'yyyy-mm-dd'),to_date(:END_DATE,'yyyy-mm-dd'),:TOTAL_FD,:FD_NORMAL,:FD_REVIEW,:CREATED_BY,:CREATED_ON)"
    ORACLE_INSERT_IP_OP_DETAILS = "INSERT INTO ug_analysis_ip$op$details (INPUT,OUTPUT,CREATED_BY,CREATED_ON) VALUES (:INPUT,:OUTPUT,:CREATED_BY,:CREATED_ON)"
    
# In[MYSQL CONNECTION]    
class dev_oracleConfig(oracleQueries):
    
    ORACLE_USERNAME = environ.get('DEV_ORACLE_USER')
    ORACLE_PASSWORD = environ.get('DEV_ORACLE_PASSWORD')
    ORACLE_HOST = environ.get('DEV_ORACLE_HOST')
    ORACLE_PORT = environ.get('DEV_ORACLE_PORT')
    ORACLE_SID = environ.get('DEV_ORACLE_SID')
    
# In[MYSQL CONNECTION]    
class cloudTesting_mysqlConfig(oracleQueries):
    
   ORACLE_USERNAME = environ.get('CLOUDTESTING_ORACLE_USER')
   ORACLE_PASSWORD = environ.get('CLOUDTESTING_ORACLE_PASSWORD')
   ORACLE_HOST = environ.get('CLOUDTESTING_ORACLE_HOST')
   ORACLE_PORT = environ.get('CLOUDTESTING_ORACLE_PORT')
   ORACLE_SID = environ.get('CLOUDTESTING_ORACLE_SID')