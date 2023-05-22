#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 15:39:34 2021

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]
from flask import current_app as app
import pyfiles.DB_connection as DBC
import pandas as pd
import numpy as np
import itertools
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score,explained_variance_score,mean_absolute_error,mean_squared_error
import joblib

# In[function to Drop NA]
def fn_createDataframe():
        
    # Declaration
    CRB_CHECK = []
    GENDER = []
    # Reading account trunover ranges
    ACC_TURNOVER_RANGE = pd.read_csv(app.config['VAR_ACCOUNT_TURNOVER_RANGE'])
    # Reading age ranges
    AGE_RANGE = pd.read_csv(app.config['VAR_AGE_RANGE'])
    # Reading CRB_SCORE ranges
    CRB_CHECK_RANGE = pd.read_csv(app.config['VAR_CRB_CHECK_RANGE'])
    # Binning the Range to values
    ACCOUNT_TURNOVER = ACC_TURNOVER_RANGE[app.config['VAR_DF_BINNING_COL']].tolist()
    CRB_CHECK = CRB_CHECK_RANGE[app.config['VAR_DF_BINNING_COL']].tolist()
    GENDER = fn_convertJSON_toList(app.config['VAR_GENDER'],GENDER)    
    AGE = AGE_RANGE[app.config['VAR_DF_BINNING_COL']].tolist()
    AVG_TURNOVER = np.arange(app.config['VAR_AVG_TRUNOVER_MIN'],app.config['VAR_AVG_TRUNOVER_MAX'],1).tolist()
    
    # Creation of List with all possible combinations 
    ITERATION_LIST = [ACCOUNT_TURNOVER,CRB_CHECK,GENDER,AGE,AVG_TURNOVER]
    ITERATION_LIST = list(itertools.product(*ITERATION_LIST))
    # Converting list to pandas dataframe
    df = pd.DataFrame(ITERATION_LIST, columns=app.config['VAR_DATAFRAME_COLUMNS'])
    
    # Assigning weight to the values
    ACC_TURNOVER_TOREPLACE = fn_convertWeights_toJson(ACC_TURNOVER_RANGE)
    AGE_TOREPLACE = fn_convertWeights_toJson(AGE_RANGE)
    CRB_CHECK_TOREPLACE = fn_convertWeights_toJson(CRB_CHECK_RANGE)
    
    # Creating weighted columns
    df = fn_mapReplace_dfValues(df,app.config['VAR_ACCOUNT_TURNOVER_COL'],app.config['VAR_ACCOUNT_TURNOVER_WEIGHT_COL'],ACC_TURNOVER_TOREPLACE)
    df = fn_mapReplace_dfValues(df,app.config['VAR_CRB_CHECK_COL'],app.config['VAR_CRB_CHECK_WEIGHT_COL'],CRB_CHECK_TOREPLACE)
    df = fn_mapReplace_dfValues(df,app.config['VAR_GENDER_COL'],app.config['VAR_GENDER_WEIGHT_COL'],app.config['VAR_GENDER_TO_REPLACE'])
    df = fn_mapReplace_dfValues(df,app.config['VAR_AGE_COL'],app.config['VAR_AGE_WEIGHT_COL'],AGE_TOREPLACE)
    
    # replace account turnover weight as 0 if the turnover amount less then 5000
    df.loc[(df[app.config['VAR_AVG_TURNOVER']] < ACC_TURNOVER_RANGE[app.config['VAR_DF_MIN_COL']][0]), app.config['VAR_ACCOUNT_TURNOVER_WEIGHT_COL']] = app.config['VAR_LOAN_AMT_LESSTHEN_MINTURNOVER']
    # Customer's total weight as per the values 
    df[app.config['VAR_CUSTOMER_WEIGHT_COL']] = df[app.config['VAR_COL_FOR_CUSTOMER_WEIGHT_SUM']].sum(axis=1)
    # Customers score in percentage
    df[app.config['VAR_CUSTOMER_SCORE_COL']] = round(df[app.config['VAR_CUSTOMER_WEIGHT_COL']] /app.config['VAR_TOTAL_WEIGHT'] * 100)
    df[app.config['VAR_CUSTOMER_SCORE_COL']]=df[app.config['VAR_CUSTOMER_SCORE_COL']].astype(int)
    
    # Replacing customer scores with proposed loan percentage 
    # Reading proposed loan ranges
    PROPOSED_LOAN_RANGE = pd.read_csv(app.config['VAR_PROPOSED_LOAN_RANGE'])
    for i in range (0,len(PROPOSED_LOAN_RANGE)):
        df.loc[(df[app.config['VAR_CUSTOMER_SCORE_COL']] >= PROPOSED_LOAN_RANGE[app.config['VAR_DF_MIN_COL']][i]) & (df[app.config['VAR_CUSTOMER_SCORE_COL']] <= PROPOSED_LOAN_RANGE[app.config['VAR_DF_MAX_COL']][i]), app.config['VAR_CUSTOMER_SCORE_COL']] = PROPOSED_LOAN_RANGE[app.config['VAR_DF_WEIGHT_COL']][i]
    df[app.config['VAR_CUSTOMER_SCORE_COL']]=df[app.config['VAR_CUSTOMER_SCORE_COL']].astype(int)
    
    # Calculating loan approved amount
    df[app.config['VAR_LOAN_AMOUNT']] = round(df[app.config['VAR_AVG_TURNOVER']]/100 * df[app.config['VAR_CUSTOMER_SCORE_COL']])
    df[app.config['VAR_LOAN_AMOUNT']]=df[app.config['VAR_LOAN_AMOUNT']].astype(int)
    
    # removing the values which has the approved loan amount greater then 52500 
    df.drop(df.loc[(df[app.config['VAR_LOAN_AMOUNT']] > app.config['VAR_MAX_LOAN_AMOUNT_FORMODEL'])].index, inplace=True)
    # to reset index 
    df.reset_index(drop=True, inplace=True)
    # Replacing Loan amount is  < 1000 then 0 and > 50000 then 50000 because Minimum Loan - 1000 AND Maximum Loan - 50000
    df.loc[df[app.config['VAR_LOAN_AMOUNT']] < app.config['VAR_MIN_LOAN_APPROVED_AMT'],app.config['VAR_LOAN_AMOUNT']] = app.config['VAR_LOAN_AMT_LESSTHEN_MINLOANAMT']
    df.loc[df[app.config['VAR_LOAN_AMOUNT']] > app.config['VAR_MAX_LOAN_APPROVED_AMT'],app.config['VAR_LOAN_AMOUNT']] = app.config['VAR_MAX_LOAN_APPROVED_AMT']
    
    return df

# In[function for json to list]
def fn_convertJSON_toList(var_json,var_list):
    for key, value in var_json.items():
        var_list.append(value)
        
    return var_list

# In[function for df to json]
def fn_convertWeights_toJson(df):
    
    data = {}
    for i in range(0,len(df)):
        data[df[app.config['VAR_DF_BINNING_COL']][i]] = df[app.config['VAR_DF_WEIGHT_COL']][i]
    
    return data

# In[function for replace a values in a dataframe]
def fn_mapReplace_dfValues(df,actual_col,weighted_col,replace_val):
    
    df[weighted_col] = df[actual_col].map(replace_val)
    
    return df

# In[function to get datetime]
def fn_getdatetime():
    
    return datetime.now().strftime("%Y%m%d%H%M")

# In[function to train test and scaling]
def fn_trainTest_split(dataframe,random_state):
    
    y = dataframe[app.config['VAR_PREDICTOR_COLUMNS']].copy()
    X = dataframe.drop(app.config['VAR_PREDICTOR_COLUMNS'], axis=1)
    
    # Splitting the dataset into the Training set and Test set. test size is 20 %
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = random_state)
    
    # writing the cleansed CSV for later use
    dataframe.to_csv(app.config['VAR_RF_REGRESSOR_CLEANSED_CSV'])
    # Feature Scaling
    # there is no need to apply future scaling on dependent variable
    sc = StandardScaler()   
    scalar = sc.fit(X_train)
    X_train = scalar.transform(X_train)
    X_test = scalar.transform(X_test)
    # here converting the whole dataframe using scalar since we train the model all possible conditions
    X = scalar.transform(X)
    # convert y dataframe to array because we train the model all possible conditions
    y = np.array(y)
    
    return scalar,X,y,X_test, y_test

# In[function for XGB classifier]
def fn_RF_regressorTrain(X,y):
    
    # Model initialization and model training
    model = RandomForestRegressor(**app.config['VAR_RF_REGRESSOR_OPTIMAL_PARAM'])
    model = MultiOutputRegressor(model,n_jobs= -1)
    model.fit(X, y)
    
    return model

# In[Save the model]
def fn_joblib_modelSave(model,filename,fileformat,compress = None):
    
    # Save the model
    filename = filename+fn_getdatetime()+fileformat
    joblib.dump(model, filename,compress = compress)
    return filename

# In[load model]
def fn_joblib_modelLoad(filename):
    
    # Load the model
    model = joblib.load(filename)
    
    return model

# In[function for model score]
def fn_regressor_modelScore(model,X_test,y_test):
    
    # prediction
    y_pred = model.predict(X_test)
    
    # calculating score values
    r2score = round(r2_score(y_test, y_pred),8)
    explained_variance = round(explained_variance_score(y_test, y_pred),8)
    mae = round(mean_absolute_error(y_test, y_pred),8)
    mse = round(mean_squared_error(y_test, y_pred),8)
    rmse = round(mean_squared_error(y_test, y_pred,squared = False),8)
    
    return r2score,explained_variance,mae,mse,rmse

# In[fnction for range to  binning]
def fn_valueTo_binning(df,bin_df,columnname):
    bin_df = pd.read_csv(bin_df)
    for i in range(0,len(bin_df)):
        df.loc[(df[columnname] >= bin_df[app.config['VAR_DF_MIN_COL']][i]) & (df[columnname] <= bin_df[app.config['VAR_DF_MAX_COL']][i]), columnname] = bin_df[app.config['VAR_DF_BINNING_COL']][i]
        
    return df

# In[function for calculating credit score grade]
def fn_calculate_creditscoreGrade(creditscore):
    
    creditPercent = round(creditscore / app.config['VAR_TOTAL_WEIGHT'] * 100 ,2)
    df = pd.read_csv(app.config['VAR_PROPOSED_LOAN_RANGE'])
    df = df[(df[app.config['VAR_DF_MIN_COL']] <= creditPercent) &  (df[app.config['VAR_DF_MAX_COL']] >= creditPercent)]
    df = df.reset_index(drop=True)
    
    return df['WEIGHT'][0]
    
# In[function for insert model details]
def fn_insert_modelDetails(modelname,model_filename,scalar_filename,r2score,explained_variance,mae,mse,rmse):
    
    data = {
        "MODEL_NAME":modelname,
        "FILE_NAME":model_filename,
        "SCALAR_NAME":scalar_filename,
        "R2SCORE":float(r2score),
        "EXPLAINEDVARIANCE":float(explained_variance),
        "MAE":float(mae),
        "MSE":float(mse),
        "RMSE":float(rmse),
        "CREATED_BY":app.config['VAR_ML_USERNAME'],
        "CREATED_ON":datetime.now()
        }
    
    DBC.mysql_insertData(app.config['MYSQL_INSERT_MODELINFORMATION'],data)

# In[function for insert prediction details]
def fn_insert_modelprediction(modelID,userinput,output):
    
    data = {
        "MODEL_ID":modelID,
        "INPUT":userinput,
        "OUTPUT":output,
        "CREATED_BY":app.config['VAR_ML_USERNAME'],
        "CREATED_ON":datetime.now()
        }
    
    DBC.mysql_insertData(app.config['MYSQL_INSERT_MODELPREDICTION'],data)

# In[function for rejecting based on age]
def fn_rejection_criteria(ACCOUNT_NUMBER,PHONE_NUMBER,AGE):
    
    STATUS = True
    #AML Blocklist
    data = {
        "ACCOUNT_NUMBER" : ACCOUNT_NUMBER
            } 
    df = DBC.mysql_readTable(app.config['MYSQL_SELECT_RF_REGRESSOR_MOBILEBLOCKEDACCOUNTS'],data)
    if (len(df) > 0):
        STATUS = app.config['VAR_AML_BLOCKLIST_REJECT']
        
        return STATUS
    
    # PAR Rejection criteria 
    PHONE_NUMBER = PHONE_NUMBER[app.config['VAR_PHONE_NUMBER_PREFIX_REMOVE']:]
    PHONE_NUMBER = app.config['VAR_PHONE_NUMBER_PREFIX_ADD'] + PHONE_NUMBER
    data = {
        "TELEPHONE" : PHONE_NUMBER
            } 
    df = DBC.mysql_readTable(app.config['MYSQL_SELECT_RF_REGRESSOR_PARREPORTSLOG'],data)
    if (len(df) > 0):
        STATUS = app.config['VAR_AML_PAR_REJECT']
        
        return STATUS

    # age Rejection criteria
    criteria = pd.read_csv(app.config['VAR_AGE_RANGE'])
    if(criteria[app.config['VAR_DF_MIN_COL']][0] > AGE):
        STATUS = app.config['VAR_AGE_REJECT']
        
        return STATUS
        
    return STATUS
            
