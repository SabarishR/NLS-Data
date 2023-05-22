#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  22 15:14:05 2022

@author: Sabarish.R

@version : 0.01

Reviewed by : ---
"""

import cryptocode
from os import environ

# In[DEV Encryption]
def dev_passkey_encryption(passkey):
	
    return (cryptocode.encrypt(passkey,environ.get('DEV_ENCRYPTION_KEY')))
    
# In[Cloud testing Encryption]
def cloudtesting_passkey_encryption(passkey):
	
    return (cryptocode.encrypt(passkey,environ.get('CLOUDTESTING_ENCRYPTION_KEY')))

# In[UAT/LIVE Encryption]
def live_passkey_encryption(passkey):
	
    return (cryptocode.encrypt(passkey,environ.get('LIVE_ENCRYPTION_KEY')))
