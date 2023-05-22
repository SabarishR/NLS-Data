#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 03 13:07:04 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""

# In[libraries]:
import mysql.connector
from flask import current_app as app
import pandas as pd
from sqlalchemy import create_engine

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
    primary_key = cursor.lastrowid
    cursor.close()
    connection.close()
    
    return primary_key

# In[MYSQL delete data]
def mysql_update_delete_Data(query,data):
    
    connection = mysql_connection()
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()

# In[SQLalchemy connection]
def mysql_sqlalchemy_engine():
    
    engine = create_engine(app.config['MYSQL_SQLALCHEMY_URL'])
    return engine

# In[Pandas DF bulk insert]
def mysql_df_to_table_insert(df,tablename):
    
    engine = mysql_sqlalchemy_engine()
    mysql_connection = engine.connect()
    df.to_sql(con=mysql_connection, name=tablename, if_exists='append',index=False)
    mysql_connection.close()