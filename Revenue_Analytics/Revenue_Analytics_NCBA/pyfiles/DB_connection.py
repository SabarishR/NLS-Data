#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 29 17:07:04 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""

# In[libraries]:
from flask import current_app as app
import pandas as pd
import cx_Oracle

# In[ORACLE connection]
def oracle_connection():
    
    oracle_connection = cx_Oracle.connect(
       user=app.config['ORACLE_USERNAME'],
       password=app.config['ORACLE_PASSWORD'],
       dsn=cx_Oracle.makedsn(host=app.config['ORACLE_HOST'], port=app.config['ORACLE_PORT'], sid=app.config['ORACLE_SID']))
   
    return oracle_connection

# In[ORACLE data read]
def oracle_readTable(query,param=None):
    
    connection = oracle_connection()
    dataframe = pd.read_sql(query, con=connection,params=param)
    # connection.close()
    
    return dataframe

# In[ORACLE insert data]
def oracle_insertData(query,data):
    
    connection = oracle_connection()
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    primary_key = cursor.lastrowid
    cursor.close()
    connection.close()
    
    return primary_key

# In[ORACLE delete data]
def oracle_update_delete_Data(query,data):
    
    connection = oracle_connection()
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()