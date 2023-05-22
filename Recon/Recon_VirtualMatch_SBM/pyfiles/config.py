#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  22 15:10:51 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""
# In[libraries]:
from os import environ
import json
import cryptocode

# In[basic app config]:
class common_config(object):
    VAR_GL_ID = "GL_ID"
    VAR_RE_ID = "RE_ID"
    VAR_GL_DATE = "GL_DATE"
    VAR_RE_DATE = "RE_DATE"
    VAR_GL_AMOUNT = "GL_AMOUNT"
    VAR_RE_AMOUNT = "RE_AMOUNT"
    VAR_GL_CRDR = "GL_CRDR"
    VAR_RE_CRDR = "RE_CRDR"
    VAR_ISMATCHED = "ISMATCHED"
    VAR_MATCH_TABLE = "MATCH_TABLE"
    VAR_MATCH_ID = "MATCH_ID"
    VAR_CREDIT_TYPE = "C"
    VAR_DEBIT_TYPE = "D"
    VAR_G_DATE = "G_DATE"
    VAR_R_DATE = "R_DATE"
    VAR_ALLOWED_VARIANCE = 1
    VAR_ALLOWED_DATE_VARIANCE = 1
    VAR_DEFAULT_MATCHED_VALUE = 0
    VAR_MATCHED_VALUE = 1
    VAR_MAX_COMBINATION_LENGTH = 4
    VAR_SCHEDULER_MODELTRAIN_TIMEZONE = 'UTC'
    VAR_GLTOGL_MATCHED_TABLE = "statement$detail$history"
    VAR_GLTONOSTRO_MATCHED_TABLE = "nostro$statement"
    VAR_DATATYPE_INT = "int"
    VAR_DATE_MATCH_FORMAT = "%Y-%m"
    VAR_NO_MATCH = "NO MATCH"
    VAR_ML_USERNAME = environ.get('DEV_ML_USERNAME')
    VAR_STATUS_ERROR = "error"
    VAR_LOGGER_TYPE ="werkzeug"
    VAR_ERROR_LOG ="log/errorlog.log"
    VAR_INFO_LOG = "log/infolog.log"
    VAR_ERROR_FORMAT = "-------------------------------------------------------------------------\n Datetime - %(asctime)s & Filename - %(name)s & Type - %(levelname)s \n-------------------------------------------------------------------------\n %(message)s"
    VAR_ERROR_BK_COUNT = 200000000
                             
# In[MYSQL QUERIES]
class mysqlQueries(common_config):
    
    MYSQL_SELECT_STATEMENTENTRY = """
                                    select his.AC_ENTRY_SR_NO As GL_ID,his.ACCOUNT_NO AS GL_ACCNO,his.VALUE_DT as GL_DATE,his.DRCR_IND as GL_CRDR,
                                    CASE 
                                        WHEN his.AC_CCY = 'KES' then his.LCY_AMOUNT
                                        ELSE his.FCY_AMOUNT
                                        END as GL_AMOUNT,
                                    his.AC_CCY as GL_CURRENCY
                                        from statement$detail$history his 
                                    INNER JOIN tbl_recon_nostro$unmatched$entry recon on recon.PRI_entryId = his.AC_ENTRY_SR_NO
                                    where his.ACCOUNT_NO = %(ACCOUNT_NUMBER)s
                                """
                                
    MYSQL_SELECT_NOSTROENTRY = """
                                select ns.ID as RE_ID,ns.ACCOUNT_NUMBER as RE_ACCNO,ns.VALUE_DATE as RE_DATE,ns.CRF_TYPE as RE_CRDR,
                                ns.SWIFT_AMOUNT as RE_AMOUNT from nostro$statement ns
                                inner join tbl_recon_nostro$unmatched$entry recon on recon.PRI_entryId = ns.id
                                where ns.ACCOUNT_NUMBER = %(ACCOUNT_NUMBER)s
                              """

    MYSQL_SELECT_DISTINCT_ACCOUNT_NO = """
                                        select distinct(fld_account_Number) as ACCOUNT_NUMBER from tbl_recon_nostro$unmatched$entry 
                                        where fld_account_Number is not null and fld_account_Number != ''
                                       """
                                       
    MYSQL_INSERT_RECON_POSSIBLE_MATCH = ("INSERT INTO tbl_recon_nostro$virtual$possible$match"
                                        "(ACCOUNT_NO,STATEMENT_DETAIL_ID,MATCH_TABLE,MATCH_ID,MATCH_AMOUNT,VARIANCE,CREATED_BY,CREATED_ON)"
                                        "VALUES (%(ACCOUNT_NO)s, %(STATEMENT_DETAIL_ID)s,%(MATCH_TABLE)s,%(MATCH_ID)s, %(MATCH_AMOUNT)s,%(VARIANCE)s,%(CREATED_BY)s,%(CREATED_ON)s)")
    
    MYSQL_INSERT_RECON_EXECUTION_HISTORY = ("INSERT INTO tbl_recon_nostro$execution$history"
                                        "(ACCOUNT_NO,RESPONSE,CREATED_BY,CREATED_ON)"
                                        "VALUES (%(ACCOUNT_NO)s, %(RESPONSE)s,%(CREATED_BY)s,%(CREATED_ON)s)")
    
    MYSQL_POSSIBLE_MATCH_STATEMENT_ID = """
                                        select STATEMENT_DETAIL_ID as GL_ID,
                                            CASE 
                                            WHEN MATCH_TABLE = 'statement$detail$history' THEN MATCH_ID
                                            ELSE 0
                                            END AS MATCH_ID
                                        from tbl_recon_nostro$virtual$possible$match
                                        where ACCOUNT_NO = %(ACCOUNT_NUMBER)s and ISMATCHED = 0    
                                        """
                                        
    MYSQL_POSSIBLE_MATCH_NOSTRO_ID = """
                                        select MATCH_ID as RE_ID from tbl_recon_nostro$virtual$possible$match
                                        where ACCOUNT_NO = %(ACCOUNT_NUMBER)s and MATCH_TABLE  != 'statement$detail$history' and ISMATCHED = 0
                                     """
    
    MYSQL_ASYNCHRONOUS_COMPLETE = """
                                    update RECON$AML$API$STATUS set AML_PROCESS_STATUS = 'COMPLETED' where id  = %(ID)s
                                  """
# In[MYSQL CONNECTION]    
class dev_mysqlConfig(mysqlQueries):
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('DEV_MYSQL_USER'),
                                  'password':cryptocode.decrypt(environ.get('DEV_MYSQL_PASSWORD'), environ.get('DEV_ENCRYPTION_KEY')),
                                  'host': environ.get('DEV_MYSQL_HOST'),
                                  'port': environ.get('DEV_MYSQL_PORT'),
                                  'database': environ.get('DEV_MYSQL_DB'),
                                  'auth_plugin' : environ.get('DEV_MYSQL_AUTH_PLUGIN'),
                                  'raise_on_warnings': json.loads(environ.get('DEV_MYSQL_RAISE_WARNING').lower())
                              }
    
# In[MYSQL CONNECTION]    
class cloudTesting_mysqlConfig(mysqlQueries):
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('CLOUDTESTING_MYSQL_USER'),
                                  'password': cryptocode.decrypt(environ.get('CLOUDTESTING_MYSQL_PASSWORD'), environ.get('CLOUDTESTING_ENCRYPTION_KEY')),
                                  'host': environ.get('CLOUDTESTING_MYSQL_HOST'),
                                  'port': environ.get('CLOUDTESTING_MYSQL_PORT'),
                                  'database': environ.get('CLOUDTESTING_MYSQL_DB'),
                                  'auth_plugin' : environ.get('CLOUDTESTING_MYSQL_AUTH_PLUGIN'),
                                  'raise_on_warnings': json.loads(environ.get('CLOUDTESTING_MYSQL_RAISE_WARNING').lower())
                              }
    
# In[MYSQL CONNECTION]    
class live_mysqlConfig(mysqlQueries):
    
    #MYSQL_USER = environ.get('MYSQL_USER')
    MYSQL_CONNECTION_CONFIG = {
                                  'user': environ.get('LIVE_MYSQL_USER'),
                                  'password': cryptocode.decrypt(environ.get('LIVE_MYSQL_PASSWORD'), environ.get('LIVE_ENCRYPTION_KEY')),
                                  'host': environ.get('LIVE_MYSQL_HOST'),
                                  'port': environ.get('LIVE_MYSQL_PORT'),
                                  'database': environ.get('LIVE_MYSQL_DB'),
                                  'auth_plugin' : environ.get('LIVE_MYSQL_AUTH_PLUGIN'),
                                  'raise_on_warnings': json.loads(environ.get('LIVE_MYSQL_RAISE_WARNING').lower())
                              }