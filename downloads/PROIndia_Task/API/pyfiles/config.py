#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 12:51:32 2023

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
# from os import environ

# In[basic app config]:
class common_config(object):
    
    VAR_ANN_SCALAR = "Models/scalar.pkl"
    VAR_ANN_MODEL = "Models/ANN_model.h5"
    VAR_SATISFACTION = "Satisfaction"
    VAR_SATISFACTION_CATEGORIES = ['Satisfied','Neutral or Dissatisfied']
    VAR_ONEHOT_LIST = ["Class","Gender","Customer Type","Type of Travel"]
    VAR_INPUT_ONEHOT = [['Eco','Business','Eco Plus'],['Female','Male'],['Loyal Customer','Disloyal Customer'],
                        ['Business travel','Personal Travel']]
    VAR_SORTED_COLUMNS = ['Age','Flight Distance','Inflight wifi service','Departure/Arrival time convenient',
                          'Ease of Online booking','Gate location','Food and drink','Online boarding','Seat comfort',
                          'Inflight entertainment','On-board service','Leg room service','Baggage handling',
                          'Checkin service','Inflight service','Cleanliness','Arrival Delay in Minutes','Class_Eco',
                          'Class_Eco Plus','Gender_Male','Customer Type_Loyal Customer','Type of Travel_Personal Travel']
    VAR_ARR_TRUE = [1]
    VAR_ARR_FALSE = [0]
    VAR_STATUS = "STATUS"
    VAR_STATUS_ERROR = "error"
    VAR_LOGGER_TYPE ="werkzeug"
    VAR_ERROR_LOG ="log/errorlog.log"
    VAR_ERROR_FORMAT = "-------------------------------------------------------------------------\n Datetime - %(asctime)s & Filename - %(name)s & Type - %(levelname)s \n-------------------------------------------------------------------------\n %(message)s"
    VAR_ERROR_BK_COUNT = 200000000
                            
    