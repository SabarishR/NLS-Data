#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:15:21 2023

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[Libraries]
from flask import current_app as app

# In[function for dynamic onehot encoding]:
def fn_onehot_encode(ONEHOT_LIST,INPUT_ONEHOT,ip_json):
    data = {}
    for i in range(0,len(ONEHOT_LIST)):
        for j in INPUT_ONEHOT[i]:  
            if j in ip_json[ONEHOT_LIST[i]]:
                data[ONEHOT_LIST[i]+'_'+ j] = app.config['VAR_ARR_TRUE']
            else:
                data[ONEHOT_LIST[i]+'_'+ j] = app.config['VAR_ARR_FALSE']
                
    return data