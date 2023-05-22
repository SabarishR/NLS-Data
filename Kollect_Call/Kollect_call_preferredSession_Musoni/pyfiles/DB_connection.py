#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 12:05:17 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""

# In[libraries]:
import mysql.connector
from flask import current_app as app
import pandas as pd

# In[MYSQL connection]
def mysql_connection():
    
    mysql_connection = mysql.connector.connect(**app.config['MYSQL_CONNECTION_CONFIG'])
    return mysql_connection

# In[MYSQL data read]
def mysql_readTable(query,param=None):
    
    connection = mysql_connection()
    dataframe = pd.read_sql(query, con=connection,params=param)
    connection.close()
    
    return dataframe

# In[MYSQL insert data]
def mysql_insertData(query,data):
    
    connection = mysql_connection()
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()