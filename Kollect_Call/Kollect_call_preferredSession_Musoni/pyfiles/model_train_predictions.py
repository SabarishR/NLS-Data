#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:04:12 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from flask import current_app as app
# from Kollect_preferredSession_app import flask_app as app
import pyfiles.DB_connection as DBC
import pyfiles.functions as CF
import pandas as pd
import numpy as np
import json

# In[function for train XGB Model Training]:
def to_kollectCall_preferredSession_xgbClassifier_modelTraining():
    
    # Reading the required table
    df = DBC.mysql_readTable(app.config['MYSQL_SELECT_CUSTOMERINFORMATION'])
    # Replacing the empty string to NA
    df.replace(r'', np.NaN, inplace=True)
    # Using forward fill replacing the NA values
    df = df.fillna(method='ffill')
    # Changing timestamp to pandas datetime
    df[app.config['VAR_TIME_STAMP']] = pd.to_datetime(df[app.config['VAR_TIME_STAMP']], errors='coerce')
    # Droping the NA Rows
    df = CF.fn_dropna(df)
    # Converting timestamp to session
    df[app.config['VAR_SESSION_COLUMNNAME']] = CF.fn_datetimeTo_sessions(df.TIME_STAMP.dt.hour)
    
    # Converting dataframe column datatype
    df[app.config['VAR_LOAN_TYPE']] = df[app.config['VAR_LOAN_TYPE']].astype('int')
    df[app.config['VAR_BRANCH']] = df[app.config['VAR_BRANCH']].astype('int')
    # Grouping the ID with sessions to get each customer call count against each session
    df[app.config['VAR_FREQUENCY_COLUMNNAME']] = df.groupby(['ID',app.config['VAR_SESSION_COLUMNNAME'],app.config['VAR_PROMISE_SUCCESS']])[app.config['VAR_SESSION_COLUMNNAME']].transform('count')
    # Removing the duplicated values
    df = CF.fn_dropDuplicates(df,["ID",app.config['VAR_SESSION_COLUMNNAME'],app.config['VAR_PROMISE_SUCCESS'],app.config['VAR_LOAN_STATUS']])
    # pivoting the table using unique id and promise status
    df_pivot = df.pivot_table(index=['ID', app.config['VAR_PROMISE_SUCCESS']], columns=app.config['VAR_SESSION_COLUMNNAME'], values=app.config['VAR_FREQUENCY_COLUMNNAME']).reset_index()
    # fill na
    df_pivot = CF.fn_fillna(df_pivot,0)
    # merge two dataframes
    df =CF.fn_mergeTwo_dataframe(df,df_pivot,['ID',app.config['VAR_PROMISE_SUCCESS']])
    
    # Removing the duplicated values
    df = CF.fn_dropDuplicates(df,["ID",app.config['VAR_PROMISE_SUCCESS'],app.config['VAR_LOAN_STATUS']])
    # Added preffered session to the respective customer
    AVL_SESSION = df[app.config['VAR_SESSION_COLUMNNAME']].unique().tolist()  
    df[app.config['VAR_PREFERREDSESSION_COLUMNAME']] = df[AVL_SESSION].idxmax(axis=1)
    # drop unnecessory columns
    df = CF.fn_dropColumns(df,["ID",app.config['VAR_TIME_STAMP'],app.config['VAR_FREQUENCY_COLUMNNAME'],app.config['VAR_SESSION_COLUMNNAME'],app.config['VAR_CUSTOMER_STATUS']])
    # store onehot list to DB
    onehotlist = CF.fn_get_onehotList(df,app.config['VAR_XGB_CLASSIFIER_ONEHOT_LIST'])
    # one hot encoding
    df = CF.fn_onehotencode(df,app.config['VAR_XGB_CLASSIFIER_ONEHOT_LIST'])
    
    # perform train,test split and scaling
    scalar,X_train, X_test, y_train, y_test,columns = CF.fn_trainTest_split(df,app.config['VAR_TRAINTESTSPLIT_RANDOMSTATE'])
    # save scalar model
    scalar_filename = CF.fn_joblib_modelSave(scalar,app.config['VAR_XGB_CLASSIFIER_SCALAR_NAME'],app.config['VAR_MODEL_FILE_FORMAT'])
    # model training
    model = CF.fn_XGB_classifierTrain(X_train,y_train)
    # save model
    model_filename = CF.fn_joblib_modelSave(model,app.config['VAR_XGB_CLASSIFIER_MODEL_NAME'],app.config['VAR_MODEL_FILE_FORMAT'])
    # model score
    accuracy,F1_score,Sensitivity,Specificity,FPR,FNR = CF.fn_classifier_modelScore(model,X_test,y_test)
    
    # save model score
    CF.fn_insert_modelDetails(app.config['VAR_XGB_CLASSIFIER_MODEL'],model_filename,scalar_filename,accuracy,F1_score,Sensitivity,Specificity,FPR,FNR,columns,onehotlist)
    
    return "Success"

# In[function for train XGB Model Training]:
def to_kollectCall_preferredSession_xgbClassifier_modelPredictions(data):
    
    # create an Empty DataFrame object
    df = pd.DataFrame()
    # select the latest model 
    df_modelInfo = DBC.mysql_readTable(app.config['MYSQL_SELECT_XGB_CLASSIFIER_MODELINFORMATION'])
    # obtaining onehot list
    onehotJson = CF.fn_generate_onehotList(app.config['VAR_XGB_CLASSIFIER_ONEHOT_LIST'],data,eval(df_modelInfo['ONEHOT_LIST'][0]))
    # constructing json from user IP
    userIPjson = {'ID':[int(data['ID'])],'BRANCH':[int(data['BRANCH'])],'LOAN_TYPE':[int(data['LOAN_TYPE'])]}   
    #merge json
    merged_json = CF.fn_jsonMerge(userIPjson,onehotJson)
    #fetching customer call history
    param = {
                "ID":str(data['ID']),
                "PROMISE_SUCCESS":str(data['PROMISE_SUCCESS'])
            }
    df_callHistory = DBC.mysql_readTable(app.config['MYSQL_SELECT_CUSTOMERINFORMATION_USINGID'],param)
    
    # constructing History table
    if (len(df_callHistory) != 0):
        # call history
        df_session = CF.fn_session_pivotforPredictions(df_callHistory)
        #json to dataframe 
        df = CF.fn_jsontoDataframe(merged_json)
        #converting id to int datatype
        df_session['ID']=df_session['ID'].astype(int)
        #merge two dataframes
        df = CF.fn_mergeTwo_dataframe(df_session,df,['ID'])
    else :
        #empty json sessions
        json_session = CF.fn_empty_jsonSessions(app.config['VAR_SESSIONS'])
        #merge json
        merged_json = CF.fn_jsonMerge(merged_json,json_session)
        #json to dataframe 
        df = CF.fn_jsontoDataframe(merged_json)
    
    #reordering the dataframe colums
    df = df[eval(df_modelInfo['DATASET_COLUMNS'][0])]
    # scalling model
    scalar = CF.fn_joblib_modelLoad(df_modelInfo['SCALAR_NAME'][0])
    modelIP = scalar.transform(df)
    #prediction
    model = CF.fn_joblib_modelLoad(df_modelInfo['FILE_NAME'][0])
    preffered_session = model.predict(modelIP)
    # selecting respective time_split for the predicted session
    session_index = app.config['VAR_SESSIONS'].index(preffered_session[0])
    time_split = str(app.config['VAR_DATETIME_SESSION_SPLIT'][session_index]) +'-'+ str(app.config['VAR_DATETIME_SESSION_SPLIT'][session_index+1])
    # json output
    output = {
                "ID" : data['ID'],
                "ACTIVITY":app.config['VAR_ACTIVITY_TYPE'],
                "TIME_SPLIT":time_split,
                "PREFERRED_SESSION" : preffered_session[0]
            }
    # inserting the details to the table
    CF.fn_insert_modelprediction(str(df_modelInfo['ID'][0]),json.dumps(data),json.dumps(output))
    # return preffered_session
    return json.dumps(output)
