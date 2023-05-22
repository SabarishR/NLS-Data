#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:41:03 2021

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import confusion_matrix,accuracy_score,f1_score
from jsonmerge import merge
from flask import current_app as app, json
import pyfiles.DB_connection as db

# In[function to identify outlier values]:
def identify_outliers(df,features):
    outlier_indices=[]
    
    for c in features:
        # 1st quartile
        Q1=np.percentile(df[c],25)
        
        # 3rd quartile
        Q3=np.percentile(df[c],75)
        
        # IQR
        IQR= Q3-Q1
        
        # Outlier Step
        outlier_step= IQR * 1.5
        
        # Detect outlier and their indeces 
        outlier_list_col = df[(df[c]< Q1 - outlier_step)|( df[c] > Q3 + outlier_step)].index
        
        # Store indices 
        outlier_indices.extend(outlier_list_col)
    
    outliers_indices = Counter(outlier_indices)
    multiple_outliers = list(i for i , v in outliers_indices.items() if v>2 )
    return multiple_outliers

# In[Model Training]:
def Model_Training(filepath):
    
    # Reading the dataset using pandas
    mortality_df = pd.read_csv(filepath['filepath'])
    # Romoving the columns which has more then 25 % nulls
    mortality_df = mortality_df.loc[:, mortality_df.isnull().mean() < .25]
    # Missing value treatment.romoving the NA rows
    mortality_df.dropna(axis=0,inplace=True)
    # In that above dataframe droping the below columns,hence columns has no significant effects as per data

    # Name , Not required for model training in bussiness perspective
    # Announcement,Death and Burial.We have the data difference in respective column data
    # Burial_Week, we will consider the day wise burial since both variable explains the same data
    mortality_df = mortality_df.drop(["Name","Announcement","Burial","Burial_Week","County_Burial"], axis = 1)
    
    # Death_to_Announce,Death_to_Burial,Announce_to_Burial,No_of_Relatives Having some non numeric values such as
    # #VALUE!, 5/25/2017 .Romoving those rows again leads to rows detuction and the data is not sufficient for
    # model traing.Hence it is testing task I just replace with random values
    # Note : In bussiness cases we should remove or replace as per requirement

    mortality_df['Death_to_Announce'] = pd.to_numeric(mortality_df.Death_to_Announce.astype(str).str.replace(',',''), errors='coerce').fillna(np.random.randint(50)).astype(int)
    mortality_df['Death_to_Burial'] = pd.to_numeric(mortality_df.Death_to_Burial.astype(str).str.replace(',',''), errors='coerce').fillna(np.random.randint(50)).astype(int)
    mortality_df['Announce_to_Burial'] = pd.to_numeric(mortality_df.Announce_to_Burial.astype(str).str.replace(',',''), errors='coerce').fillna(np.random.randint(50)).astype(int)
    mortality_df['No_of_Relatives'] = pd.to_numeric(mortality_df.No_of_Relatives.astype(str).str.replace(',',''), errors='coerce').fillna(np.random.randint(50)).astype(int)
    
    # Replacing the catogorical values 
    mortality_df["Burial_Day"] = mortality_df["Burial_Day"].replace("saturday","Saturday")

    mortality_df["Color"] = mortality_df["Color"].replace("yes","Yes")
    mortality_df["Color"] = mortality_df["Color"].replace("no","No")

    mortality_df["Married"] = mortality_df["Married"].replace("yes","Yes")
    mortality_df["Married"] = mortality_df["Married"].replace("no","No")
    
    # To drop outliers
    #binning

    # The outlier affects both results and assumptions. In this situation, it is not legitimate to simply drop
    # the outlier. You may run the analysis both with and without it, but you should state in at least a footnote
    # the dropping of any such data points and how the results changed


    #mortality_df_outliered = mortality_df.drop(identify_outliers(mortality_df,numerical_features.columns))
    mortality_df = mortality_df.loc[(mortality_df['Death_to_Announce'] >= 0) & (mortality_df['Death_to_Announce'] <= 500)]
    
    # To do one hot encode the categories
    # added the parameter drop_first is true in one hot , always n-1 columns enough to explain the categories
    mortality_df = pd.get_dummies(mortality_df, drop_first =True ,columns=["Burial_Day","Gender", "Color", "Fundraising","Married"],dtype = bool, sparse=True)
    
    # spliting the data to dependent and independent variable
    y = mortality_df['Fundraising_Yes'].copy()
    X = mortality_df.drop('Fundraising_Yes', axis=1)

    # Splitting the dataset into the Training set and Test set. test size is 20 %
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    # Feature Scaling
    # there is no need to apply future scaling on dependent variable
    sc = StandardScaler()
    scalar = sc.fit(X_train)
    
    # Save the model
    Model_Name = "Models/scalar.pkl"
    joblib.dump(scalar, Model_Name)
    
    X_train = scalar.transform(X_train)
    X_test = scalar.transform(X_test)
    
    # random forest model creation
    Model = RandomForestClassifier(n_estimators = 50,random_state=0,max_depth=25,min_samples_split= 5,
                               min_samples_leaf = 1,bootstrap= True)
    # Training the model on the Training set
    Model.fit(X_train, y_train)
    
    # Save the model
    Model_Name = "Models/random_forest.pkl"
    joblib.dump(Model, Model_Name)
    
    #making predictions 
    y_pred = Model.predict(X_test)
    
    #  F1 score - F-score or F-measure is a measure of a test's accuracy
    # Sensitivity(recall) - true positive rate
    # specificity - true negative rate

    tn, fp, fn, tp = confusion_matrix(np.array(y_test), y_pred).ravel()
    F1_score = f1_score(np.array(y_test), y_pred, average='binary')
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    
    Accuracy =round(accuracy_score(np.array(y_test), y_pred),3)
    F1_Score = round(F1_score,3)
    Sensitivity = round(sensitivity,3)
    Specificity = round(specificity,3)
    
    data = {'ModelName': Model_Name, 'Accuracy': Accuracy,'F1_Score' : F1_Score, 'Sensitivity' : 
                              Sensitivity, 'Specificity' : Specificity }
    

    return json.dumps(data)

# In[Model Predictions]:
def Model_Prediction(inputdata):
    
    Days = app.config['DAYS']
    data = {}
    for i in Days:
        if i in inputdata['Burial_Day']:
            data['Burial_Day_'+ i] = [1]
        else:
            data['Burial_Day_'+ i] = [0]
            
    d = {'Size':[inputdata['Size']],'Word_Count':[inputdata['Word_Count']],
     'No_of_Children':[inputdata['No_of_Children']],'Significant_Children':[inputdata['Significant_Children']],
     'Significant_Relatives':[inputdata['Significant_Relatives']],'Death_to_Announce':[inputdata['Death_to_Announce']],
     'Death_to_Burial':[inputdata['Death_to_Burial']],'Announce_to_Burial':[inputdata['Announce_to_Burial']],
     'No_of_Relatives':[inputdata['No_of_Relatives']],'Burial_Day':[inputdata['Burial_Day']],
     'Gender':[inputdata['Gender']],'Color':[inputdata['Color']],'Married':[inputdata['Married']]}
    
    result = merge(d, data)
    df = pd.DataFrame(data=result)
    
    df = df.replace(['Male','Female','Yes','No'], [1, 0, 1, 0])
    df=df[['Size','Word_Count','No_of_Children','Significant_Children','Significant_Relatives','Death_to_Announce','Death_to_Burial','Announce_to_Burial','No_of_Relatives','Burial_Day_Monday','Burial_Day_Saturday','Burial_Day_Sunday','Burial_Day_Thursday','Burial_Day_Tuesday','Burial_Day_Wednesday','Gender','Color','Married']] 
    
    scalar = joblib.load('Models/scalar.pkl')
    pred = scalar.transform(df)
    
    loaded_model = joblib.load('Models/random_forest.pkl')
    y_pred = loaded_model.predict(pred)
    
    if y_pred:
        data ={'Fundraising':'Yes'}
    else:
        data ={'Fundraising':'No'} 
    db.Insert_model_output(inputdata,data)

    return json.dumps(data)
