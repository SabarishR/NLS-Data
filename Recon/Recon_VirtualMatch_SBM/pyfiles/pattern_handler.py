#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  22 15:03:40 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from flask import current_app as app
import pyfiles.DB_connection as DBC
import pyfiles.functions as CF
import pandas as pd
from datetime import datetime

# In[function for loop all available accounts]
def to_loop_available_accounts(ID):

    ACC_df = DBC.mysql_readTable(app.config['MYSQL_SELECT_DISTINCT_ACCOUNT_NO'])
    ACC_df = ACC_df['ACCOUNT_NUMBER'].tolist()
    
    for acc_no in ACC_df:
        try :
            app.logger.info("ACC NO = {}, API_EXECUTION_ID = {}".format(str(acc_no),ID))
            data = to_recon_virtualMatch_customModel(acc_no)
            param = {
                        "ACCOUNT_NO" : acc_no,
                        "RESPONSE" : data,
                        "CREATED_BY":app.config['VAR_ML_USERNAME'],
                        "CREATED_ON":datetime.now()
                    }
            DBC.mysql_insertData(app.config['MYSQL_INSERT_RECON_EXECUTION_HISTORY'],param)
        except:
            pass
        
    param = {
                "ID" : ID
            }   
    DBC.mysql_updateData(app.config['MYSQL_ASYNCHRONOUS_COMPLETE'],param)
     
    return "SUCCESS"

# In[function for Recon Virtual custom Model]
def to_recon_virtualMatch_customModel(acc_no):
    
    # To fetch the unmatched records against the account number
    param = {
                "ACCOUNT_NUMBER" : str(acc_no)
            }
    GL_df = DBC.mysql_readTable(app.config['MYSQL_SELECT_STATEMENTENTRY'],param)
    RE_df = DBC.mysql_readTable(app.config['MYSQL_SELECT_NOSTROENTRY'],param)
    # Convering id to int
    GL_df[app.config['VAR_GL_ID']] = GL_df[app.config['VAR_GL_ID']].astype(app.config['VAR_DATATYPE_INT'])
    RE_df[app.config['VAR_RE_ID']] = RE_df[app.config['VAR_RE_ID']].astype(app.config['VAR_DATATYPE_INT'])
    
    # Filtering and removing existing match
    matched_GL = DBC.mysql_readTable(app.config['MYSQL_POSSIBLE_MATCH_STATEMENT_ID'],param)
    matched_RE = DBC.mysql_readTable(app.config['MYSQL_POSSIBLE_MATCH_NOSTRO_ID'],param)
    # Find existing possible matched ID's
    GL_list = CF.fn_existingGLID(matched_GL)
    RE_list = CF.fn_existingREID(matched_RE)
    # Filter the possible match statement id
    GL_df = GL_df[~GL_df[app.config['VAR_GL_ID']].isin(GL_list)]
    GL_df = CF.fn_reset_dfIndex(GL_df)
    # Filter the possible match nostro id
    RE_df = RE_df[~RE_df[app.config['VAR_RE_ID']].isin(RE_list)]
    RE_df = CF.fn_reset_dfIndex(RE_df)
    
    # Converting to time_stamp
    GL_df[app.config['VAR_GL_DATE']] = pd.to_datetime(GL_df[app.config['VAR_GL_DATE']])
    RE_df[app.config['VAR_RE_DATE']] = pd.to_datetime(RE_df[app.config['VAR_RE_DATE']])
    # Remove negative signs if exists
    GL_df[app.config['VAR_GL_AMOUNT']] = GL_df[app.config['VAR_GL_AMOUNT']].abs()
    # Adding negative sign to Debit transactions
    GL_df.loc[(GL_df[app.config['VAR_GL_CRDR']] == app.config['VAR_DEBIT_TYPE']), app.config['VAR_GL_AMOUNT']] =  GL_df[app.config['VAR_GL_AMOUNT']]*-1
    # Replace CRDR value
    RE_df[app.config['VAR_RE_CRDR']] = RE_df[app.config['VAR_RE_CRDR']].replace(['CREDIT', 'DEBIT'], [app.config['VAR_CREDIT_TYPE'],app.config['VAR_DEBIT_TYPE']])
    
    # Virtual match custom algorithm
    data = CF.fn_recon_virtualMatch(GL_df,RE_df,acc_no)
    
    return data