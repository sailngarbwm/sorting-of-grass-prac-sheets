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
#use_dir = r'C:\Users\jgarber\Documents\Ecology Prac\sort_folder'


def EC_tonum(dtype,data,sheet,downcaster=None):
    '''
    catching data that wont work for me, by cleaning the data up and return
    the dataset ready to go it will remove nans, convert to numeric data and print errors
    if theres a problem
    input: dtype - string 'WS' for wandering search, NQ for nested quadrat and QUAD for the abundance measurements
    data - series input will probably have nans and will be an object series, downcast - whether or not to downcast to int (for NQ)
    sheet - the name of the spreadsheet so we can call an error
    '''
    data = data.dropna()
    data = pd.to_numeric(data,errors='coerce',downcast=downcaster)
    #nullct = np.array(data[data.isnull()].index.tolist())
    #nullct+=12
#    if nullct.shape[0]  > 0:
#        for nullrow in nullct:
#            rownum = str(nullrow)
#            print ('error value in ' +sheet + ' in column ' +dtype+ ' and row: ' + rownum)
    return data.dropna()

def EC_tonum_QUAD(dtype,data,sheet,downcaster=None):
    '''
    same as the function above except it turns all the original NA's to zero
    and returns a corrected data set for abundance
    '''
    data = data.fillna(0)
    data = pd.to_numeric(data,errors='coerce',downcast=downcaster)
    #nullct = np.array(data[data.isnull()].index.tolist())
#    #nullct+=12
#    if nullct.shape[0]  > 0:
#        for nullrow in nullct:
#            rownum = str(nullrow)
#            print ('error value in ' +sheet + ' in column ' +dtype+ ' and row: ' + rownum)
    return data.dropna()


def add_df_row(df, numrows):
    '''
    This will add empty rows at the bottom of a dataframe
    inputs -data frame, the number of rows you want to add
    '''
    row_arr = np.zeros(df.shape[1])
    row_arr = row_arr.fill(np.nan)
    col_list = list(df.columns.values)
    emptser = pd.Series(row_arr,index= col_list)
    for j in range(1,numrows):
       df = df.append(emptser, ignore_index=True)
    return df

#generate empty out dataframes, note abundance dataframe will be made in first loop iteration





def grass_sort(use_dir,sheetlist):
    '''
    function for sorting everythign and bringing out the
    '''

    ws_cat = [3,6,9,12,15,18,21,24,27,30] #Wandering Search Categories
    df_ws = pd.DataFrame(columns = ['sheet','groupID','Day/time','Names','3','6','9','12','15','18','21','24','27','30'])
    nQ_cat = [0.065,0.125,0.25,0.5,1,2,4,8,16]
    df_Nq = pd.DataFrame(columns = ['sheet','groupID','Day/time','Names','0.065','0.125','0.25','0.5','1','2','4','8','16'])

    ct = 0
    groupID = ct+1

    ns_ct = 70

    os.chdir(use_dir)

    for sheet in sheetlist:


        try:
            df_data = pd.read_excel(sheet, header=None)
        except:
            print('could not upload', sheet)
            continue

        prac = df_data.at[5,3]

        names = df_data.at[7,3]
        #if pd.isnull(names) == False:
        try:
            names = names.replace(',',' ') #replacing commas because it seemed to have mucked up certain CSV reads
        except:
            names = sheet+'_'+str(groupID)+'_noname'
        if pd.isnull(prac):
            names = sheet+'_'+str(groupID)+'_noprac'
        df_d2 = df_data[12:] # getting the header out

        '''
        Pulling out the Wanderin search data
        '''

        WS_data = df_d2[4]

        WS_data2 = EC_tonum('WS',WS_data,sheet)

        #now I need to fill out the out spreadsheet

        df_ws.loc[ct,['sheet','groupID','Day/time','Names']] = [sheet,str(groupID),prac,names]

        for times in ws_cat:
            #edited 4/10/17 to cover for students who put zeros in unobserved columns by starting at 0.00001
            df_ws.loc[ct,str(times)] = WS_data2[WS_data2.between(0.00001,times,inclusive=False)].values.shape[0]

        '''
        Next I am doing the Nested quadrat
        '''

        NQ_data = df_d2[5]

        NQ_data2 = EC_tonum('NQ',NQ_data,sheet,downcaster = None)

        NQqt = 1
        Nqcount = 0

        df_Nq.loc[ct,['sheet','groupID','Day/time','Names']] = [sheet,str(groupID),prac,names]

        while NQqt <= 9:
            Nqcount += NQ_data2[NQ_data2==NQqt].values.shape[0]
            df_Nq.loc[ct,str(nQ_cat[NQqt-1])] = Nqcount
            NQqt+=1

        '''
        and now the Foliage Projective Cover
        '''

        if ct ==0:
            #need to create the master dataframe
            df_quad = df_d2.loc[:,[0,1,2,3]]
            #add a bunch mroe rows for unknowns
            df_quad = add_df_row(df_quad,50)

        s_q1 = df_d2[6]
        s_q2 = df_d2[7]
        s_q3 = df_d2[8]

        #clean up the quad data and look for errors!
        s_q1_2 = EC_tonum_QUAD('Quad1',s_q1,sheet,downcaster=None).values
        s_q2_2 = EC_tonum_QUAD('Quad2',s_q2,sheet,downcaster=None).values
        s_q3_2 = EC_tonum_QUAD('Quad3',s_q3,sheet,downcaster=None).values

        #calculate means for each species
        df_d3 = df_d2.reset_index() #need this to call the list of potential unknowns


        i = 0
        mean_quad = np.zeros(df_quad.shape[0])
        while i < s_q1_2.shape[0]-1:
            mean_quad[i] = np.mean([s_q1_2[i],s_q2_2[i],s_q3_2[i]])

            if i >= 51 and mean_quad[i] > 0:
                df_quad.loc[ns_ct,[0,1,2,3]] = df_d3.loc[i,[0,1,2,3]].values
                mean_quad[ns_ct] = mean_quad[i]
                mean_quad[i] = 0
                #print('unk moved')
                ns_ct+=1
            i +=1

        df_quad[names] = mean_quad
        ct +=1
        groupID +=1

    df_quad['sum'] = df_quad.sum(axis=1,numeric_only=True)

    #df_quadfilt = df_quad[df_quad.index.values <51 | (df_quad['sum'].values >0 & df_quad.index.values>=51)]
    df_reg = df_quad[df_quad.index.values <51]
    df_upp = df_quad[df_quad.index.values >51]
    df_upp = df_upp[df_upp['sum'].values >0]
    df_quad_out = df_reg.append(df_upp)
    return df_quad_out,df_ws,df_Nq

#finding and adding unmarked data
#df_quad_out.loc[77,3] = 'Lamandra'
#df_quad_out.loc[79,3] = 'Fleshy Red Stem'
#df_quad_out.loc[90,3] = 'Moss'
#df_quad_out.loc[91,3] = 'Litter'

#need to create some steps to fold in the data to each other
def address_unk(df_quad_out, mix_dict):


    for key in list(mix_dict.keys()):

        indl =  mix_dict[key]
        df_quad_out.loc[indl[0]] = df_quad_out.loc[indl].sum(axis=0,numeric_only=True)
        df_quad_out.loc[indl[0],3] = str(key)
        df_quad_out = df_quad_out.drop(indl[1:])

        #df_quad_out.drop(2,axis = 1,inplace = True)

    return df_quad_out.rename(columns = {0:'family',1:'Species', 3:'Common'})



