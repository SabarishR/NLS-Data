#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 02 17:49:52 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
import numpy as np
import pandas as pd
from flask import current_app as app

# In[level/band split using seperator]
def fn_str_split(string):
    return string.split(app.config['LEVEL_BAND_SEP'])

# In[for first char validation. remove '^' if first charecter without any values]
def fn_level_band_firstchar_validation(df_charges):
    for column in df_charges:
        for i in range(0,len(df_charges)):
            if(df_charges[column][i] != None):
                if(str(df_charges[column][i][0]) == app.config['LEVEL_BAND_SEP']):
                    df_charges[column][i] =  df_charges[column][i][1:]
    return df_charges

# In[for charge history duration mapping]
def fn_history_charges_duration(df_charges):
    df_charges['START_DATE'] = np.nan
    df_charges['END_DATE'] = np.nan
    for i in range (0,len(df_charges)):
        if (i ==0):
            df_charges['END_DATE'][i] = df_charges['DATE_TIME'][i]
        elif (df_charges['DATE_TIME'][i] == None):
            df_charges['START_DATE'][i] = str(pd.to_datetime(df_charges['DATE_TIME']).max())
        else:
            df_charges['START_DATE'][i] = df_charges['DATE_TIME'][i - 1]
            df_charges['END_DATE'][i] = df_charges['DATE_TIME'][i]
    df_charges = df_charges[['id','FLAT_AMOUNT','CALC_TYPE','PERCENTAGE','UPTO_AMOUNT','MINIMUM_AMOUNT','MAXIMUM_AMOUNT','TRANSACTION_CODE','TAX','START_DATE','END_DATE']]
    # datatype conversion
    df_charges['START_DATE'] = pd.to_datetime(df_charges['START_DATE'])
    df_charges['END_DATE'] = pd.to_datetime(df_charges['END_DATE'])
    
    return df_charges

# In[using seperator construct multiple rows from multiple level/band]
def fn_level_band_split(df_charges,is_history):
    
    cols_to_df_list = ['CALC_TYPE','PERCENTAGE','UPTO_AMOUNT','MINIMUM_AMOUNT','MAXIMUM_AMOUNT','id','TAX']
    df_chg = pd.DataFrame(columns = cols_to_df_list)
    
    # split multiple level/band into multiple rows
    for j in range (0,len(df_charges)):
        df_len = len(df_chg)
        for i in cols_to_df_list:
            if df_charges[i][j]:
                split_list = fn_str_split(df_charges[i][j])
                for k in range (0,len(split_list)):
                    if((i == "id") | (i == 'TAX')):
                        df_chg.loc[df_len + k,i] = df_charges[i][j]
                    else:
                        df_chg.loc[df_len + k,i] = split_list[k]
    
    # fill the empty rows using forward fill
    df_chg['id'] = df_chg[['id']].ffill()
    df_chg['TAX'] = df_chg.groupby('id')['TAX'].ffill()
    df_chg=df_chg.replace(r'', 0, regex=True)
    
    # data type conversion
    df_chg['PERCENTAGE'] = df_chg['PERCENTAGE'].astype('float')
    df_chg['MAX_AMT'] = df_chg['UPTO_AMOUNT'].astype('float')
    df_chg['MIN_CHARGE'] = df_chg['MINIMUM_AMOUNT'].astype('float')
    df_chg['MAX_CHARGE'] = df_chg['MAXIMUM_AMOUNT'].astype('float')
    df_chg['TAX'] = df_chg['TAX'].astype('float')
    
    # creating the minimum amount for the level/band
    df_chg['MIN_AMT'] = 0
    for i in range(0,len(df_chg)):
        if(i == 0):
            df_chg['MIN_AMT'][i] =  0
        else:
            df_chg['MIN_AMT'][i] =  df_chg['MAX_AMT'][i-1] + 1

    df_chg.loc[(df_chg['MIN_AMT'].isnull()) | (df_chg['MIN_AMT'] > df_chg['MAX_AMT']),'MIN_AMT'] = 0
    df_chg = df_chg[["id","CALC_TYPE","PERCENTAGE","MIN_AMT","MAX_AMT","MIN_CHARGE","MAX_CHARGE","TAX"]]
    
    if(is_history != 0):
        df_chg['START_DATE'] = df_chg.id.map(df_charges.set_index('id')['START_DATE'])
        df_chg['END_DATE'] = df_chg.id.map(df_charges.set_index('id')['END_DATE'])
    
    return df_chg

# In[For FLAT AMOUNT with no history]
def fn_flat_amount_with_no_history(df,df_charges):
    data = {}
    for i in range(0,len(df_charges)):
        # Creating expected charge column
        data[df_charges['TRANSACTION_CODE'][i]] = df_charges['FLAT_AMOUNT'][i]
        df['EXPECTED_CHARGE'] = df['TRANSACTION_CODE'].map(data)
        # Creating expected Tax percentage
        data[df_charges['TRANSACTION_CODE'][i]] = df_charges['TAX'][i]
        df['EXPECTED_TAX'] = df['TRANSACTION_CODE'].map(data)
        #conversion
        df['EXPECTED_CHARGE'] = df['EXPECTED_CHARGE'].astype('float')
        df['EXPECTED_TAX'] = df['EXPECTED_TAX'].astype('float')
        # expected tax calculation
        df['EXPECTED_TAX'] = df['EXPECTED_CHARGE'] /100 * df['EXPECTED_TAX']
        
        return df
    
# In[for single level/band with no history]
def fn_single_level_band_with_no_history(df,df_charges):
    data = {}
    for i in range(0,len(df_charges)): 
        # Creating expected charge percentage
        data[df_charges['TRANSACTION_CODE'][i]] = df_charges['PERCENTAGE'][i]
        df['EXPECTED_CHARGE'] = df['TRANSACTION_CODE'].map(data)
        # Creating expected Tax percentage
        data[df_charges['TRANSACTION_CODE'][i]] = df_charges['TAX'][i]
        df['EXPECTED_TAX'] = df['TRANSACTION_CODE'].map(data)
        #conversion
        df['EXPECTED_CHARGE'] = df['EXPECTED_CHARGE'].astype('float')
        df['EXPECTED_TAX'] = df['EXPECTED_TAX'].astype('float')
        df_charges['MINIMUM_AMOUNT'] = df_charges['MINIMUM_AMOUNT'].astype('float')
        df_charges['MAXIMUM_AMOUNT'] = df_charges['MAXIMUM_AMOUNT'].astype('float')
        # expected charge and tax calculation
        df['EXPECTED_CHARGE'] = round(df['TRANSACTION_AMOUNT'] /100 * df['EXPECTED_CHARGE'],2)
        df['EXPECTED_TAX'] = round(df['EXPECTED_CHARGE'] /100 * df['EXPECTED_TAX'],2)
        # comparing charges with minimum maximum amount
        # for charge lesser then minimum charge amount
        if(pd.isnull(df_charges.iloc[i]['MINIMUM_AMOUNT']) == False):
            df.loc[(df['EXPECTED_CHARGE'] < df_charges['MINIMUM_AMOUNT'][i]) , 'EXPECTED_CHARGE'] =  df_charges['MINIMUM_AMOUNT'][i]
        # for charge greter then minimum charge amount
        if(pd.isnull(df_charges.iloc[i]['MAXIMUM_AMOUNT']) == False):
            df.loc[(df['EXPECTED_CHARGE'] > df_charges['MAXIMUM_AMOUNT'][i]) , 'EXPECTED_CHARGE'] =  df_charges['MAXIMUM_AMOUNT'][i]      
    
    return df

# In[for multi level with no history]
def fn_multi_level_with_no_history(df,df_chg):
    # for expected charge initialization
    df['EXPECTED_CHARGE'] = 0
    df['EXPECTED_TAX'] = 0

    for i in range (0,len(df_chg)):
        # for charge as per percentage
        df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'CHARGE'] = round((df['TRANSACTION_AMOUNT'] * df_chg['PERCENTAGE'][i] /100),2)
        # for charge lesser then minimum charge amount
        if(pd.isnull(df_chg.iloc[i]['MIN_CHARGE']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]) & (df['CHARGE'] < df_chg['MIN_CHARGE'][i]) , 'CHARGE'] =  df_chg['MIN_CHARGE'][i]
        # for charge greter then minimum charge amount
        if(pd.isnull(df_chg.iloc[i]['MAX_CHARGE']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]) & (df['CHARGE'] > df_chg['MAX_CHARGE'][i]) , 'CHARGE'] =  df_chg['MAX_CHARGE'][i]
        # for tax as per percentage
        if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

        # for expected charge
        df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
        # for expected tax
        if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)

    df_chg = df_chg.loc[(df_chg['MAX_AMT'].isnull())]
    df_chg.reset_index(drop=True, inplace=True)

    for i in range (0,len(df_chg)):
        # for charge as per percentage
        df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGE'] = round((df['TRANSACTION_AMOUNT'] * df_chg['PERCENTAGE'][i] /100),2)
        # for charge lesser then minimum charge amount
        if(pd.isnull(df_chg.iloc[i]['MIN_CHARGE']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['CHARGE'] < df_chg['MIN_CHARGE'][i]) , 'CHARGE'] =  df_chg['MIN_CHARGE'][i]
        # for charge greter then minimum charge amount
        if(pd.isnull(df_chg.iloc[i]['MAX_CHARGE']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['CHARGE'] > df_chg['MAX_CHARGE'][i]) , 'CHARGE'] =  df_chg['MAX_CHARGE'][i]
        # for tax as per percentage
        if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

        # for expected charge
        df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
        # for expected tax
        if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)  
        
    return df

# In[for multi band with no history]
def fn_multi_band_with_no_history(df,df_chg):
    # for expected charge initialization
    df['EXPECTED_CHARGE'] = 0
    df['EXPECTED_TAX'] = 0

    for i in range (0,len(df_chg)):
        # Chargable amount calculation
        df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGABLE_AMT'] = df['TRANSACTION_AMOUNT'] - (df_chg['MIN_AMT'][i])
        if(pd.isnull(df_chg.iloc[i]['MAX_AMT']) == False):
            df.loc[(df['CHARGABLE_AMT'] > (df_chg['MAX_AMT'][i] - df_chg['MIN_AMT'][i])), 'CHARGABLE_AMT'] = df_chg['MAX_AMT'][i] - df_chg['MIN_AMT'][i]
        else:
            df.loc[(df['TRANSACTION_AMOUNT'] > (df_chg['MIN_AMT'][i])), 'CHARGABLE_AMT'] = df['TRANSACTION_AMOUNT'] - (df_chg['MIN_AMT'][i])
        # for charge as per percentage
        df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGE'] = round((df['CHARGABLE_AMT'] * df_chg['PERCENTAGE'][i] /100),2)
        # for tax as per percentage
        if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

        # for expected charge
        df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
        # for expected tax
        if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
            df.loc[(df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)
            
    return df

# In[For FLAT AMOUNT with history]
def fn_flat_amount_with_history(df,df_charges):
    for i in range(0,len(df_charges)):
        # Creating expected charge and expected tax percentage column
        if(pd.isnull(df_charges['START_DATE'][i])):
            df.loc[(df['TIME_STAMP'] <= df_charges['END_DATE'][i]),'EXPECTED_CHARGE'] = df_charges['FLAT_AMOUNT'][i]
            df.loc[(df['TIME_STAMP'] <= df_charges['END_DATE'][i]),'EXPECTED_TAX'] = df_charges['TAX'][i]
        elif(pd.isnull(df_charges['END_DATE'][i])):
            df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]),'EXPECTED_CHARGE'] = df_charges['FLAT_AMOUNT'][i]
            df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]),'EXPECTED_TAX'] = df_charges['TAX'][i]
        else:
            df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]) & (df['TIME_STAMP'] <= df_charges['END_DATE'][i]),'EXPECTED_CHARGE'] = df_charges['FLAT_AMOUNT'][i]
            df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]) & (df['TIME_STAMP'] <= df_charges['END_DATE'][i]),'EXPECTED_TAX'] = df_charges['TAX'][i]
        #conversion
        df['EXPECTED_CHARGE'] = df['EXPECTED_CHARGE'].astype('float')
        df['EXPECTED_TAX'] = df['EXPECTED_TAX'].astype('float')
        # expected tax calculation
        df['EXPECTED_TAX'] = df['EXPECTED_CHARGE'] /100 * df['EXPECTED_TAX']
        
    return df

# In[for single level/band with history]
def fn_single_level_band_with_history(df,df_charges):
    for i in range(0,len(df_charges)): 
        if(pd.isnull(df_charges['START_DATE'][i])):
            df.loc[(df['TIME_STAMP'] <= df_charges['END_DATE'][i]),'EXPECTED_CHARGE'] = df_charges['PERCENTAGE'][i]
            df.loc[(df['TIME_STAMP'] <= df_charges['END_DATE'][i]),'EXPECTED_TAX'] = df_charges['TAX'][i]
        elif(pd.isnull(df_charges['END_DATE'][i])):
            df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]),'EXPECTED_CHARGE'] = df_charges['PERCENTAGE'][i]
            df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]),'EXPECTED_TAX'] = df_charges['TAX'][i]
        else:
            df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]) & (df['TIME_STAMP'] <= df_charges['END_DATE'][i]),'EXPECTED_CHARGE'] = df_charges['PERCENTAGE'][i]
            df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]) & (df['TIME_STAMP'] <= df_charges['END_DATE'][i]),'EXPECTED_TAX'] = df_charges['TAX'][i] 
        #conversion
        df['EXPECTED_CHARGE'] = df['EXPECTED_CHARGE'].astype('float')
        df['EXPECTED_TAX'] = df['EXPECTED_TAX'].astype('float')
        df_charges['MINIMUM_AMOUNT'] = df_charges['MINIMUM_AMOUNT'].astype('float')
        df_charges['MAXIMUM_AMOUNT'] = df_charges['MAXIMUM_AMOUNT'].astype('float')
        # expected charge and tax calculation
        df['EXPECTED_CHARGE'] = round(df['TRANSACTION_AMOUNT'] /100 * df['EXPECTED_CHARGE'],2)
        df['EXPECTED_TAX'] = round(df['EXPECTED_CHARGE'] /100 * df['EXPECTED_TAX'],2)
        # comparing charges with minimum maximum amount
        if(pd.isnull(df_charges['START_DATE'][i])):
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_charges.iloc[i]['MINIMUM_AMOUNT']) == False):
                df.loc[(df['TIME_STAMP'] <= df_charges['END_DATE'][i]) & (df['EXPECTED_CHARGE'] < df_charges['MINIMUM_AMOUNT'][i]) , 'EXPECTED_CHARGE'] =  df_charges['MINIMUM_AMOUNT'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_charges.iloc[i]['MAXIMUM_AMOUNT']) == False):
                df.loc[(df['TIME_STAMP'] <= df_charges['END_DATE'][i]) & (df['EXPECTED_CHARGE'] > df_charges['MAXIMUM_AMOUNT'][i]) , 'EXPECTED_CHARGE'] =  df_charges['MAXIMUM_AMOUNT'][i]
        elif(pd.isnull(df_charges['END_DATE'][i])):
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_charges.iloc[i]['MINIMUM_AMOUNT']) == False):
                df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]) & (df['EXPECTED_CHARGE'] < df_charges['MINIMUM_AMOUNT'][i]) , 'EXPECTED_CHARGE'] =  df_charges['MINIMUM_AMOUNT'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_charges.iloc[i]['MAXIMUM_AMOUNT']) == False):
                df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]) & (df['EXPECTED_CHARGE'] > df_charges['MAXIMUM_AMOUNT'][i]) , 'EXPECTED_CHARGE'] =  df_charges['MAXIMUM_AMOUNT'][i]
        else:
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_charges.iloc[i]['MINIMUM_AMOUNT']) == False):
                df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]) & (df['TIME_STAMP'] <= df_charges['END_DATE'][i]) & (df['EXPECTED_CHARGE'] < df_charges['MINIMUM_AMOUNT'][i]) , 'EXPECTED_CHARGE'] =  df_charges['MINIMUM_AMOUNT'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_charges.iloc[i]['MAXIMUM_AMOUNT']) == False):
                df.loc[(df['TIME_STAMP'] >= df_charges['START_DATE'][i]) & (df['TIME_STAMP'] <= df_charges['END_DATE'][i]) & (df['EXPECTED_CHARGE'] > df_charges['MAXIMUM_AMOUNT'][i]) , 'EXPECTED_CHARGE'] =  df_charges['MAXIMUM_AMOUNT'][i]
                
    return df

# In[for multi level with history]
def fn_multi_level_with_history(df,df_chg):
    # for expected charge initialization
    df['EXPECTED_CHARGE'] = 0
    df['EXPECTED_TAX'] = 0

    for i in range (0,len(df_chg)):
        if(pd.isnull(df_chg['START_DATE'][i])):
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'CHARGE'] = round((df['TRANSACTION_AMOUNT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MIN_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]) & (df['CHARGE'] < df_chg['MIN_CHARGE'][i]) , 'CHARGE'] =  df_chg['MIN_CHARGE'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MAX_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]) & (df['CHARGE'] > df_chg['MAX_CHARGE'][i]) , 'CHARGE'] =  df_chg['MAX_CHARGE'][i]
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)


        elif(pd.isnull(df_chg['END_DATE'][i])):  
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'CHARGE'] = round((df['TRANSACTION_AMOUNT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MIN_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]) & (df['CHARGE'] < df_chg['MIN_CHARGE'][i]) , 'CHARGE'] =  df_chg['MIN_CHARGE'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MAX_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]) & (df['CHARGE'] > df_chg['MAX_CHARGE'][i]) , 'CHARGE'] =  df_chg['MAX_CHARGE'][i]
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax & 
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)



        else:
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'CHARGE'] = round((df['TRANSACTION_AMOUNT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MIN_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]) & (df['CHARGE'] < df_chg['MIN_CHARGE'][i]) , 'CHARGE'] =  df_chg['MIN_CHARGE'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MAX_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]) & (df['CHARGE'] > df_chg['MAX_CHARGE'][i]) , 'CHARGE'] =  df_chg['MAX_CHARGE'][i]
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['TRANSACTION_AMOUNT'] <= df_chg['MAX_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)



    df_chg = df_chg.loc[(df_chg['MAX_AMT'].isnull())]
    df_chg.reset_index(drop=True, inplace=True)

    for i in range (0,len(df_chg)):
        if(pd.isnull(df_chg['START_DATE'][i])):
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGE'] = round((df['TRANSACTION_AMOUNT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MIN_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['CHARGE'] < df_chg['MIN_CHARGE'][i]) , 'CHARGE'] =  df_chg['MIN_CHARGE'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MAX_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['CHARGE'] > df_chg['MAX_CHARGE'][i]) , 'CHARGE'] =  df_chg['MAX_CHARGE'][i]
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)  


        elif(pd.isnull(df_chg['END_DATE'][i])):
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGE'] = round((df['TRANSACTION_AMOUNT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MIN_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['CHARGE'] < df_chg['MIN_CHARGE'][i]) , 'CHARGE'] =  df_chg['MIN_CHARGE'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MAX_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['CHARGE'] > df_chg['MAX_CHARGE'][i]) , 'CHARGE'] =  df_chg['MAX_CHARGE'][i]
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)  


        else:
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGE'] = round((df['TRANSACTION_AMOUNT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for charge lesser then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MIN_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['CHARGE'] < df_chg['MIN_CHARGE'][i]) , 'CHARGE'] =  df_chg['MIN_CHARGE'][i]
            # for charge greter then minimum charge amount
            if(pd.isnull(df_chg.iloc[i]['MAX_CHARGE']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]) & (df['CHARGE'] > df_chg['MAX_CHARGE'][i]) , 'CHARGE'] =  df_chg['MAX_CHARGE'][i]
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)  
                
    return df

# In[for multi band with history]
def fn_multi_band_with_history(df,df_chg):
    # for expected charge initialization
    df['EXPECTED_CHARGE'] = 0
    df['EXPECTED_TAX'] = 0

    for i in range (0,len(df_chg)):
        if(pd.isnull(df_chg['START_DATE'][i])):
            # Chargable amount calculation
            df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGABLE_AMT'] = df['TRANSACTION_AMOUNT'] - (df_chg['MIN_AMT'][i])
            if(pd.isnull(df_chg.iloc[i]['MAX_AMT']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['CHARGABLE_AMT'] > (df_chg['MAX_AMT'][i] - df_chg['MIN_AMT'][i])), 'CHARGABLE_AMT'] = df_chg['MAX_AMT'][i] - df_chg['MIN_AMT'][i]
            else:
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] > (df_chg['MIN_AMT'][i])), 'CHARGABLE_AMT'] = df['TRANSACTION_AMOUNT'] - (df_chg['MIN_AMT'][i])
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGE'] = round((df['CHARGABLE_AMT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)


        elif(pd.isnull(df_chg['END_DATE'][i])):
            # Chargable amount calculation
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGABLE_AMT'] = df['TRANSACTION_AMOUNT'] - (df_chg['MIN_AMT'][i])
            if(pd.isnull(df_chg.iloc[i]['MAX_AMT']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['CHARGABLE_AMT'] > (df_chg['MAX_AMT'][i] - df_chg['MIN_AMT'][i])), 'CHARGABLE_AMT'] = df_chg['MAX_AMT'][i] - df_chg['MIN_AMT'][i]
            else:
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] > (df_chg['MIN_AMT'][i])), 'CHARGABLE_AMT'] = df['TRANSACTION_AMOUNT'] - (df_chg['MIN_AMT'][i])
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGE'] = round((df['CHARGABLE_AMT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)


        else:
            # Chargable amount calculation
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGABLE_AMT'] = df['TRANSACTION_AMOUNT'] - (df_chg['MIN_AMT'][i])
            if(pd.isnull(df_chg.iloc[i]['MAX_AMT']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['CHARGABLE_AMT'] > (df_chg['MAX_AMT'][i] - df_chg['MIN_AMT'][i])), 'CHARGABLE_AMT'] = df_chg['MAX_AMT'][i] - df_chg['MIN_AMT'][i]
            else:
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] > (df_chg['MIN_AMT'][i])), 'CHARGABLE_AMT'] = df['TRANSACTION_AMOUNT'] - (df_chg['MIN_AMT'][i])
            # for charge as per percentage
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'CHARGE'] = round((df['CHARGABLE_AMT'] * df_chg['PERCENTAGE'][i] /100),2)
            # for tax as per percentage
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'TAX'] = round((df['CHARGE'] * df_chg['TAX'][i] /100),2)

            # for expected charge
            df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_CHARGE'] = round((df['EXPECTED_CHARGE'] + df['CHARGE']),2)
            # for expected tax
            if(pd.isnull(df_chg.iloc[i]['TAX']) == False):
                df.loc[(df['TIME_STAMP'] >= df_chg['START_DATE'][i]) & (df['TIME_STAMP'] <= df_chg['END_DATE'][i]) & (df['TRANSACTION_AMOUNT'] >= df_chg['MIN_AMT'][i]), 'EXPECTED_TAX'] = round((df['EXPECTED_TAX'] + df['TAX']),2)
                
    return df