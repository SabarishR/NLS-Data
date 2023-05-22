#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 03 15:11:24 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from os import environ
from sqlalchemy.engine.url import URL

# In[basic app config]:
class common_config(object):
    VAR_TRANSACTION_CODE = 'TRANSACTION_CODE'
    VAR_CHARGE_TRANSACTION_CODE = 'CHARGE_TRANSACTION_CODE'
    VAR_TAX_TRANSACTION_CODE = 'TAX_TRANSACTION_CODE'
    VAR_TRANS_REFERENCE = 'TRANS_REFERENCE'
    VAR_TRANSACTION_TYPE = "TRANSACTION_TYPE"
    VAR_AMOUNT_LCY = "AMOUNT_LCY"
    VAR_TRANSACTION_AMOUNT = "TRANSACTION_AMOUNT"
    VAR_CHARGE_AMOUNT = "CHARGE_AMOUNT"
    VAR_TAX_AMOUNT = "TAX_AMOUNT"
    VAR_TIME_STAMP = "TIME_STAMP"
    VAR_EXPECTED_CHARGE ="EXPECTED_CHARGE"
    VAR_EXPECTED_TAX = "EXPECTED_TAX"
    VAR_CHARGE_DEVIATION = "CHARGE_DEVIATION"
    VAR_TAX_DEVIATION = "TAX_DEVIATION"
    VAR_OVERALL_DEVIATION = "OVERALL_DEVIATION"
    VAR_PRECISELY_CHARGED = "PRECISELY_CHARGED"
    VAR_ACCURATE_CHARGE = "ACCURATE_CHARGE"
    VAR_ACCURATE_TAX = "ACCURATE_TAX"
    VAR_CHARGE_CODE = "CHARGE_CODE"
    VAR_DATE_TIME = "DATE_TIME"
    VAR_TAX = "TAX"
    VAR_TRANSACTION_TYPES = ['TRANSACTION_AMOUNT','CHARGE_AMOUNT','TAX_AMOUNT']
    LEVEL_BAND_SEP = "^"
    VAR_TRANSACTION_NAME = "TRANSACTION_NAME"
    VAR_STATUS_SUCCESS = "SUCCESS"
    VAR_STATUS_NO_DATA = "NO DATA"
    VAR_STATUS_ERROR = "ERROR"
    VAR_LOGGER_TYPE ="werkzeug"
    VAR_ERROR_LOG ="log/errorlog.log"
    VAR_ERROR_FORMAT = "\n-------------------------------------------------------------------------\n Datetime - %(asctime)s & Filename - %(name)s & Type - %(levelname)s \n-------------------------------------------------------------------------\n %(message)s"
    VAR_ERROR_BK_COUNT = 200000000
    VAR_ML_USERNAME = "ML_USER"
    
# In[MYSQL QUERIES]
class mysqlQueries(common_config):
    
    MYSQL_DF_INSERT_DAYWISE_TRANS_REFERENCE = "daywise$trans_reference$details"
    MYSQL_DF_INSERT_DAYWISE_TRANSACTION_ANALYSIS = "daywise$transaction$analysis"
    
    MYSQL_SELECT_TRANSACTION_CHARGE_CODES = "select * from transaction$charge$codes where TRANSACTION_CODE = %(TRANSACTION_CODE)s"
    MYSQL_SELECT_STATEMENT_ENTRY = "SELECT AMOUNT_LCY,TRANSACTION_CODE,TRANS_REFERENCE,TIME_STAMP from statement$entry_2022_jan12 where cast(TIME_STAMP as date) between %(START_DATE)s and %(END_DATE)s and TRANSACTION_CODE in ("
    MYSQL_SELECT_BANK_CHARGE_TYPE_HIS = "select id,FLAT_AMOUNT,CALC_TYPE,PERCENTAGE,UPTO_AMOUNT,MINIMUM_AMOUNT,MAXIMUM_AMOUNT,DATE_TIME from bnk_charge$types$history where id REGEXP %(CHARG_CODE)s"
    MYSQL_SELECT_BANK_CHARGE_TYPES_REGEXP = "select id,FLAT_AMOUNT,CALC_TYPE,PERCENTAGE,UPTO_AMOUNT,MINIMUM_AMOUNT,MAXIMUM_AMOUNT,DATE_TIME from bnk_charge$types where id REGEXP %(CHARG_CODE)s"
    MYSQL_SELECT_BANK_CHARGE_TYPES = "select bct.id,tcc.TRANSACTION_CODE,bct.CALCULATION_BASIS,bct.FLAT_AMOUNT,bct.CALC_TYPE,bct.PERCENTAGE,bct.UPTO_AMOUNT,bct.MINIMUM_AMOUNT,bct.MAXIMUM_AMOUNT,tcc.TAX from bnk_charge$types bct inner join transaction$charge$codes tcc on bct.id = tcc.CHARGE_CODE where tcc.TRANSACTION_CODE = %(TRANSACTION_CODE)s"
    MYSQL_SELECT_DAYWISE_TRANSREFERENCE_TIMESTAMP = "SELECT TIME_STAMP from daywise$transaction$analysis where cast(TIME_STAMP as date) between %(START_DATE)s and %(END_DATE)s and TRANSACTION_CODE = %(TRANSACTION_CODE)s and IS_REGENERATED = FALSE"
    MYSQL_SELECT_DAYWISE_TRANSREFERENCE = "select * from daywise$trans_reference$details where TIME_STAMP between %(START_DATE)s and %(END_DATE)s and TRANSACTION_CODE = %(TRANSACTION_CODE)s and IS_REGENERATED = FALSE"
    MYSQL_SELECT_DAYWISE_TRANSACTION_ANALYSIS = "select * from daywise$transaction$analysis where TIME_STAMP between %(START_DATE)s and %(END_DATE)s and TRANSACTION_CODE = %(TRANSACTION_CODE)s and IS_REGENERATED = FALSE"
    MYSQL_SELECT_DAYWISE_TRANSREFERENCE_INPUTID = "select * from daywise$trans_reference$details where INPUT_ID = %(INPUT_ID)s"
    MYSQL_SELECT_DAYWISE_TRANSACTION_ANALYSIS_INPUTID = "select * from daywise$transaction$analysis where INPUT_ID = %(INPUT_ID)s"
    
    MYSQL_INSERT_TRANS_REFERENCE_DETAILS = ("INSERT INTO transaction$trans_reference$details"
                                            "(TRANSACTION_TYPE,TRANSACTION_CODE,START_DATE,END_DATE,EXPECTED_CHARGES,PRECISELY_CHARGED,NOT_PRECISELY_CHARGED,MISSING_CHARGE,MISSING_TAX_BUT_CHARGE_PRESENT,WRONG_CHARGE,REVENUE_LOSS_IN_CHARGE,REVENUE_EXTRA_IN_CHARGE,REVENUE_LOSS_IN_TAX,REVENUE_EXTRA_IN_TAX,REVENUE_BELOW_ACCEPTANCE_IN_CHARGE,REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE,CREATED_BY,CREATED_ON)"
                                            "VALUES (%(TRANSACTION_TYPE)s, %(TRANSACTION_CODE)s,%(START_DATE)s,%(END_DATE)s, %(EXPECTED_CHARGES)s,%(PRECISELY_CHARGED)s,%(NOT_PRECISELY_CHARGED)s,%(MISSING_CHARGE)s,%(MISSING_TAX_BUT_CHARGE_PRESENT)s,%(WRONG_CHARGE)s,%(REVENUE_LOSS_IN_CHARGE)s,%(REVENUE_EXTRA_IN_CHARGE)s,%(REVENUE_LOSS_IN_TAX)s,%(REVENUE_EXTRA_IN_TAX)s,%(REVENUE_BELOW_ACCEPTANCE_IN_CHARGE)s,%(REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE)s,%(CREATED_BY)s,%(CREATED_ON)s)")
    MYSQL_INSERT_IP_OP_DETAILS = ("INSERT INTO transaction_input$output$details"
                                    "(TRANS_REFERENCE_DETAIL_ID,INPUT,OUTPUT,CREATED_BY,CREATED_ON)"
                                    "VALUES (%(detail_id)s, %(INPUT)s,%(OUTPUT)s,%(CREATED_BY)s, %(CREATED_ON)s)")
    
    MYSQL_UPDATE_IP_OP_DETAILS = "UPDATE transaction_input$output$details SET TRANS_REFERENCE_DETAIL_ID = %(detail_id)s,OUTPUT = %(OUTPUT)s,CREATED_ON =  %(CREATED_ON)s where ID = %(id)s"
    
    MYSQL_DELETE_DAYWISE_TRANSACTION_ANALYSIS = "delete from daywise$transaction$analysis where TIME_STAMP = %(CURRENT_DATE)s"
    MYSQL_DELETE_DAYWISE_TRANS_REFERENCE = "delete from daywise$trans_reference$details where TIME_STAMP = %(CURRENT_DATE)s"
    
# In[MYSQL CONNECTION]    
class dev_mysqlConfig(mysqlQueries):
    
    MYSQL_SQLALCHEMY_URL = URL(
                                drivername=environ.get('DEV_MYSQL_DRIVER_NAME'), 
                                host=environ.get('DEV_MYSQL_HOST'),
                                port=environ.get('DEV_MYSQL_PORT'),
                                username=environ.get('DEV_MYSQL_USER'),
                                password=environ.get('DEV_MYSQL_PASSWORD'),
                                database=environ.get('DEV_MYSQL_DB')
                               )
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('DEV_MYSQL_USER'),
                                  'password': environ.get('DEV_MYSQL_PASSWORD'),
                                  'host': environ.get('DEV_MYSQL_HOST'),
                                  'port': environ.get('DEV_MYSQL_PORT'),
                                  'database': environ.get('DEV_MYSQL_DB'),
                                  'auth_plugin' : "mysql_native_password",
                                  'raise_on_warnings': True
                              }
    
    
# In[MYSQL CONNECTION]    
class cloudTesting_mysqlConfig(mysqlQueries):
    
    MYSQL_SQLALCHEMY_URL = URL(
                                drivername=environ.get('CLOUDTESTING_MYSQL_DRIVER_NAME'), 
                                host=environ.get('CLOUDTESTING_MYSQL_HOST'),
                                port=environ.get('CLOUDTESTING_MYSQL_PORT'),
                                username=environ.get('CLOUDTESTING_MYSQL_USER'),
                                password=environ.get('CLOUDTESTING_MYSQL_PASSWORD'),
                                database=environ.get('CLOUDTESTING_MYSQL_DB')
                               )
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('CLOUDTESTING_MYSQL_USER'),
                                  'password': environ.get('CLOUDTESTING_MYSQL_PASSWORD'),
                                  'host': environ.get('CLOUDTESTING_MYSQL_HOST'),
                                  'port': environ.get('CLOUDTESTING_MYSQL_PORT'),
                                  'database': environ.get('CLOUDTESTING_MYSQL_DB'),
                                  'auth_plugin' : "mysql_native_password",
                                  'raise_on_warnings': True
                              }