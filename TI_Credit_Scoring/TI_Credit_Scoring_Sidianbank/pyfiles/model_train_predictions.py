#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  25 11:27:03 2021

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
import json

# In[function for train RF Model Training]:
def to_TI_creditScoring_rfRegressor_modelTraining():
    
    #Creating required dataframe using all possible conditions
    df = CF.fn_createDataframe()
    ## Selecting the exact features required for modelling
    df = df[app.config['VAR_RF_REGRESSPR_COLUMNS_LIST']]
    # perform train,test split and scaling
    scalar,X,y,X_test, y_test = CF.fn_trainTest_split(df,app.config['VAR_TRAINTESTSPLIT_RANDOMSTATE'])
    # save scalar model
    scalar_filename = CF.fn_joblib_modelSave(scalar,app.config['VAR_RF_REGRESSOR_SCALAR_NAME'],app.config['VAR_MODEL_FILE_FORMAT'])
    # model training
    model = CF.fn_RF_regressorTrain(X,y)
    # save model
    model_filename = CF.fn_joblib_modelSave(model,app.config['VAR_RF_REGRESSOR_MODEL_NAME'],app.config['VAR_MODEL_FILE_FORMAT'],9)
    # model score
    r2score,explained_variance,mae,mse,rmse = CF.fn_regressor_modelScore(model,X_test,y_test)
    
    # save model score
    CF.fn_insert_modelDetails(app.config['VAR_RF_REGRESSOR_MODEL'],model_filename,scalar_filename,r2score,explained_variance,mae,mse,rmse)
    
    return "Success"

# In[function for Predict RF model]:
def to_TI_creditScoring_rfRegressor_modelPredictions(data):
    
    # select the latest model 
    df_modelInfo = DBC.mysql_readTable(app.config['MYSQL_SELECT_RF_REGRESSOR_MODELINFORMATION'])
    # select AGE,GENDER,CRB_SCORE against the document id 
    param = {
                "ID_NUMBER":data['ID_DOCUMENT']
            }
    df_customerDetail = DBC.mysql_readTable(app.config['MYSQL_SELECT_RF_REGRESSOR_CUSTOMERDETAILS'],param)
    # rejection criteria's
    STATUS = CF.fn_rejection_criteria(str(data['ACCOUNT_NUMBER']),str(data['PHONE_NUMBER']),int(df_customerDetail['AGE'][0]))
    if (STATUS == True):
        #binning CRB_SCORE
        # Reading CRB_SCORE ranges
        CRB_CHECK = pd.read_csv(app.config['VAR_CRB_CHECK_RANGE'])
        CRB_CHECK = CRB_CHECK[(CRB_CHECK[app.config['VAR_DF_MIN_COL']] <= int(df_customerDetail['CRB_SCORE'][0])) &  (CRB_CHECK[app.config['VAR_DF_MAX_COL']] >= int(df_customerDetail['CRB_SCORE'][0]))]  
        CRB_CHECK = CRB_CHECK.reset_index(drop=True)
    
        # Json conversion
        df = {'ACCOUNT_TURNOVER':[int(data['ACCOUNT_TURNOVER'])],'CRB_CHECK':[CRB_CHECK[app.config['VAR_DF_WEIGHT_COL']][0]],'GENDER':[app.config['VAR_GENDER'][df_customerDetail['GENDER'][0]]],'AGE':[int(df_customerDetail['AGE'][0])],'AVG_TURNOVER':[int(data['ACCOUNT_TURNOVER'])]}
        #converting json to dataframe
        df = pd.DataFrame(data=df)
        # converting value to binning
        df = CF.fn_valueTo_binning(df,app.config['VAR_ACCOUNT_TURNOVER_RANGE'],app.config['VAR_ACCOUNT_TURNOVER_COL'])
        df = CF.fn_valueTo_binning(df,app.config['VAR_AGE_RANGE'],app.config['VAR_AGE_COL'])
        # scalling model
        scalar = CF.fn_joblib_modelLoad(df_modelInfo['SCALAR_NAME'][0])
        modelIP = scalar.transform(df)
        #prediction
        model = CF.fn_joblib_modelLoad(df_modelInfo['FILE_NAME'][0])
        creditScore = model.predict(modelIP)
        # calculating credit score grade
        creditScore_grade = CF.fn_calculate_creditscoreGrade(creditScore[0][0])
        if (int(creditScore[0][1]) <= 0):
            STATUS = app.config['VAR_AMOUNT_REJECT']
        # json output
        output = {
                     "ID_DOCUMENT" : data['ID_DOCUMENT'],
                     "ACCOUNT_NUMBER" : data['ACCOUNT_NUMBER'],
                     "CREDIT_SCORE_POINTS" : round(creditScore[0][0],2),
                     "CREDIT_SCORE_GRADE" : int(creditScore_grade),
                     "ALLOCATED_CREDIT_LIMIT" : int(creditScore[0][1]),
                     "STATUS" : STATUS
                 }
    else:
        output = {
                    "ID_DOCUMENT" : data['ID_DOCUMENT'],
                    "ACCOUNT_NUMBER" : data['ACCOUNT_NUMBER'],
                    "STATUS" : STATUS
                 }
    
    # inserting the details to the table
    CF.fn_insert_modelprediction(str(df_modelInfo['ID'][0]),json.dumps(data),json.dumps(output))
    # return preffered_session
    return json.dumps(output)

    
    
    
