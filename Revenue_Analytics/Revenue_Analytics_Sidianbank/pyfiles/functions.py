#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 03 13:15:05 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]
from flask import current_app as app
import pyfiles.DB_connection as DBC
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# In[function to Drop NA]
def fn_unique_list(df,columnname):

    unique_list = df[columnname].unique().tolist()
    
    return unique_list

# In[function for filter with multiple values]
def fn_dfFilter_values(df,filter_col,filter_val):
    
    df = df[df[filter_col].isin(filter_val)]

    return df

# In[function for reset index]
def fn_dfResetIndex(df):
    
    df.reset_index(drop=True, inplace=True)
    
    return df

# In[function for nested list to json]
def fn_nestedlist_tojson(list1,list2):
    
    data = {}
    for i in range(0,len(list1)):
        for j in range(0,len(list2[i])):
            data[list2[i][j]] = list1[i]
            
    return data

# In[function for replace a values in a dataframe]
def fn_mapReplace_dfValues(df,actual_col,new_col,replace_val):
    
    df[new_col] = df[actual_col].map(replace_val)
    
    return df

# In[function for fill NA with values]
def fn_fillNA(df,value):
    
    df.fillna(value, inplace=True)
    
    return df

# In[function for merging two dataframes]
def fn_merge_twoDataframe(df,df1,on_col):
    
    df = pd.merge(df, df1, on=[on_col])

    return df

# In[function for drop duplicates]
def fn_dropduplicates(df,on_col):
    
    df = df.drop_duplicates(on_col,ignore_index = True)
    
    return df

# In[function for list to json]
def fn_dfcols_tojson(df,attribute_col,value_col):
    
    data = {}
    for i in range(0,len(df)):
        data[df[attribute_col][i]] = df[value_col][i]
    return data

# In[function for list of dates with frequency of month between start and end date]
def fn_monthwise_datelist(START_DATE,END_DATE):
    
    date_list = [START_DATE]
    current_date = datetime.strptime(START_DATE, '%Y-%m-%d').date()
    end_date = datetime.strptime(END_DATE, '%Y-%m-%d').date()
    
    while current_date < end_date:
        current_date += relativedelta(months=1)
        if (current_date > end_date):
            current_date = end_date
        date_list.append(str(current_date))
    
    return date_list

# In[function for datatype conversion]
def fn_datatype_conversion(df):
    
    # data type conversion
    df[app.config['VAR_CHARGE_AMOUNT']] = df[app.config['VAR_CHARGE_AMOUNT']].astype('float')
    df[app.config['VAR_TAX_AMOUNT']] = df[app.config['VAR_TAX_AMOUNT']].astype('float')
    df[app.config['VAR_EXPECTED_CHARGE']] = df[app.config['VAR_EXPECTED_CHARGE']].astype('float')
    df[app.config['VAR_EXPECTED_TAX']] = df[app.config['VAR_EXPECTED_TAX']].astype('float')
    
    return df

# In[function for calculations]
def fn_deviation_calculations(df):
    
    # charge_deviation calculation
    df[app.config['VAR_CHARGE_DEVIATION']] = df[app.config['VAR_CHARGE_AMOUNT']] - df[app.config['VAR_EXPECTED_CHARGE']]
    # tax_deviation calculation
    df[app.config['VAR_TAX_DEVIATION']] = df[app.config['VAR_TAX_AMOUNT']] - df[app.config['VAR_EXPECTED_TAX']]
    
    # precisely_chrgd calculation
    df.loc[(df[app.config['VAR_CHARGE_DEVIATION']] == 0) & (df[app.config['VAR_TAX_DEVIATION']] == 0),app.config['VAR_PRECISELY_CHARGED']] = True
    df.loc[(df[app.config['VAR_CHARGE_DEVIATION']] != 0) | (df[app.config['VAR_TAX_DEVIATION']] != 0),app.config['VAR_PRECISELY_CHARGED']] = False
    
    return df

# In[funtion for insert daywise trans reference details]
def fn_insert_daywise_transreference_details(df,TRANSACTION_CODE,dates,INPUT_ID,IS_REGENERATED):
    
    split= app.config['LEVEL_BAND_SEP']
    # for daywise list
    daywise_list = []
    # for looping daywise and appending it to list
    for i in range(0,len(dates)):
        EXPECTED_CHARGES = split.join(df.loc[df[app.config['VAR_TIME_STAMP']] == dates[i]].TRANS_REFERENCE.unique().tolist())
        PRECISELY_CHARGED = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_PRECISELY_CHARGED']] == True)].TRANS_REFERENCE.tolist())
        NOT_PRECISELY_CHARGED = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_PRECISELY_CHARGED']] == False)].TRANS_REFERENCE.tolist())
        MISSING_CHARGE = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_AMOUNT']] == 0)].TRANS_REFERENCE.tolist())
        MISSING_TAX_BUT_CHARGE_PRESENT = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_AMOUNT']] != 0) & (df[app.config['VAR_TAX_AMOUNT']] == 0)].TRANS_REFERENCE.tolist())
        WRONG_CHARGE = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) &(df[app.config['VAR_CHARGE_AMOUNT']] != 0) & (df[app.config['VAR_CHARGE_DEVIATION']] != 0)].TRANS_REFERENCE.tolist())
        # REVENUE_LOSS_EXTRA_IN_CHARGE = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_DEVIATION']] != 0)].TRANS_REFERENCE.tolist())
        REVENUE_LOSS_IN_CHARGE = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_DEVIATION']] < 0)].TRANS_REFERENCE.tolist())
        REVENUE_EXTRA_IN_CHARGE = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_DEVIATION']] > 0)].TRANS_REFERENCE.tolist())
        # REVENUE_LOSS_EXTRA_IN_TAX = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_TAX_DEVIATION']] == 0)].TRANS_REFERENCE.tolist())
        REVENUE_LOSS_IN_TAX = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_TAX_DEVIATION']] < 0)].TRANS_REFERENCE.tolist())
        REVENUE_EXTRA_IN_TAX = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_TAX_DEVIATION']] > 0)].TRANS_REFERENCE.tolist())
        REVENUE_BELOW_ACCEPTANCE_IN_CHARGE = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_AMOUNT']] != 0) & (df[app.config['VAR_CHARGE_DEVIATION']] < 0) ==True].TRANS_REFERENCE.tolist())
        REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE = split.join(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_AMOUNT']] != 0) & (df[app.config['VAR_CHARGE_DEVIATION']] > 0) ==True].TRANS_REFERENCE.tolist())
    
        day_list = [TRANSACTION_CODE,INPUT_ID,dates[i],EXPECTED_CHARGES,PRECISELY_CHARGED,NOT_PRECISELY_CHARGED,MISSING_CHARGE,
                     MISSING_TAX_BUT_CHARGE_PRESENT,WRONG_CHARGE,REVENUE_LOSS_IN_CHARGE,REVENUE_EXTRA_IN_CHARGE,
                     REVENUE_LOSS_IN_TAX,REVENUE_EXTRA_IN_TAX,REVENUE_BELOW_ACCEPTANCE_IN_CHARGE,
                     REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE,IS_REGENERATED,app.config['VAR_ML_USERNAME'],datetime.now()]
        daywise_list.append(day_list)
    
    daywise_df = pd.DataFrame(daywise_list)
    daywise_df.columns = ['TRANSACTION_CODE','INPUT_ID','TIME_STAMP','EXPECTED_CHARGES','PRECISELY_CHARGED','NOT_PRECISELY_CHARGED',
                          'MISSING_CHARGE','MISSING_TAX_BUT_CHARGE_PRESENT','WRONG_CHARGE','REVENUE_LOSS_IN_CHARGE','REVENUE_EXTRA_IN_CHARGE',
                          'REVENUE_LOSS_IN_TAX','REVENUE_EXTRA_IN_TAX','REVENUE_BELOW_ACCEPTANCE_IN_CHARGE','REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE',
                          'IS_REGENERATED','CREATED_BY','CREATED_ON']
    daywise_df[app.config['VAR_TIME_STAMP']] = pd.to_datetime(daywise_df[app.config['VAR_TIME_STAMP']])
    
    # data insert
    DBC.mysql_df_to_table_insert(daywise_df,app.config['MYSQL_DF_INSERT_DAYWISE_TRANS_REFERENCE'])
    
# In[function for insert daywise analysis details]
def fn_insert_daywise_analysis_details(df,TRANSACTION_CODE,dates,INPUT_ID,IS_REGENERATED):
    
    # for daywise list
    daywise_list = []
    # for looping daywise and appending it to list
    for i in range(0,len(dates)):
    
        EXPECTED_COUNT = len(df.loc[df[app.config['VAR_TIME_STAMP']] == dates[i]].TRANS_REFERENCE.unique())
        PRECISELY_CHARGED = df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_PRECISELY_CHARGED']] == True)].PRECISELY_CHARGED.count()
        NOT_PRECISELY_CHARGED = df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_PRECISELY_CHARGED']] == False)].PRECISELY_CHARGED.count()
        MISSING_CHARGE = df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_AMOUNT']] == 0)].CHARGE_AMOUNT.count()
        MISSING_TAX_BUT_CHARGE_PRESENT = df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_AMOUNT']] != 0) & (df[app.config['VAR_TAX_AMOUNT']] == 0)].CHARGE_AMOUNT.count()
        WRONG_CHARGE = df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) &(df[app.config['VAR_CHARGE_AMOUNT']] != 0) & (df[app.config['VAR_CHARGE_DEVIATION']] != 0)].CHARGE_AMOUNT.count()
        
        EXPECTED_CHARGE_AMOUNT = round(df.loc[df[app.config['VAR_TIME_STAMP']] == dates[i]].EXPECTED_CHARGE.sum(),2)
        EXPECTED_TAX_AMOUNT = round(df.loc[df[app.config['VAR_TIME_STAMP']] == dates[i]].EXPECTED_TAX.sum(),2)
        ACTUAL_CHARGE_AMOUNT = round(df.loc[df[app.config['VAR_TIME_STAMP']] == dates[i]].CHARGE_AMOUNT.sum(),2)
        ACTUAL_TAX_AMOUNT = round(df.loc[df[app.config['VAR_TIME_STAMP']] == dates[i]].TAX_AMOUNT.sum(),2)
        # REVENUE_LOSS_OR_EXTRA_IN_CHARGE_AMOUNT = round(ACTUAL_CHARGE_AMOUNT - EXPECTED_CHARGE_AMOUNT,2)
        REVENUE_LOSS_IN_CHARGE_AMOUNT = round(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_DEVIATION']] < 0)].CHARGE_DEVIATION.sum(),2)
        REVENUE_EXTRA_IN_CHARGE_AMOUNT = round(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_DEVIATION']] > 0)].CHARGE_DEVIATION.sum(),2)
        # REVENUE_LOSS_OR_EXTRA_IN_TAX_AMOUNT = round(ACTUAL_TAX_AMOUNT - EXPECTED_TAX_AMOUNT,2)
        REVENUE_LOSS_IN_TAX_AMOUNT = round(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_TAX_DEVIATION']] < 0)].TAX_DEVIATION.sum(),2)
        REVENUE_EXTRA_IN_TAX_AMOUNT = round(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_TAX_DEVIATION']] > 0)].TAX_DEVIATION.sum(),2)
        REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT = round(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_AMOUNT']] != 0) & (df[app.config['VAR_CHARGE_DEVIATION']] < 0) ==True].CHARGE_DEVIATION.sum(),2)
        REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT = round(df.loc[(df[app.config['VAR_TIME_STAMP']] == dates[i]) & (df[app.config['VAR_CHARGE_AMOUNT']] != 0) & (df[app.config['VAR_CHARGE_DEVIATION']] > 0) ==True].CHARGE_DEVIATION.sum(),2)
        
        day_list = [TRANSACTION_CODE,INPUT_ID,dates[i],EXPECTED_COUNT,PRECISELY_CHARGED,NOT_PRECISELY_CHARGED,MISSING_CHARGE,
                     MISSING_TAX_BUT_CHARGE_PRESENT,WRONG_CHARGE,EXPECTED_CHARGE_AMOUNT,EXPECTED_TAX_AMOUNT,
                     ACTUAL_CHARGE_AMOUNT,ACTUAL_TAX_AMOUNT,REVENUE_LOSS_IN_CHARGE_AMOUNT,REVENUE_EXTRA_IN_CHARGE_AMOUNT,
                     REVENUE_LOSS_IN_TAX_AMOUNT,REVENUE_EXTRA_IN_TAX_AMOUNT,REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT,
                     REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT,IS_REGENERATED,app.config['VAR_ML_USERNAME'],datetime.now()]
        daywise_list.append(day_list)
        
    daywise_df = pd.DataFrame(daywise_list)
    daywise_df.columns = ['TRANSACTION_CODE','INPUT_ID','TIME_STAMP','EXPECTED_COUNT','PRECISELY_CHARGED','NOT_PRECISELY_CHARGED',
                   'MISSING_CHARGE','MISSING_TAX_BUT_CHARGE_PRESENT','WRONG_CHARGE','EXPECTED_CHARGE_AMOUNT',
                   'EXPECTED_TAX_AMOUNT','ACTUAL_CHARGE_AMOUNT','ACTUAL_TAX_AMOUNT','REVENUE_LOSS_IN_CHARGE','REVENUE_EXTRA_IN_CHARGE',
                   'REVENUE_LOSS_IN_TAX','REVENUE_EXTRA_IN_TAX','REVENUE_BELOW_ACCEPTANCE_IN_CHARGE','REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE',
                   'IS_REGENERATED','CREATED_BY','CREATED_ON']
    daywise_df[app.config['VAR_TIME_STAMP']] = pd.to_datetime(daywise_df[app.config['VAR_TIME_STAMP']])
    # data insert
    DBC.mysql_df_to_table_insert(daywise_df,app.config['MYSQL_DF_INSERT_DAYWISE_TRANSACTION_ANALYSIS'])
    
# In[function for insert trans_reference details]
def fn_insert_trans_reference_details(TRANSACTION_TYPE,TRANSACTION_CODE,START_DATE,END_DATE,INPUT_ID,IS_REGENERATED):
    
    split= app.config['LEVEL_BAND_SEP']
    
    # To read data
    param = {
                "TRANSACTION_CODE":TRANSACTION_CODE,
                "START_DATE":START_DATE,
                "END_DATE":END_DATE,
                "INPUT_ID":INPUT_ID
            }
    if(IS_REGENERATED == True):
        df = DBC.mysql_readTable(app.config['MYSQL_SELECT_DAYWISE_TRANSREFERENCE_INPUTID'],param)
    else:
        df = DBC.mysql_readTable(app.config['MYSQL_SELECT_DAYWISE_TRANSREFERENCE'],param)
    # To remove duplicates
    df = fn_dropduplicates(df,[app.config['VAR_TIME_STAMP']])

    EXPECTED_CHARGES = split.join(df['EXPECTED_CHARGES'].loc[df['EXPECTED_CHARGES'] != ''].tolist())
    PRECISELY_CHARGED = split.join(df['PRECISELY_CHARGED'].loc[df['PRECISELY_CHARGED'] != ''].tolist())
    NOT_PRECISELY_CHARGED = split.join(df['NOT_PRECISELY_CHARGED'].loc[df['NOT_PRECISELY_CHARGED'] != ''].tolist())
    MISSING_CHARGE = split.join(df['MISSING_CHARGE'].loc[df['MISSING_CHARGE'] != ''].tolist())
    MISSING_TAX_BUT_CHARGE_PRESENT = split.join(df['MISSING_TAX_BUT_CHARGE_PRESENT'].loc[df['MISSING_TAX_BUT_CHARGE_PRESENT'] != ''].tolist())
    WRONG_CHARGE = split.join(df['WRONG_CHARGE'].loc[df['WRONG_CHARGE'] != ''].tolist())
    # REVENUE_LOSS_EXTRA_IN_CHARGE = split.join(df['REVENUE_LOSS_EXTRA_IN_CHARGE'].loc[df['REVENUE_LOSS_EXTRA_IN_CHARGE'] != ''].tolist())
    REVENUE_LOSS_IN_CHARGE = split.join(df['REVENUE_LOSS_IN_CHARGE'].loc[df['REVENUE_LOSS_IN_CHARGE'] != ''].tolist())
    REVENUE_EXTRA_IN_CHARGE = split.join(df['REVENUE_EXTRA_IN_CHARGE'].loc[df['REVENUE_EXTRA_IN_CHARGE'] != ''].tolist())
    # REVENUE_LOSS_EXTRA_IN_TAX = split.join(df['REVENUE_LOSS_EXTRA_IN_TAX'].loc[df['REVENUE_LOSS_EXTRA_IN_TAX'] != ''].tolist())
    REVENUE_LOSS_IN_TAX = split.join(df['REVENUE_LOSS_IN_TAX'].loc[df['REVENUE_LOSS_IN_TAX'] != ''].tolist())
    REVENUE_EXTRA_IN_TAX = split.join(df['REVENUE_EXTRA_IN_TAX'].loc[df['REVENUE_EXTRA_IN_TAX'] != ''].tolist())
    REVENUE_BELOW_ACCEPTANCE_IN_CHARGE = split.join(df['REVENUE_BELOW_ACCEPTANCE_IN_CHARGE'].loc[df['REVENUE_BELOW_ACCEPTANCE_IN_CHARGE'] != ''].tolist())
    REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE = split.join(df['REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE'].loc[df['REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE'] != ''].tolist())
    
    param = {
                'TRANSACTION_TYPE' : TRANSACTION_TYPE,
                'TRANSACTION_CODE' : TRANSACTION_CODE,
                'START_DATE' : START_DATE,
                'END_DATE' : END_DATE,
                'EXPECTED_CHARGES' : EXPECTED_CHARGES,
                'PRECISELY_CHARGED' : PRECISELY_CHARGED,
                'NOT_PRECISELY_CHARGED' : NOT_PRECISELY_CHARGED,
                'MISSING_CHARGE' : MISSING_CHARGE,
                'MISSING_TAX_BUT_CHARGE_PRESENT' : MISSING_TAX_BUT_CHARGE_PRESENT,
                'WRONG_CHARGE' : WRONG_CHARGE,
                'REVENUE_LOSS_IN_CHARGE' : REVENUE_LOSS_IN_CHARGE,
                'REVENUE_EXTRA_IN_CHARGE' : REVENUE_EXTRA_IN_CHARGE,
                'REVENUE_LOSS_IN_TAX' : REVENUE_LOSS_IN_TAX,
                'REVENUE_EXTRA_IN_TAX' : REVENUE_EXTRA_IN_TAX,
                'REVENUE_BELOW_ACCEPTANCE_IN_CHARGE' : REVENUE_BELOW_ACCEPTANCE_IN_CHARGE,
                'REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE' : REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE,
                "CREATED_BY":app.config['VAR_ML_USERNAME'],
                "CREATED_ON":datetime.now()
            }
    primary_id = DBC.mysql_insertData(app.config['MYSQL_INSERT_TRANS_REFERENCE_DETAILS'],param)
    
    return primary_id

# In[function for output params]
def fn_output_params(primary_id,TRANSACTION_CODE,START_DATE,END_DATE,INPUT_ID,IS_REGENERATED):
    
    # To read data
    param = {
                "TRANSACTION_CODE":TRANSACTION_CODE,
                "START_DATE":START_DATE,
                "END_DATE":END_DATE,
                "INPUT_ID":INPUT_ID
            }
    if(IS_REGENERATED == True):
        df = DBC.mysql_readTable(app.config['MYSQL_SELECT_DAYWISE_TRANSACTION_ANALYSIS_INPUTID'],param)
    else:
        df = DBC.mysql_readTable(app.config['MYSQL_SELECT_DAYWISE_TRANSACTION_ANALYSIS'],param)
    # To remove duplicates
    df = fn_dropduplicates(df,[app.config['VAR_TIME_STAMP']])
    
    if(len(df) > 0):
    
        EXPECTED_COUNT = df['EXPECTED_COUNT'].sum()
        PRECISELY_CHARGED = df['PRECISELY_CHARGED'].sum()
        NOT_PRECISELY_CHARGED = df['NOT_PRECISELY_CHARGED'].sum()
        MISSING_CHARGE = df['MISSING_CHARGE'].sum()
        MISSING_TAX_BUT_CHARGE_PRESENT = df['MISSING_TAX_BUT_CHARGE_PRESENT'].sum()
        WRONG_CHARGE = df['WRONG_CHARGE'].sum()
        
    
        PRECISELY_CHARGED_PERCENTAGE = round(PRECISELY_CHARGED / EXPECTED_COUNT * 100,2).astype(str)+'%'
        NOT_PRECISELY_CHARGED_PERCENTAGE = round(NOT_PRECISELY_CHARGED / EXPECTED_COUNT * 100,2).astype(str)+'%'
        MISSING_CHARGE_PERCENTAGE = round(MISSING_CHARGE / EXPECTED_COUNT * 100,2).astype(str)+'%'
        MISSING_TAX_BUT_CHARGE_PRESENT_PERCENTAGE = round(MISSING_TAX_BUT_CHARGE_PRESENT / EXPECTED_COUNT * 100,2).astype(str)+'%'
        WRONG_CHARGE_PERCENTAGE = round(WRONG_CHARGE / EXPECTED_COUNT * 100,2).astype(str)+'%'
        
        EXPECTED_CHARGE_AMOUNT = df['EXPECTED_CHARGE_AMOUNT'].sum()
        EXPECTED_TAX_AMOUNT = df['EXPECTED_TAX_AMOUNT'].sum()
        ACTUAL_CHARGE_AMOUNT = df['ACTUAL_CHARGE_AMOUNT'].sum()
        ACTUAL_TAX_AMOUNT = df['ACTUAL_TAX_AMOUNT'].sum()
        # REVENUE_LOSS_OR_EXTRA_IN_CHARGE_AMOUNT = df['REVENUE_LOSS_EXTRA_IN_CHARGE'].sum()
        REVENUE_LOSS_IN_CHARGE_AMOUNT = df['REVENUE_LOSS_IN_CHARGE'].sum()
        REVENUE_EXTRA_IN_CHARGE_AMOUNT = df['REVENUE_EXTRA_IN_CHARGE'].sum()
        # REVENUE_LOSS_OR_EXTRA_IN_TAX_AMOUNT = df['REVENUE_LOSS_EXTRA_IN_TAX'].sum()
        REVENUE_LOSS_IN_TAX_AMOUNT = df['REVENUE_LOSS_IN_TAX'].sum()
        REVENUE_EXTRA_IN_TAX_AMOUNT = df['REVENUE_EXTRA_IN_TAX'].sum()
        REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT = df['REVENUE_BELOW_ACCEPTANCE_IN_CHARGE'].sum()
        REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT = df['REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE'].sum()
        
        ACTUAL_CHARGE_AMOUNT_PERCENTAGE = round(ACTUAL_CHARGE_AMOUNT/EXPECTED_CHARGE_AMOUNT*100,2).astype(str)+'%'
        ACTUAL_TAX_AMOUNT_PERCENTAGE = round(ACTUAL_TAX_AMOUNT/EXPECTED_TAX_AMOUNT*100 ,2).astype(str)+'%'
        REVENUE_LOSS_IN_CHARGE_AMOUNT_PERCENTAGE = round(REVENUE_LOSS_IN_CHARGE_AMOUNT/EXPECTED_CHARGE_AMOUNT*100,2).astype(str)+'%'
        REVENUE_EXTRA_IN_CHARGE_AMOUNT_PERCENTAGE = round(REVENUE_EXTRA_IN_CHARGE_AMOUNT/EXPECTED_CHARGE_AMOUNT*100,2).astype(str)+'%'
        REVENUE_LOSS_IN_TAX_AMOUNT_PERCENTAGE = round(REVENUE_LOSS_IN_TAX_AMOUNT/EXPECTED_TAX_AMOUNT*100,2).astype(str)+'%'
        REVENUE_EXTRA_IN_TAX_AMOUNT_PERCENTAGE = round(REVENUE_EXTRA_IN_TAX_AMOUNT/EXPECTED_TAX_AMOUNT*100,2).astype(str)+'%'
        REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT_PERCENTAGE = round(REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT/EXPECTED_CHARGE_AMOUNT*100,2).astype(str)+'%'
        REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT_PERCENTAGE = round(REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT/EXPECTED_CHARGE_AMOUNT*100,2).astype(str)+'%'
        
        output = {
                    "STATUS" : app.config['VAR_STATUS_SUCCESS'],
                    "TRANS_REFERENCE_DETAILS_ID" :int(primary_id),
                    "EXPECTED_COUNT" : int(EXPECTED_COUNT),
                    "PRECISELY_CHARGED" : int(PRECISELY_CHARGED),
                    "NOT_PRECISELY_CHARGED" : int(NOT_PRECISELY_CHARGED),
                    "MISSING_CHARGE" : int(MISSING_CHARGE),
                    "MISSING_TAX_BUT_CHARGE_PRESENT" : int(MISSING_TAX_BUT_CHARGE_PRESENT),
                    "WRONG_CHARGE" : int(WRONG_CHARGE),
                    "PRECISELY_CHARGED_PERCENTAGE" : PRECISELY_CHARGED_PERCENTAGE,
                    "NOT_PRECISELY_CHARGED_PERCENTAGE" : NOT_PRECISELY_CHARGED_PERCENTAGE,
                    "MISSING_CHARGE_PERCENTAGE" : MISSING_CHARGE_PERCENTAGE,
                    "MISSING_TAX_BUT_CHARGE_PRESENT_PERCENTAGE" : MISSING_TAX_BUT_CHARGE_PRESENT_PERCENTAGE,
                    "WRONG_CHARGE_PERCENTAGE" : WRONG_CHARGE_PERCENTAGE,
                    "EXPECTED_CHARGE_AMOUNT" : EXPECTED_CHARGE_AMOUNT,
                    "EXPECTED_TAX_AMOUNT" : EXPECTED_TAX_AMOUNT,
                    "ACTUAL_CHARGE_AMOUNT" : ACTUAL_CHARGE_AMOUNT,
                    "ACTUAL_TAX_AMOUNT" : ACTUAL_TAX_AMOUNT,
                    "REVENUE_LOSS_IN_CHARGE_AMOUNT" : REVENUE_LOSS_IN_CHARGE_AMOUNT,
                    "REVENUE_EXTRA_IN_CHARGE_AMOUNT" : REVENUE_EXTRA_IN_CHARGE_AMOUNT,
                    "REVENUE_LOSS_IN_TAX_AMOUNT" : REVENUE_LOSS_IN_TAX_AMOUNT,
                    "REVENUE_EXTRA_IN_TAX_AMOUNT" : REVENUE_EXTRA_IN_TAX_AMOUNT,
                    "REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT" : REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT,
                    "REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT" : REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT,
                    "ACTUAL_CHARGE_AMOUNT_PERCENTAGE" : ACTUAL_CHARGE_AMOUNT_PERCENTAGE,
                    "ACTUAL_TAX_AMOUNT_PERCENTAGE" : ACTUAL_TAX_AMOUNT_PERCENTAGE,
                    "REVENUE_LOSS_IN_CHARGE_AMOUNT_PERCENTAGE" : REVENUE_LOSS_IN_CHARGE_AMOUNT_PERCENTAGE,
                    "REVENUE_EXTRA_IN_CHARGE_AMOUNT_PERCENTAGE" : REVENUE_EXTRA_IN_CHARGE_AMOUNT_PERCENTAGE,
                    "REVENUE_LOSS_IN_TAX_AMOUNT_PERCENTAGE" : REVENUE_LOSS_IN_TAX_AMOUNT_PERCENTAGE,
                    "REVENUE_EXTRA_IN_TAX_AMOUNT_PERCENTAGE" : REVENUE_EXTRA_IN_TAX_AMOUNT_PERCENTAGE,
                    "REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT_PERCENTAGE" : REVENUE_BELOW_ACCEPTANCE_IN_CHARGE_AMOUNT_PERCENTAGE,
                    "REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT_PERCENTAGE" : REVENUE_ABOVE_ACCEPTANCE_IN_CHARGE_AMOUNT_PERCENTAGE
                 }
    else:
        output = {
                    "STATUS" : app.config['VAR_STATUS_NO_DATA']
                 }
    return output

# In[function for insert output details]
def fn_insert_output_details(detail_id,userinput,output):
    
    data = {
        "detail_id":detail_id,
        "INPUT":userinput,
        "OUTPUT":output,
        "CREATED_BY":app.config['VAR_ML_USERNAME'],
        "CREATED_ON":datetime.now()
        }
    
    primary_key = DBC.mysql_insertData(app.config['MYSQL_INSERT_IP_OP_DETAILS'],data)
    
    return primary_key

# In[function for updating the output details]
def fn_update_output_details(input_id,detail_id,output):
    
    data = {
        "id":input_id,
        "detail_id":detail_id,
        "OUTPUT":output,
        "CREATED_ON":datetime.now()
        }
    DBC.mysql_update_delete_Data(app.config['MYSQL_UPDATE_IP_OP_DETAILS'],data)
