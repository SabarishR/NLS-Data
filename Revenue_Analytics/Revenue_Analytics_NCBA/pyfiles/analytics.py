#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 29 16:10:03 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from flask import current_app as app
import pyfiles.DB_connection as DBC
import pyfiles.functions as CF
import pandas as pd
import json

# In[function for loan analysis]:
def to_get_loan_analysis(data):
    
    # reading data from oracle database
    df = DBC.oracle_readTable(app.config['ORACLE_SELECT_LOAN_DETAILS'])
    # removing  duplicates
    df = df.drop_duplicates([app.config['VAR_ID'],app.config['VAR_CUSTOMER_ID']],ignore_index = True)
    # datetime conversion
    df[app.config['VAR_CONTRACT_DATE']] = pd.to_datetime(df[app.config['VAR_CONTRACT_DATE']], format=app.config['VAR_ORACLE_DATE_FORMAT'])
    # filtering datetange
    df = df.loc[(df[app.config['VAR_CONTRACT_DATE']] >= data['START_DATE']) & (df[app.config['VAR_CONTRACT_DATE']] <= data['END_DATE'])]
    
    if(len(df) > 0):    
        # calculations
        total_loans = len(df)
        charged_loans = len(df.loc[df[app.config['VAR_CHARGED_CUSTOMER']].notnull()])
        not_charged_loans = len(df.loc[(df[app.config['VAR_CHARGED_CUSTOMER']].isnull()) & (df[app.config['VAR_DESCRIPTION']] != app.config['VAR_STAFF_VAL'])])
        staff_loans = len(df.loc[(df[app.config['VAR_CHARGED_CUSTOMER']].isnull()) & (df[app.config['VAR_DESCRIPTION']] == app.config['VAR_STAFF_VAL'])])
        
        # arrangement id split
        split = app.config['VAR_SPLIT']
        total_loan_arr_id = split.join(df[app.config['VAR_ID']].tolist())
        charged_loan_arr_id = split.join(df.loc[df[app.config['VAR_CHARGED_CUSTOMER']].notnull()].ID.tolist())
        not_charged_loan_arr_id = split.join(df.loc[(df[app.config['VAR_CHARGED_CUSTOMER']].isnull()) & (df[app.config['VAR_DESCRIPTION']] != app.config['VAR_STAFF_VAL'])].ID.tolist())
        staff_loan_arr_id = split.join(df.loc[(df[app.config['VAR_CHARGED_CUSTOMER']].isnull()) & (df[app.config['VAR_DESCRIPTION']] == app.config['VAR_STAFF_VAL'])].ID.tolist())
    
        # insert arrangement id split details
        CF.fn_insert_loan_arrangementid_details(data,total_loan_arr_id,charged_loan_arr_id,not_charged_loan_arr_id,staff_loan_arr_id)
        
        # output
        output = {
                'STATUS' : app.config['VAR_STATUS_SUCCESS'],
                'TOTAL_LOANS' : total_loans,
                'CHARGED_LOANS' : charged_loans,
                'NOT_CHARGED_LOANS' : not_charged_loans,
                'STAFF_LOANS' : staff_loans,
                'CHARGED_LOAN_PERCENTAGE' : str(round(charged_loans/total_loans*100,2))+'%',
                'NOT_CHARGED_LOAN_PERCENTAGE' : str(round(not_charged_loans/total_loans*100,2))+'%',
                'STAFF_LOAN_PERCENTAGE' : str(round(staff_loans/total_loans*100,2))+'%',
                'TOTAL_LOAN_ARRANGEMENT_ID' : total_loan_arr_id,
                'CHARGED_LOAN_ARRANGEMENT_ID' : charged_loan_arr_id,
                'NOT_CHARGED_LOAN_ARRANGEMENT_ID' : not_charged_loan_arr_id,
                'STAFF_LOAN_ARRANGEMENT_ID' : staff_loan_arr_id
            }
    else:
        
        output = {
                    "STATUS" : app.config['VAR_STATUS_NO_DATA']
                 }
    # inserting input,output details
    CF.fn_insert_output_details(json.dumps(data),json.dumps(output))
        
    return json.dumps(output)

# In[function for fd analysis]:
def to_get_fd_analysis(data):
    
    # reading data from oracle database
    df = DBC.oracle_readTable(app.config['ORACLE_SELECT_FD_REPORT_UG'],[data['CURRENCY']])
    # datetime conversion
    df[app.config['VAR_DATE_OF_BOOKED']] = pd.to_datetime(df[app.config['VAR_DATE_OF_BOOKED']], format=app.config['VAR_ORACLE_DATE_FORMAT'])
    # filtering datetange
    df = df.loc[(df[app.config['VAR_DATE_OF_BOOKED']] >= data['START_DATE']) & (df[app.config['VAR_DATE_OF_BOOKED']] <= data['END_DATE'])]
    
    if(len(df) > 0):
        # data type conversion
        df[app.config['VAR_INTEREST_RATE']] = df[app.config['VAR_INTEREST_RATE']].astype('float')
        # calculations
        total_fd = len(df)
        fd_normal = len(df.loc[(df[app.config['VAR_INTEREST_RATE']] >= data['BAND_LIMIT'][0]) & (df[app.config['VAR_INTEREST_RATE']] <= data['BAND_LIMIT'][1])])
        fd_review = len(df.loc[(df[app.config['VAR_INTEREST_RATE']] < data['BAND_LIMIT'][0]) | (df[app.config['VAR_INTEREST_RATE']] > data['BAND_LIMIT'][1])])
        
        # arrangement id split
        split = app.config['VAR_SPLIT']
        total_fd_arr_id = split.join(df[app.config['VAR_ARRANGEMENT_ID']].tolist())
        fd_normal_arr_id = split.join(df.loc[(df[app.config['VAR_INTEREST_RATE']] >= data['BAND_LIMIT'][0]) & (df[app.config['VAR_INTEREST_RATE']] <= data['BAND_LIMIT'][1])].ARRANGEMENT_ID.tolist())
        fd_review_arr_id = split.join(df.loc[(df[app.config['VAR_INTEREST_RATE']] < data['BAND_LIMIT'][0]) | (df[app.config['VAR_INTEREST_RATE']] > data['BAND_LIMIT'][1])].ARRANGEMENT_ID.tolist())
        
        # insert arrangement id split details
        CF.fn_insert_fd_arrangementid_details(data,total_fd_arr_id,fd_normal_arr_id,fd_review_arr_id)
        
        # output
        output = {
            'STATUS' : app.config['VAR_STATUS_SUCCESS'],
            'CURRENCY' : data['CURRENCY'],
            'TOTAL_FD' : total_fd,
            'FD_NORMAL' : fd_normal,
            'FD_REVIEW' : fd_review,
            'FD_NORMAL_PERCENTAGE' : str(round(fd_normal/total_fd*100,2))+'%',
            'FD_REVIEW_PERCENTAGE' : str(round(fd_review/total_fd*100,2))+'%',
            'TOTAL_FD_ARRANGEMENT_ID' : total_fd_arr_id,
            'FD_NORMAL_ARRANGEMENT_ID' : fd_normal_arr_id,
            'FD_REVIEW_ARRANGEMENT_ID' : fd_review_arr_id
        }
        
    else:
        
        output = {
                    "STATUS" : app.config['VAR_STATUS_NO_DATA']
                 }
    # inserting input,output details
    CF.fn_insert_output_details(json.dumps(data),json.dumps(output))    
    
    return json.dumps(output)
    
