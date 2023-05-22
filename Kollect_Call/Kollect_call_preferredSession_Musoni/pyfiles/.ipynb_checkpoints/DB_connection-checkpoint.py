#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:41:03 2021

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
import json
from sqlalchemy import create_engine

# In[Functions Start]:
engine = create_engine('postgresql://postgres:eNoah@123@localhost:5432/Production')

def Insert_model_output(input,output):
        
    with engine.connect() as connection:
        connection.execute("INSERT INTO predictions (inputdata,outputdata,createdby,createdon) values('"+json.dumps(input)+"','"+json.dumps(output)+"','ML User',now())")
    