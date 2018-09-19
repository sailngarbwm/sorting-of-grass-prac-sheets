# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 13:20:16 2017

Script written for Melbourne Uni Ecology Practical in order to efficiently put together
the plant practical sheets from each group

Spreadsheets will all need to be in the same folder with unique names

@author: jgarber
"""

import pandas as pd
import numpy as np
import os

#np.set_printoptions(threshold='nan')
# choose directory with all of the excel spreadsheets


errlist = {}
err_str = ''

def EC_tonum(dtype,data,sheet,errlist,downcaster=None, err_str = err_str):
    '''
    catching data that wont work for me, by cleaning the data up and return
    the dataset ready to go it will remove nans, convert to numeric data and print errors
    if theres a problem
    input: dtype - string 'WS' for wandering search, NQ for nested quadrat and QUAD for the abundance measurements
    data - series input will probably have nans and will be an object series, downcast - whether or not to downcast to int (for NQ)
    sheet - the name of the spreadsheet so we can call an error

    2/10/2017 added error list as a list of the errors because the print was crashing everything
    '''
    data = data.dropna()
    data = pd.to_numeric(data,errors='coerce',downcast=downcaster)
    nullct = np.array(data[data.isnull()].index.tolist())
    #nullct+=12
    if nullct.shape[0]  > 0:
        #errlist.append('error value in ' +sheet + ' in column ' +dtype)
        print(' error value in ' +sheet + ' in column ' +dtype)
        err_str+= ' error value in '+ dtype +';'
    return err_str



#generate empty out dataframes, note abundance dataframe will be made in first loop iteration

ws_cat = [3,6,9,12,15,18,21,24,27,30] #Wandering Search Categories
df_ws = pd.DataFrame(columns = ['groupID','Day/time','Names','3','6','9','12','15','18','21','24','27','30'])
nQ_cat = [0.065,0.125,0.25,0.5,1,2,4,8,16]
df_Nq = pd.DataFrame(columns = ['groupID','Day/time','Names','0.065','0.125','0.25','0.5','1','2','4','8','16'])

ct = 0
groupID = ct+1
def check_data(current_dir, sheetlist):
    '''
    Data checker looks for non numeric data in each sheet, prints off any
    issues, and saves a dictionary full of issues
    '''
    os.chdir(current_dir)
    for sheet in sheetlist:

        err_str = ""


        try:
            df_data = pd.read_excel(sheet, header=None)
        except:
            print('could not upload', sheet)
            continue


        prac = df_data.at[5,3]

        names = df_data.at[7,3]

        try:
            len(names)
        except:
            print(sheet, 'Has no names')
        try:
            len(prac)
        except:
            print(sheet, 'Has no pracs')


        df_d2 = df_data[12:] # getting the header out

        '''
        Pulling out the Wanderin search data
        '''

        WS_data = df_d2[4]

        err_str = EC_tonum('WS',WS_data,sheet,errlist)

        #now I need to fill out the out spreadsheet



        '''
        Next I am doing the Nested quadrat
        '''

        NQ_data = df_d2[5]

        err_str = EC_tonum('NQ',NQ_data,sheet,errlist)

        s_q1 = df_d2[6]
        s_q2 = df_d2[7]
        s_q3 = df_d2[8]



        #clean up the quad data and look for errors!
        err_str = EC_tonum('Quad1',s_q1,sheet,errlist,downcaster=None)
        err_str= EC_tonum('Quad2',s_q2,sheet,errlist,downcaster=None)
        err_str = EC_tonum('Quad3',s_q3,sheet,errlist,downcaster=None)

        if (len(err_str) >= 1):
            errlist[sheet] = err_str

    return errlist









