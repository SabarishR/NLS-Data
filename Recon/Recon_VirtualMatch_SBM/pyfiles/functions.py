#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  22 15:08:40 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]
from flask import current_app as app
import pyfiles.DB_connection as DBC
from datetime import datetime
from itertools import combinations
import pandas as pd
import json

# In[function for virtual match logic]
def fn_recon_virtualMatch(GL_df,RE_df,acc_no):
    
    # Column declaration
    GL_df[app.config['VAR_ISMATCHED']] = app.config['VAR_DEFAULT_MATCHED_VALUE']
    RE_df[app.config['VAR_ISMATCHED']] = app.config['VAR_DEFAULT_MATCHED_VALUE']
    GL_df[app.config['VAR_MATCH_TABLE']] = ''
    GL_df[app.config['VAR_MATCH_ID']] = ''
    
    # With in GL account match
    if(len(GL_df.loc[GL_df[app.config['VAR_ISMATCHED']]==0]) > 1):
        GL_df = fn_GLtoGL_Match(GL_df,acc_no)
        
    if((len(GL_df.loc[GL_df[app.config['VAR_ISMATCHED']]==0]) > 0) & (len(RE_df.loc[RE_df[app.config['VAR_ISMATCHED']]==0]) > 0)):
        # One to one match with GL to Nostro to avoid more combinations
        GL_df,RE_df = fn_GLtoNOSTRO_oneMatch(GL_df,RE_df,acc_no)
        # GL to Nostro all other combinations possible match
        GL_df,RE_df = fn_GLtoNOSTRO_combinationsMatch(GL_df,RE_df,acc_no)
    
    df = GL_df[(GL_df[app.config['VAR_ISMATCHED']] == 1) & (GL_df[app.config['VAR_MATCH_TABLE']].notnull())].copy()
    df[app.config['VAR_GL_ID']] = df[app.config['VAR_GL_ID']].astype('int')
    if(len(df) > 0):
        df = df.groupby([app.config['VAR_MATCH_ID'],app.config['VAR_MATCH_TABLE']])[app.config['VAR_GL_ID']].apply(list).reset_index(name=app.config['VAR_GL_ID'])
        df = df[[app.config['VAR_GL_ID'],app.config['VAR_MATCH_TABLE'],app.config['VAR_MATCH_ID']]]
        
        for i in range (0,len(df)):
            if(type(eval(df[app.config['VAR_MATCH_ID']][i])) != list):
                df.loc[i,app.config['VAR_MATCH_ID']] = str([int(df[app.config['VAR_MATCH_ID']][i])])
            
        json_data = df.to_json(orient='records')[1:-1]
    else:
        json_data = app.config['VAR_NO_MATCH']
    
    app.logger.info('Success')
    return json_data

# In[function for GL to Gl Match]
def fn_GLtoGL_Match(GL_df,acc_no):
    
    for i in range(0,len(GL_df)-1):
        if (GL_df[app.config['VAR_ISMATCHED']][i] == app.config['VAR_MATCHED_VALUE']):
            continue
        for j in range(i+1,len(GL_df)):
            if((GL_df[app.config['VAR_ISMATCHED']][j] == app.config['VAR_MATCHED_VALUE'])):
                continue
            amount = abs(GL_df[app.config['VAR_GL_AMOUNT']][i] + GL_df[app.config['VAR_GL_AMOUNT']][j])
            if amount <= app.config['VAR_ALLOWED_VARIANCE']:
                GL_df.loc[i,app.config['VAR_ISMATCHED']] = app.config['VAR_MATCHED_VALUE']
                GL_df.loc[j,app.config['VAR_ISMATCHED']] = app.config['VAR_MATCHED_VALUE']
                GL_df.loc[j,app.config['VAR_MATCH_TABLE']] = app.config['VAR_GLTOGL_MATCHED_TABLE']
                GL_df.loc[j,app.config['VAR_MATCH_ID']] = str(GL_df[app.config['VAR_GL_ID']][i])
                fn_insert_recon_virtualMatch(acc_no,str([int(GL_df[app.config['VAR_GL_ID']][i])]),app.config['VAR_GLTOGL_MATCHED_TABLE'],str([int(GL_df[app.config['VAR_GL_ID']][j])]),float(abs(GL_df[app.config['VAR_GL_AMOUNT']][i])),amount)
                break
    return GL_df

# In[function for GL to NOSTRO One match]
def fn_GLtoNOSTRO_oneMatch(GL_df,RE_df,acc_no):
    for i in range(0,len(GL_df)):
        if (GL_df[app.config['VAR_ISMATCHED']][i] == app.config['VAR_MATCHED_VALUE']):
            continue
        for j in range(0,len(RE_df)):
            if((RE_df[app.config['VAR_ISMATCHED']][j] == app.config['VAR_MATCHED_VALUE'])):
                continue
            amount = abs(GL_df[app.config['VAR_GL_AMOUNT']][i] + RE_df[app.config['VAR_RE_AMOUNT']][j])
            if amount <= app.config['VAR_ALLOWED_VARIANCE']:
                GL_df.loc[i,app.config['VAR_ISMATCHED']] = app.config['VAR_MATCHED_VALUE']
                RE_df.loc[j,app.config['VAR_ISMATCHED']] = app.config['VAR_MATCHED_VALUE']
                GL_df.loc[i,app.config['VAR_MATCH_TABLE']] = app.config['VAR_GLTONOSTRO_MATCHED_TABLE']
                GL_df.loc[i,app.config['VAR_MATCH_ID']] = str(RE_df[app.config['VAR_RE_ID']][j])
                fn_insert_recon_virtualMatch(acc_no,str([int(GL_df[app.config['VAR_GL_ID']][i])]),app.config['VAR_GLTONOSTRO_MATCHED_TABLE'],str([int(RE_df[app.config['VAR_RE_ID']][j])]),float(abs(GL_df[app.config['VAR_GL_AMOUNT']][i])),amount)
                break
    return GL_df,RE_df

# In[function for GL to NOSTRO combination matches]
def fn_GLtoNOSTRO_combinationsMatch(GL_df,RE_df,acc_no):
    
    GL_per_com_list = fn_iterate_combinations(GL_df,app.config['VAR_GL_ID'],app.config['VAR_GL_AMOUNT'])
    RE_per_com_list = fn_iterate_combinations(RE_df,app.config['VAR_RE_ID'],app.config['VAR_RE_AMOUNT'])
   
    GL_df[app.config['VAR_G_DATE']] = GL_df[app.config['VAR_GL_DATE']].dt.strftime(app.config['VAR_DATE_MATCH_FORMAT'])
    RE_df[app.config['VAR_R_DATE']] = RE_df[app.config['VAR_RE_DATE']].dt.strftime(app.config['VAR_DATE_MATCH_FORMAT'])
    
    GL_dict = fn_df_to_json(GL_df)
    RE_dict = fn_df_to_json(RE_df)
    
    GL_per_com_list = GL_per_com_list[:2500]    
    RE_per_com_list = RE_per_com_list[:2500]
    
    app.logger.info("GL Unmatched = {} , RE Unmatched = {}, Total Combination= {}".format(str(len(GL_df)),str(len(RE_df)),(len(GL_per_com_list)*len(GL_per_com_list))))
    # print("ACC NO - ",acc_no,"GL - ",len(GL_per_com_list),"RE - ",len(GL_per_com_list),"TOTAL - ",(len(GL_per_com_list)*len(GL_per_com_list)))
    
    for i in range(0,len(GL_per_com_list)):
        if (len([k for k in [dt for dt in GL_dict if dt[app.config['VAR_GL_ID']] in list(GL_per_com_list[i])] if k[app.config['VAR_ISMATCHED']] == 1]) > 0):
            continue
        if (len(set(k[app.config['VAR_G_DATE']] for k in [dt for dt in GL_dict if dt[app.config['VAR_GL_ID']] in list(GL_per_com_list[i])])) > 1):
            continue
        for j in range(0,len(RE_per_com_list)):
            if (len([k for k in [dt for dt in RE_dict if dt[app.config['VAR_RE_ID']] in list(RE_per_com_list[j])] if k[app.config['VAR_ISMATCHED']] == 1]) > 0):
                continue
            if (len(set(k[app.config['VAR_R_DATE']] for k in [dt for dt in RE_dict if dt[app.config['VAR_RE_ID']] in list(RE_per_com_list[j])])) > 1):
                continue
            if (set(k[app.config['VAR_G_DATE']] for k in [dt for dt in GL_dict if dt[app.config['VAR_GL_ID']] in list(GL_per_com_list[i])]) != set(k[app.config['VAR_R_DATE']] for k in [dt for dt in RE_dict if dt[app.config['VAR_RE_ID']] in list(RE_per_com_list[j])])):
                continue
            
            amount = abs(sum(k[app.config['VAR_GL_AMOUNT']] for k in [dt for dt in GL_dict if dt[app.config['VAR_GL_ID']] in list(GL_per_com_list[i])]) + sum(k[app.config['VAR_RE_AMOUNT']] for k in [dt for dt in RE_dict if dt[app.config['VAR_RE_ID']] in list(RE_per_com_list[j])]))
            
            if amount <= app.config['VAR_ALLOWED_VARIANCE']:
                for k in [dt for dt in GL_dict if dt[app.config['VAR_GL_ID']] in list(GL_per_com_list[i])]:
                    k[app.config['VAR_ISMATCHED']] = app.config['VAR_MATCHED_VALUE']
                    k[app.config['VAR_MATCH_TABLE']] = app.config['VAR_GLTONOSTRO_MATCHED_TABLE']
                    k[app.config['VAR_MATCH_ID']] = str(list(RE_per_com_list[j]))
    
                for k in [dt for dt in RE_dict if dt[app.config['VAR_RE_ID']] in list(RE_per_com_list[j])]:
                    k[app.config['VAR_ISMATCHED']] = app.config['VAR_MATCHED_VALUE']
                
                fn_insert_recon_virtualMatch(acc_no,str(list(GL_per_com_list[i])),app.config['VAR_GLTONOSTRO_MATCHED_TABLE'],str(list(RE_per_com_list[j])),float(abs(sum(k[app.config['VAR_GL_AMOUNT']] for k in [dt for dt in GL_dict if dt[app.config['VAR_GL_ID']] in list(GL_per_com_list[i])]))),amount)
                break
            
    GL_df = fn_json_to_df(GL_dict)
    RE_df = fn_json_to_df(RE_dict)
            
    return GL_df,RE_df

# In[function for GL to NOSTRO combination matches]
# def fn_GLtoNOSTRO_combinationsMatch(GL_df,RE_df):
    
#     GL_per_com_list = fn_iterate_combinations(GL_df,app.config['VAR_GL_ID'],app.config['VAR_GL_AMOUNT'])
#     RE_per_com_list = fn_iterate_combinations(RE_df,app.config['VAR_RE_ID'],app.config['VAR_RE_AMOUNT'])
    
#     GL = len(GL_per_com_list)
#     RE = len(RE_per_com_list)
#     TOT = len(GL_per_com_list)*len(RE_per_com_list)
#     print('GL Combinations - ',GL)
#     print('RE Combinations - ',RE)
#     print('Total Combinations - ',TOT)
    
#     for i in range(0,len(GL_per_com_list)):
#         if app.config['VAR_MATCHED_VALUE'] in (GL_df[GL_df[app.config['VAR_GL_ID']].isin(list(GL_per_com_list[i]))][app.config['VAR_ISMATCHED']].values):
#             continue
#         if len(GL_df[GL_df[app.config['VAR_GL_ID']].isin(list(GL_per_com_list[i]))][app.config['VAR_GL_DATE']].dt.strftime(app.config['VAR_DATE_MATCH_FORMAT']).unique()) > app.config['VAR_ALLOWED_DATE_VARIANCE']:
#             continue
#         for j in range(0,len(RE_per_com_list)):
#             print('GL Combinations - ',GL,' RE Combinations - ',RE,' GL - ',i," RE - ",j)
#             if app.config['VAR_MATCHED_VALUE'] in (RE_df[RE_df[app.config['VAR_RE_ID']].isin(list(RE_per_com_list[j]))][app.config['VAR_ISMATCHED']].values):
#                 continue
#             if len(RE_df[RE_df[app.config['VAR_RE_ID']].isin(list(RE_per_com_list[j]))][app.config['VAR_RE_DATE']].dt.strftime(app.config['VAR_DATE_MATCH_FORMAT']).unique()) > app.config['VAR_ALLOWED_DATE_VARIANCE']:
#                 continue
#             if ((GL_df[GL_df[app.config['VAR_GL_ID']].isin(list(GL_per_com_list[i]))][app.config['VAR_GL_DATE']].dt.strftime(app.config['VAR_DATE_MATCH_FORMAT']).unique()[0]) != (RE_df[RE_df[app.config['VAR_RE_ID']].isin(list(RE_per_com_list[j]))][app.config['VAR_RE_DATE']].dt.strftime(app.config['VAR_DATE_MATCH_FORMAT']).unique()[0])):
#                 continue
#             amount = abs((GL_df[GL_df[app.config['VAR_GL_ID']].isin(list(GL_per_com_list[i]))][app.config['VAR_GL_AMOUNT']].sum()) + (RE_df[RE_df[app.config['VAR_RE_ID']].isin(list(RE_per_com_list[j]))][app.config['VAR_RE_AMOUNT']].sum()))
#             if amount <= app.config['VAR_ALLOWED_VARIANCE']:
#                 GL_df.loc[GL_df[app.config['VAR_GL_ID']].isin(list(GL_per_com_list[i])),app.config['VAR_ISMATCHED']] = app.config['VAR_MATCHED_VALUE']
#                 RE_df.loc[RE_df[app.config['VAR_RE_ID']].isin(list(RE_per_com_list[j])),app.config['VAR_ISMATCHED']] = app.config['VAR_MATCHED_VALUE']
#                 GL_df.loc[GL_df[app.config['VAR_GL_ID']].isin(list(GL_per_com_list[i])),app.config['VAR_MATCH_TABLE']] = app.config['VAR_GLTONOSTRO_MATCHED_TABLE']
#                 GL_df.loc[GL_df[app.config['VAR_GL_ID']].isin(list(GL_per_com_list[i])),app.config['VAR_MATCH_ID']] = str(list(RE_per_com_list[j]))
#                 break
#     return GL_df,RE_df
    
# In[function for iterate combinations]
def fn_iterate_combinations(df,id,amount):
    
    dict_data = df.loc[df[app.config['VAR_ISMATCHED']]==0].set_index(id)[amount].to_dict()
    combination = [i for j in range((app.config['VAR_MAX_COMBINATION_LENGTH']+1)) for i in combinations(dict_data, j) if sum(map(dict_data.get, i))]
    
    return combination

# In[function to convert df to json]
def fn_df_to_json(df):
    
    df_dict = df.to_json(orient='records')
    df_dict = json.loads(df_dict)
    
    return df_dict

# In[function to convert json to df]
def fn_json_to_df(df_dict):
    
    df = pd.json_normalize(df_dict)
    
    return df

# In[function for reset dataframe index]
def fn_reset_dfIndex(df):
    
    df.reset_index(drop=True, inplace=True)
    
    return df

# In[function for find existing statement id]
def fn_existingGLID(matched_GL):
    
    GL_list = []
    for i in matched_GL[app.config['VAR_GL_ID']]:
        GL_list += eval(i)
    for i in matched_GL[app.config['VAR_MATCH_ID']]:
        if eval(i) != 0 :
            GL_list += eval(i)
    
    return GL_list

# In[function for find existing nostro id]
def fn_existingREID(matched_RE):
    
    RE_list = []
    for i in matched_RE[app.config['VAR_RE_ID']]:
        RE_list += eval(i)
    
    return RE_list

# In[function for insert prediction details]
def fn_insert_recon_virtualMatch(acc_no,statement_id,match_table,match_id,match_amount,variance):
    
    param = {
            'ACCOUNT_NO' : acc_no,
            'STATEMENT_DETAIL_ID' : statement_id,
            'MATCH_TABLE' : match_table,
            'MATCH_ID' : match_id,
            'MATCH_AMOUNT' : match_amount,
            'VARIANCE' : round(variance,2),
            "CREATED_BY":app.config['VAR_ML_USERNAME'],
            "CREATED_ON":datetime.now()
            }
    
    DBC.mysql_insertData(app.config['MYSQL_INSERT_RECON_POSSIBLE_MATCH'],param)
    
# In[function for insert prediction details]
def fn_insert_recon_execution_history(acc_no,response):
    
    param = {
            'ACCOUNT_NO' : acc_no,
            'RESPONSE' : response,
            "CREATED_BY":app.config['VAR_ML_USERNAME'],
            "CREATED_ON":datetime.now()
            }
    
    DBC.mysql_insertData(app.config['MYSQL_INSERT_RECON_POSSIBLE_MATCH'],param)
            
