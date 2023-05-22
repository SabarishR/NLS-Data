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
from datetime import datetime
from jsonmerge import merge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score,f1_score
import joblib

# In[function to Drop NA]
def fn_dropna(dataframe):
    
    # Replacing emoty string with NA
    dataframe.replace(r'', np.NaN, inplace=True)
    #dropping NA
    dataframe.dropna(inplace=True)
    dataframe.reset_index(drop=True, inplace=True)
    
    return dataframe

# In[funtion to fill NA]
def fn_fillna(dataframe,fillvalue):
    
    dataframe.fillna(fillvalue, inplace=True)
    
    return dataframe

# In[pandas drop columns]
def fn_dropColumns(dataframe,columns):
    
    dataframe = dataframe.drop(columns, axis = 1)
    
    return dataframe

# In[function to drop duplicates]
def fn_dropDuplicates(dataframe,columns):
    
    dataframe = dataframe.drop_duplicates(columns,ignore_index = True)
    
    return dataframe

# In[function to merge to dataframe]
def fn_mergeTwo_dataframe(df1,df2,merge_column):
    
    df1 = pd.merge(df1, df2, on=merge_column)
    
    return df1

# In[Function for replace values in a dataframe column]
def fn_replace_dfcolumnvalues(df,columnname,actualval,replaceval):
    
    df[columnname] = df[columnname].replace(actualval,replaceval)
    
    return df

# In[function for merge json]
def fn_jsonMerge(json1,json2):
    
    json1 = merge(json1,json2)
    
    return json1 

# In[function for json to pandas dataframe]
def fn_jsontoDataframe(json):
    
    df = pd.DataFrame(data=json)
    
    return df

# In[function to convert datetime to sessions]
def fn_datetimeTo_sessions(datetime):
    
    session = pd.cut(datetime, bins=app.config['VAR_DATETIME_SESSION_SPLIT'], labels=app.config['VAR_SESSIONS'], include_lowest=True)
    
    return session

# In[fuction to get onehot list]
def fn_get_onehotList(df,onehot_columns):
    
    onehot_list = []
    for i in onehot_columns:
        onehot_list.append(df[i].unique().tolist())
        
    return onehot_list

# In[funtion to onehot encode]
def fn_onehotencode(dataframe,columns):
    
    dataframe = pd.get_dummies(dataframe, drop_first =True ,columns=columns,dtype = int,sparse=True)
    
    return dataframe

# In[function to label encode]
def fn_labelEncode(dataframe,labelval):
    
    dataframe = dataframe.replace(labelval)
    
    return dataframe

# In[function to get datetime]
def fn_getdatetime():
    
    return datetime.now().strftime("%Y%m%d%H%M")

# In[function to train test and scaling]
def fn_trainTest_split(dataframe,random_state):
    
    y = dataframe[app.config['VAR_PREFERREDSESSION_COLUMNAME']].copy()
    X = dataframe.drop(app.config['VAR_PREFERREDSESSION_COLUMNAME'], axis=1)
    
    # Storing dataset column order
    columns = X.columns.tolist()
    
    # Splitting the dataset into the Training set and Test set. test size is 20 %
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = random_state)
    
    # writing the cleansed CSV for later use
    # dataframe.to_csv(app.config['VAR_XGB_CLASSIFIER_CLEANSED_CSV'])
    # Feature Scaling
    # there is no need to apply future scaling on dependent variable
    sc = StandardScaler()   
    scalar = sc.fit(X_train)
    X_train = scalar.transform(X_train)
    X_test = scalar.transform(X_test)
    
    return scalar,X_train, X_test, y_train, y_test,columns

# In[function for XGB classifier]
def fn_XGB_classifierTrain(X_train,y_train):
    
    # Model training
    model = XGBClassifier(**app.config['VAR_XGB_CLASSIFIER_OPTIMAL_PARAM'], num_class = y_train.nunique())
    model.fit(X_train,y_train)
    
    return model

# In[Save the model]
def fn_joblib_modelSave(model,filename,fileformat):
    
    # Save the model
    filename = filename+fn_getdatetime()+fileformat
    joblib.dump(model, filename)
    return filename

# In[load model]
def fn_joblib_modelLoad(filename):
    
    # Load the model
    model = joblib.load(filename)
    
    return model

# In[function for model score]
def fn_classifier_modelScore(model,X_test,y_test):
    
    # prediction
    y_pred = model.predict(X_test)
    
    # confusion matrix for the predictions
    cnf_matrix = confusion_matrix(y_true = np.array(y_test),y_pred = y_pred, labels = model.classes_)
    # Accuracy is used when the True Positives and True negatives are more important while 
    accuracy = np.round(accuracy_score(np.array(y_test), y_pred),3)
    #  F1 score - F-score or F-measure is a measure of a test's accuracy
    # Sensitivity(recall) - true positive rate
    # specificity - true negative rate
    F1_score = np.round(f1_score(np.array(y_test), y_pred, average='weighted'),3)
    
    FP = np.mean(cnf_matrix.sum(axis=0) - np.diag(cnf_matrix))
    FN = np.mean(cnf_matrix.sum(axis=1) - np.diag(cnf_matrix))
    TP = np.mean(np.diag(cnf_matrix))
    TN = np.mean(cnf_matrix.sum() - (FP + FN + TP))
    
    # Sensitivity, hit rate, recall, or true positive rate
    Sensitivity = np.round(TP/(TP+FN))
    # Specificity or true negative rate
    Specificity =np.round(TN/(TN+FP),3) 
    # Fall out or false positive rate
    FPR = np.round(FP/(FP+TN),3)
    FNR = np.round(FN/(TP+FN),3)
    
    return accuracy,F1_score,Sensitivity,Specificity,FPR,FNR

# In[function for get picked call list]
def fn_getpickedcalllist():
    
    # To read csv as dataframe
    outcome = pd.read_csv(app.config['VAR_OUTCOME_LIST'])
    # To filter picked calls outcomes and convert it as list
    outcome = outcome[outcome[app.config['VAR_ACTIVITY_TYPE']].isin([app.config['VAR_CALL_PICKED']])]
    outcome = outcome[app.config['VAR_OUTCOME']].tolist()
    # converting list to string
    outcome = ', '.join(f"'{w}'" for w in outcome)
    
    return outcome
    
# In[function for insert model details]
def fn_insert_modelDetails(modelname,model_filename,scalar_filename,accuracy,F1_score,Sensitivity,Specificity,FPR,FNR,columns,onehotlist):
    
    data = {
        "MODEL_NAME":modelname,
        "FILE_NAME":model_filename,
        "SCALAR_NAME":scalar_filename,
        "ACCURACY":float(accuracy),
        "F1_SCORE":float(F1_score),
        "SENSITIVITY":float(Sensitivity),
        "SPECIFICITY":float(Specificity),
        "FALSE_POSITIVE":float(FPR),
        "FALSE_NEGATIVE":float(FNR),
        "DATASET_COLUMNS":str(columns),
        "ONEHOT_LIST":str(onehotlist),
        "CREATED_BY":app.config['VAR_ML_USERNAME'],
        "CREATED_ON":datetime.now()
        }
    
    DBC.mysql_insertData(app.config['MYSQL_INSERT_MODELINFORMATION'],data)
    
# In[function for generate distinct categorical]
def fn_generate_onehotList(ONEHOT_COLS,data,ONEHOT_CATEGORIES):
    
    jsonList = {}
    for i in range(0,len(ONEHOT_COLS)):
        for j in ONEHOT_CATEGORIES[i]:  
            if j in data[ONEHOT_COLS[i]]:
                jsonList[ONEHOT_COLS[i]+'_'+ j] = [1]
            else:
                jsonList[ONEHOT_COLS[i]+'_'+ j] = [0]
            
    return jsonList

# In[function for session pivot]
def fn_session_pivotforPredictions(df):
    
    df['TIME_STAMP'] = pd.to_datetime(df['TIME_STAMP'], errors='coerce')
    df[app.config['VAR_SESSION_COLUMNNAME']] = pd.cut(df.TIME_STAMP.dt.hour, bins=app.config['VAR_DATETIME_SESSION_SPLIT'], labels=app.config['VAR_SESSIONS'], include_lowest=True)
    # Grouping the ID with sessions to get each customer call count against each session
    df[app.config['VAR_FREQUENCY_COLUMNNAME']] = df.groupby(["ID",app.config['VAR_SESSION_COLUMNNAME']])[app.config['VAR_SESSION_COLUMNNAME']].transform('count')
    df = df.pivot_table(index=['ID'], columns=app.config['VAR_SESSION_COLUMNNAME'], values=app.config['VAR_FREQUENCY_COLUMNNAME'], fill_value=0, dropna=False).reset_index()
    
    return df

# In[funvtion for empty json session]
def fn_empty_jsonSessions(session):
    
    json ={}
    for i in session:
        json[i] = [0]
        
    return json

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
            
