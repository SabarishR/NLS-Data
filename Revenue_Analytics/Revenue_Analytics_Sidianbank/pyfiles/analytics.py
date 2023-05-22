#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 03 13:10:03 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from flask import current_app as app
# from Kollect_preferredSession_app import flask_app as app
import pyfiles.DB_connection as DBC
import pyfiles.functions as CF
import pyfiles.calculations as CL
import pandas as pd
import json
from datetime import datetime

# In[function for revenue analysis]:
def to_get_revenue_analysis(data):
    
    # storing current date for future purpose. analytics code may take much time, based on data load. so storing the current date at the initial
    CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')
    # selecting the charge_code and tax_code
    param = {
                "TRANSACTION_CODE": data['TRANSACTION_CODE']
            }
    TRANSACTION_CHARGE_CODES = DBC.mysql_readTable(app.config['MYSQL_SELECT_TRANSACTION_CHARGE_CODES'],param)
    # for regerate the report without fetching histories
    INPUT_ID = None
    if (TRANSACTION_CHARGE_CODES['IS_ALWAYS_REGENERATE'][0] == True):
        INPUT_ID = CF.fn_insert_output_details(None,json.dumps(data),None)
    # get the transaction,charge,tax code list
    TRANSACTION_CODE = CF.fn_unique_list(TRANSACTION_CHARGE_CODES,app.config['VAR_TRANSACTION_CODE'])
    CHARGE_CODE = [TRANSACTION_CHARGE_CODES[app.config['VAR_CHARGE_TRANSACTION_CODE']][0]]
    TAX_CODE = CF.fn_unique_list(TRANSACTION_CHARGE_CODES,app.config['VAR_TAX_TRANSACTION_CODE'])
    # validating and removing None from the tax code
    TAX_CODE = [x for x in TAX_CODE if x is not None]
    # converting codes to list
    CODES = TRANSACTION_CODE + CHARGE_CODE + TAX_CODE
    # converting list to string
    FILTER_CODES = ','.join(CODES)
    
    # list of dates with frequency of month between start and end date
    date_list = CF.fn_monthwise_datelist(data['START_DATE'],data['END_DATE'])
    #loop the datelist for analysis in monthwise
    for i in range (0,len(date_list)):
        
        # for finding start and end date
        if(len(date_list) == 1):
            START_DATE = date_list[i]
            END_DATE = date_list[i]
        elif(i == (len(date_list)-1)):
                break
        else:
            START_DATE = date_list[i]
            END_DATE = date_list[i + 1]
        # selecting the data using filter codes
        query = app.config['MYSQL_SELECT_STATEMENT_ENTRY'] + FILTER_CODES +')'
        param = {
                    "START_DATE" : START_DATE,
                    "END_DATE" : END_DATE,
                    "TRANSACTION_CODE" : data['TRANSACTION_CODE']
                }
        df = DBC.mysql_readTable(query,param)
        # for regerate the report without fetching histories
        if (TRANSACTION_CHARGE_CODES['IS_ALWAYS_REGENERATE'][0] == False):
            # getting the dates already having history
            history_df = DBC.mysql_readTable(app.config['MYSQL_SELECT_DAYWISE_TRANSREFERENCE_TIMESTAMP'],param)
            # converting time_stamp as list
            history_df[app.config['VAR_TIME_STAMP']] = pd.to_datetime(history_df[app.config['VAR_TIME_STAMP']])
            history_dates = history_df[app.config['VAR_TIME_STAMP']].dt.strftime('%Y-%m-%d').unique().tolist()
            
            # timestamp string to datetime conversion
            df[app.config['VAR_TIME_STAMP']] = pd.to_datetime(df[app.config['VAR_TIME_STAMP']])
            # converting date_time column to date column to filter
            df['DATE'] = df[app.config['VAR_TIME_STAMP']].dt.date
            df['DATE'] = pd.to_datetime(df['DATE'])
            # filtering dates which has the history records
            df = df[~df['DATE'].isin(history_dates)]
            df = CF.fn_dfResetIndex(df) 
                
        # removing annotations from trans reference
        df[app.config['VAR_TRANS_REFERENCE']] = df[app.config['VAR_TRANS_REFERENCE']].str.split("\\").str[0]
        # filtering transaction charge code data's for trans reference
        TRANS_REFERENCE = CF.fn_dfFilter_values(df,app.config['VAR_TRANSACTION_CODE'],TRANSACTION_CODE)
        TRANS_REFERENCE = TRANS_REFERENCE[[app.config['VAR_TRANS_REFERENCE']]]
        TRANS_REFERENCE = CF.fn_dfResetIndex(TRANS_REFERENCE)
        
        # converting trans reference as list
        TRANS_REFERENCE = CF.fn_unique_list(TRANS_REFERENCE,app.config['VAR_TRANS_REFERENCE'])
        # filtering charge code data's using trans reference
        df = CF.fn_dfFilter_values(df,app.config['VAR_TRANS_REFERENCE'],TRANS_REFERENCE)
        df = CF.fn_dfResetIndex(df)
        
        # performing further if the dataframe length greater then zero
        if (len(df) > 0):
            # creating list for map the code with respective transactions
            TRANSACTION_CODES = [TRANSACTION_CODE,CHARGE_CODE,TAX_CODE]
            TRANSACTION_JSON = CF.fn_nestedlist_tojson(app.config['VAR_TRANSACTION_TYPES'],TRANSACTION_CODES)
            df = CF.fn_mapReplace_dfValues(df,app.config['VAR_TRANSACTION_CODE'],app.config['VAR_TRANSACTION_TYPE'],TRANSACTION_JSON)
            
            # pivoting the table using TRANS_REFERENCE
            df_pivot = df.pivot_table(index=[app.config['VAR_TRANS_REFERENCE']], columns=app.config['VAR_TRANSACTION_TYPE'], values=app.config['VAR_AMOUNT_LCY']).reset_index()
            df_pivot = CF.fn_fillNA(df_pivot,0)
            df = CF.fn_merge_twoDataframe(df,df_pivot,app.config['VAR_TRANS_REFERENCE'])
            df = CF.fn_dfFilter_values(df,app.config['VAR_TRANSACTION_TYPE'],[app.config['VAR_TRANSACTION_AMOUNT']])
            df = CF.fn_dfResetIndex(df)
            df = CF.fn_dropduplicates(df,[app.config['VAR_TRANS_REFERENCE']])
            # converting transaction amount negative sign to positive sign
            df[app.config['VAR_TRANSACTION_AMOUNT']] = df[app.config['VAR_TRANSACTION_AMOUNT']].abs()
            #filtering the columns
            df = df[[app.config['VAR_TRANS_REFERENCE'],app.config['VAR_TRANSACTION_CODE'],app.config['VAR_TRANSACTION_AMOUNT'],app.config['VAR_CHARGE_AMOUNT'],app.config['VAR_TAX_AMOUNT'],app.config['VAR_TIME_STAMP']]]
            # charge amount which has sum of both charge and tax in negative sign
            # summing up the both charge in tax in positive sign will gives the exact charge amount
            df.loc[(df[app.config['VAR_CHARGE_AMOUNT']] != 0),app.config['VAR_CHARGE_AMOUNT']] = df[[app.config['VAR_CHARGE_AMOUNT'],app.config['VAR_TAX_AMOUNT']]].sum(axis=1)  
            # converting charge amount negative sign to positive sign
            df[app.config['VAR_CHARGE_AMOUNT']] = df[app.config['VAR_CHARGE_AMOUNT']].abs()
            # timestamp string to datetime conversion
            df[app.config['VAR_TIME_STAMP']] = pd.to_datetime(df[app.config['VAR_TIME_STAMP']])
            
            # selecting the unique charge codes for validating history 
            CHARGE_CODE = CF.fn_unique_list(TRANSACTION_CHARGE_CODES,app.config['VAR_CHARGE_CODE'])
            # joing the codes with '|' if multiple for MYSQL REGEXP query
            FILTER_CHARGE_CODES = '|'.join(CHARGE_CODE)
            # checking for history records
            param = {
                        'CHARG_CODE': FILTER_CHARGE_CODES
                    }
            CHARGE_HIS = DBC.mysql_readTable(app.config['MYSQL_SELECT_BANK_CHARGE_TYPE_HIS'],param)
            # charge history flag
            is_charge_history = len(CHARGE_HIS)
            
            # selecting the charge table if has history and merging with history records
            if(is_charge_history != 0):
                df_charges = DBC.mysql_readTable(app.config['MYSQL_SELECT_BANK_CHARGE_TYPES_REGEXP'],param)
                # merging chare table with charge history table
                df_charges = pd.concat([df_charges,CHARGE_HIS], ignore_index=True)
                df_charges = df_charges.sort_values(by=app.config['VAR_DATE_TIME'], ascending=True)
                df_charges = CF.fn_dfResetIndex(df_charges)
                df_charges[app.config['VAR_TRANSACTION_CODE']] = data['TRANSACTION_CODE']
                df_charges['TAX'] = TRANSACTION_CHARGE_CODES[app.config['VAR_TAX']][0]
            else  :
            # if no history directly selecting the records
                param = {
                            "TRANSACTION_CODE": data['TRANSACTION_CODE']
                        }
                df_charges = DBC.mysql_readTable(app.config['MYSQL_SELECT_BANK_CHARGE_TYPES'],param)
              
            # To find respective charge type and do the necessory calculations
            if((is_charge_history == 0) & (df_charges['FLAT_AMOUNT'][0] != None)):
                df = CL.fn_flat_amount_with_no_history(df,df_charges)
            elif((is_charge_history == 0) & ((df_charges['CALC_TYPE'][0] == 'LEVEL') | (df_charges['CALC_TYPE'][0] == 'BAND'))):
                df_charges = CL.fn_level_band_firstchar_validation(df_charges)
                df = CL.fn_single_level_band_with_no_history(df,df_charges)
            elif((is_charge_history == 0) & (df_charges['FLAT_AMOUNT'][0] == None)): 
                df_charges = CL.fn_level_band_firstchar_validation(df_charges)
                df_chg = CL.fn_level_band_split(df_charges,is_charge_history)
                if(df_chg['CALC_TYPE'][0] == "LEVEL"):
                    df = CL.fn_multi_level_with_no_history(df,df_chg)
                elif(df_chg['CALC_TYPE'][0] == "BAND"): 
                    df = CL.fn_multi_band_with_no_history(df,df_chg)
            elif((is_charge_history != 0) & (df_charges['FLAT_AMOUNT'][0] != None)):
                df_charges = CL.fn_history_charges_duration(df_charges)
                df = CL.fn_flat_amount_with_history(df,df_charges)
            elif((is_charge_history == 0) & ((df_charges['CALC_TYPE'][0] == 'LEVEL') | (df_charges['CALC_TYPE'][0] == 'BAND'))):
                df_charges = CL.fn_level_band_firstchar_validation(df_charges)
                df_charges = CL.fn_history_charges_duration(df_charges)
                df = CL.fn_single_level_band_with_history(df,df_charges)
            elif((is_charge_history != 0) & (df_charges['FLAT_AMOUNT'][0] == None)): 
                df_charges = CL.fn_level_band_firstchar_validation(df_charges)
                df_charges = CL.fn_history_charges_duration(df_charges)
                df_chg = CL.fn_level_band_split(df_charges,is_charge_history)
                if(df_chg['CALC_TYPE'][0] == "LEVEL"):
                    df = CL.fn_multi_level_with_history(df,df_chg)
                elif(df_chg['CALC_TYPE'][0] == "BAND"): 
                    df = CL.fn_multi_band_with_history(df,df_chg)
                
            # data type conversion
            df = CF.fn_datatype_conversion(df) 
            # calculations
            df = CF.fn_deviation_calculations(df)
            # convert datetime to yyyy-mm-dd format
            df[app.config['VAR_TIME_STAMP']] = pd.to_datetime(df[app.config['VAR_TIME_STAMP']].dt.strftime('%Y-%m-%d'))
            # To identify unique dates in the DF
            dates = df[app.config['VAR_TIME_STAMP']].dt.strftime('%Y-%m-%d').unique().tolist()
            # To insert day-wise trans_reference details
            CF.fn_insert_daywise_transreference_details(df,data['TRANSACTION_CODE'],dates,INPUT_ID,TRANSACTION_CHARGE_CODES['IS_ALWAYS_REGENERATE'][0])
            # To insert day-wise analysis details
            CF.fn_insert_daywise_analysis_details(df,data['TRANSACTION_CODE'],dates,INPUT_ID,TRANSACTION_CHARGE_CODES['IS_ALWAYS_REGENERATE'][0])
            
        
    # insert trans_reference details
    primary_id = CF.fn_insert_trans_reference_details(TRANSACTION_CHARGE_CODES[app.config['VAR_TRANSACTION_NAME']][0],data['TRANSACTION_CODE'],data['START_DATE'],data['END_DATE'],INPUT_ID,TRANSACTION_CHARGE_CODES['IS_ALWAYS_REGENERATE'][0])
    # required parameters calculations
    output = CF.fn_output_params(primary_id,data['TRANSACTION_CODE'],data['START_DATE'],data['END_DATE'],INPUT_ID,TRANSACTION_CHARGE_CODES['IS_ALWAYS_REGENERATE'][0])
    # inserting the details to the table
    if (TRANSACTION_CHARGE_CODES['IS_ALWAYS_REGENERATE'][0] == True):
        CF.fn_update_output_details(INPUT_ID,primary_id,json.dumps(output))
    else:    
        CF.fn_insert_output_details(primary_id,json.dumps(data),json.dumps(output))
    # deleting the current date records
    param = {
            "CURRENT_DATE":CURRENT_DATE
            }
    DBC.mysql_update_delete_Data(app.config['MYSQL_DELETE_DAYWISE_TRANSACTION_ANALYSIS'],param)
    DBC.mysql_update_delete_Data(app.config['MYSQL_DELETE_DAYWISE_TRANS_REFERENCE'],param)
    # return preffered_session
    return json.dumps(output)

    
    
    
