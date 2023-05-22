#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 29 13:45:05 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]
from flask import current_app as app
import pyfiles.DB_connection as DBC
from datetime import datetime

# In[function for insert loan split details]
def fn_insert_loan_arrangementid_details(data,total_loan_arr_id,charged_loan_arr_id,not_charged_loan_arr_id,staff_loan_arr_id):
    
    param = {
            'START_DATE' : data['START_DATE'],
            'END_DATE' : data['END_DATE'],
            'TOTAL_LOAN' : total_loan_arr_id,
            'CHARGED_LOAN' : charged_loan_arr_id,
            'NOT_CHARGED_LOAN' : not_charged_loan_arr_id,
            'STAFF_LOAN' : staff_loan_arr_id,
            'CREATED_BY' : app.config['VAR_ML_USERNAME'],
            'CREATED_ON' : datetime.now()
        }
    DBC.oracle_insertData(app.config['ORACLE_INSERT_LOAN_ARRANGEMENTID_DETAILS'],param)
    
# In[function for insert fd split details]
def fn_insert_fd_arrangementid_details(data,total_fd_arr_id,fd_normal_arr_id,fd_review_arr_id):
    
    param = {
            'CURRENCY' : data['CURRENCY'],
            'BAND_LIMIT' : str(data['BAND_LIMIT']),
            'START_DATE' : data['START_DATE'],
            'END_DATE' : data['END_DATE'],
            'TOTAL_FD' : total_fd_arr_id,
            'FD_NORMAL' : fd_normal_arr_id,
            'FD_REVIEW' : fd_review_arr_id,
            'CREATED_BY' : app.config['VAR_ML_USERNAME'],
            'CREATED_ON' : datetime.now()
        }
    DBC.oracle_insertData(app.config['ORACLE_INSERT_FD_ARRANGEMENTID_DETAILS'],param)
    
# In[function for insert output details]
def fn_insert_output_details(userinput,output):
    
    data = {
        "INPUT":userinput,
        "OUTPUT":output,
        "CREATED_BY":app.config['VAR_ML_USERNAME'],
        "CREATED_ON":datetime.now()
        }
    
    DBC.oracle_insertData(app.config['ORACLE_INSERT_IP_OP_DETAILS'],data)

